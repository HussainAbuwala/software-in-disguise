"""Clean a phone voice recording: remove rumble, background noise and hiss without touching the voice.

    python -m kit.clean_voice in.m4a out.wav --noise 0.05 0.55 --trim 1.76 8.75

The noise profile is learned from a stretch of the recording where nobody is speaking (`--noise START END`, usually
the half-second before the first word). Chain:

1. 75 Hz high-pass: rumble, handling noise and hum; below a speaking voice's lowest fundamental.
2. FFT denoise (afftdn) using the sampled profile, with noise tracking for anything that drifts.
3. Soft gate (-38 dB threshold, at most -24 dB of reduction) so pauses go quiet without chopping word tails.
4. 15 kHz low-pass: remaining hiss above the useful voice range.

Episode 04's take: noise went from -48 dBFS to about -75 dBFS while speech level and the 150 Hz-6 kHz band
levels were unchanged to within 0.1 dB.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def chain(noise_start: float, noise_end: float) -> str:
    return ",".join([
        "highpass=f=75:poles=2",
        f"asendcmd=c='{noise_start} afftdn sn start; {noise_end} afftdn sn stop'",
        "afftdn=nr=20:nf=-50:tn=1",
        "agate=threshold=0.012:ratio=3:range=0.06:attack=5:release=180",
        "lowpass=f=15000",
    ])


def clean(src: Path, dst: Path, noise=(0.05, 0.55), trim: tuple[float, float] | None = None, sr: int = 48000):
    af = chain(*noise)
    if trim:
        start, end = trim
        fade = 0.03
        af += f",atrim={start}:{end},asetpts=PTS-STARTPTS,afade=t=in:d={fade},afade=t=out:st={end - start - fade}:d={fade}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", str(sr), "-af", af, str(dst)], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("src", type=Path)
    p.add_argument("dst", type=Path)
    p.add_argument("--noise", type=float, nargs=2, default=(0.05, 0.55), metavar=("START", "END"))
    p.add_argument("--trim", type=float, nargs=2, default=None, metavar=("START", "END"))
    a = p.parse_args()
    clean(a.src, a.dst, tuple(a.noise), tuple(a.trim) if a.trim else None)


if __name__ == "__main__":
    main()
