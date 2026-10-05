"""Voices for Episode 1, "The Last Room": reference voices (Qwen3-TTS), then each exchange (Dia), see kit/voices.py.

Run (mlx venv):  ../../.venv-mlx/bin/python voices.py refs     # design the missing reference voices
                 ../../.venv-mlx/bin/python voices.py scenes   # all exchanges (or name some)
Output: audio/refs/<who>/take-N.wav, audio/scenes/<scene>/seed-NN.wav, audio/scenes/<scene>/reel.m4a, voices.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit.voices import (ASR, DIA, QWEN_CLONE, QWEN_DESIGN, match, median_f0, reel, resample,  # noqa: E402
                        speaker_cut, tighten)

HERE = Path(__file__).parent
# Version A: two aunts (Meena, Lata), a male clerk, Priya. Version B (--b): two uncles (Raj, Vikram), Nisha at the
# desk, Dev explaining, all with deliberately lower, natural voices. Role ids stay MEENA/LATA/CLERK/PRIYA so the
# renderer is shared; only the drawings, voices and folders change.
VARIANT = "b" if "--b" in sys.argv else "a"
AUDIO = HERE / ("audio-b" if VARIANT == "b" else "audio")
REFS = AUDIO / "refs"
SCENES_DIR = AUDIO / "scenes"
REPORT = AUDIO / "voices.json"
# Natural speaking pitch ranges a reference voice must fall in (Hz). Version A's women came out around 300 Hz,
# which Hussain heard as too high.
PITCH = {"f": (165, 235), "m": (85, 150)}

if VARIANT == "a":
    # Meena (the aunt) and Priya were designed for the "Wait, you didn't know?" draft and are reused.
    CAST = {
        "MEENA": dict(take="meena/take-1", gender="f"),
        "PRIYA": dict(take="priya/take-2", gender="f"),
        "LATA": dict(gender="f", desc="A woman in her late fifties with a sharp, proud, slightly haughty voice, quick "
                                      "to take offence, crisp and precise.",
                     text="Excuse me, I have been coming to this hotel for twenty years. I know how it works."),
        "CLERK": dict(gender="m", desc="A man in his mid twenties with a flat, tired, polite voice, a deadpan hotel "
                                       "receptionist at the end of a long shift.",
                      text="Good evening. Yes, ma'am. I understand. I'm just checking the system for you."),
    }
else:
    CAST = {
        "MEENA": dict(gender="m", desc="A man in his early sixties with a very deep, low, gravelly bass voice, speaking "
                                       "firmly and slowly, a heavy, low-pitched baritone.",
                      text="Excuse me? I have been coming to this hotel for twenty years. I know how it works."),
        "LATA": dict(gender="m", desc="A man in his late sixties with a low, dry, precise voice, calm but stubborn, "
                                      "speaking slowly, natural low pitch.",
                     text="Now listen, young lady, I made this booking myself, on my own phone, three weeks ago."),
        "CLERK": dict(gender="f", desc="A woman in her late twenties with a low, calm, warm voice, a polite and "
                                       "unbothered hotel receptionist, natural low pitch, never shrill.",
                      text="Good evening, sir. Yes, I understand. I'm just checking the system for you."),
        "PRIYA": dict(gender="m", desc="A man in his late twenties with a relaxed, warm, friendly mid-low voice, "
                                       "easygoing and clear, like explaining something to his uncles.",
                      text="Okay, okay, everybody calm down. Let me just have a look at this, alright?"),
    }

SIR = "Sir" if VARIANT == "b" else "Ma'am"
TELL = "Tell him!" if VARIANT == "b" else "Tell her!"
SCENES = {
    "r01-mine": dict(who=("MEENA", "LATA"), text="[S1] That's my room! [S2] Excuse me, I booked it first!", max_s=5.0),
    "r02-one-room": dict(who=("LATA", "CLERK"), text=f"[S1] {TELL} [S2] {SIR}... we have one room.", max_s=4.5),
    "r03-got-it": dict(who=("MEENA", "LATA"), text="[S1] Got it! [S2] Got it!", max_s=3.0),
    "r04-show-me": dict(who=("PRIYA", "MEENA"), text="[S1] Wait. Show me your phones. [S2] Look! It says confirmed!",
                        max_s=5.0),
    "r05-same-moment": dict(who=("PRIYA", "LATA"),
                            text="[S1] You both tapped at the same moment. It checked for both of you before either "
                                 "booking was saved. [S2] So it sold it twice?!", max_s=8.5),
    "r06-race": dict(who=("PRIYA", "MEENA"),
                     text="[S1] Engineers call that a race condition. The fix is to lock the room while one booking "
                          "finishes. [S2] Hmph.", max_s=8.0),
    "r07-key": dict(who=("CLERK", "MEENA"), text="[S1] So... who gets the key? [S2] Mine!", max_s=4.0),
}
SEEDS = range(1, 7)
KEEP = 3

# Single lines where Dia wouldn't keep the speaker's voice or clipped the line: cloned per line with Qwen3-TTS Base.
LINES = {
    "lata_tell": ("LATA", TELL),
    "meena_got": ("MEENA", "Got it!"),
    "lata_got": ("LATA", "Got it!"),
    "meena_minegrab": ("MEENA", "Mine!"),
    "lata_mine": ("LATA", "Mine!"),
}
# Every line's key, per exchange (the renderer uses the same keys).
KEYS = {"r01-mine": ("meena_mine", "lata_first"), "r02-one-room": ("lata_tell", "clerk_one"),
        "r03-got-it": ("meena_got", "lata_got"), "r04-show-me": ("priya_wait", "meena_look"),
        "r05-same-moment": ("priya_same", "lata_twice"), "r06-race": ("priya_race", "meena_hmph"),
        "r07-key": ("clerk_key", "meena_minegrab")}
if VARIANT == "b":
    # Dia wouldn't hold the deep male reference voices (it came out at 290-350 Hz), so version B clones every line
    # with Qwen3-TTS from the character's reference voice.
    for scene, (k1, k2) in KEYS.items():
        spec = SCENES[scene]
        t1, t2 = spec["text"].split("[S2]")
        LINES[k1] = (spec["who"][0], t1.replace("[S1]", "").strip())
        LINES[k2] = (spec["who"][1], t2.strip())
LINES_DIR = AUDIO / "lines"


def ref_path(who: str) -> Path:
    return REFS / f"{CAST[who]['take']}.wav"


def design_refs():
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    todo = [w for w, c in CAST.items() if "desc" in c]
    model = load_model(QWEN_DESIGN)
    stt = load_stt(ASR)
    for who in todo:
        c = CAST[who]
        d = REFS / who.lower()
        d.mkdir(parents=True, exist_ok=True)
        best = None
        for k in range(1, 5):
            mx.random.seed(100 + k)
            res = list(model.generate_voice_design(text=c["text"], language="English", instruct=c["desc"]))
            a = np.concatenate([np.asarray(r.audio, np.float32).reshape(-1) for r in res])
            a = a / (np.abs(a).max() or 1) * 0.89
            path = d / f"take-{k}.wav"
            sf.write(path, a, model.sample_rate)
            (d / f"take-{k}.txt").write_text(c["text"])
            f0 = median_f0(a, model.sample_rate)
            m = match(c["text"], stt.generate(str(path)).text)
            lo, hi = PITCH[c["gender"]]
            off = 0 if lo <= f0 <= hi else min(abs(f0 - lo), abs(f0 - hi))
            print(f"{who} take {k}: f0 {f0:.0f} match {m:.2f} {'fits' if not off else f'off by {off:.0f} Hz'}",
                  flush=True)
            score = (-off, m)
            if best is None or score > best[1]:
                best = (k, score)
        c["take"] = f"{who.lower()}/take-{best[0]}"
        reel([d / f"take-{k}.wav" for k in range(1, 5)], d / "reel.wav")
    picks = {w: c["take"] for w, c in CAST.items()}
    (REFS / "picks.json").write_text(json.dumps(picks, indent=2))
    print("reference picks:", picks)


def load_picks():
    p = REFS / "picks.json"
    if p.exists():
        for w, take in json.loads(p.read_text()).items():
            CAST[w]["take"] = take


def generate_scenes(names):
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    load_picks()
    tts = load_model(DIA)
    stt = load_stt(ASR)
    sr = tts.sample_rate
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {}
    for name in names:
        spec = SCENES[name]
        clips, texts, ref_f0 = [], [], []
        for tag, who in zip(("[S1]", "[S2]"), spec["who"]):
            a, r = sf.read(ref_path(who), dtype="float32")
            ref_f0.append(median_f0(a, r))
            clips += [resample(a, r, sr), np.zeros(int(sr * 0.35), np.float32)]
            texts.append(f"{tag} {ref_path(who).with_suffix('.txt').read_text().strip()}")
        ref_audio, ref_text = np.concatenate(clips), " ".join(texts)
        d = SCENES_DIR / name
        d.mkdir(parents=True, exist_ok=True)
        takes = []
        for seed in SEEDS:
            mx.random.seed(seed)
            res = list(tts.generate(text=spec["text"], ref_audio=mx.array(ref_audio), ref_text=ref_text))
            a = tighten(np.concatenate([np.asarray(r.audio, np.float32).reshape(-1) for r in res]), sr)
            a = a / (np.abs(a).max() or 1) * 0.89
            path = d / f"seed-{seed:02d}.wav"
            sf.write(path, a, sr)
            r = stt.generate(str(path))
            m = match(spec["text"], r.text)
            cut = speaker_cut(r, spec["text"], len(a) / sr)
            f1, f2 = median_f0(a[:int(cut * sr)], sr), median_f0(a[int(cut * sr):], sr)
            dur = len(a) / sr
            pitch_ok = all(rf / 1.35 < f < rf * 1.35 for f, rf in ((f1, ref_f0[0]), (f2, ref_f0[1])))
            ok = m >= 0.75 and dur <= spec["max_s"] and pitch_ok
            takes.append(dict(seed=seed, heard=r.text.strip(), match=round(m, 2), f0=[round(f1), round(f2)],
                              ref_f0=[round(x) for x in ref_f0], cut=round(cut, 2), dur=round(dur, 2), ok=ok))
            print(f"{name:16s} seed {seed} {'OK ' if ok else '-- '} match {m:.2f} f0 {f1:4.0f}/{f2:4.0f} "
                  f"(ref {ref_f0[0]:.0f}/{ref_f0[1]:.0f}) {dur:4.1f}s | {r.text.strip()}", flush=True)
        picks = sorted([t for t in takes if t["ok"]], key=lambda t: (-t["match"], t["dur"]))[:KEEP] or \
            sorted(takes, key=lambda t: (-t["match"], t["dur"]))[:KEEP]
        reel([d / f"seed-{t['seed']:02d}.wav" for t in picks], d / "reel.wav")
        report[name] = dict(text=spec["text"], who=spec["who"], takes=takes, reel=[t["seed"] for t in picks])
        REPORT.write_text(json.dumps(report, indent=2))
        print(f"{name}: reel = seeds {[t['seed'] for t in picks]}", flush=True)


def clone_lines(names):
    from mlx_audio.stt.utils import load_model as load_stt
    from mlx_audio.tts.utils import load_model

    load_picks()
    model = load_model(QWEN_CLONE)
    stt = load_stt(ASR)
    LINES_DIR.mkdir(parents=True, exist_ok=True)
    picks = {}
    for key in names:
        who, text = LINES[key]
        ref = ref_path(who)
        rf0 = median_f0(*sf.read(ref, dtype="float32"))
        best = None
        for seed in range(1, 5):
            mx.random.seed(seed)
            res = list(model.generate(text=text, ref_audio=str(ref), ref_text=ref.with_suffix(".txt").read_text()))
            a = np.concatenate([np.asarray(r.audio, np.float32).reshape(-1) for r in res])
            a = tighten(a / (np.abs(a).max() or 1) * 0.89, model.sample_rate)
            path = LINES_DIR / f"{key}-{seed}.wav"
            sf.write(path, a, model.sample_rate)
            m = match(text, stt.generate(str(path)).text)
            f0 = median_f0(a, model.sample_rate)
            ok = m >= 0.75 and rf0 / 1.35 < f0 < rf0 * 1.35
            print(f"{key} seed {seed} {'OK ' if ok else '-- '} match {m:.2f} f0 {f0:.0f} (ref {rf0:.0f})", flush=True)
            score = (ok, m)
            if best is None or score > best[0]:
                best = (score, seed)
        picks[key] = best[1]
        sf.write(LINES_DIR / f"{key}.wav", *sf.read(LINES_DIR / f"{key}-{best[1]}.wav"))
    print("line picks:", picks)


if __name__ == "__main__":
    sys.argv = [a for a in sys.argv if a != "--b"]
    what = sys.argv[1]
    if what == "refs":
        design_refs()
    elif what == "lines":
        clone_lines(sys.argv[2:] or list(LINES))
    else:
        generate_scenes(sys.argv[2:] or list(SCENES))
