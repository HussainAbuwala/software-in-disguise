"""Generate Episode 04 dialogue with Kokoro-82M (local, Apache-2.0).

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
    "TV": ("bm_george", 0.88),  # golf commentator, heard quietly from the TV
    # Stand-in for Hussain's recorded reveal. Replaced automatically when audio/reveal-hussain.* exists.
    "NARRATOR": ("am_michael", 1.0),
}

LINES = {
    "dev-batteries-now": ("DEV", "Batteries. Now.", 1.0),
    "mira-remote-first": ("MIRA", "Remote first.", 0.95),
    "dev-doesnt-work": ("DEV", "It doesn't even work without them!", 1.05),
    "mira-why-holding": ("MIRA", "Then why are you holding it?", 0.95),
    "dev-let-go": ("DEV", "You could just let go.", 0.92),
    "mira-you-first": ("MIRA", "You first.", 0.9),
    "jo-button": ("JO", "It has a button.", 0.9),
    "tv-golf-1": ("TV", "Lovely conditions out here this morning.", 0.88),
    "tv-golf-2": ("TV", "He'll want to take his time with this one.", 0.88),
    "reveal-1": ("NARRATOR", "That's a deadlock.", 1.0),
    "reveal-2": ("NARRATOR", "Each one holds what the other needs,", 1.0),
    "reveal-3": ("NARRATOR", "so both wait forever.", 0.97),
    "reveal-4": ("NARRATOR", "It's one reason apps freeze.", 1.0),
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
