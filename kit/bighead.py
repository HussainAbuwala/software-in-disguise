"""Big-head cartoon characters (chosen 2026-10-05 for Episode 1, "The Last Room").

Big round heads on small bodies, big eyes, thick brows, little nose: simple on purpose, so the look reads as a
deliberate cartoon and the acting carries the comedy. Flat colours with a dark ink outline; app screens are pasted
on top crisp and realistic (kit/phone.py).

Everything is drawn at 2x and downsampled. A `Pen` can "boil": with a boil seed, every outline point is nudged by a
pixel or two, and changing the seed every other frame makes the lines shimmer like hand-drawn animation.

A character is drawn from a head centre (cx, cy) and a head radius r. Faces read the pose: `expr` sets brows, lids
and the resting mouth; `mouth` (0..1, from the dialogue loudness) opens it; `gaze` moves the pupils; `arms` picks a
pose for the small arms.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2

INK = (29, 27, 31)
WHITE = (255, 255, 255)
PAPER = (250, 245, 234)
RED = (226, 76, 58)
YELLOW = (242, 193, 78)
TEAL = (38, 150, 140)
BLUE = (66, 112, 196)
GOLD = (236, 184, 52)
HAIR = (31, 28, 33)
GREY_HAIR = (150, 146, 150)
CHEEK = (232, 122, 110)
TONGUE = (214, 92, 96)

HAND_FONT = ("/System/Library/Fonts/Noteworthy.ttc", 1)
BOLD_FONT = ("/System/Library/Fonts/Avenir Next.ttc", 8)


class Pen:
    def __init__(self, img: Image.Image, boil: int | None = None, lw: float = 9):
        self.img = img
        self.d = ImageDraw.Draw(img)
        self.lw = lw
        self.rng = random.Random(boil) if boil is not None else None

    def j(self, pts, amt=1.6):
        if not self.rng:
            return pts
        return [(x + self.rng.uniform(-amt, amt), y + self.rng.uniform(-amt, amt)) for x, y in pts]

    def _s(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill, lw=None, outline=INK):
        pts = self.j(pts)
        if fill is not None:
            self.d.polygon(self._s(pts), fill=fill)
        if lw != 0 and outline is not None:
            self.line(pts + [pts[0]], outline, lw, jitter=False)

    def line(self, pts, fill=INK, lw=None, jitter=True):
        pts = self.j(pts) if jitter else pts
        w = (lw or self.lw) * S
        self.d.line(self._s(pts), fill=fill, width=round(w), joint="curve")
        for x, y in (pts[0], pts[-1]):
            self.d.ellipse([x * S - w / 2, y * S - w / 2, x * S + w / 2, y * S + w / 2], fill=fill)

    def ell(self, cx, cy, rx, ry, fill, lw=None, outline=INK, n=48):
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.poly(pts, fill, lw, outline)

    def arc(self, cx, cy, rx, ry, a0, a1, fill=INK, lw=None):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
               for a in [a0 + (a1 - a0) * i / 20 for i in range(21)]]
        self.line(pts, fill, lw)

    def rrect(self, x0, y0, x1, y1, r, fill, lw=None, outline=INK):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill,
                                 outline=outline if lw != 0 else None, width=round((lw or self.lw) * S))

    def text(self, xy, s, size, font=HAND_FONT, fill=INK, anchor="mm", angle=0.0):
        f = ImageFont.truetype(font[0], round(size * S), index=font[1])
        if not angle:
            self.d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)
            return
        l, t, r, b = f.getbbox(s)
        im = Image.new("RGBA", (r - l + 40, b - t + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20 - l, 20 - t), s, font=f, fill=fill)
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        self.img.paste(im, (round(xy[0] * S - im.width / 2), round(xy[1] * S - im.height / 2)), im)


@dataclass(frozen=True)
class Char:
    name: str
    skin: tuple
    hair: str                     # bun | long | short | ponytail
    outfit: tuple
    outfit2: tuple | None = None  # scarf / vest / collar colour
    hair_color: tuple = HAIR
    glasses: bool = False
    earrings: tuple | None = GOLD
    moustache: bool = False
    grey: bool = False            # grey streaks
    bags: bool = False            # tired eyes (the receptionist)
    name_tag: str | None = None
    top: str = "plain"            # scarf | vest | neckline | collar | kurta | hoodie | blazer | sweater_vest


MEENA = Char("Meena", (196, 135, 92), "bun", RED, YELLOW, grey=True, top="scarf")
LATA = Char("Lata", (168, 110, 72), "long", YELLOW, None, glasses=True, top="collar")
CLERK = Char("Clerk", (150, 100, 66), "short", (60, 66, 92), WHITE, earrings=None, bags=True, name_tag="STAFF",
             top="vest")
PRIYA = Char("Priya", (190, 128, 86), "ponytail", TEAL, None, earrings=GOLD, top="neckline")

# Cast B (2026-10-05): two uncles, a calm receptionist, and Dev (Priya's brother) as the explainer.
RAJ = Char("Raj", (176, 118, 80), "bald_sides", (74, 108, 176), (240, 226, 196), hair_color=(58, 54, 58),
           earrings=None, moustache=True, top="kurta")
VIKRAM = Char("Vikram", (150, 98, 64), "short", (150, 52, 62), WHITE, hair_color=(168, 164, 166), glasses=True,
              earrings=None, top="sweater_vest")
NISHA = Char("Nisha", (160, 105, 70), "bun", (40, 46, 70), WHITE, earrings=None, name_tag="NISHA", top="blazer")
DEV = Char("Dev", (166, 112, 76), "short", (227, 178, 60), None, earrings=None, top="hoodie")

CAST = {c.name.upper(): c for c in (MEENA, LATA, CLERK, PRIYA, RAJ, VIKRAM, NISHA, DEV)}

# brows: (inner y, outer y) in head units, negative = up; lid: 0 open .. 1 shut; mouth: resting shape
EXPR = {
    "neutral": dict(brows=(-0.3, -0.36), lid=0.0, mouth="smile", smile=0.3),
    "angry": dict(brows=(-0.15, -0.32), lid=0.15, mouth="frown", smile=0.0),
    "furious": dict(brows=(-0.1, -0.34), lid=0.3, mouth="frown", smile=0.0),
    "smug": dict(brows=(-0.32, -0.3), lid=0.45, mouth="smirk", smile=0.6),
    "shocked": dict(brows=(-0.48, -0.46), lid=0.0, mouth="o", smile=0.0),
    "deadpan": dict(brows=(-0.3, -0.3), lid=0.5, mouth="flat", smile=0.0),
    "happy": dict(brows=(-0.4, -0.42), lid=0.0, mouth="smile", smile=1.0),
    "explaining": dict(brows=(-0.38, -0.36), lid=0.05, mouth="smile", smile=0.5),
    "worried": dict(brows=(-0.44, -0.3), lid=0.0, mouth="flat", smile=0.0),
    "triumphant": dict(brows=(-0.42, -0.4), lid=0.25, mouth="grin", smile=1.0),
}


def body(p: Pen, c: Char, cx, cy, r, bottom, lean=0.0):
    top = cy + r * 0.9
    sw = r * 0.82
    pts = [(cx - sw * 1.18 + lean, bottom), (cx - sw + lean * 0.5, top + r * 0.12), (cx - sw * 0.6, top),
           (cx + sw * 0.6, top), (cx + sw + lean * 0.5, top + r * 0.12), (cx + sw * 1.18 + lean, bottom)]
    p.poly(pts, c.outfit)
    if c.top == "scarf":  # a scarf across one shoulder
        p.poly([(cx - sw * 0.55, top), (cx - sw * 0.2, top), (cx + sw * 0.55, bottom), (cx + sw * 0.05, bottom)], c.outfit2)
    if c.top in ("vest", "blazer"):  # white shirt under a dark vest or blazer, a name tag
        p.poly([(cx - sw * 0.3, top), (cx + sw * 0.3, top), (cx, top + r * 0.5)], WHITE)
        p.poly([(cx - r * 0.12, top + r * 0.04), (cx + r * 0.12, top + r * 0.04), (cx + r * 0.05, top + r * 0.16),
                (cx - r * 0.05, top + r * 0.16)], RED, 5)
        if c.name_tag:
            p.rrect(cx + sw * 0.35, top + r * 0.32, cx + sw * 0.85, top + r * 0.5, 6, WHITE, 4)
            p.text((cx + sw * 0.6, top + r * 0.41), c.name_tag, r * 0.075, BOLD_FONT)
    if c.top == "neckline":  # a round neckline
        p.arc(cx, top - r * 0.02, sw * 0.35, r * 0.16, 10, 170, INK, 6)
    if c.top in ("collar", "sweater_vest"):  # a collar (over a V-neck vest)
        if c.top == "sweater_vest":
            p.poly([(cx - sw * 0.35, top), (cx + sw * 0.35, top), (cx, top + r * 0.55)], c.outfit2)
    if c.top == "kurta":  # a placket with buttons
        p.poly([(cx - r * 0.1, top), (cx + r * 0.1, top), (cx + r * 0.1, top + r * 0.75), (cx - r * 0.1, top + r * 0.75)],
               c.outfit2, 5)
        for k in range(3):
            p.ell(cx, top + r * (0.18 + 0.2 * k), r * 0.03, r * 0.03, INK, 0)
    if c.top == "hoodie":  # hood behind the neck and two strings
        p.arc(cx, top + r * 0.02, sw * 0.62, r * 0.22, 0, 180, INK, 7)
        for side in (-1, 1):
            p.line([(cx + side * r * 0.14, top + r * 0.12), (cx + side * r * 0.16, top + r * 0.5)], WHITE, 6)
    if c.top in ("collar", "sweater_vest"):
        for side in (-1, 1):
            p.poly([(cx, top + r * 0.05), (cx + side * sw * 0.42, top - r * 0.02), (cx + side * sw * 0.3, top + r * 0.2)],
                   WHITE, 6)


def head(p: Pen, c: Char, cx, cy, r, expr="neutral", mouth=0.0, gaze=(0.0, 0.0), blink=False, turn=0.0):
    e = EXPR[expr]
    fx = cx + turn * r * 0.12  # features slide a little for a three-quarter look
    if c.hair == "ponytail":
        side = -1 if turn > 0 else 1
        p.poly([(cx + side * r * 0.6, cy - r * 0.8), (cx + side * r * 1.35, cy - r * 0.55), (cx + side * r * 1.45, cy + r * 0.4),
                (cx + side * r * 1.2, cy + r * 1.1), (cx + side * r * 1.0, cy + r * 0.3), (cx + side * r * 0.8, cy - r * 0.3)],
               c.hair_color, 6)
    if c.earrings:
        for side in (-1, 1):
            p.ell(cx + side * r * 1.0, cy + r * 0.45, r * 0.07, r * 0.07, c.earrings, 5)
    # head
    p.ell(cx, cy, r, r * 1.05, c.skin)
    # hair cap
    if c.hair in ("bun", "long", "ponytail"):  # middle parting
        cap = [(cx - r * 1.02, cy - r * 0.12)]
        cap += [(cx + r * 1.04 * math.cos(math.radians(a)), cy - r * 0.05 + r * 1.1 * math.sin(math.radians(a)))
                for a in range(190, 351, 8)]
        cap += [(cx + r * 1.02, cy - r * 0.12), (cx + r * 0.5, cy - r * 0.62), (cx, cy - r * 0.8), (cx - r * 0.5, cy - r * 0.62)]
        p.poly(cap, c.hair_color, 6)
        p.line([(cx, cy - r * 1.13), (cx, cy - r * 0.82)], c.skin, 6)
    elif c.hair == "bald_sides":  # bald on top, hair over the ears, a shine
        for side in (-1, 1):
            p.poly([(cx + side * r * 0.98, cy - r * 0.45), (cx + side * r * 0.62, cy - r * 0.62), (cx + side * r * 0.72, cy - r * 0.3),
                    (cx + side * r * 1.02, cy + r * 0.05)], c.hair_color, 6)
        p.arc(cx - r * 0.35, cy - r * 0.72, r * 0.2, r * 0.1, 200, 300, WHITE, 7)
    elif c.hair == "short":  # a neat side part
        cap = [(cx - r * 1.02, cy - r * 0.2)]
        cap += [(cx + r * 1.05 * math.cos(math.radians(a)), cy - r * 0.08 + r * 1.1 * math.sin(math.radians(a)))
                for a in range(188, 353, 8)]
        cap += [(cx + r * 1.02, cy - r * 0.2), (cx + r * 0.7, cy - r * 0.55), (cx - r * 0.2, cy - r * 0.62),
                (cx - r * 0.55, cy - r * 0.78), (cx - r * 0.85, cy - r * 0.5)]
        p.poly(cap, c.hair_color, 6)
    if c.hair == "bun":
        p.ell(cx, cy - r * 1.2, r * 0.38, r * 0.3, c.hair_color, 6)
    # eyes
    lid = 1.0 if blink else e["lid"]
    for side in (-1, 1):
        ex, ey = fx + side * r * 0.34, cy + r * 0.05
        rx, ry = r * 0.2, r * 0.25
        if lid >= 0.95:
            p.arc(ex, ey + ry * 0.2, rx, ry * 0.5, 15, 165, INK, 7) if expr != "happy" else \
                p.arc(ex, ey + ry * 0.4, rx, ry * 0.6, 200, 340, INK, 7)
            continue
        p.ell(ex, ey, rx, ry, WHITE, 6)
        px, py = ex + gaze[0] * rx * 0.45, ey + r * 0.05 + gaze[1] * ry * 0.3
        p.ell(px, py, r * 0.1, r * 0.11, INK, 0)
        p.ell(px - r * 0.03, py - r * 0.04, r * 0.03, r * 0.03, WHITE, 0)
        if lid > 0.05:  # upper lid: skin over the top of the eye, with its edge line
            yl = ey - ry + 2 * ry * lid
            p.d.polygon(p._s([(ex - rx * 1.15, ey - ry * 1.25), (ex + rx * 1.15, ey - ry * 1.25), (ex + rx * 1.05, yl + ry * 0.1),
                              (ex, yl - ry * 0.05), (ex - rx * 1.05, yl + ry * 0.1)]), fill=c.skin)
            p.line([(ex - rx * 1.05, yl + ry * 0.1), (ex, yl - ry * 0.05), (ex + rx * 1.05, yl + ry * 0.1)], INK, 7)
        if c.bags:
            p.arc(ex, ey + ry * 0.95, rx * 0.8, ry * 0.25, 20, 160, INK, 4)
        # brows
        inner, outer = e["brows"]
        p.line([(fx + side * r * 0.14, cy + r * inner), (fx + side * r * 0.55, cy + r * outer)], c.hair_color if c.hair_color != GREY_HAIR else INK, 16)
    if c.glasses:
        for side in (-1, 1):
            p.ell(fx + side * r * 0.34, cy + r * 0.07, r * 0.27, r * 0.3, None, 7)
        p.line([(fx - r * 0.07, cy + r * 0.05), (fx + r * 0.07, cy + r * 0.05)], INK, 7)
    # nose
    p.arc(fx + r * 0.03, cy + r * 0.47, r * 0.09, r * 0.09, 100, 280 if turn >= 0 else 260, INK, 6)
    # cheeks when happy
    if e["smile"] >= 0.8:
        for side in (-1, 1):
            p.ell(fx + side * r * 0.58, cy + r * 0.48, r * 0.12, r * 0.07, CHEEK, 0)
    # mouth
    mx, my = fx, cy + r * 0.78
    if mouth > 0.08:
        w = r * (0.2 + 0.08 * e["smile"])
        h = r * (0.06 + 0.24 * mouth)
        p.ell(mx, my + h * 0.3, w, h, INK, 0)
        p.ell(mx, my + h * 0.85, w * 0.55, h * 0.35, TONGUE, 0)
    elif e["mouth"] == "o":
        p.ell(mx, my + r * 0.05, r * 0.11, r * 0.14, INK, 0)
    elif e["mouth"] == "frown":
        p.arc(mx, my + r * 0.08, r * 0.2, r * 0.1, 200, 340, INK, 8)
    elif e["mouth"] == "flat":
        p.line([(mx - r * 0.15, my + r * 0.03), (mx + r * 0.15, my + r * 0.03)], INK, 8)
    elif e["mouth"] == "smirk":
        p.line([(mx - r * 0.16, my + r * 0.04), (mx + r * 0.06, my + r * 0.03), (mx + r * 0.2, my - r * 0.06)], INK, 8)
    elif e["mouth"] == "grin":
        p.d.chord([(mx - r * 0.28) * S, (my - r * 0.2) * S, (mx + r * 0.28) * S, (my + r * 0.25) * S], 0, 180, fill=INK)
        p.d.chord([(mx - r * 0.24) * S, (my - r * 0.16) * S, (mx + r * 0.24) * S, (my + r * 0.05) * S], 0, 180, fill=WHITE)
    else:
        s = e["smile"]
        p.arc(mx, my - r * 0.05, r * 0.2, r * (0.04 + 0.1 * s), 20, 160, INK, 8)
    if c.moustache:  # a big bushy moustache over the top lip
        pts = [(mx, my - r * 0.18), (mx + r * 0.12, my - r * 0.22), (mx + r * 0.3, my - r * 0.16), (mx + r * 0.4, my - r * 0.02),
               (mx + r * 0.3, my - r * 0.06), (mx + r * 0.14, my - r * 0.06), (mx, my - r * 0.1),
               (mx - r * 0.14, my - r * 0.06), (mx - r * 0.3, my - r * 0.06), (mx - r * 0.4, my - r * 0.02),
               (mx - r * 0.3, my - r * 0.16), (mx - r * 0.12, my - r * 0.22)]
        p.poly(pts, c.hair_color, 6)


def limb(p: Pen, c: Char, r, pts, hand=True, finger=None):
    """An arm along pts (shoulder, elbow, ..., wrist): a sleeve-coloured tube with a round hand."""
    lw = r * 0.2
    p.line(pts, INK, lw + 9)
    p.line(pts, c.outfit, lw - 6, jitter=False)
    if hand:
        hx, hy = pts[-1]
        p.ell(hx, hy, r * 0.13, r * 0.12, c.skin, 6)
        if finger:
            p.line([(hx, hy), (hx + finger[0] * r * 0.22, hy + finger[1] * r * 0.22)], INK, r * 0.09 + 6)
            p.line([(hx, hy), (hx + finger[0] * r * 0.2, hy + finger[1] * r * 0.2)], c.skin, r * 0.09 - 2, jitter=False)


def arms(p: Pen, c: Char, cx, cy, r, pose: str, bottom, k: float = 1.0):
    """Small arms: rest | point (toward +x) | point_left | crossed | phone | reach | hands_up. k animates the reach."""
    top = cy + r * 0.9
    sw = r * 0.82
    def arm(pts, hand=True, finger=None):
        limb(p, c, r, pts, hand, finger)

    shoulder_l, shoulder_r = (cx - sw * 0.92, top + r * 0.2), (cx + sw * 0.92, top + r * 0.2)
    if pose == "point":
        arm([shoulder_r, (cx + sw * 1.3, top + r * 0.45), (cx + sw * (1.3 + 0.5 * k), top + r * 0.1)], finger=(1, -0.3))
    elif pose == "point_left":
        arm([shoulder_l, (cx - sw * 1.3, top + r * 0.45), (cx - sw * (1.3 + 0.5 * k), top + r * 0.1)], finger=(-1, -0.3))
    elif pose == "crossed":
        arm([shoulder_l, (cx - sw * 0.7, top + r * 0.75), (cx + sw * 0.55, top + r * 0.62)])
        arm([shoulder_r, (cx + sw * 0.7, top + r * 0.85), (cx - sw * 0.5, top + r * 0.72)])
    elif pose == "phone":  # holding a phone up at chest height, screen facing us
        hx, hy = cx + sw * 0.15, top + r * 0.55
        arm([shoulder_r, (cx + sw * 0.9, top + r * 0.9), (hx + r * 0.2, hy + r * 0.25)])
        p.rrect(hx - r * 0.22, hy - r * 0.42, hx + r * 0.22, hy + r * 0.38, r * 0.06, INK, 0)
        p.rrect(hx - r * 0.18, hy - r * 0.37, hx + r * 0.18, hy + r * 0.33, r * 0.04, (236, 244, 252), 0)
        p.ell(hx, hy - r * 0.08, r * 0.08, r * 0.08, (52, 199, 89), 0)
    elif pose in ("reach", "reach_left"):
        d = 1 if pose == "reach" else -1
        sh = shoulder_r if d > 0 else shoulder_l
        arm([sh, (cx + d * sw * (1.2 + 0.9 * k), top + r * (0.5 - 0.2 * k))])
    elif pose == "hold_up":  # right hand raised beside the head, holding something up
        arm([shoulder_r, (cx + sw * 1.45, top + r * 0.1), (cx + sw * 1.4, cy - r * 0.2)])
    elif pose == "hands_up":
        arm([shoulder_l, (cx - sw * 1.3, top - r * 0.1), (cx - sw * 1.2, top - r * 0.6)])
        arm([shoulder_r, (cx + sw * 1.3, top - r * 0.1), (cx + sw * 1.2, top - r * 0.6)])


def hair_back(p: Pen, c: Char, cx, cy, r):
    """Long hair falls behind the shoulders: drawn before the body."""
    if c.hair == "long":
        pts = [(cx - r * 1.08, cy - r * 0.2), (cx - r * 1.18, cy + r * 0.8), (cx - r * 1.05, cy + r * 1.3),
               (cx - r * 0.6, cy + r * 1.38), (cx + r * 0.6, cy + r * 1.38), (cx + r * 1.05, cy + r * 1.3),
               (cx + r * 1.18, cy + r * 0.8), (cx + r * 1.08, cy - r * 0.2), (cx, cy - r * 1.0)]
        p.poly(pts, c.hair_color, 6)


def character(p: Pen, c: Char, cx, cy, r, expr="neutral", mouth=0.0, gaze=(0.0, 0.0), blink=False, arm="rest",
              bottom=1100, turn=0.0, k=1.0):
    hair_back(p, c, cx, cy, r)
    body(p, c, cx, cy, r, bottom)
    if arm in ("rest", "phone", "crossed"):
        arms(p, c, cx, cy, r, arm, bottom, k)
        head(p, c, cx, cy, r, expr, mouth, gaze, blink, turn)
    else:  # gesturing arms go in front of the head's side
        head(p, c, cx, cy, r, expr, mouth, gaze, blink, turn)
        arms(p, c, cx, cy, r, arm, bottom, k)


def speech(p: Pen, box, tail, text, size=60):
    x0, y0, x1, y1 = box
    tx = (x0 + x1) / 2 + (tail[0] - (x0 + x1) / 2) * 0.35
    edge = y1 - 6 if tail[1] > y1 else y0 + 6
    p.poly([(tx - 30, edge), tail, (tx + 30, edge)], WHITE, 7)
    p.rrect(x0, y0, x1, y1, 44, WHITE, 8)
    p.d.polygon(p._s([(tx - 24, edge), (tx + 24, edge), (tx, edge + (10 if tail[1] > y1 else -10))]), fill=WHITE)
    p.text(((x0 + x1) / 2, (y0 + y1) / 2), text, size)


def new_frame(bg=PAPER) -> Image.Image:
    return Image.new("RGB", (W * S, H * S), bg)


def finish(img: Image.Image) -> Image.Image:
    return img.resize((W, H), Image.LANCZOS)
