"""Audio for code-drawn episodes: loading and levelling speech, synthesized sound effects and music, and a mixer
that ducks everything under dialogue. Everything is generated; no downloaded samples.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000


def upsample(x: np.ndarray, src: int) -> np.ndarray:
    """Band-limited resample to 48 kHz via FFT zero-padding (Kokoro outputs 24 kHz)."""
    if src == SR:
        return x.astype(np.float64)
    n = len(x)
    m = round(n * SR / src)
    spec = np.fft.rfft(x)
    out = np.zeros(m // 2 + 1, dtype=complex)
    k = min(len(spec), len(out))
    out[:k] = spec[:k]
    return np.fft.irfft(out, n=m) * (m / n)


def load_wav(path: Path) -> np.ndarray:
    audio, sr = sf.read(path, always_2d=False)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    return upsample(audio, sr)


def level(x: np.ndarray, rms_db: float = -20.0) -> np.ndarray:
    """Match speech loudness across voices (a whispery voice peaks low but should sound as present)."""
    active = x[np.abs(x) > 0.01]
    rms = np.sqrt(np.mean(active**2)) if len(active) else 1.0
    y = x * (10 ** (rms_db / 20) / rms)
    peak = np.max(np.abs(y))
    return y / peak * 0.95 if peak > 0.95 else y


def env(n: int, attack=0.005, release=0.05) -> np.ndarray:
    e = np.ones(n)
    a, r = min(n, int(attack * SR)), min(n, int(release * SR))
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def band(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    spec[(freqs < lo) | (freqs > hi)] = 0
    return np.fft.irfft(spec, n=len(x))


def noise(seconds: float, lo: float, hi: float, seed: int = 0) -> np.ndarray:
    x = band(np.random.default_rng(seed).standard_normal(int(seconds * SR)), lo, hi)
    return x / (np.max(np.abs(x)) + 1e-9)


def t_axis(seconds: float) -> np.ndarray:
    return np.arange(int(seconds * SR)) / SR


def pluck(freq: float, seconds: float = 1.4, damp: float = 0.995, seed: int = 0) -> np.ndarray:
    """Karplus-Strong plucked string: a low pizzicato bass for the standoff."""
    n, period = int(seconds * SR), int(SR / freq)
    buf = np.random.default_rng(seed).uniform(-1, 1, period)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = damp * 0.5 * (buf[i % period] + buf[(i + 1) % period])
    out = band(out, 30, 2500)
    return out / (np.max(np.abs(out)) + 1e-9) * env(n, 0.002, 0.3)


def tick() -> np.ndarray:
    t = t_axis(0.06)
    return (np.sin(2 * np.pi * 1900 * t) * 0.7 + np.sin(2 * np.pi * 1150 * t) * 0.5) * np.exp(-t * 90)


def click() -> np.ndarray:
    t = t_axis(0.04)
    return (np.sin(2 * np.pi * 2600 * t) + noise(0.04, 2000, 9000, 5) * 0.6) * np.exp(-t * 160)


def thump(seed=0) -> np.ndarray:
    t = t_axis(0.12)
    return (np.sin(2 * np.pi * 85 * t) + noise(0.12, 60, 400, seed) * 0.4) * np.exp(-t * 40)


def tv_on() -> np.ndarray:
    t = t_axis(0.45)
    sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(90, 170, len(t))) / SR) * np.exp(-t * 6)
    crackle = noise(0.45, 1500, 8000, 7) * np.exp(-t * 20) * 0.5
    return (sweep + crackle) * env(len(t), 0.003, 0.1)


def chirp(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(rng.integers(2, 4)):
        d = rng.uniform(0.05, 0.09)
        t = t_axis(d)
        f0, f1 = rng.uniform(2800, 3400), rng.uniform(3900, 4700)
        ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR
        out += [np.sin(ph) * np.sin(np.pi * t / d), np.zeros(int(rng.uniform(0.03, 0.07) * SR))]
    return np.concatenate(out)


def snore(low: bool) -> np.ndarray:
    d = 0.8 if low else 0.6
    t = t_axis(d)
    shape = np.sin(np.pi * t / d) ** 1.5
    if low:
        rattle = 1 + 0.7 * np.sin(2 * np.pi * 26 * t)
        return noise(d, 90, 700, 11) * rattle * shape
    whistle = np.sin(2 * np.pi * np.cumsum(np.linspace(1150, 880, len(t))) / SR)
    return (whistle * 0.6 + noise(d, 300, 1500, 12) * 0.3) * shape


def slide_whistle() -> np.ndarray:
    t = t_axis(0.6)
    f = np.linspace(1500, 420, len(t)) * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.25 * np.sin(2 * ph)) * env(len(t), 0.01, 0.12)


def pad(seconds: float) -> np.ndarray:
    t = t_axis(seconds)
    chord = [130.81, 164.81, 196.0, 246.94, 293.66]  # Cmaj9: calm, "here's the answer"
    x = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t) for f in chord)
    return x / len(chord) * env(len(t), 0.7, 1.2)


def murmur(seconds: float, seed=21) -> np.ndarray:
    x = noise(seconds, 180, 1400, seed)
    slow = np.interp(t_axis(seconds), np.linspace(0, seconds, 12), np.random.default_rng(seed).uniform(0.5, 1, 12))
    return x * slow


def hum(seconds: float) -> np.ndarray:
    t = t_axis(seconds)
    return (np.sin(2 * np.pi * 60 * t) + 0.4 * np.sin(2 * np.pi * 120 * t)) * env(len(t), 0.2, 0.3)


class Mix:
    def __init__(self, seconds: float):
        n = int(seconds * SR) + SR
        self.dialogue = np.zeros(n)
        self.bed = np.zeros(n)  # everything that ducks under dialogue

    def add(self, wave: np.ndarray, start: float, gain: float = 1.0, dialogue: bool = False):
        track = self.dialogue if dialogue else self.bed
        i = int(start * SR)
        if i >= len(track):
            return
        j = min(len(track), i + len(wave))
        track[i:j] += wave[: j - i] * gain

    def render(self) -> np.ndarray:
        active = np.abs(self.dialogue) > 0.02
        k = int(0.12 * SR)
        near = np.convolve(active.astype(float), np.ones(k) / k, mode="same")
        duck = 1 - 0.55 * np.clip(near * 4, 0, 1)
        out = self.dialogue + self.bed * duck
        return out / max(1.0, np.max(np.abs(out)) / 0.95)


# --- added for Episode 05 --------------------------------------------------------------------------------------


def ding() -> np.ndarray:
    """Small bell: a memory note popping up."""
    t = t_axis(0.7)
    return (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t) + 0.2 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 7)


def scribble(seconds: float = 0.45, seed: int = 31) -> np.ndarray:
    """Pencil on paper: bursts of bright noise, one per stroke."""
    x = noise(seconds, 2500, 9000, seed)
    t = t_axis(seconds)
    strokes = np.clip(np.sin(2 * np.pi * 11 * t), 0, 1) ** 2
    return x * strokes * env(len(t), 0.01, 0.05)


def drip() -> np.ndarray:
    t = t_axis(0.12)
    f = np.linspace(700, 1800, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)


def gulp(seed: int = 0) -> np.ndarray:
    t = t_axis(0.16)
    f = np.linspace(260, 140, len(t))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.16)
    return body + noise(0.16, 150, 900, seed) * 0.25 * np.exp(-t * 20)


def thunder(seconds: float = 2.2, seed: int = 51) -> np.ndarray:
    """A crack followed by a long rolling rumble."""
    t = t_axis(seconds)
    crack = noise(seconds, 800, 7000, seed) * np.exp(-t * 18)
    roll = noise(seconds, 30, 260, seed + 1) * (np.exp(-t * 1.4)) * (1 + 0.5 * np.sin(2 * np.pi * 3 * t))
    return (crack * 0.7 + roll) * env(len(t), 0.004, 0.4)


def rain(seconds: float, seed: int = 61) -> np.ndarray:
    return noise(seconds, 900, 7000, seed) * 0.6 + noise(seconds, 200, 900, seed + 1) * 0.3


def sad_trombone() -> np.ndarray:
    """Four falling notes, the last one wobbling: the classic 'wah wah wah wahhh'."""
    out = []
    for f, d in ((233.08, 0.28), (220.0, 0.28), (207.65, 0.28), (196.0, 0.8)):
        t = t_axis(d)
        vib = 1 + (0.012 * np.sin(2 * np.pi * 6 * t) if d > 0.5 else 0)
        ph = 2 * np.pi * np.cumsum(f * vib * np.ones(len(t))) / SR
        tone = sum(np.sin(k * ph) / k for k in range(1, 7))  # brassy saw-ish stack
        out.append(band(tone, 80, 2200) * env(len(t), 0.02, 0.06))
    x = np.concatenate(out)
    return x / (np.max(np.abs(x)) + 1e-9)


def crumple(seed: int = 71) -> np.ndarray:
    t = t_axis(0.35)
    crackles = (np.random.default_rng(seed).random(len(t)) > 0.985).astype(float)
    return band(crackles, 1500, 9000) * 6 * env(len(t), 0.01, 0.1) + noise(0.35, 1000, 5000, seed) * 0.2 * np.exp(-t * 8)


def door_thunk(seed: int = 81) -> np.ndarray:
    t = t_axis(0.2)
    return (np.sin(2 * np.pi * 70 * t) + noise(0.2, 80, 600, seed) * 0.6) * np.exp(-t * 25)


def tonk() -> np.ndarray:
    """Hollow knock: an empty carton set down."""
    t = t_axis(0.25)
    return (np.sin(2 * np.pi * 330 * t) + 0.6 * np.sin(2 * np.pi * 495 * t)) * np.exp(-t * 22)
