"""Generate Episode 03 (remake) dialogue with Kokoro-82M (local, Apache-2.0).

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
    # New, heard only through the phone. Hussain picked mom-E by ear (audio/audition/casting.md).
    "MOM": ("bf_isabella", 0.95),
    # Stand-in for Hussain's recorded reveal. Replaced automatically when audio/reveal-hussain.* exists.
    "NARRATOR": ("am_michael", 1.0),
}

LINES = {
    "dev-quick-thing": ("DEV", "Just one quick thing—", 1.0),
    "mira-writing": ("MIRA", "I'm writing Priya's wedding speech!", 1.0),
    "dev-two-minutes": ("DEV", "Just two minutes!", 1.0),
    "mom-quick": ("MOM", "Sweetie, one quick thing... did you eat?", 0.95),
    "mira-yes-mom": ("MIRA", "Yes, Mom?", 0.9),
    "mira-laundry": ("MIRA", "Laundry. Two minutes.", 0.95),
    "mira-wedding": ("MIRA", "The wedding is tomorrow.", 0.85),
    "jo-every-one": ("JO", "Every one of those was quick.", 0.9),
    "jo-went-first": ("JO", "So they always went first.", 0.9),
    "mira-nine-sharp": ("MIRA", "Tomorrow. Nine sharp.", 0.95),
    "reveal-1": ("NARRATOR", "If quick jobs always go first, the big one never runs.", 1.0),
    "reveal-2": ("NARRATOR", "That's called starvation.", 1.0),
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
