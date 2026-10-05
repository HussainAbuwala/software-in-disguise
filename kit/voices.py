"""Character voices (from Episode 1's remake, 2026-10-04/05), run in the mlx venv (`.venv-mlx`, Apple Silicon).

The pipeline that worked:
1. Each character's voice is designed once with Qwen3-TTS VoiceDesign from a written description (age, tone). Dia
   alone can't be told who is speaking (it rarely gave an old man).
2. Each two-person exchange is generated with Dia, using the two characters' reference clips as its audio prompt, so
   it keeps their voices and adds natural timing, gasps and pauses. Dia's output excludes the prompt.
3. Takes are checked with speech-to-text (right words), length, and each speaker's pitch against their reference.
4. Where Dia won't give a line the right voice (it happened with a reply right after another speaker), Qwen3-TTS Base
   clones the reference voice for that line instead.
"""

from __future__ import annotations

import difflib
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

QWEN_DESIGN = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16"
QWEN_CLONE = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
DIA = "mlx-community/Dia-1.6B-fp16"
ASR = "mlx-community/parakeet-tdt-0.6b-v3"


def words(s: str) -> str:
    s = re.sub(r"\[S\d\]|\([^)]*\)", " ", s.lower())
    return " ".join(re.findall(r"[a-z']+", s))


def match(expected: str, heard: str) -> float:
    return difflib.SequenceMatcher(None, words(expected), words(heard)).ratio()


def median_f0(a: np.ndarray, sr: int) -> float:
    """Median pitch over voiced frames (autocorrelation, 60–400 Hz)."""
    n, hop = int(sr * 0.04), int(sr * 0.01)
    if len(a) < n * 2:
        return 0.0
    rms_floor = np.sqrt(np.mean(a ** 2)) * 0.5
    lo, hi = int(sr / 400), int(sr / 60)
    f0s = []
    for i in range(0, len(a) - n, hop):
        f = a[i:i + n] - a[i:i + n].mean()
        if np.sqrt(np.mean(f ** 2)) < rms_floor:
            continue
        ac = np.correlate(f, f, "full")[n - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.5:
            f0s.append(sr / lag)
    return float(np.median(f0s)) if f0s else 0.0


def tighten(a: np.ndarray, sr: int, gap_s=0.45) -> np.ndarray:
    """Trim silence at both ends and shorten any pause longer than gap_s."""
    hop = int(sr * 0.02)
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    voiced = e > max(0.01, e.max() * 0.06)
    if not voiced.any():
        return a
    idx = np.flatnonzero(voiced)
    keep, run = [], 0
    for k in range(idx[0], idx[-1] + 1):
        run = 0 if voiced[k] else run + 1
        if run * 0.02 <= gap_s:
            keep.append(k)
    pad = np.zeros(int(sr * 0.08), np.float32)
    return np.concatenate([pad, np.concatenate([a[k * hop:(k + 1) * hop] for k in keep]), pad])


def resample(a: np.ndarray, src: int, dst: int) -> np.ndarray:
    if src == dst:
        return a
    n = int(len(a) * dst / src)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)


def speaker_cut(asr_result, text: str, dur: float) -> float:
    """Where S2 starts: the first heard word after as many words as S1's line has."""
    n1 = len(words(text.split("[S2]")[0]).split())
    starts = [t.start for s in asr_result.sentences for t in s.tokens if t.text.startswith(" ")]
    return starts[n1] if len(starts) > n1 else dur / 2


def to_m4a(wav: Path):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "160k",
                    str(wav.with_suffix(".m4a"))], check=True)


def reel(paths, out: Path, gap_s=1.0):
    parts, sr0 = [], None
    for p in paths:
        a, sr = sf.read(p, dtype="float32")
        sr0 = sr0 or sr
        parts += [resample(a, sr, sr0), np.zeros(int(sr0 * gap_s), np.float32)]
    sf.write(out, np.concatenate(parts), sr0)
    to_m4a(out)
