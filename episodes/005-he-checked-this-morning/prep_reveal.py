"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.m4a (WhatsApp voice note, 2026-09-24, one take, 11.8 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 10 ms energy map of the cleaned take. A phone tap sits at 0.04-0.10 s; the first word
starts at 1.76 s. Phrase gaps are at 2.93-3.18 s, 5.73-6.29 s and 8.59-8.81 s (plus a comma pause at 4.41-4.62 s
inside phrase 2). The take ends at 10.15 s. Re-measure if the take changes.
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

NOISE = (0.27, 0.73)  # quiet stretch between the phone tap and the first word
TRIM = (1.68, 10.28)  # 80 ms before "That's", 130 ms after "expire"
PHRASES = [  # absolute times in the raw take
    (1.76, "That's a stale cache."),
    (3.18, "An answer saved once, and never checked again."),
    (6.29, "It's why a site can show you yesterday's price."),
    (8.81, "Good caches expire."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
