"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.mp4 (WhatsApp voice note, 2026-09-26, one take, 4.2 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 10 ms energy map of the take: the first phrase runs 0.58-2.02 s, a pause, then the second
phrase 2.35-3.33 s. Re-measure if the take changes.
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

NOISE = (0.05, 0.50)  # silence before the first word
TRIM = (0.50, 3.45)  # 80 ms before "Computers", 120 ms after "leader"
PHRASES = [  # absolute times in the raw take
    (0.58, "Computers get stuck like this too."),
    (2.35, "So they elect a leader."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
