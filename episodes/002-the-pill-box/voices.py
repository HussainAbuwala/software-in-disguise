"""Generate Episode 02 (remake, the pill box) dialogue with Kokoro-82M (local, Apache-2.0).

The cast voices chosen here are permanent for the recurring cast. Choice rationale is in audio/casting.md.

    KOKORO_MODEL_DIR=/path/to/models ../../.venv/bin/python voices.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = Path(__file__).resolve().parent
MODEL_DIR = Path(os.environ.get("KOKORO_MODEL_DIR", "/Users/hussainabuwala/Documents/ChatGPT/New project/concert-short/v3/models"))
OUT = HERE / "audio" / "dialogue"

CAST = {
    "DEV": ("am_puck", 1.0),
    "MIRA": ("af_heart", 0.95),
    "JO": ("af_nicole", 0.9),
    "MOM": ("bf_isabella", 0.95),  # Hussain picked mom-E by ear for Episode 03's remake
    # Stand-in for Hussain's recorded reveal. Replaced automatically when audio/reveal-hussain.* exists.
    "NARRATOR": ("am_michael", 1.0),
}

LINES = {
    # Hook v2 (2026-09-29): open on the danger, voice at frame 0.
    "mira-stop": ("MIRA", "Mom! Stop!", 1.1),
    "mom-my-pill": ("MOM", "What? It's my pill.", 1.0),
    "mira-already": ("MIRA", "You already took it!", 1.05),
    "mom-did-i": ("MOM", "...Did I?", 0.85),
    "mom-to-be-safe": ("MOM", "One more won't hurt. Just to be safe.", 0.95),
    "mira-yesterday": ("MIRA", "That's what you said yesterday!", 1.05),
    "mira-three-gone": ("MIRA", "Three gone. It's only Tuesday.", 0.95),
    "mom-which-day": ("MOM", "The strip doesn't say which day!", 1.0),
    "mira-use-this": ("MIRA", "Then we use this.", 0.95),
    "mira-wednesday-empty": ("MIRA", "Wednesday's empty. You took it.", 1.0),
    "mom-forget-again": ("MOM", "And if I forget again?", 1.0),
    "mira-ten-times": ("MIRA", "Check ten times. Still one pill.", 1.0),
    "mom-thursday": ("MOM", "Then I'll take Thursday's now.", 1.0),
    "mom-saves-time": ("MOM", "Saves time.", 0.95),
    # Hussain records these; the stand-in narrator is only for timing.
    "reveal-1": ("NARRATOR", "Doing it twice should only count once.", 1.0),
    "reveal-2": ("NARRATOR", "That's called idempotency.", 1.0),
    "reveal-3": ("NARRATOR", "It's why tapping Pay twice doesn't charge you twice.", 1.0),
}


def trim(audio: np.ndarray, sr: int) -> np.ndarray:
    active = np.flatnonzero(np.abs(audio) > 0.006)
    if not len(active):
        return audio
    start = max(0, active[0] - int(0.04 * sr))
    end = min(len(audio), active[-1] + int(0.12 * sr))
    return audio[start:end]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    kokoro = Kokoro(str(MODEL_DIR / "kokoro.onnx"), str(MODEL_DIR / "voices.bin"))
    manifest = {"engine": "Kokoro-82M via kokoro-onnx", "cast": {k: {"voice": v, "base_speed": s} for k, (v, s) in CAST.items()}, "lines": {}}
    for key, (who, text, speed) in LINES.items():
        voice = CAST[who][0]
        audio, sr = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
        audio = trim(audio, sr)
        peak = float(np.max(np.abs(audio)))
        audio = audio * (0.85 / peak)
        sf.write(OUT / f"{key}.wav", audio, sr)
        manifest["lines"][key] = {"speaker": who, "voice": voice, "speed": speed, "text": text, "duration": round(len(audio) / sr, 3)}
        print(f"{key:20s} {who:8s} {len(audio) / sr:5.2f}s  {text}")
    (HERE / "audio" / "dialogue.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
