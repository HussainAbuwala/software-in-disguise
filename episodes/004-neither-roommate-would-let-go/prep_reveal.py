"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.m4a (WhatsApp voice note, 2026-09-24, one take, 10.3 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 10 ms energy map of the cleaned take. A lip click (0.75 s) and a breath (1.42 s) precede
the first word at 1.84 s. Phrase gaps are at 2.80-3.24 s, 4.87-5.07 s and 6.36-6.97 s. The take ends at 8.62 s.
Re-measure if the take changes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kit.clean_voice import clean  # noqa: E402

RAW = HERE / "audio" / "source" / "reveal-hussain-raw.m4a"
OUT = HERE / "audio" / "reveal-hussain.wav"
TIMINGS = HERE / "audio" / "reveal-hussain.json"

NOISE = (0.05, 0.55)  # silence before the first sound
TRIM = (1.76, 8.75)  # 80 ms before "That's", 130 ms after "freeze"
PHRASES = [  # absolute times in the raw take
    (1.84, "That's a deadlock."),
    (3.24, "Each one holds what the other needs,"),
    (5.05, "so both wait forever."),
    (6.97, "It's one reason apps freeze."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
