"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.m4a (WhatsApp voice note, 2026-09-25, one take, 9.5 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 10 ms energy map of the cleaned take. The first word starts at 1.56 s. Sentence gaps are at
2.76-3.30 s and 5.62-6.01 s (plus a comma pause after "zero" at 4.44-4.78 s and before "or a crash" at 7.64-7.78 s).
The take ends at 8.50 s. Re-measure if the take changes.
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

NOISE = (0.10, 1.30)  # silence before the first word
TRIM = (1.48, 8.63)  # 80 ms before "That's", 130 ms after "crash"
PHRASES = [  # absolute times in the raw take
    (1.56, "That's an off-by-one error."),
    (3.30, "Computers count from zero, people from one."),
    (6.01, "One slip means a skipped item, or a crash."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
