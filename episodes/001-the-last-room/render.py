"""Episode 1, "The Last Room" (race condition): render the Short.

Two aunts both booked the last room at the wedding hotel and both got a confirmation. Priya tilts a phone into
X-ray view and everyone watches what the app did: two requests read "Room 204: FREE" at the same moment, and both
booked it. Then the fix (a lock), and a final grab for the one key.

Big-head characters (kit/bighead.py), crisp app screens (kit/phone.py), Dia voices picked in audio/voices.json.
Animated on twos (15 drawings a second, shown at 30 fps); a new boil seed per drawing makes the lines shimmer.

Run: ../../.venv/bin/python render.py [--preview]   →  deliverables/the-last-room.mp4 (+ thumbnail.png)
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit import sound  # noqa: E402
from kit.bighead import (CLERK, GOLD, INK, LATA, MEENA, PAPER, PRIYA, RED, S, WHITE, YELLOW, Pen,  # noqa: E402
                         character, limb, speech)
from kit.phone import BG, BLUE, GREEN, GREY, LINE, ORANGE, ScreenDraw, phone  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE / "deliverables"
BUILD = HERE / "build"
W, H = 1080, 1920
FPS, DRAW_FPS = 30, 15

WALL = (247, 236, 214)
STRIPE = (242, 228, 202)
DESK = (183, 116, 74)
FLASHBACK = (220, 232, 240)
NAVY = (12, 22, 44)
CYAN = (90, 220, 255)
RED_UI = (255, 69, 58)

CAST = {"MEENA": MEENA, "LATA": LATA, "CLERK": CLERK, "PRIYA": PRIYA}

# ----------------------------------------------------------------------------------------------------------------
# Dialogue: one Dia take per exchange (the first of each reel unless overridden), split into its two speakers.

TAKE_OVERRIDE: dict[str, int] = {}  # e.g. {"r01-mine": 3} once Hussain picks by ear


@dataclass
class Line:
    scene: str
    who: str
    text: str
    audio: np.ndarray        # 48 kHz
    start: float = 0.0
    env: np.ndarray = field(default_factory=lambda: np.zeros(0))  # mouth openness per output frame

    @property
    def dur(self):
        return len(self.audio) / sound.SR

    @property
    def end(self):
        return self.start + self.dur


def load_exchange(scene: str) -> tuple[Line, Line]:
    report = json.loads((HERE / "audio" / "voices.json").read_text())[scene]
    seed = TAKE_OVERRIDE.get(scene, report["reel"][0])
    take = next(t for t in report["takes"] if t["seed"] == seed)
    a = sound.load_wav(HERE / "audio" / "scenes" / scene / f"seed-{seed:02d}.wav")
    cut = int(take["cut"] * sound.SR)
    s1, s2 = report["text"].split("[S2]")
    parts = []
    for who, text, audio in ((report["who"][0], s1.replace("[S1]", ""), a[:cut]), (report["who"][1], s2, a[cut:])):
        audio = _trim(audio)
        parts.append(Line(scene, who, text.strip(), sound.level(audio, -18)))
    return parts[0], parts[1]


def _trim(a: np.ndarray) -> np.ndarray:
    hop = int(sound.SR * 0.01)
    e = np.array([np.abs(a[i:i + hop]).max() for i in range(0, len(a), hop)])
    on = np.flatnonzero(e > max(0.02, e.max() * 0.08))
    if not len(on):
        return a
    i0, i1 = max(0, on[0] * hop - hop * 3), min(len(a), (on[-1] + 4) * hop)
    out = a[i0:i1].copy()
    f = min(len(out), int(0.01 * sound.SR))
    out[:f] *= np.linspace(0, 1, f)
    out[-f:] *= np.linspace(1, 0, f)
    return out


def mouth_env(a: np.ndarray) -> np.ndarray:
    hop = sound.SR // FPS
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
    e = e / (np.percentile(e, 95) + 1e-9)
    return np.clip((e - 0.12) * 1.3, 0, 1)


# ----------------------------------------------------------------------------------------------------------------
# The timeline


@dataclass
class Shot:
    name: str
    start: float
    dur: float
    draw: object

    @property
    def end(self):
        return self.start + self.dur


class Episode:
    def __init__(self):
        self.lines: dict[str, Line] = {}
        self.shots: list[Shot] = []
        self.sfx: list[tuple[str, float, float]] = []  # (name, time, gain)
        t = 0.0

        def place(scene, keys, start, gap=0.12, overlap=False):
            a, b = load_exchange(scene)
            for ln, key in ((a, keys[0]), (b, keys[1])):  # a per-line clone replaces Dia's version if there is one
                cloned = HERE / "audio" / "lines" / f"{key}.wav"
                if cloned.exists():
                    ln.audio = sound.level(_trim(sound.load_wav(cloned)), -18)
            a.start = start
            b.start = start + 0.04 if overlap else a.end + gap
            self.lines[keys[0]], self.lines[keys[1]] = a, b
            return max(a.end, b.end)

        # S1: the standoff (frame 1 = both confirmations on screen)
        end = place("r01-mine", ("meena_mine", "lata_first"), t + 0.05)
        self.sfx += [("ding", 0.0, 0.25), ("ding", 0.06, 0.2)]
        self.shots.append(Shot("standoff", t, end + 0.25 - t, self.s_standoff))
        t = end + 0.25
        # S2: the clerk and the one key
        end = place("r02-one-room", ("lata_tell", "clerk_one"), t + 0.1, gap=0.25)
        self.sfx.append(("jingle", self.lines["clerk_one"].start + 0.3, 0.5))
        self.shots.append(Shot("one_room", t, end + 0.4 - t, self.s_one_room))
        t = end + 0.4
        # S3: flashback, both tap "Book now" at 9:41:07
        tap = t + 1.1
        self.sfx += [("whoosh", t, 0.35), ("tap", tap, 0.8), ("tap", tap + 0.004, 0.8), ("ding", tap + 0.35, 0.4)]
        end = place("r03-got-it", ("meena_got", "lata_got"), tap + 0.55, overlap=True)
        self.tap = tap
        self.shots.append(Shot("flashback", t, end + 0.45 - t, self.s_flashback))
        t = end + 0.45
        # S4: Priya arrives
        self.sfx.append(("whoosh", t, 0.3))
        end = place("r04-show-me", ("priya_wait", "meena_look"), t + 0.45)
        self.shots.append(Shot("priya", t, end + 0.2 - t, self.s_priya))
        t = end + 0.2
        # S5: X-ray
        self.xray_t0 = t
        self.sfx += [("whoosh", t + 0.3, 0.6), ("pad", t + 0.3, 0.12)]
        end = place("r05-same-moment", ("priya_same", "lata_twice"), t + 1.2)
        end = place("r06-race", ("priya_race", "meena_hmph"), end + 0.3)
        self.sfx.append(("thump", self.lines["priya_race"].start + 0.9, 0.7))
        self.shots.append(Shot("xray", t, end + 0.3 - t, self.s_xray))
        t = end + 0.3
        # S6: the key
        end = place("r07-key", ("clerk_key", "meena_minegrab"), t + 0.3)
        self.grab = self.lines["meena_minegrab"].start + 0.05
        self.sfx += [("scrape", t + 0.2, 0.25), ("thump", self.grab + 0.18, 0.8)]
        self.shots.append(Shot("key", t, end + 1.1 - t, self.s_key))
        self.duration = end + 1.1
        for ln in self.lines.values():
            ln.env = mouth_env(ln.audio)

    # -- helpers -------------------------------------------------------------------------------------------------

    def mouth(self, who: str, t: float) -> float:
        for ln in self.lines.values():
            if ln.who == who and ln.start <= t < ln.end:
                i = int((t - ln.start) * FPS)
                return float(ln.env[min(i, len(ln.env) - 1)])
        return 0.0

    def speaking(self, key: str, t: float, pad=0.25) -> bool:
        ln = self.lines[key]
        return ln.start - 0.05 <= t < ln.end + pad

    def pop(self, key: str, t: float) -> float:
        """0..1 as a line's bubble pops in."""
        return max(0.0, min(1.0, (t - self.lines[key].start + 0.05) / 0.12))

    def blink(self, who: str, t: float) -> bool:
        period = {"MEENA": 3.1, "LATA": 3.7, "CLERK": 2.6, "PRIYA": 3.4}[who]
        return (t + period * 0.37) % period < 0.12

    # -- shots ---------------------------------------------------------------------------------------------------

    def reception(self, p: Pen, desk_y=1040, sign=True):
        p.d.rectangle([0, 0, W * S, desk_y * S], fill=WALL)
        for x in range(0, W, 90):
            p.d.rectangle([x * S, 0, (x + 30) * S, desk_y * S], fill=STRIPE)
        if sign:
            p.rrect(330, 70, 750, 160, 16, RED)
            p.text((540, 116), "RECEPTION", 50, ("/System/Library/Fonts/Avenir Next.ttc", 8), WHITE)

    def desk(self, p: Pen, y=1040, h=160):
        p.d.rectangle([0, y * S, W * S, (y + h) * S], fill=DESK)
        p.line([(0, y), (W, y)], INK, 8)

    def key(self, p: Pen, x, y, scale=1.0):
        s = scale
        p.ell(x, y, 22 * s, 22 * s, GOLD, 6)
        p.ell(x, y, 8 * s, 8 * s, DESK, 4)
        p.line([(x + 22 * s, y), (x + 92 * s, y)], INK, 9 * s)
        p.line([(x + 72 * s, y), (x + 72 * s, y + 18 * s)], INK, 7 * s)
        p.line([(x + 86 * s, y), (x + 86 * s, y + 14 * s)], INK, 7 * s)
        p.rrect(x - 22 * s, y + 26 * s, x + 34 * s, y + 64 * s, 6 * s, (250, 245, 232), 5)
        p.text((x + 6 * s, y + 45 * s), "204", 21 * s, ("/System/Library/Fonts/Avenir Next.ttc", 8))

    def s_standoff(self, p: Pen, t: float, k: float):
        self.reception(p)
        lata_talks = self.speaking("lata_first", t)
        character(p, MEENA, 285, 640, 200, "furious" if not lata_talks else "angry", self.mouth("MEENA", t),
                  gaze=(0.9, 0.1), blink=self.blink("MEENA", t), arm="point" if not lata_talks else "rest",
                  bottom=1045, turn=0.3)
        character(p, LATA, 800, 665, 192, "angry" if lata_talks else "smug", self.mouth("LATA", t),
                  gaze=(-0.9, 0.1), blink=self.blink("LATA", t), arm="crossed", bottom=1045, turn=-0.3)
        self.desk(p)
        self.key(p, 505, 1080)
        if t >= self.lines["meena_mine"].start - 0.05:
            speech(p, (40, 215, 500, 335), (230, 395), "That's MY room!", 58)
        if t >= self.lines["lata_first"].start - 0.05:
            speech(p, (560, 215, 1050, 335), (820, 420), "I booked it first!", 54)

    def s_one_room(self, p: Pen, t: float, k: float):
        self.reception(p)
        talking = self.speaking("clerk_one", t)
        raised = max(0.0, min(1.0, (t - self.lines["clerk_one"].start - 0.15) / 0.25))
        character(p, CLERK, 540, 760, 285, "deadpan", self.mouth("CLERK", t), gaze=(0, 0.25 if talking else 0),
                  blink=self.blink("CLERK", t), arm="hold_up" if raised > 0 else "rest", bottom=1500)
        if raised > 0:
            hx, hy = 540 + 285 * 0.82 * 1.4, 760 - 285 * 0.2
            swing = math.sin(t * 5) * 6
            p.line([(hx, hy + 20), (hx + swing * 0.3, hy + 70)], INK, 5)
            self.key(p, hx - 40 + swing, hy + 100, 1.25)
        self.desk(p, 1500, 420)
        if t >= self.lines["lata_tell"].start - 0.05:
            speech(p, (30, 230, 380, 350), (-20, 420), "Tell her!", 58)
        if t >= self.lines["clerk_one"].start - 0.05:
            speech(p, (330, 1230, 1050, 1370), (560, 1135), "We have ONE room.", 60)

    def s_flashback(self, p: Pen, t: float, k: float, img: Image.Image | None = None):
        p.d.rectangle([0, 0, W * S, H * S], fill=FLASHBACK)
        p.text((540, 115), "3 weeks ago · 9:41 PM", 46, ("/System/Library/Fonts/Avenir Next.ttc", 8), (60, 80, 110))
        for i, (c, x) in enumerate(((MEENA, 280), (LATA, 800))):
            who = "MEENA" if i == 0 else "LATA"
            happy = t > self.tap + 0.35
            character(p, c, x, 360, 135, "triumphant" if happy else "worried", self.mouth(who, t),
                      gaze=(0, 0.8) if not happy else (0, 0), blink=self.blink(who, t), arm="rest", bottom=560)
        p.line([(540, 200), (540, 1500)], (160, 180, 205), 6)
        if t >= self.lines["meena_got"].start - 0.05:
            speech(p, (20, 1500, 400, 1610), (200, 1440), "Got it!", 58)
            speech(p, (680, 1500, 1060, 1610), (880, 1440), "Got it!", 58)

    def flashback_phones(self, img: Image.Image, t: float):
        tapped = t >= self.tap
        confirmed = t >= self.tap + 0.35
        for x, ang, bid in ((280, 2, "MH-48213"), (800, -2, "MH-48214")):
            phone(img, x, 1030, 400, booking_screen(tapped, confirmed, bid), angle=ang)
        if abs(t - self.tap) < 0.6:  # the same second on both clocks
            d = ImageDraw.Draw(img)
            from kit.phone import sf as sffont
            d.rounded_rectangle([370, 600, 710, 690], 20, fill=(29, 27, 31))
            d.text((540, 645), "9:41:07", font=sffont(19, "Bold"), fill=WHITE, anchor="mm")

    def s_priya(self, p: Pen, t: float, k: float):
        self.reception(p)
        enter = min(1.0, (t - self.shots[3].start) / 0.45)
        ease = 1 - (1 - enter) ** 3
        px = 1300 - (1300 - 540) * ease
        character(p, PRIYA, px, 600, 175, "explaining" if self.speaking("priya_wait", t) else "neutral",
                  self.mouth("PRIYA", t), gaze=(-0.3, 0.2), blink=self.blink("PRIYA", t), arm="rest", bottom=1045)
        meena_shows = t >= self.lines["meena_look"].start - 0.1
        character(p, MEENA, 215, 760, 175, "angry" if not meena_shows else "triumphant", self.mouth("MEENA", t),
                  gaze=(0.8, 0), blink=self.blink("MEENA", t), arm="phone" if meena_shows else "rest", bottom=1045)
        character(p, LATA, 870, 780, 170, "angry", self.mouth("LATA", t), gaze=(-0.8, 0), blink=self.blink("LATA", t),
                  arm="crossed", bottom=1045)
        self.desk(p, 1040, 880)
        if t >= self.lines["priya_wait"].start - 0.05:
            speech(p, (300, 150, 1000, 280), (560, 400), "Wait. Show me your phones.", 50)
        if t >= self.lines["meena_look"].start - 0.05:
            speech(p, (30, 1180, 640, 1300), (200, 1090), "Look! It says confirmed!", 48)

    def s_xray(self, p: Pen, t: float, k: float):
        p.d.rectangle([0, 0, W * S, H * S], fill=(20, 30, 58))
        for y in range(0, H, 60):
            p.d.line([(0, y * S), (W * S, y * S)], fill=(28, 42, 76), width=2)
        # reaction heads at the top
        priya_talk = t < self.lines["lata_twice"].start or self.speaking("priya_race", t, 0.1)
        character(p, PRIYA, 170, 165, 92, "explaining", self.mouth("PRIYA", t), gaze=(0.5, 0.6),
                  blink=self.blink("PRIYA", t), bottom=290)
        lata_expr = "shocked" if t >= self.lines["lata_twice"].start - 0.1 else "worried"
        character(p, LATA, 910, 165, 90, lata_expr, self.mouth("LATA", t), gaze=(-0.5, 0.6),
                  blink=self.blink("LATA", t), bottom=290)
        character(p, MEENA, 540, 170, 85, "furious" if t >= self.lines["meena_hmph"].start - 0.1 else "worried",
                  self.mouth("MEENA", t), gaze=(0, 0.8), blink=self.blink("MEENA", t), bottom=290)
        del priya_talk

    def xray_phone(self, img: Image.Image, t: float):
        x0 = self.xray_t0
        phone(img, 540, 1000, 660, xray_screen(t - x0, self), angle=0)
        # captions for Priya's long lines
        live = [k for k in ("priya_same", "lata_twice", "priya_race", "meena_hmph")
                if self.lines[k].start - 0.05 <= t < self.lines[k].end + 0.3]
        if live:  # only the most recent line, so captions never stack
            key = max(live, key=lambda k: self.lines[k].start)
            ln = self.lines[key]
            caption(img, CAPTIONS[key](t - ln.start, ln.dur), 1585)

    def s_key(self, p: Pen, t: float, k: float):
        self.reception(p, sign=False)
        character(p, CLERK, 540, 560, 150, "deadpan", self.mouth("CLERK", t), gaze=(0, 0.6), blink=self.blink("CLERK", t),
                  bottom=830)
        self.desk(p, 820, 1100)
        slide = min(1.0, max(0.0, (t - self.shots[-1].start - 0.2) / 0.6))
        ky = 900 + 260 * (1 - (1 - slide) ** 2)
        reach = max(0.0, min(1.0, (t - self.grab + 0.25) / 0.25))
        for c, cx, d, who in ((MEENA, 150, 1, "MEENA"), (LATA, 930, -1, "LATA")):
            cy = 1000 if c is MEENA else 1020
            r = 210
            expr = "furious" if reach > 0 else "angry"
            character(p, c, cx, cy, r, expr, self.mouth(who, t), gaze=(d * 0.7, 0.8), blink=self.blink(who, t),
                      bottom=1700)
            sh = (cx + d * r * 0.75, cy + r * 1.1)
            target = (540 - d * 38, ky + 6)
            hand = (sh[0] + (target[0] - sh[0]) * (0.25 + 0.75 * reach), sh[1] + (target[1] - sh[1]) * (0.25 + 0.75 * reach))
            if reach > 0:
                limb(p, c, r, [sh, ((sh[0] + hand[0]) / 2, min(sh[1], hand[1]) - 40), hand])
        self.key(p, 512, ky, 1.5)
        if reach >= 1:  # both hands land on the key at once
            for c, d in ((MEENA, 1), (LATA, -1)):
                p.ell(540 - d * 38, ky + 6, 26, 24, c.skin, 6)
        if t >= self.lines["clerk_key"].start - 0.05:
            speech(p, (330, 120, 1050, 240), (560, 400), "So... who gets the key?", 50)
        if t >= self.lines["meena_minegrab"].start - 0.05:
            speech(p, (40, 1340, 420, 1450), (190, 1270), "MINE!", 64)
            speech(p, (660, 1340, 1040, 1450), (890, 1270), "MINE!", 64)

    # -- rendering -----------------------------------------------------------------------------------------------

    def frame(self, t: float, boil: int) -> Image.Image:
        shot = next((s for s in self.shots if s.start <= t < s.end), self.shots[-1])
        img = Image.new("RGB", (W * S, H * S), PAPER)
        p = Pen(img, boil=boil)
        k = (t - shot.start) / shot.dur
        shot.draw(p, t, k)
        img = img.resize((W, H), Image.LANCZOS)
        if shot.name == "standoff":
            phone(img, 290, 1500, 370, confirmation("MH-48213"), angle=4)
            phone(img, 790, 1500, 370, confirmation("MH-48214"), angle=-4)
        if shot.name == "flashback":
            self.flashback_phones(img, t)
        if shot.name == "xray":
            self.xray_phone(img, t)
        if shot.name == "key" and t >= self.grab + 0.18:
            stamp(img, "RACE CONDITION", 620, min(1.0, (t - self.grab - 0.18) / 0.15))
        return img

    def mix(self) -> np.ndarray:
        m = sound.Mix(self.duration + 0.5)
        m.add(sound.murmur(self.duration + 0.5) * 0.04, 0)
        for ln in self.lines.values():
            m.add(ln.audio, ln.start, 1.0, dialogue=True)
        fx = {"ding": sound.ding, "tap": sound.click, "thump": sound.thump, "whoosh": sound.whoosh,
              "scrape": lambda: sound.scrape(0.5), "jingle": jingle, "pad": lambda: sound.pad(9.0)}
        for name, at, gain in self.sfx:
            m.add(fx[name](), at, gain)
        return m.render()

    def render(self, preview=False):
        frames = BUILD / "frames"
        if frames.exists():
            shutil.rmtree(frames)
        frames.mkdir(parents=True)
        n = int(self.duration * DRAW_FPS)
        step = 3 if preview else 1
        for i in range(0, n, step):
            t = i / DRAW_FPS
            self.frame(t, boil=i).save(frames / f"f{i // step:05d}.png")
            if i % 30 == 0:
                print(f"frame {i}/{n}", flush=True)
        audio = self.mix()
        sf.write(BUILD / "mix.wav", audio, sound.SR)
        OUT.mkdir(exist_ok=True)
        out = OUT / ("the-last-room-preview.mp4" if preview else "the-last-room.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(DRAW_FPS / step), "-i",
                        str(frames / "f%05d.png"), "-i", str(BUILD / "mix.wav"), "-r", str(FPS), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)],
                       check=True)
        self.frame(0.6, 0).save(OUT / "thumbnail-frame1.png")
        print("wrote", out, f"{self.duration:.1f}s")


# ----------------------------------------------------------------------------------------------------------------
# Screens and overlays


def confirmation(booking_id: str):
    def draw(d: ScreenDraw):
        d.rect(0, 0, 390, 844, BG)
        d.status_bar("9:41")
        d.text(20, 62, "‹ Bookings", 17, "Regular", BLUE)
        d.circle(195, 160, 44, GREEN)
        d.line([(175, 160), (189, 175), (216, 146)], WHITE, 7)
        d.text(195, 222, "Booking confirmed", 27, "Bold", (17, 17, 20), "ma")
        d.text(195, 260, "Marigold Hall & Rooms", 17, "Regular", GREY, "ma")
        d.rect(20, 302, 370, 572, WHITE, r=14)
        d.rect(36, 318, 186, 346, (255, 239, 214), r=8)
        d.text(111, 324, "Last room left!", 14, "Semibold", ORANGE, "ma")
        d.text(36, 362, "Deluxe Room 204", 21, "Semibold")
        d.text(36, 394, "Sat, Nov 14 · 1 night · 2 guests", 15, "Regular", GREY)
        d.line([(36, 436), (354, 436)], LINE, 1)
        for i, (k, v) in enumerate((("Booked", "9:41:07 PM"), ("Booking ID", booking_id), ("Paid", "$129.00"))):
            d.text(36, 452 + i * 36, k, 16, "Regular", GREY)
            d.text(354, 452 + i * 36, v, 16, "Semibold", (17, 17, 20), "ra")
        d.rect(20, 742, 370, 794, BLUE, r=14)
        d.text(195, 757, "View booking", 18, "Semibold", WHITE, "ma")
    return draw


def booking_screen(tapped: bool, confirmed: bool, booking_id: str):
    if confirmed:
        return confirmation(booking_id)

    def draw(d: ScreenDraw):
        d.rect(0, 0, 390, 844, BG)
        d.status_bar("9:41")
        d.rect(0, 50, 390, 300, (214, 170, 120))
        for i in range(6):  # a simple "photo" of the hotel: windows on a facade
            for j in range(3):
                d.rect(40 + i * 55, 90 + j * 62, 78 + i * 55, 130 + j * 62, (250, 226, 170), r=4)
        d.text(20, 320, "Marigold Hall & Rooms", 22, "Bold")
        d.text(20, 354, "The wedding venue · ★ 4.6", 15, "Regular", GREY)
        d.rect(20, 396, 370, 560, WHITE, r=14)
        d.rect(36, 412, 186, 440, (255, 239, 214), r=8)
        d.text(111, 418, "Last room left!", 14, "Semibold", ORANGE, "ma")
        d.text(36, 456, "Deluxe Room 204", 21, "Semibold")
        d.text(36, 490, "Sat, Nov 14 · 1 night", 15, "Regular", GREY)
        d.text(354, 520, "$129", 22, "Bold", (17, 17, 20), "ra")
        d.rect(20, 742, 370, 794, (0, 90, 200) if tapped else BLUE, r=14)
        d.text(195, 757, "Book now", 18, "Semibold", WHITE, "ma")
        if tapped:
            d.circle(250, 768, 34, (255, 255, 255, 90) if False else (120, 170, 240))
            d.text(195, 757, "Book now", 18, "Semibold", WHITE, "ma")
    return draw


def xray_screen(t: float, ep: "Episode"):
    """What the app did, drawn crisp inside the phone. t is seconds since the X-ray shot began."""
    same = ep.lines["priya_same"]
    race = ep.lines["priya_race"]
    t_same = same.start - ep.xray_t0
    t_race = race.start - ep.xray_t0
    t_twice = ep.lines["lata_twice"].start - ep.xray_t0
    W_ = (230, 236, 248)

    def draw(d: ScreenDraw):
        if t < 0.3:
            return confirmation("MH-48213")(d)
        scan = min(1.0, (t - 0.3) / 0.6)
        d.rect(0, 0, 390, 844, NAVY)
        for y in range(60, 844, 28):
            d.line([(0, y), (390, y)], (22, 36, 66), 1)
        d.text(195, 62, "INSIDE THE APP", 17, "Heavy", CYAN, "ma")
        fix = t >= t_race + 2.0
        u = (t - (t_race + 2.0)) if fix else (t - t_same)
        span = (race.end - ep.xray_t0 - (t_race + 2.0)) if fix else (t_twice - t_same)
        q = max(0.0, min(1.0, u / max(span, 0.1)))
        # the two requests
        for i, (who, ms, col) in enumerate((("Meena's phone", ".07.120", RED), ("Lata's phone", ".07.124", YELLOW))):
            x0 = 12 + i * 188
            d.rect(x0, 100, x0 + 178, 226, (28, 44, 80), r=14, outline=col, width=3)
            d.text(x0 + 89, 112, who, 17, "Bold", W_, "ma")
            d.text(x0 + 89, 140, "9:41" + ms, 17, "Semibold", CYAN, "ma")
            d.text(x0 + 89, 176, "book 204", 22, "Heavy", WHITE, "ma")
        # the database row
        d.text(195, 452, "the database", 14, "Bold", (150, 170, 210), "ma")
        d.rect(18, 364, 372, 446, (28, 44, 80), r=12, outline=(70, 96, 150), width=2)
        d.text(36, 390, "Room 204", 24, "Bold", WHITE)
        booked = q > (0.45 if fix else 0.62)
        st, sc = ("BOOKED", RED_UI) if booked else ("FREE", GREEN)
        d.rect(232, 380, 358, 430, sc, r=12)
        d.text(295, 391, st, 20, "Heavy", WHITE, "ma")
        if fix and 0.1 < q < 0.55:  # the lock
            d.rect(190, 384, 220, 420, GOLD, r=5)
            d.line([(196, 386), (196, 372), (214, 372), (214, 386)], GOLD, 4)

        def arrow(x, y0, y1, k, col, label):
            if k <= 0:
                return
            y = y0 + (y1 - y0) * min(1.0, k)
            d.line([(x, y0), (x, y)], col, 4)
            if k >= 1:
                d.line([(x - 9, y1 - 11), (x, y1), (x + 9, y1 - 11)], col, 4)
            if label:
                d.text(x + 10, (y0 + y) / 2 - 10, label, 14, "Bold", col)

        if not fix:
            for x in (101, 289):
                arrow(x - 40, 228, 360, q / 0.25, CYAN, "check")
                if q > 0.3:
                    d.rect(x - 4, 250, x + 84, 290, GREEN, r=10)
                    d.text(x + 40, 258, "FREE ✓", 17, "Heavy", WHITE, "ma")
                arrow(x + 40, 292, 360, (q - 0.4) / 0.2, (255, 160, 150), "")
                if q > 0.5:
                    d.text(x + 40, 300, "book!", 15, "Bold", (255, 160, 150), "ma")
            d.text(195, 484, "BOOKINGS", 15, "Heavy", (150, 170, 210), "ma")
            for j, (bid, who) in enumerate((("MH-48213", "Meena"), ("MH-48214", "Lata"))):
                if q > 0.62 + 0.08 * j:
                    y = 506 + j * 70
                    d.rect(18, y, 372, y + 58, (70, 30, 44), r=12, outline=RED_UI, width=3)
                    d.text(36, y + 16, f"{bid} · {who} · 204", 20, "Bold", WHITE)
            if q > 0.85:
                d.text(195, 664, "2 bookings. 1 room.", 26, "Heavy", RED_UI, "ma")
        else:
            arrow(61, 228, 360, q / 0.15, CYAN, "check + lock")
            if q > 0.15:
                d.rect(97, 250, 185, 290, GREEN, r=10)
                d.text(141, 258, "FREE ✓", 17, "Heavy", WHITE, "ma")
            if 0.1 < q < 0.55:
                d.text(289, 262, "waiting…", 19, "Bold", (200, 210, 230), "ma")
            arrow(249, 228, 360, (q - 0.55) / 0.15, CYAN, "check")
            if q > 0.72:
                d.rect(226, 250, 352, 290, RED_UI, r=10)
                d.text(289, 258, "SOLD OUT", 17, "Heavy", WHITE, "ma")
            d.text(195, 484, "BOOKINGS", 15, "Heavy", (150, 170, 210), "ma")
            if q > 0.45:
                d.rect(18, 506, 372, 564, (24, 60, 44), r=12, outline=GREEN, width=3)
                d.text(36, 522, "MH-48213 · Meena · 204", 20, "Bold", WHITE)
            d.text(195, 610, "THE FIX:", 18, "Heavy", GOLD, "ma")
            d.text(195, 638, "lock, then book", 24, "Heavy", GOLD, "ma")
        if scan < 1:  # the X-ray scan line revealing the inside, top to bottom
            yy = 844 * scan
            d.rect(0, yy, 390, 844, BG)
            d.line([(0, yy), (390, yy)], CYAN, 5)
    return draw


CAPTIONS = {
    "priya_same": lambda u, dur: "You both tapped at the same moment." if u < dur * 0.45
    else "It checked for both of you before either booking was saved.",
    "lata_twice": lambda u, dur: "So it sold it TWICE?!",
    "priya_race": lambda u, dur: "Engineers call that a race condition." if u < dur * 0.4
    else "The fix: lock the room while one booking finishes.",
    "meena_hmph": lambda u, dur: "Hmph.",
}


def caption(img: Image.Image, text: str, y: float):
    from kit.phone import sf as sffont
    d = ImageDraw.Draw(img)
    f = sffont(17, "Bold")
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) > 900:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    for i, ln in enumerate(lines):
        yy = y - (len(lines) - 1 - i) * 62
        d.text((540, yy), ln, font=f, fill=WHITE, anchor="mm", stroke_width=7, stroke_fill=(20, 20, 24))


def stamp(img: Image.Image, text: str, y: float, k: float):
    from kit.phone import sf as sffont
    s = 1.6 - 0.6 * k
    layer = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = sffont(30 * s, "Heavy")
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([540 - tw / 2 - 40, 150 - 70 * s, 540 + tw / 2 + 40, 150 + 70 * s], 18, outline=RED_UI,
                        width=12, fill=(255, 255, 255, 230))
    d.text((540, 150), text, font=f, fill=RED_UI, anchor="mm")
    layer = layer.rotate(-6, resample=Image.BICUBIC)
    img.paste(layer, (0, int(y - 150)), layer)


def jingle() -> np.ndarray:
    t = sound.t_axis(0.5)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 9) for f in (2600, 3400, 4100))
    return x / 3


if __name__ == "__main__":
    Episode().render(preview="--preview" in sys.argv)
