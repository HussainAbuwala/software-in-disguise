from __future__ import annotations

from pathlib import Path
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


ROOT = Path(__file__).resolve().parent
MODEL_DIR = Path(os.environ.get(
    "KOKORO_MODEL_DIR",
    "/Users/hussainabuwala/Documents/ChatGPT/New project/concert-short/v3/models",
))
OUT = ROOT / "audio"
AUDITIONS = OUT / "auditions"
FINAL = OUT / "dialogue"
AUDITIONS.mkdir(parents=True, exist_ok=True)
FINAL.mkdir(parents=True, exist_ok=True)

kokoro = Kokoro(str(MODEL_DIR / "kokoro.onnx"), str(MODEL_DIR / "voices.bin"))


def lang_for(voice: str) -> str:
    return "en-gb" if voice.startswith("b") else "en-us"


def synth(path: Path, text: str, voice: str, speed: float = 1.0) -> dict:
    audio, sample_rate = kokoro.create(
        text, voice=voice, speed=speed, lang=lang_for(voice)
    )
    active = np.flatnonzero(np.abs(audio) > 0.006)
    if len(active):
        start = max(0, active[0] - int(0.075 * sample_rate))
        end = min(len(audio), active[-1] + int(0.18 * sample_rate))
        audio = audio[start:end]
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    if peak:
        audio *= min(1.0, 0.82 / peak)
    sf.write(path, audio, sample_rate)
    return {
        "voice": voice,
        "speed": speed,
        "language": lang_for(voice),
        "text": text,
        "duration": len(audio) / sample_rate,
        "sample_rate": sample_rate,
        "peak": float(np.max(np.abs(audio))) if len(audio) else 0.0,
        "rms": float(np.sqrt(np.mean(audio**2))) if len(audio) else 0.0,
    }


auditions = {
    "groom-G1": ("am_liam", "I'm getting married at two. Time for a haircut? What if you just cut the front? That's quick.", 1.00),
    "groom-G2": ("am_eric", "I'm getting married at two. Time for a haircut? What if you just cut the front? That's quick.", 0.98),
    "groom-G3": ("am_michael", "I'm getting married at two. Time for a haircut? What if you just cut the front? That's quick.", 0.98),
    "barber-B1": ("bm_george", "Plenty of time. You're next. Won't take a minute.", 0.96),
    "barber-B2": ("am_adam", "Plenty of time. You're next. Won't take a minute.", 0.95),
    "barber-B3": ("am_onyx", "Plenty of time. You're next. Won't take a minute.", 0.96),
    "narrator-N1": ("bf_emma", "That's starvation. Imagine your report never printing because every new one-page job jumps ahead. Good software makes sure waiting work gets a turn.", 1.01),
    "narrator-N2": ("bm_daniel", "That's starvation. Imagine your report never printing because every new one-page job jumps ahead. Good software makes sure waiting work gets a turn.", 1.00),
    "beard-C1A": ("am_puck", "Just a quick beard trim?", 1.00),
    "beard-C1B": ("am_echo", "Just a quick beard trim?", 0.98),
    "neckline-C2A": ("am_fenrir", "Just the neckline.", 1.00),
    "neckline-C2B": ("bm_lewis", "Just the neckline.", 0.98),
    "moustache-C3A": ("bm_fable", "Only the moustache.", 0.95),
    "moustache-C3B": ("am_santa", "Only the moustache.", 0.96),
}

manifest = {"engine": "Kokoro-82M via kokoro-onnx", "candidates": {}}
for candidate, (voice, text, speed) in auditions.items():
    manifest["candidates"][candidate] = synth(
        AUDITIONS / f"{candidate}.wav", text, voice, speed
    )


provisional = {
    "groom": ("am_liam", 1.00),
    "barber": ("bm_george", 0.96),
    "beard_customer": ("am_echo", 0.98),
    "neckline_customer": ("bm_lewis", 0.98),
    "moustache_customer": ("bm_fable", 0.95),
    "narrator": ("bf_emma", 1.01),
}

dialogue = [
    ("01-groom-opening", "groom", "I'm getting married at two. Time for a haircut?"),
    ("02-barber-promise", "barber", "Plenty of time. You're next."),
    ("03-beard-request", "beard_customer", "Just a quick beard trim?"),
    ("04-barber-two-minutes", "barber", "Two minutes."),
    ("05-groom-sure", "groom", "Sure."),
    ("06-neckline-request", "neckline_customer", "Just the neckline."),
    ("07-barber-then-you", "barber", "Then you're up."),
    ("08-moustache-request", "moustache_customer", "Only the moustache."),
    ("09-barber-one-minute", "barber", "Won't take a minute."),
    ("10-groom-payoff", "groom", "What if you just cut the front? That's quick."),
    ("11-narrator-reveal", "narrator", "That's starvation. Imagine your report never printing because every new one-page job jumps ahead. Good software makes sure waiting work gets a turn."),
]

dialogue_meta = {}
for line_id, role, text in dialogue:
    voice, speed = provisional[role]
    dialogue_meta[line_id] = {
        "speaker": role,
        **synth(FINAL / f"{line_id}.wav", text, voice, speed),
    }


def silence(path: Path, seconds: float, sample_rate: int = 24000) -> None:
    sf.write(path, np.zeros(int(seconds * sample_rate), dtype=np.float32), sample_rate)


silence_clip = AUDITIONS / "silence-700ms.wav"
silence(silence_clip, 0.7)


def concat_wavs(output: Path, inputs: list[Path]) -> None:
    file_list = output.with_suffix(".txt")
    file_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in inputs))
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", str(file_list), "-ar", "24000", "-ac", "1", str(output)
    ], check=True)


for role, names in {
    "groom": ["groom-G1", "groom-G2", "groom-G3"],
    "barber": ["barber-B1", "barber-B2", "barber-B3"],
    "narrator": ["narrator-N1", "narrator-N2"],
    "supporting": ["beard-C1A", "beard-C1B", "neckline-C2A", "neckline-C2B", "moustache-C3A", "moustache-C3B"],
}.items():
    clips: list[Path] = []
    for name in names:
        clips.extend([AUDITIONS / f"{name}.wav", silence_clip])
    concat_wavs(AUDITIONS / f"comparison-{role}.wav", clips[:-1])


def chemistry(name: str, groom_voice: str, barber_voice: str, groom_speed: float, barber_speed: float) -> None:
    folder = AUDITIONS / f"chemistry-{name}"
    folder.mkdir(exist_ok=True)
    pieces = [
        ("01.wav", "I'm getting married at two. Time for a haircut?", groom_voice, groom_speed),
        ("02.wav", "Plenty of time. You're next.", barber_voice, barber_speed),
        ("03.wav", "Just a quick beard trim?", "am_echo", 0.98),
        ("04.wav", "Two minutes.", barber_voice, barber_speed),
        ("05.wav", "What if you just cut the front? That's quick.", groom_voice, groom_speed),
    ]
    files: list[Path] = []
    for filename, text, voice, speed in pieces:
        path = folder / filename
        synth(path, text, voice, speed)
        files.extend([path, silence_clip])
    concat_wavs(AUDITIONS / f"chemistry-{name}.wav", files[:-1])


chemistry("P1-restrained", "am_liam", "bm_george", 1.00, 0.96)
chemistry("P2-warmer", "am_michael", "am_adam", 0.98, 0.95)

concat_wavs(AUDITIONS / "comparison-reel.wav", [
    AUDITIONS / "comparison-groom.wav", silence_clip,
    AUDITIONS / "comparison-barber.wav", silence_clip,
    AUDITIONS / "comparison-narrator.wav", silence_clip,
    AUDITIONS / "comparison-supporting.wav", silence_clip,
    AUDITIONS / "chemistry-P1-restrained.wav", silence_clip,
    AUDITIONS / "chemistry-P2-warmer.wav",
])

(AUDITIONS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
(OUT / "dialogue.json").write_text(json.dumps(dialogue_meta, indent=2) + "\n")
print(json.dumps({
    "audition_candidates": len(auditions),
    "dialogue_lines": len(dialogue),
    "provisional": provisional,
}, indent=2))
