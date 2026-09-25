"""The recurring cast: Dev, Mira, and Jo.

Each character is built from simple shapes so they look identical in every episode. A frame of a character is
described by a `Pose`: where they are, which way they face, their expression, how open their mouth is (driven by
the dialogue audio), whether they are blinking, and what their hands are doing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .canvas import ALERT, INK, MUSTARD, PAPER, TEAL, Canvas, lid_chord_angles

HAIR = (34, 30, 30)
HEAD_R = 78


@dataclass(frozen=True)
class Look:
    name: str
    skin: tuple
    top: tuple
    bottoms: tuple
    hair: str  # spiky | ponytail | buzz
    glasses: bool = False
    hoodie: bool = False
    pajamas: bool = False


DEV = Look("Dev", skin=(166, 112, 76), top=MUSTARD, bottoms=(58, 60, 72), hair="spiky", hoodie=True)
MIRA = Look("Mira", skin=(196, 142, 102), top=TEAL, bottoms=(120, 120, 124), hair="ponytail", glasses=True)
JO = Look("Jo", skin=(112, 74, 52), top=(176, 176, 180), bottoms=(150, 150, 156), hair="buzz", pajamas=True)

# Expression = eyelid level (0 open .. 1 shut), brow (inner, outer) offsets per eye (negative = raised), mouth shape.
EXPRESSIONS = {
    "neutral": dict(lid=0.1, brow=(0, 0), mouth="flat"),
    "angry": dict(lid=0.22, brow=(12, -8), mouth="frown"),
    "determined": dict(lid=0.3, brow=(14, -6), mouth="flat"),
    "smug": dict(lid=0.42, brow=(-4, -4), brow_raise_far=-16, mouth="smirk"),
    "unimpressed": dict(lid=0.35, brow=(0, 0), brow_raise_far=-12, mouth="flat"),
    "tired": dict(lid=0.55, brow=(-6, 8), mouth="flat", bags=True),
    "tired_angry": dict(lid=0.55, brow=(10, -2), mouth="frown", bags=True),
    "asleep": dict(lid=1.0, brow=(-2, 4), mouth="o_small"),
    "shock": dict(lid=0.0, brow=(-18, -14), mouth="o", pupil=0.6),
    "deadpan": dict(lid=0.45, brow=(0, 0), mouth="flat"),
    "confident": dict(lid=0.3, brow=(-6, -10), mouth="smile"),
    "phone": dict(lid=0.4, brow=(-2, -4), mouth="smile", gaze_y=1.0),  # absorbed in a phone, pleased with himself
    "annoyed": dict(lid=0.32, brow=(12, -2), mouth="flat"),
    "cheerful": dict(lid=0.15, brow=(-10, -8), mouth="smile"),
}


@dataclass
class Pose:
    x: float
    y: float  # seated: hip point on the couch; standing: feet on the floor
    facing: int = 1  # +1 faces right, -1 faces left
    expr: str = "neutral"
    mouth: float = 0.0  # 0..1 from dialogue loudness
    blink: bool = False
    gaze: float | None = None  # pupils: -1 left .. 1 right; default = facing
    gaze_y: float | None = None  # pupils: -1 up .. 1 down; default from the expression
    standing: bool = False
    hands: str = "rest"  # raise_remote | clutch_batteries | mug | reach | shrug | rest
    raise_amt: float = 1.0  # raise_remote: 1 = high, lower when tired
    reach: tuple | None = None  # reach target in world coordinates
    head_dx: float = 0.0
    head_dy: float = 0.0
    extras: dict = field(default_factory=dict)


# --------------------------------------------------------------------------------------------------------------
# Face


def _eye(c: Canvas, cx, cy, look: Look, lid: float, gaze: float, pupil_scale: float, blink: bool, gaze_y: float = 0.0):
    rx, ry = 17, 21
    if blink or lid >= 0.95:
        c.arc(cx - rx, cy - 6, cx + rx, cy + 10, 10, 170, width=6)
        return
    c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, fill=PAPER, width=5)
    pr = 8 * pupil_scale
    px, py = cx + gaze * 7, cy + 2 + gaze_y * 9
    c.ellipse(px - pr, py - pr, px + pr, py + pr, fill=INK, outline=None)
    if lid > 0.02:
        start, end = lid_chord_angles(lid)
        c.chord(cx - rx, cy - ry, cx + rx, cy + ry, start, end, fill=look.skin, width=5)


def _brow(c: Canvas, cx, cy, inner_dy, outer_dy, inner_side: int):
    inner_x, outer_x = cx + inner_side * 20, cx - inner_side * 20
    c.line([(outer_x, cy + outer_dy), (inner_x, cy + inner_dy)], width=9)


def _mouth(c: Canvas, mx, my, shape: str, openness: float, facing: int):
    if openness > 0.12:
        h = 8 + 26 * min(1.0, openness)
        c.ellipse(mx - 17, my - h / 2, mx + 17, my + h / 2, fill=(92, 34, 40), width=5)
        if h > 16:
            c.chord(mx - 11, my + h / 2 - 12, mx + 11, my + h / 2 + 2, 180, 360, fill=ALERT, outline=None)
        return
    if shape == "frown":
        c.arc(mx - 20, my - 4, mx + 20, my + 16, 200, 340)
    elif shape == "smile":
        c.arc(mx - 20, my - 16, mx + 20, my + 6, 20, 160)
    elif shape == "smirk":
        c.line([(mx - 18, my + 2), (mx + 14, my - 2)], width=6)
        c.arc(mx + 4 * facing - 8, my - 16, mx + 4 * facing + 12, my + 2, 330 if facing > 0 else 150, 60 if facing > 0 else 240)
    elif shape == "o":
        c.ellipse(mx - 11, my - 14, mx + 11, my + 14, fill=(92, 34, 40), width=5)
    elif shape == "o_small":
        c.ellipse(mx - 7, my - 6, mx + 7, my + 8, fill=(92, 34, 40), width=4)
    else:  # flat
        c.line([(mx - 16, my), (mx + 16, my)], width=6)


def _hair_back(c: Canvas, look: Look, hx, hy, f):
    if look.hair == "ponytail":
        bx = hx - f * 48
        c.poly([(bx, hy - 72), (bx - f * 72, hy - 100), (bx - f * 92, hy - 30), (bx - f * 66, hy + 30), (bx - f * 26, hy - 12)], fill=HAIR)


def _hair_front(c: Canvas, look: Look, hx, hy, f):
    if look.hair == "spiky":
        pts = [(-82, -5), (-88, -60), (-55, -95), (-30, -117), (-5, -93), (25, -121), (45, -90), (80, -100), (78, -45),
               (60, -35), (30, -53), (-10, -45), (-45, -55), (-70, -20)]
        c.poly([(hx + f * dx, hy + dy) for dx, dy in pts], fill=HAIR)
    elif look.hair == "ponytail":
        c.chord(hx - 81, hy - 90, hx + 81, hy + 20, 180, 360, fill=HAIR)
        c.circle(hx - f * 44, hy - 84, 17, fill=HAIR)
    elif look.hair == "buzz":
        c.chord(hx - 79, hy - 80, hx + 79, hy + 6, 185, 355, fill=(70, 58, 50), width=5)


def head(c: Canvas, look: Look, pose: Pose, hx: float, hy: float):
    f = pose.facing
    ex = EXPRESSIONS[pose.expr]
    gaze = f * 1.0 if pose.gaze is None else pose.gaze
    gaze_y = ex.get("gaze_y", 0.0) if pose.gaze_y is None else pose.gaze_y
    _hair_back(c, look, hx, hy, f)
    c.circle(hx, hy, HEAD_R, fill=look.skin)
    # Ear on the far side from the face.
    c.ellipse(hx - f * 82 - 12, hy - 4, hx - f * 82 + 12, hy + 26, fill=look.skin, width=5)
    _hair_front(c, look, hx, hy, f)

    fx = hx + f * 16  # face center shifted toward facing: a simple three-quarter view
    eyes = (fx - 23, fx + 23)
    lid = ex["lid"]
    for i, e in enumerate(eyes):
        _eye(c, e, hy + 3, look, lid, gaze, ex.get("pupil", 1.0), pose.blink, gaze_y)
    if ex.get("bags"):
        for e in eyes:
            c.arc(e - 16, hy + 12, e + 16, hy + 34, 20, 160, fill=(120, 80, 70), width=4)
    if look.glasses:
        for e in eyes:
            c.circle(e, hy + 3, 28, width=6)
        c.line([(eyes[0] + 28, hy + 1), (eyes[1] - 28, hy + 1)], width=6)
    inner_dy, outer_dy = ex["brow"]
    for e in eyes:
        side = 1 if e < fx else -1  # which way is the nose
        far = (e < fx) == (f > 0)  # the eye further from the viewer's side of the face
        o_dy = outer_dy + (ex.get("brow_raise_far", 0) if far else 0)
        i_dy = inner_dy + (ex.get("brow_raise_far", 0) if far else 0)
        _brow(c, e, hy - 32, i_dy, o_dy, side)
    _mouth(c, fx + f * 4, hy + 46, ex["mouth"], pose.mouth, f)


# --------------------------------------------------------------------------------------------------------------
# Props held in hands


def remote(c: Canvas, x, y, scale=1.0, empty=True):
    """Remote seen from the back, battery compartment open."""
    w, h = 26 * scale, 150 * scale
    c.rect(x - w, y - h, x + w, y, fill=(60, 58, 56), radius=18 * scale)
    if empty:
        c.rect(x - w + 11 * scale, y - h + 38 * scale, x + w - 11 * scale, y - 30 * scale, fill=(222, 218, 210), width=4, radius=6 * scale)
        c.line([(x, y - h + 46 * scale), (x, y - 38 * scale)], fill=(150, 145, 138), width=3)


def battery(c: Canvas, x, y, scale=1.0):
    w, h = 15 * scale, 70 * scale
    c.rect(x - w, y - h, x + w, y, fill=MUSTARD, width=5, radius=6 * scale)
    c.rect(x - 6 * scale, y - h - 9 * scale, x + 6 * scale, y - h, fill=INK, outline=None)
    c.line([(x - w, y - h * 0.62), (x + w, y - h * 0.62)], width=4)


def mug(c: Canvas, x, y):
    c.rect(x - 30, y - 60, x + 30, y, fill=PAPER, radius=8)
    c.arc(x + 18, y - 48, x + 50, y - 14, 270, 90, width=7)


def phone(c: Canvas, x, y, glow=(170, 210, 235)):
    """Phone held flat-ish, screen toward the holder; a sliver of screen glow shows."""
    c.rect(x - 34, y - 58, x + 34, y + 58, fill=(40, 40, 46), radius=12, width=6)
    c.rect(x - 24, y - 46, x + 24, y + 44, fill=glow, outline=None, radius=6)


def milk_carton(c: Canvas, x, y, upside_down=False, scale=1.0):
    """Gable-top carton. (x, y) is the bottom center, or the top center when upside down."""
    k, d = scale, (-1 if upside_down else 1)
    w, h, gable = 34 * k, 110 * k, 34 * k
    body = [(x - w, y), (x + w, y), (x + w, y - d * h), (x - w, y - d * h)]
    c.poly(body, fill=PAPER, width=6)
    c.poly([(x - w, y - d * h), (x + w, y - d * h), (x + w * 0.6, y - d * (h + gable)), (x - w * 0.6, y - d * (h + gable))], fill=(236, 240, 246), width=6)
    c.rect(x - w * 0.5, y - d * (h + gable) - (8 * k if d > 0 else 0), x + w * 0.5, y - d * (h + gable) + (0 if d > 0 else 8 * k), fill=(236, 240, 246), width=5)
    band_y = y - d * h * 0.55
    c.rect(x - w, band_y - 16 * k, x + w, band_y + 16 * k, fill=(70, 130, 200), width=5)


def hand(c: Canvas, x, y, look: Look, r=26):
    c.circle(x, y, r, fill=look.skin)


# --------------------------------------------------------------------------------------------------------------
# Whole character


def seated(c: Canvas, look: Look, pose: Pose):
    """Seated on the couch; the couch's seat front is drawn afterwards by the set and hides the legs."""
    x, y, f = pose.x, pose.y, pose.facing
    breathe = pose.extras.get("breathe", 0.0)
    y_body = y + breathe * 0.4
    # Torso.
    c.rect(x - 82, y_body - 40, x + 82, y_body + 170, fill=look.top, radius=55)
    if look.hoodie:
        c.line([(x + f * 2 - 12, y_body + 8), (x + f * 2 - 12, y_body + 58)], width=5)
        c.line([(x + f * 2 + 14, y_body + 8), (x + f * 2 + 14, y_body + 50)], width=5)
    hx, hy = x + f * 6 + pose.head_dx, y_body - 115 + breathe + pose.head_dy
    head(c, look, pose, hx, hy)
    _arms(c, look, pose, x, y_body)


def standing(c: Canvas, look: Look, pose: Pose):
    x, y, f = pose.x, pose.y, pose.facing
    bob = pose.extras.get("bob", 0.0)
    # Legs.
    for lx in (x - 30, x + 30):
        c.ellipse(lx - 34 + f * 6, y - 18, lx + 34 + f * 12, y + 10, fill=(90, 84, 80), width=5)
    c.rect(x - 58, y - 230 + bob, x - 4, y - 6, fill=look.bottoms, radius=20)
    c.rect(x + 4, y - 230 + bob, x + 58, y - 6, fill=look.bottoms, radius=20)
    torso_top = y - 490 + bob
    c.rect(x - 80, torso_top, x + 80, y - 200 + bob, fill=look.top, radius=50)
    if look.pajamas:
        for i in range(3):
            c.circle(x + f * 6, torso_top + 60 + i * 60, 6, fill=PAPER, width=3)
        c.line([(x - 40, torso_top + 6), (x + f * 6, torso_top + 50), (x + 40, torso_top + 6)], width=5)
    head(c, look, pose, x + f * 4 + pose.head_dx, torso_top - 70 + pose.head_dy)
    _arms(c, look, pose, x, torso_top + 40, standing=True)


def _arms(c: Canvas, look: Look, pose: Pose, x: float, y: float, standing: bool = False):
    f = pose.facing
    sleeve = 38
    near_sh = (x + f * 58, y + 20)
    far_sh = (x - f * 58, y + 20)

    if pose.hands == "raise_remote":
        a = pose.raise_amt
        elbow = (x + f * 150, y - 10 - 20 * a)
        hand_p = (x + f * (168 - 30 * (1 - a)), y - 110 * a + 40 * (1 - a))
        c.limb([near_sh, elbow, hand_p], look.top, sleeve)
        remote(c, hand_p[0], hand_p[1] - 10)
        hand(c, *hand_p, look, r=30)
    elif pose.hands == "clutch_batteries":
        for bx in (x - 20, x + 18):
            battery(c, bx, y + 80)
        for hx_, sh in ((x - 58, (x - 76, y + 4)), (x + 50, (x + 76, y + 4))):
            c.limb([sh, (sh[0], y + 58), (hx_, y + 62)], look.top, sleeve)
            hand(c, hx_, y + 60, look, r=24)
    elif pose.hands == "mug":
        c.limb([far_sh, (x - f * 70, y + 150)], look.top, sleeve)
        hand(c, x - f * 70, y + 165, look, r=22)
        c.limb([near_sh, (x + f * 70, y + 130), (x + f * 30, y + 110)], look.top, sleeve)
        mug(c, x + f * 30, y + 120)
        hand(c, x + f * 30 + 30, y + 95, look, r=22)
    elif pose.hands == "reach":
        tx, ty = pose.reach
        mid = ((near_sh[0] + tx) / 2, (near_sh[1] + ty) / 2 - 20)
        c.limb([far_sh, (x - f * 70, y + 150)], look.top, sleeve)
        mug(c, x - f * 70, y + 200)
        hand(c, x - f * 70, y + 170, look, r=22)
        c.limb([near_sh, mid, (tx - f * 22, ty)], look.top, sleeve)
        hand(c, tx - f * 22, ty, look, r=22)
        c.line([(tx - f * 22, ty), (tx, ty)], fill=look.skin, width=14)  # pointing finger
    elif pose.hands == "phone":
        for hx_, sh in ((x - 34, (x - 76, y + 4)), (x + 34, (x + 76, y + 4))):
            c.limb([sh, (sh[0], y + 70), (hx_, y + 60)], look.top, sleeve)
        phone(c, x + f * 4, y + 40)
        for hx_ in (x - 34, x + 34):
            hand(c, hx_, y + 64, look, r=22)
    elif pose.hands == "carton":
        # Near hand holds the carton upside down at head height; far hand on the hip.
        # Held up high and shaken, so the empty carton is the first thing you see.
        shake = pose.extras.get("shake", 0.0)
        hand_p = (x + f * 135 + shake, y - 170)
        c.limb([near_sh, (x + f * 150, y - 40), hand_p], look.top, sleeve)
        milk_carton(c, hand_p[0], hand_p[1] - 20, upside_down=True, scale=1.5)
        hand(c, *hand_p, look, r=26)
        drop = pose.extras.get("drop")
        if drop is not None:  # one last drop falling from the spout
            sy = hand_p[1] - 20 + (110 + 34 + 12) * 1.5
            c.ellipse(hand_p[0] - 9, sy + drop, hand_p[0] + 9, sy + 26 + drop, fill=PAPER, width=4)
        c.limb([far_sh, (x - f * 110, y + 110), (x - f * 70, y + 170)], look.top, sleeve)
        hand(c, x - f * 70, y + 170, look, r=22)
    elif pose.hands == "wave_mug":
        wave = pose.extras.get("wave", 0.0)
        hand_p = (x + f * (120 + 20 * wave), y - 90)
        c.limb([near_sh, (x + f * 110, y + 10), hand_p], look.top, sleeve)
        hand(c, *hand_p, look, r=24)
        c.limb([far_sh, (x - f * 70, y + 130), (x - f * 30, y + 110)], look.top, sleeve)
        mug(c, x - f * 30, y + 120)
        hand(c, x - f * 30 - 30, y + 95, look, r=22)
    elif pose.hands == "mug_up":
        # Holding an empty mug up, like the carton in the opening: the loop rhyme.
        hand_p = (x + f * 120, y - 40)
        c.limb([near_sh, (x + f * 130, y + 50), hand_p], look.top, sleeve)
        mug(c, hand_p[0] + f * 4, hand_p[1] - 8)
        hand(c, *hand_p, look, r=24)
        c.limb([far_sh, (x - f * 110, y + 110), (x - f * 70, y + 170)], look.top, sleeve)
        hand(c, x - f * 70, y + 170, look, r=22)
    elif pose.hands == "far_rest":
        # Near arm drawn separately by the shot (e.g. reaching into a fridge in screen space).
        c.limb([far_sh, (x - f * 75, y + 150)], look.top, sleeve)
    elif pose.hands == "shrug":
        for side in (-1, 1):
            sh = (x + side * 58, y + 20)
            hand_p = (x + side * 150, y - 40)
            c.limb([sh, (x + side * 120, y + 70), hand_p], look.top, sleeve)
            hand(c, *hand_p, look, r=22)
        mug(c, x + f * 150, y - 30)
    else:
        for side in (-1, 1):
            c.limb([(x + side * 58, y + 20), (x + side * 75, y + 150)], look.top, sleeve)


def zzz(c: Canvas, x, y, t: float, phase: float = 0.0, bg=(238, 230, 214)):
    """Floating Z's above a sleeper, looping every 1.2 s, fading into the background color."""
    for i in range(3):
        k = ((t + phase) / 1.2 + i / 3) % 1.0
        col = tuple(round(a + (b - a) * k) for a, b in zip(INK, bg))
        c.text(x + k * 60 + i * 6, y - k * 150, "z", 28 + 30 * k, fill=col, weight=8)


def draw(c: Canvas, look: Look, pose: Pose):
    (standing if pose.standing else seated)(c, look, pose)


def blinking(t: float, seed: int) -> bool:
    """Deterministic blink schedule: a 0.12 s blink every ~2.6-4 s, offset per character."""
    period = 2.6 + (seed % 5) * 0.35
    return ((t + seed * 0.77) % period) < 0.12


def jolt(t: float, strength: float = 16.0) -> float:
    """A quick upward jump that settles, for surprise."""
    if t < 0:
        return 0.0
    return -strength * math.exp(-t * 12) * math.cos(t * 30)
