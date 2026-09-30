"""Prepare Hussain's reveal take: denoise, trim to the spoken words, and record phrase timings for the captions.

    ../../.venv/bin/python prep_reveal.py

Input:  audio/source/reveal-hussain-raw.mp4 (WhatsApp voice note, 2026-09-29 9:11 PM, one take, 7.7 s)
Output: audio/reveal-hussain.wav   cleaned + trimmed; render_episode.py picks it up automatically
        audio/reveal-hussain.json  phrase start times relative to the trimmed file

Timings were read from a 50 ms energy map of the take and checked against whisper.cpp word times: speech runs
1.10-6.65 s, with pauses before "That's" (2.60-2.85 s) and before "It's" (4.05-4.40 s). Re-measure if the take changes.
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

NOISE = (0.35, 1.0)  # silence before the first word (after the tap at 0.15 s)
TRIM = (1.02, 6.80)  # 80 ms before "Doing", ~150 ms after "twice"
PHRASES = [  # absolute times in the raw take
    (1.10, "Doing it twice should only count once."),
    (2.90, "That's called idempotency."),
    (4.45, "It's why tapping Pay twice doesn't charge you twice."),
]


def main():
    clean(RAW, OUT, NOISE, TRIM)
    captions = [[round(t - TRIM[0], 3), text] for t, text in PHRASES]
    TIMINGS.write_text(json.dumps({"source": RAW.name, "trim": TRIM, "captions": captions}, indent=2) + "\n")
    print(OUT, TIMINGS)


if __name__ == "__main__":
    main()
