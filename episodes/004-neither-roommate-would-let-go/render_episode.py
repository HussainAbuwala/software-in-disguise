"""Render Episode 04 end to end: code-drawn shots, dialogue, sound design, captions, thumbnail.

    ../../.venv/bin/python voices.py           # once, or after changing lines
    ../../.venv/bin/python render_episode.py   # deliverables/episode-04-neither-roommate-would-let-go-final.mp4

Drop Hussain's recording at audio/reveal-hussain.(wav|m4a|mp3) and re-run: it replaces the stand-in narrator, and
the reveal graphic's captions and beats are rescaled to its length.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import soundfile as sf
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import reveal  # noqa: E402
from kit import cast  # noqa: E402
from kit import living_room as room  # noqa: E402
from kit.canvas import (  # noqa: E402
    ALERT, DEMI, HEAVY, INK, MUSTARD, PAPER, SCREEN, W, H, Camera, Canvas, ease, finish, font, lerp, new_frame,
)
from kit.cast import DEV, JO, MIRA, Pose  # noqa: E402

FPS = 30
SR = 48000
DIALOGUE = HERE / "audio" / "dialogue"
BUILD = HERE / "build"
DELIVERABLES = HERE / "deliverables"
FINAL = DELIVERABLES / "episode-04-neither-roommate-would-let-go-final.mp4"

PROMISE_UNTIL = 3.0
LOOKS = {"DEV": DEV, "MIRA": MIRA, "JO": JO}
SEEDS = {"DEV": 1, "MIRA": 3, "JO": 4}


# ==============================================================================================================
# Audio helpers


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


# ==============================================================================================================
# Screen-space overlays


def promise(c: Canvas):
    text = "Programmers have a name for this."
    f = font(44, DEMI)
    w = c.d.textlength(text, font=f) / 2 + 64
    c.rect(540 - w / 2, 230, 540 + w / 2, 318, fill=PAPER, radius=44, width=5)
    c.text(540, 274, text, 44, weight=DEMI)


def card(c: Canvas, text: str, k: float):
    """Time card: a mustard strip that snaps in."""
    y = lerp(-120, 380, ease(k * 3))
    c.rect(-20, y, W + 20, y + 150, fill=MUSTARD, width=8)
    c.text(540, y + 75, text, 76, weight=HEAVY)


def wrap(text: str, size: int, width: float) -> list[str]:
    f = font(size)
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if f.getlength(trial) / 2 > width and line:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line]


def bubble(c: Canvas, speaker: str, text: str, x: float, y: float, w: float, target: tuple[float, float]):
    lines = wrap(text, 52, w - 70)
    h = 64 + 64 * len(lines)
    # Tail toward the speaker, capped so it never covers the face.
    bx, by = x + w * 0.35, y + h
    dx, dy = target[0] - bx, target[1] - by
    dist = math.hypot(dx, dy) or 1
    length = min(dist - 40, 120)
    tip = (bx + dx / dist * length, by + dy / dist * length)
    c.poly([(bx - 26, by - 6), (bx + 26, by - 6), tip], fill=PAPER, width=6)
    c.rect(x, y, x + w, y + h, fill=PAPER, radius=38, width=6)
    c.line([(bx - 22, by - 3), (bx + 22, by - 3)], fill=PAPER, width=9, rounded=False)
    c.text(x + 36, y + 36, speaker, 30, fill=(125, 115, 105), weight=DEMI, anchor="lm")
    for i, line in enumerate(lines):
        c.text(x + 36, y + 88 + 64 * i, line, 52, anchor="lm")


def mouth_point(cam: Camera, pose: Pose) -> tuple[float, float]:
    f = pose.facing
    if pose.standing:
        hx, hy = pose.x + f * 4, pose.y - 560
    else:
        hx, hy = pose.x + f * 6 + pose.head_dx, pose.y - 115 + pose.head_dy
    return cam.to_screen(hx + f * 20, hy + 46)


# ==============================================================================================================
# Timeline


@dataclass
class Line:
    key: str
    offset: float
    bubble: tuple | None = None  # (x, y, w) on screen; None = no bubble (e.g. TV audio)
    gain: float = 1.0
    speaker: str = ""
    text: str = ""
    start: float = 0.0
    audio: np.ndarray | None = None


@dataclass
class Shot:
    name: str
    dur: float
    draw: Callable
    lines: list[Line] = field(default_factory=list)
    start: float = 0.0


class Ctx:
    """What a shot's draw function needs for one frame."""

    def __init__(self, ep: "Episode", shot: Shot, t: float):
        self.ep, self.shot, self.t = ep, shot, t
        self.g = shot.start + t

    def mouth(self, who: str) -> float:
        env_ = self.ep.mouths.get(who)
        if env_ is None:
            return 0.0
        i = min(len(env_) - 1, int(self.g * FPS))
        return float(env_[i])

    def blink(self, who: str) -> bool:
        return cast.blinking(self.g, SEEDS[who])

    def breathe(self, period=3.2, amp=3.0, phase=0.0) -> float:
        return math.sin(2 * math.pi * (self.g / period + phase)) * amp

    def seated(self, who: str, facing: int, expr: str, **kw) -> Pose:
        x, y = room.DEV_SEAT if who == "DEV" else room.MIRA_SEAT
        pose = Pose(x, y, facing, expr, mouth=self.mouth(who), blink=self.blink(who), **kw)
        pose.extras.setdefault("breathe", self.breathe(phase=SEEDS[who] * 0.3))
        return pose

    def bubbles(self, c: Canvas, cam: Camera, poses: dict):
        for line in self.shot.lines:
            if line.bubble and self.t >= line.offset:
                x, y, w = line.bubble
                pose = poses.get(line.speaker)
                target = mouth_point(cam, pose) if pose else (x + w * 0.35 + 200, y + 600)
                bubble(c, line.speaker, line.text, x, y, w, target)


def scene(ctx: Ctx, cam: Camera, time: str, tv: str, pizza: bool, dev: Pose | None, mira: Pose | None,
          jo: Pose | None = None, sleepers: bool = False) -> Image.Image:
    img = new_frame(room.wall_color(time))
    c = Canvas(img, cam)
    room.back(c, time, tv, pizza, ctx.g)
    if dev:
        cast.draw(c, DEV, dev)
    if mira:
        cast.draw(c, MIRA, mira)
    room.front(c, pizza)
    if jo:
        cast.draw(c, JO, jo)
    if sleepers:
        cast.zzz(c, dev.x + 60, dev.y - 230, ctx.g, 0.0, room.wall_color(time))
        cast.zzz(c, mira.x - 20, mira.y - 240, ctx.g, 0.5, room.wall_color(time))
    screen = Canvas(img, SCREEN)
    ctx.bubbles(screen, cam, {"DEV": dev, "MIRA": mira, "JO": jo})
    if ctx.g < PROMISE_UNTIL:
        promise(screen)
    return img


# Seat bottom (world y 1380) sits just above the bottom 20% reserved for the Shorts UI.
TWO_SHOT = Camera(1.42, 598, 1080, 540, 1090)
WIDE = Camera(0.86, 335, 1150, 540, 1250)


def cam_lerp(a: Camera, b: Camera, k: float) -> Camera:
    return Camera(lerp(a.zoom, b.zoom, k), lerp(a.fx, b.fx, k), lerp(a.fy, b.fy, k), lerp(a.sx, b.sx, k), lerp(a.sy, b.sy, k))


# --- shots ----------------------------------------------------------------------------------------------------


def s01_standoff(ctx: Ctx):
    return scene(ctx, TWO_SHOT, "day", "off", False,
                 ctx.seated("DEV", 1, "angry", hands="raise_remote"),
                 ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries"))


def s02_mira(ctx: Ctx):
    cam = Camera(2.2, 826, 1040, 540, 960)
    return scene(ctx, cam, "day", "off", False, None, ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries"))


def s03_insert(ctx: Ctx):
    """Close-up of Dev's hand gripping the empty remote. Drawn in screen space."""
    img = new_frame((150, 142, 132))
    c = Canvas(img, SCREEN)
    for i in range(-10, 30):  # couch fabric weave
        c.line([(i * 70, 0), (i * 70 - 900, 1920)], fill=(140, 132, 122), width=10, rounded=False)
    shake = math.sin(ctx.t * 45) * 4 if ctx.t > 0.1 else 0
    x0 = shake
    skin, sleeve = DEV.skin, DEV.top
    c.poly([(640, 1920), (1100, 1380), (1100, 1920)], fill=sleeve, width=8)
    c.ellipse(560 + x0, 1060, 900 + x0, 1440, fill=skin, width=8)  # palm behind the remote
    # Remote back, cover off.
    c.rect(400 + x0, 330, 680 + x0, 1380, fill=(60, 58, 56), radius=90, width=10)
    c.rect(452 + x0, 470, 628 + x0, 1030, fill=(222, 218, 210), radius=18, width=7)
    c.line([(540 + x0, 480), (540 + x0, 1020)], fill=(150, 145, 138), width=6)
    for sx in (496, 584):  # empty slots: flat contact at top, spring at bottom
        sx += x0
        c.rect(sx - 26, 490, sx + 26, 510, fill=(185, 185, 190), width=4)
        zig = [(sx + (-22 if i % 2 else 22), 1010 - i * 14) for i in range(7)]
        c.line(zig, fill=(150, 150, 158), width=7)
        c.text(sx, 560, "+" if sx - x0 < 540 else "−", 44, fill=(150, 145, 138), weight=HEAVY)
    for i, fy in enumerate((1110, 1180, 1250, 1320)):  # fingers wrap the right edge
        c.rect(610 + x0, fy, 740 + x0 - i * 8, fy + 64, fill=skin, radius=32, width=7)
    c.rect(356 + x0, 1080, 470 + x0, 1160, fill=skin, radius=40, width=7)  # thumb
    ctx.bubbles(c, SCREEN, {})
    return img


def s04_mira_smug(ctx: Ctx):
    cam = Camera(3.0, 830, 1020, 540, 1000)
    return scene(ctx, cam, "day", "off", False, None, ctx.seated("MIRA", -1, "smug", hands="clutch_batteries"))


def night_two_shot(ctx: Ctx, talking=True):
    k = ctx.t / max(ctx.shot.dur, 0.1)
    cam = cam_lerp(TWO_SHOT, Camera(1.6, 595, 1070, 540, 1060), k)
    return scene(ctx, cam, "night", "off", True,
                 ctx.seated("DEV", 1, "tired_angry", hands="raise_remote", raise_amt=0.55),
                 ctx.seated("MIRA", -1, "tired", hands="clutch_batteries"))


def card1(ctx: Ctx):
    img = night_two_shot(ctx)
    card(Canvas(img, SCREEN), "3 HOURS LATER", ctx.t)
    return img


def s05b_mira_tired(ctx: Ctx):
    cam = Camera(2.6, 826, 1030, 540, 980)
    return scene(ctx, cam, "night", "off", True, None, ctx.seated("MIRA", -1, "tired", hands="clutch_batteries"))


def asleep_poses(ctx: Ctx):
    dev = ctx.seated("DEV", 1, "asleep", hands="raise_remote", raise_amt=0.2, head_dx=18, head_dy=12)
    mira = ctx.seated("MIRA", -1, "asleep", hands="clutch_batteries", head_dx=-18, head_dy=12)
    dev.extras["breathe"] = ctx.breathe(2.4, 6, 0.0)
    mira.extras["breathe"] = ctx.breathe(2.4, 6, 0.5)
    dev.blink = mira.blink = False
    return dev, mira


def card2(ctx: Ctx):
    img = s06_asleep(ctx)
    card(Canvas(img, SCREEN), "NEXT MORNING", ctx.t)
    return img


def s06_asleep(ctx: Ctx):
    dev, mira = asleep_poses(ctx)
    return scene(ctx, TWO_SHOT, "morning", "off", True, dev, mira, sleepers=True)


JO_X, JO_FEET = 20, 1480
BUTTON_AT = 1.0


def s07_button(ctx: Ctx):
    t = ctx.t
    dev, mira = asleep_poses(ctx)
    walk = ease(t / 0.5)
    x = lerp(-260, JO_X, walk)
    bob = -abs(math.sin(t * math.pi * 5)) * 10 if t < 0.5 else 0
    if t < 0.6:
        jo = Pose(x, JO_FEET, 1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="mug", extras={"bob": bob})
    else:
        k = ease((t - 0.6) / 0.35)
        start = (JO_X - 80, 1150)
        reach = (lerp(start[0], room.POWER_BUTTON[0], k), lerp(start[1], room.POWER_BUTTON[1], k))
        jo = Pose(JO_X, JO_FEET, -1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="reach", reach=reach)
    tv = "golf" if t >= BUTTON_AT else "off"
    return scene(ctx, WIDE, "morning", tv, True, dev, mira, jo, sleepers=True)


def s08a_shock(ctx: Ctx):
    j = cast.jolt(ctx.t)
    dev = ctx.seated("DEV", -1, "shock", hands="raise_remote", head_dy=j)
    mira = ctx.seated("MIRA", -1, "shock", hands="clutch_batteries", head_dy=j * 0.8)
    jo = Pose(JO_X, JO_FEET, 1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="mug")
    return scene(ctx, Camera(1.0, 400, 1150, 540, 1200), "morning", "golf", True, dev, mira, jo)


def s08b_jo(ctx: Ctx):
    jo = Pose(JO_X, JO_FEET, 1, "deadpan", mouth=ctx.mouth("JO"), blink=ctx.blink("JO"), standing=True, hands="mug")
    return scene(ctx, Camera(2.3, 30, 930, 540, 960), "morning", "golf", True, None, None, jo)


def s08c_stare(ctx: Ctx):
    both_blink = 0.55 <= ctx.t < 0.72  # a synchronized slow blink sells the silence
    dev = ctx.seated("DEV", -1, "neutral", hands="raise_remote", gaze=-1)
    mira = ctx.seated("MIRA", -1, "neutral", hands="clutch_batteries", gaze=-1)
    dev.blink = mira.blink = both_blink
    return scene(ctx, Camera(1.6, 580, 1060, 540, 1060), "morning", "golf", True, dev, mira)


REVEAL_NODES = None


def r1_reveal(ctx: Ctx):
    global REVEAL_NODES
    if REVEAL_NODES is None:
        REVEAL_NODES = (reveal.node_layer("story"), reveal.node_layer("software"))
    return reveal.render_frame(ctx.t, *REVEAL_NODES, captions=ctx.ep.reveal_captions)


def s10_golf(ctx: Ctx):
    k = ease(ctx.t / ctx.shot.dur)
    cam = cam_lerp(WIDE, Camera(1.3, 590, 1080, 540, 1100), k)
    looking_at_tv = ctx.t < 0.55
    if looking_at_tv:
        dev = ctx.seated("DEV", 1, "neutral", hands="raise_remote", gaze=-1)
        mira = ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries", gaze=-1)
    else:
        dev = ctx.seated("DEV", 1, "determined", hands="raise_remote")
        mira = ctx.seated("MIRA", -1, "determined", hands="clutch_batteries")
    return scene(ctx, cam, "day", "golf", True, dev, mira)


# ==============================================================================================================
# Episode assembly


class Episode:
    def __init__(self):
        self.meta = json.loads((HERE / "audio" / "dialogue.json").read_text())["lines"]
        self.hussain = next((p for ext in ("wav", "m4a", "mp3", "aiff") if (p := HERE / "audio" / f"reveal-hussain.{ext}").exists()), None)
        self.build_reveal_audio()
        self.shots = self.build_shots()
        t = 0.0
        for shot in self.shots:
            shot.start = t
            for line in shot.lines:
                line.start = t + line.offset
            t += shot.dur
        self.duration = t
        self.mouths = self.build_mouths()

    def line(self, key, offset, bubble=None, gain=1.0) -> Line:
        m = self.meta[key]
        return Line(key, offset, bubble, gain, m["speaker"], m["text"], audio=level(load_wav(DIALOGUE / f"{key}.wav")))

    def dur(self, key) -> float:
        return self.meta[key]["duration"]

    def build_reveal_audio(self):
        chunks = ["reveal-1", "reveal-2", "reveal-3", "reveal-4"]
        gap, lead = 0.2, 0.1
        starts, t = [], lead
        for key in chunks:
            starts.append(t)
            t += self.dur(key) + gap
        stand_in_len = t - gap - lead
        texts = [self.meta[k]["text"] for k in chunks]
        timings = HERE / "audio" / "reveal-hussain.json"
        if self.hussain and timings.exists():
            # Prepared by prep_reveal.py: already denoised and trimmed, with measured phrase starts.
            audio = level(load_wav(self.hussain))
            captions = json.loads(timings.read_text())["captions"]
            self.reveal_lines = [Line("reveal-hussain", lead, speaker="HUSSAIN", text=" ".join(texts), audio=audio)]
            self.reveal_captions = [(lead + t, txt) for t, txt in captions]
            self.reveal_dur = lead + len(audio) / SR + 0.5
        elif self.hussain:
            # Unprepared recording: trim silence and spread the captions proportionally.
            wav = BUILD / "reveal-hussain-48k.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(self.hussain), "-ac", "1", "-ar", str(SR),
                            "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                                   "silenceremove=start_periods=1:start_threshold=-45dB,areverse", str(wav)], check=True)
            audio = level(load_wav(wav))
            scale = (len(audio) / SR) / stand_in_len
            self.reveal_lines = [Line("reveal-hussain", lead, speaker="HUSSAIN", text=" ".join(texts), audio=audio)]
            self.reveal_captions = [(lead + (s - lead) * scale, txt) for s, txt in zip(starts, texts)]
            self.reveal_dur = lead + len(audio) / SR + 0.5
        else:
            self.reveal_lines = [self.line(k, s) for k, s in zip(chunks, starts)]
            self.reveal_captions = list(zip(starts, texts))
            self.reveal_dur = t - gap + 0.5

    def build_shots(self) -> list[Shot]:
        d = self.dur
        return [
            Shot("S01 standoff", max(1.8, 0.12 + d("dev-batteries-now") + 0.4), s01_standoff,
                 [self.line("dev-batteries-now", 0.12, (50, 470, 520))]),
            Shot("S02 Mira", max(1.5, 0.08 + d("mira-remote-first") + 0.35), s02_mira,
                 [self.line("mira-remote-first", 0.08, (120, 380, 560))]),
            Shot("S03 empty remote", 0.1 + d("dev-doesnt-work") + 0.4, s03_insert,
                 [self.line("dev-doesnt-work", 0.1, (80, 150, 920))]),
            Shot("S04 Mira smug", 0.1 + d("mira-why-holding") + 0.55, s04_mira_smug,
                 [self.line("mira-why-holding", 0.1, (170, 330, 740))]),
            Shot("Card 3 hours later", 0.75, card1),
            Shot("S05a night", 0.2 + d("dev-let-go") + 0.35, night_two_shot,
                 [self.line("dev-let-go", 0.2, (50, 430, 560))]),
            Shot("S05b Mira tired", 0.1 + d("mira-you-first") + 0.5, s05b_mira_tired,
                 [self.line("mira-you-first", 0.1, (230, 380, 520))]),
            Shot("Card next morning", 0.65, card2),
            Shot("S06 asleep", 2.0, s06_asleep),
            Shot("S07 button", 2.2, s07_button, [self.line("tv-golf-1", BUTTON_AT + 0.25, gain=0.2)]),
            Shot("S08a shock", 0.8, s08a_shock),
            Shot("S08b Jo", 0.1 + d("jo-button") + 0.45, s08b_jo, [self.line("jo-button", 0.1, (170, 330, 620))]),
            Shot("S08c stare", 1.1, s08c_stare),
            Shot("R1 reveal", self.reveal_dur, r1_reveal, self.reveal_lines),
            Shot("S10 golf (loops to S01)", 1.6, s10_golf, [self.line("tv-golf-2", 0.05, gain=0.2)]),
        ]

    def dialogue_lines(self):
        for shot in self.shots:
            for line in shot.lines:
                yield shot, line

    def build_mouths(self) -> dict:
        n = int(self.duration * FPS) + 2
        mouths = {}
        for _, line in self.dialogue_lines():
            if line.speaker not in LOOKS:
                continue
            arr = mouths.setdefault(line.speaker, np.zeros(n))
            a = line.audio
            win = SR // FPS
            rms = np.array([np.sqrt(np.mean(a[i:i + win] ** 2)) for i in range(0, len(a), win)])
            rms = rms / (rms.max() + 1e-9)
            vals = np.clip((rms - 0.12) / 0.55, 0, 1)
            i0 = int(line.start * FPS)
            for k, v in enumerate(vals):
                if i0 + k < n:
                    arr[i0 + k] = max(arr[i0 + k], v)
        for arr in mouths.values():  # light smoothing so the jaw doesn't flicker
            arr[1:] = np.maximum(arr[1:], arr[:-1] * 0.5)
        return mouths

    # --- audio -----------------------------------------------------------------------------------------------
    def mix(self) -> np.ndarray:
        mix = Mix(self.duration)
        for shot, line in self.dialogue_lines():
            wave = line.audio
            if line.speaker == "TV":
                wave = band(wave, 350, 3200)  # small TV speaker
            mix.add(wave, line.start, 0.9 * line.gain, dialogue=line.speaker != "TV")

        at = {s.name.split()[0]: s for s in self.shots}
        s01, s02, s03, s04 = at["S01"], at["S02"], at["S03"], at["S04"]
        E2, F2, Fs2, G2, B1 = 82.41, 87.31, 92.5, 98.0, 61.74
        # Standoff: low plucks on the cuts, like a duel.
        for when, f in ((0.0, E2), (0.45, B1), (0.9, E2), (s02.start, F2), (s03.start, E2), (s03.start + 0.5, G2),
                        (s04.start, Fs2), (s04.start + 0.6, F2)):
            mix.add(pluck(f, seed=int(f)), when, 0.2)
        mix.add(click(), s03.start + 0.08, 0.3)

        c1 = next(s for s in self.shots if s.name == "Card 3 hours later")
        for i in range(3):
            mix.add(tick(), c1.start + 0.05 + i * 0.22, 0.35)
        night = [s for s in self.shots if s.name.startswith("S05")]
        mix.add(hum(sum(s.dur for s in night) + c1.dur), c1.start, 0.05)

        c2 = next(s for s in self.shots if s.name == "Card next morning")
        s06, s07 = at["S06"], at["S07"]
        for i, off in enumerate((0.05, 0.4, 0.9, 1.5, 2.1, 2.4)):
            mix.add(chirp(40 + i), c2.start + off, 0.06)
        mix.add(snore(True), s06.start + 0.1, 0.22)
        mix.add(snore(False), s06.start + 1.0, 0.09)
        mix.add(snore(True), s07.start + 0.2, 0.18)

        for i, off in enumerate((0.1, 0.28, 0.46)):
            mix.add(thump(i), s07.start + off, 0.35)
        mix.add(click(), s07.start + BUTTON_AT, 0.45)
        mix.add(tv_on(), s07.start + BUTTON_AT + 0.02, 0.35)
        r1 = at["R1"]
        mix.add(murmur(r1.start - (s07.start + BUTTON_AT)), s07.start + BUTTON_AT, 0.03)

        s08a, s08c = at["S08a"], at["S08c"]
        mix.add(pluck(164.81, 0.6, seed=3) + pluck(233.08, 0.6, seed=4), s08a.start, 0.2)  # surprise stab
        mix.add(slide_whistle(), s08c.start + 0.25, 0.14)

        mix.add(pad(r1.dur), r1.start, 0.07)
        mix.add(pluck(329.63, 0.8, 0.99, seed=9), r1.start + reveal.beats_for(self.reveal_captions)["pulse"], 0.18)

        s10 = at["S10"]
        mix.add(murmur(s10.dur, 22), s10.start, 0.03)
        mix.add(pluck(B1, seed=2), self.duration - 0.45, 0.2)  # lands on the loop back into S01's first pluck
        return mix.render()


# ==============================================================================================================
# Output


def srt_time(t: float) -> str:
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_subtitles(ep: Episode, path: Path):
    entries = []
    for shot, line in ep.dialogue_lines():
        if line.speaker in LOOKS:
            entries.append((line.start, line.start + len(line.audio) / SR + 0.2, f"{line.speaker}: {line.text}"))
    r1 = next(s for s in ep.shots if s.name.startswith("R1"))
    caps = ep.reveal_captions
    for i, (start, text) in enumerate(caps):
        end = caps[i + 1][0] if i + 1 < len(caps) else r1.dur - 0.3
        entries.append((r1.start + start, r1.start + end, text))
    entries.sort()
    path.write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(entries)))


def thumbnail(path: Path, ep: Episode):
    cam = Camera(1.55, 580, 1060, 540, 1180)
    img = new_frame()
    c = Canvas(img, cam)
    room.back(c, "day", "off", False, 0)
    cast.draw(c, DEV, Pose(*room.DEV_SEAT, 1, "angry", hands="raise_remote"))
    cast.draw(c, MIRA, Pose(*room.MIRA_SEAT, -1, "smug", hands="clutch_batteries"))
    room.front(c)
    s = Canvas(img, SCREEN)
    s.text(540, 250, "SOFTWARE IN DISGUISE · 04", 34, weight=DEMI)
    s.rect(60, 340, 1020, 620, fill=MUSTARD, width=9, radius=20)
    s.text(540, 425, "NOBODY", 118, weight=HEAVY)
    s.text(540, 540, "LETS GO.", 118, fill=ALERT, weight=HEAVY)
    finish(img).save(path)


def main():
    BUILD.mkdir(exist_ok=True)
    DELIVERABLES.mkdir(exist_ok=True)
    ep = Episode()
    print(f"duration {ep.duration:.2f}s  ({'Hussain recording' if ep.hussain else 'stand-in narrator'})")
    for s in ep.shots:
        print(f"  {s.start:6.2f}  {s.dur:4.2f}  {s.name}")

    audio = ep.mix()
    sf.write(BUILD / "mix.wav", np.stack([audio, audio], axis=1), SR)

    silent = BUILD / "video-silent.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                           "-preset", "medium", str(silent)], stdin=subprocess.PIPE)
    samples = []
    n_frames = round(ep.duration * FPS)
    si = 0
    for n in range(n_frames):
        g = n / FPS
        while si + 1 < len(ep.shots) and g >= ep.shots[si + 1].start:
            si += 1
        shot = ep.shots[si]
        frame = shot.draw(Ctx(ep, shot, g - shot.start))
        if frame.size != (W, H):
            frame = finish(frame)
        ff.stdin.write(frame.tobytes())
        if not samples or samples[-1][0] != shot.name:
            samples.append([shot.name, None, shot.start + shot.dur * 0.7])
        if samples[-1][1] is None and g >= samples[-1][2]:
            samples[-1][1] = frame
    ff.stdin.close()
    ff.wait()

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(BUILD / "mix.wav"),
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(FINAL)], check=True)

    cols, tw, th = 5, W // 5, H // 5
    frames = [f for _, f, _ in samples if f is not None]
    sheet = Image.new("RGB", (cols * tw, math.ceil(len(frames) / cols) * th), INK)
    for i, f in enumerate(frames):
        sheet.paste(f.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(BUILD / "contact-sheet.png")
    write_subtitles(ep, DELIVERABLES / "subtitles.srt")
    thumbnail(DELIVERABLES / "thumbnail.png", ep)
    print(FINAL)


if __name__ == "__main__":
    main()
