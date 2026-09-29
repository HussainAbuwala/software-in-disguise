"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.mp4 (WhatsApp voice note, 2026-09-27, one take, 6.8 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 50 ms energy map of the take: speech runs 1.45-5.70 s, with the sentence break (the
quietest dip) at 4.35-4.55 s. Re-measure if the take changes.
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

NOISE = (0.05, 1.35)  # silence before the first word
TRIM = (1.37, 5.82)  # 80 ms before "If", 120 ms after "starvation"
PHRASES = [  # absolute times in the raw take
    (1.45, "If quick jobs always go first, the big one never runs."),
    (4.55, "That's called starvation."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
