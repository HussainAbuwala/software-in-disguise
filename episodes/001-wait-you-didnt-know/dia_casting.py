"""Dia casting round for the Episode 1 remake.

Dia picks a new voice on every run (it can't be told "old man" or "woman"), so each character gets several seeded
takes. A take is kept only if speech-to-text hears the right words, it isn't too long, and its pitch fits the
character's gender. Hussain then picks one voice per character by ear; that take becomes the character's voice
reference (Dia's audio prompt) for every scene, so the voice stays the same across the episode.

Run: ../../.venv-mlx/bin/python dia_casting.py [CHARACTER ...]
Output: audio/casting/<character>/seed-NN.wav, audio/casting/<character>/reel.m4a, audio/casting/casting.json
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf

OUT = Path(__file__).parent / "audio" / "casting"
SEEDS = range(1, 11)
KEEP = 4  # takes per character in the reel

# Each line is long enough (3–5 s) to work later as the character's voice reference.
CAST = {
    "AUNT": dict(text="[S1] Congratulations!! Oh, I'm so happy for you!", gender="f", max_s=5.0),
    "GRANDPA": dict(text="[S1] Hm? ...On what? What did I miss?", gender="m", max_s=5.5),
    "PRIYA": dict(text="[S1] Mom... guess what? I'm engaged!", gender="f", max_s=5.0),
    "MOM": dict(text="[S1] (gasps) Oh my God! Priya's engaged!", gender="f", max_s=5.0),
    "DAD": dict(text="[S1] Mm. Nice. Good for her.", gender="m", max_s=4.5),
}


def words(s: str) -> str:
    s = re.sub(r"\[S\d\]|\([^)]*\)", " ", s.lower())
    return " ".join(re.findall(r"[a-z']+", s))


def median_f0(a: np.ndarray, sr: int) -> float:
    """Median pitch over voiced frames (autocorrelation, 60–400 Hz)."""
    n, hop = int(sr * 0.04), int(sr * 0.01)
    rms_floor = np.sqrt(np.mean(a ** 2)) * 0.5
    lo, hi = int(sr / 400), int(sr / 60)
    f0s = []
    for i in range(0, len(a) - n, hop):
        f = a[i:i + n] - a[i:i + n].mean()
        if np.sqrt(np.mean(f ** 2)) < rms_floor:
            continue
        ac = np.correlate(f, f, "full")[n - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.5:
            f0s.append(sr / lag)
    return float(np.median(f0s)) if f0s else 0.0


def tighten(a: np.ndarray, sr: int, gap_s=0.45) -> np.ndarray:
    """Trim silence at both ends and shorten any pause longer than gap_s."""
    hop = int(sr * 0.02)
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    voiced = e > max(0.01, e.max() * 0.06)
    if not voiced.any():
        return a
    idx = np.flatnonzero(voiced)
    keep, run = [], 0
    for k in range(idx[0], idx[-1] + 1):
        run = 0 if voiced[k] else run + 1
        if run * 0.02 <= gap_s:
            keep.append(k)
    pad = int(sr * 0.08)
    out = np.concatenate([a[k * hop:(k + 1) * hop] for k in keep])
    return np.concatenate([np.zeros(pad, np.float32), out, np.zeros(pad, np.float32)])


def main(names):
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    tts = load_model("mlx-community/Dia-1.6B-fp16")
    stt = load_stt("mlx-community/parakeet-tdt-0.6b-v3")
    report_path = OUT / "casting.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    for name in names:
        spec = CAST[name]
        d = OUT / name.lower()
        d.mkdir(parents=True, exist_ok=True)
        takes = []
        for seed in SEEDS:
            mx.random.seed(seed)
            # Dia runs ~86 audio tokens per second; a cap stops runaway laughs and babble.
            res = list(tts.generate(text=spec["text"], max_tokens=int(spec["max_s"] * 86) + 60))
            a = np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in res])
            sr = tts.sample_rate
            a = tighten(a, sr)
            a = a / (np.abs(a).max() or 1) * 0.89
            path = d / f"seed-{seed:02d}.wav"
            sf.write(path, a, sr)
            heard = stt.generate(str(path)).text.strip()
            match = difflib.SequenceMatcher(None, words(spec["text"]), words(heard)).ratio()
            f0 = median_f0(a, sr)
            dur = len(a) / sr
            gender_ok = (f0 >= 165) if spec["gender"] == "f" else (0 < f0 < 160)
            ok = match >= 0.75 and dur <= spec["max_s"] and gender_ok
            takes.append(dict(seed=seed, file=path.name, heard=heard, match=round(match, 2), f0=round(f0),
                              dur=round(dur, 2), ok=ok))
            print(f"{name:8s} seed {seed:2d}  {'OK ' if ok else '-- '} match {match:.2f}  f0 {f0:5.0f}  "
                  f"{dur:4.1f}s  | {heard}")
        picks = sorted([t for t in takes if t["ok"]], key=lambda t: -t["match"])[:KEEP]
        # Reel: the kept takes in order, with a short gap, so "take 1, 2, 3…" maps to the list below.
        if picks:
            parts = []
            for t in picks:
                a, sr = sf.read(d / t["file"], dtype="float32")
                parts += [a, np.zeros(int(sr * 0.9), np.float32)]
            sf.write(d / "reel.wav", np.concatenate(parts), sr)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "reel.wav"), "-c:a", "aac",
                            "-b:a", "160k", str(d / "reel.m4a")], check=True)
        report[name] = dict(text=spec["text"], takes=takes, reel=[t["seed"] for t in picks])
        report_path.write_text(json.dumps(report, indent=2))
        print(f"{name}: reel = seeds {[t['seed'] for t in picks]}")


if __name__ == "__main__":
    main(sys.argv[1:] or list(CAST))
