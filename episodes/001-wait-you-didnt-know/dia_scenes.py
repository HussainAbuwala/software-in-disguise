"""Character dialogue for the Episode 1 remake: Dia scenes in voices designed with Qwen3-TTS.

Unprompted, Dia picks random voices (it rarely gave an old man for Grandpa), so each scene starts from a reference
clip: the two characters' designed voices (`voice_refs.py`) back to back, with their transcript tagged [S1]/[S2].
Dia then continues the scene in those voices with its own natural timing, gasps and pauses.

Takes are kept if speech-to-text hears the scene's words, the take isn't too long, and the speakers' pitch matches
the reference voices. Hussain picks one take per scene by ear.

Run: ../../.venv-mlx/bin/python dia_scenes.py [scene ...]
Output: audio/scenes/<scene>/seed-NN.wav, audio/scenes/<scene>/reel.m4a, audio/scenes/scenes.json
"""

from __future__ import annotations

import difflib
import json
import subprocess
import sys
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf

from dia_casting import median_f0, tighten, words

HERE = Path(__file__).parent
REFS = HERE / "audio" / "refs"
OUT = HERE / "audio" / "scenes"
SEEDS = range(1, 7)
KEEP = 3

# The reference take chosen for each character (pitch and transcript checked, 2026-10-04).
VOICE = {"GRANDPA": "grandpa/take-1", "AUNT": "aunt/take-1", "MOM": "mom/take-3", "DAD": "dad/take-2",
         "PRIYA": "priya/take-2"}

SCENES = {
    "s01-lunch": dict(who=("AUNT", "GRANDPA"),
                      text="[S1] Congratulations!! Oh, I'm so happy for you! [S2] ...On what?", max_s=6.0),
    "s02-phone": dict(who=("PRIYA", "MOM"),
                      text="[S1] Mom... guess what? I'm engaged! [S2] (gasps) Oh my God! Oh my God!", max_s=6.5),
    "s03-couch": dict(who=("MOM", "DAD"), text="[S1] Priya's engaged! Can you believe it? [S2] Mm. Nice.", max_s=5.5),
    "s06-tells": dict(who=("MOM", "GRANDPA"), text="[S1] Dad... Priya's engaged! [S2] Oh!", max_s=4.0),
    "s08-june": dict(who=("PRIYA", "MOM"), text="[S1] Also... we moved the wedding to June. [S2] (gasps) What?",
                     max_s=5.0),
}


def speaker_cut(r, text: str, dur: float) -> float:
    """Where S2 starts: the start of the first heard word after as many words as S1's line has."""
    n1 = len(words(text.split("[S2]")[0]).split())
    starts = [t.start for s in r.sentences for t in s.tokens if t.text.startswith(" ")]
    return starts[n1] if len(starts) > n1 else dur / 2


def reference(a_name: str, b_name: str, sr: int):
    clips, texts = [], []
    for tag, name in (("[S1]", a_name), ("[S2]", b_name)):
        a, r = sf.read(REFS / f"{VOICE[name]}.wav", dtype="float32")
        if r != sr:
            n = int(len(a) * sr / r)
            a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
        clips += [a, np.zeros(int(sr * 0.35), np.float32)]
        texts.append(f"{tag} {(REFS / f'{VOICE[name]}.txt').read_text().strip()}")
    return np.concatenate(clips), " ".join(texts)


def main(names):
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    tts = load_model("mlx-community/Dia-1.6B-fp16")
    stt = load_stt("mlx-community/parakeet-tdt-0.6b-v3")
    sr = tts.sample_rate
    report_path = OUT / "scenes.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    for name in names:
        spec = SCENES[name]
        ref_audio, ref_text = reference(*spec["who"], sr)
        ref_f0 = [median_f0(*sf.read(REFS / f"{VOICE[w]}.wav", dtype="float32")) for w in spec["who"]]
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        takes = []
        for seed in SEEDS:
            mx.random.seed(seed)
            res = list(tts.generate(text=spec["text"], ref_audio=mx.array(ref_audio), ref_text=ref_text))
            a = np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in res])
            a = tighten(a, sr)
            a = a / (np.abs(a).max() or 1) * 0.89
            path = d / f"seed-{seed:02d}.wav"
            sf.write(path, a, sr)
            r = stt.generate(str(path))
            heard = r.text.strip()
            match = difflib.SequenceMatcher(None, words(spec["text"]), words(heard)).ratio()
            cut = speaker_cut(r, spec["text"], len(a) / sr)
            f1, f2 = median_f0(a[:int(cut * sr)], sr), median_f0(a[int(cut * sr):], sr)
            dur = len(a) / sr
            # Each speaker within ~35% of their reference pitch (pitch reads are rough on 1–2 words).
            pitch_ok = all(0 < f < rf * 1.35 and f > rf / 1.35 for f, rf in ((f1, ref_f0[0]), (f2, ref_f0[1])))
            ok = match >= 0.75 and dur <= spec["max_s"] and pitch_ok
            takes.append(dict(seed=seed, file=path.name, heard=heard, match=round(match, 2),
                              f0=[round(f1), round(f2)], ref_f0=[round(x) for x in ref_f0], dur=round(dur, 2), ok=ok))
            print(f"{name:10s} seed {seed}  {'OK ' if ok else '-- '} match {match:.2f}  f0 {f1:4.0f}/{f2:4.0f} "
                  f"(ref {ref_f0[0]:.0f}/{ref_f0[1]:.0f})  {dur:4.1f}s | {heard}", flush=True)
        picks = sorted([t for t in takes if t["ok"]], key=lambda t: (-t["match"], t["dur"]))[:KEEP]
        if not picks:  # nothing passed every check: still give Hussain the closest takes to judge by ear
            picks = sorted(takes, key=lambda t: (-t["match"], t["dur"]))[:KEEP]
        parts = []
        for t in picks:
            a, _ = sf.read(d / t["file"], dtype="float32")
            parts += [a, np.zeros(int(sr * 1.0), np.float32)]
        sf.write(d / "reel.wav", np.concatenate(parts), sr)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "reel.wav"), "-c:a", "aac", "-b:a", "160k",
                        str(d / "reel.m4a")], check=True)
        report[name] = dict(text=spec["text"], who=spec["who"], takes=takes, reel=[t["seed"] for t in picks])
        report_path.write_text(json.dumps(report, indent=2))
        print(f"{name}: reel = seeds {[t['seed'] for t in picks]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(SCENES))
