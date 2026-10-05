"""Dia casting for the Episode 1 remake, one two-person scene at a time.

Dia sounds natural on a short exchange between two speakers and poor on a lone short line (clipped, shouty), and it
picks a new pair of voices on every seed (it can't be told "old man" or "woman"). So each scene gets several seeded
takes, and a take is kept only if:
- speech-to-text hears the right words,
- it isn't too long once silences are tightened,
- each speaker's pitch fits the character's gender (the turn is split at the biggest gap between heard words).

Hussain picks a take per scene by ear. The picked takes become the voice references (Dia's audio prompt) for the
remaining lines, so each character keeps one voice across the episode.

Run: ../../.venv-mlx/bin/python dia_casting.py [scene ...]
Output: audio/casting/<scene>/seed-NN.wav, audio/casting/<scene>/reel.m4a, audio/casting/casting.json
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
SEEDS = range(1, 9)
KEEP = 4  # takes per scene in the reel

SCENES = {
    "lunch": dict(text="[S1] Congratulations!! Oh, I'm so happy for you! [S2] ...On what?",
                  who=("AUNT", "GRANDPA"), genders=("f", "m"), max_s=6.5),
    "phone": dict(text="[S1] Mom... guess what? I'm engaged! [S2] (gasps) Oh my God! Oh my God!",
                  who=("PRIYA", "MOM"), genders=("f", "f"), max_s=7.0),
    "couch": dict(text="[S1] Priya's engaged! Can you believe it? [S2] Mm. Nice.",
                  who=("MOM", "DAD"), genders=("f", "m"), max_s=6.0),
}


def words(s: str) -> str:
    s = re.sub(r"\[S\d\]|\([^)]*\)", " ", s.lower())
    return " ".join(re.findall(r"[a-z']+", s))


def median_f0(a: np.ndarray, sr: int) -> float:
    """Median pitch over voiced frames (autocorrelation, 60–400 Hz)."""
    n, hop = int(sr * 0.04), int(sr * 0.01)
    if len(a) < n * 2:
        return 0.0
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
    pad = np.zeros(int(sr * 0.08), np.float32)
    return np.concatenate([pad, np.concatenate([a[k * hop:(k + 1) * hop] for k in keep]), pad])


def gender_ok(f0: float, g: str) -> bool:
    return f0 >= 165 if g == "f" else 0 < f0 < 165


def main(names):
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    tts = load_model("mlx-community/Dia-1.6B-fp16")
    stt = load_stt("mlx-community/parakeet-tdt-0.6b-v3")
    sr = tts.sample_rate
    report_path = OUT / "casting.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    for name in names:
        spec = SCENES[name]
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        takes = []
        for seed in SEEDS:
            mx.random.seed(seed)
            res = list(tts.generate(text=spec["text"], max_tokens=int(spec["max_s"] * 86 * 1.8)))
            a = np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in res])
            a = tighten(a, sr)
            a = a / (np.abs(a).max() or 1) * 0.89
            path = d / f"seed-{seed:02d}.wav"
            sf.write(path, a, sr)
            r = stt.generate(str(path))
            heard = r.text.strip()
            match = difflib.SequenceMatcher(None, words(spec["text"]), words(heard)).ratio()
            # Split the two speakers at the biggest gap between heard words.
            toks = [t for s in r.sentences for t in s.tokens]
            gaps = [(toks[i + 1].start - toks[i].end, i) for i in range(len(toks) - 1)]
            if gaps:
                _, i = max(gaps)
                cut = (toks[i].end + toks[i + 1].start) / 2
            else:
                cut = len(a) / sr / 2
            f1, f2 = median_f0(a[:int(cut * sr)], sr), median_f0(a[int(cut * sr):], sr)
            dur = len(a) / sr
            ok = (match >= 0.75 and dur <= spec["max_s"] and gender_ok(f1, spec["genders"][0])
                  and gender_ok(f2, spec["genders"][1]))
            takes.append(dict(seed=seed, file=path.name, heard=heard, match=round(match, 2), f0=[round(f1), round(f2)],
                              cut=round(cut, 2), dur=round(dur, 2), ok=ok))
            print(f"{name:6s} seed {seed:2d}  {'OK ' if ok else '-- '} match {match:.2f}  f0 {f1:4.0f}/{f2:4.0f}  "
                  f"{dur:4.1f}s  | {heard}", flush=True)
        picks = sorted([t for t in takes if t["ok"]], key=lambda t: (-t["match"], t["dur"]))[:KEEP]
        if picks:
            parts = []
            for t in picks:
                a, _ = sf.read(d / t["file"], dtype="float32")
                parts += [a, np.zeros(int(sr * 1.0), np.float32)]
            sf.write(d / "reel.wav", np.concatenate(parts), sr)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "reel.wav"), "-c:a", "aac",
                            "-b:a", "160k", str(d / "reel.m4a")], check=True)
        report[name] = dict(text=spec["text"], who=spec["who"], takes=takes, reel=[t["seed"] for t in picks])
        report_path.write_text(json.dumps(report, indent=2))
        print(f"{name}: reel = seeds {[t['seed'] for t in picks]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(SCENES))
