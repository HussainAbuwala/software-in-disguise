"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.mp4 (WhatsApp voice note, 2026-09-27, one take, 5.0 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 10 ms energy map of the take: speech runs 0.63-3.85 s, with the sentence break (the
quietest dip) at about 2.45 s. Re-measure if the take changes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kit.clean_voice import clean  # noqa: E402

RAW = HERE / "audio" / "source" / "reveal-hussain-raw.mp4"
OUT = HERE / "audio" / "reveal-hussain.wav"
TIMINGS = HERE / "audio" / "reveal-hussain.json"

NOISE = (0.05, 0.55)  # silence before the first word
TRIM = (0.55, 3.97)  # 80 ms before "Software", 120 ms after "criteria"
PHRASES = [  # absolute times in the raw take
    (0.63, "Software teams write this list first."),
    (2.50, "It's called acceptance criteria."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
