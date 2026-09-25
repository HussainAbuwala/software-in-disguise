"""Generate Episode 05 dialogue with Kokoro-82M (local, Apache-2.0).

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
    # Stand-in for Hussain's recorded reveal. Replaced automatically when audio/reveal-hussain.* exists.
    "NARRATOR": ("am_michael", 1.0),
}

LINES = {
    "mira-said-milk": ("MIRA", "You said there was milk.", 0.95),
    "dev-i-checked": ("DEV", "There is. I checked.", 1.0),
    "mira-jo-asleep": ("MIRA", "Is Jo still asleep?", 0.95),
    "dev-fast-asleep": ("DEV", "Fast asleep.", 1.0),
    "jo-morning": ("JO", "Morning!", 0.95),
    "mira-raining": ("MIRA", "Is it still raining?", 0.95),
    "dev-sunny": ("DEV", "Nope. Sunny.", 1.0),
    "dev-sunny-at-seven": ("DEV", "It was sunny at seven.", 0.95),
    "mira-coffee": ("MIRA", "Is there coffee?", 0.95),
    "dev-yep-checked": ("DEV", "Yep. Checked.", 1.0),
    "reveal-1": ("NARRATOR", "That's a stale cache.", 1.0),
    "reveal-2": ("NARRATOR", "An answer saved once, and never checked again.", 1.0),
    "reveal-3": ("NARRATOR", "It's why a site can show you yesterday's price.", 1.0),
    "reveal-4": ("NARRATOR", "Good caches expire.", 0.97),
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
