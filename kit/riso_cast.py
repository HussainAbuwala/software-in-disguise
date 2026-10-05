"""The family, in the risograph look (Episode 1's remake): Grandpa, the aunt, Mom, Dad and Priya.

A person is drawn from a head center (cx, cy) and a head half-width R, so the same design works from a close-up to a
wide. Features live in head units (u across, v down; the eyes sit near v = 0). `turn` (-1..1) slides the features
sideways for a three-quarter look; `gaze` moves the pupils; `mouth` (0..1) comes from the dialogue loudness.

Clothes use the riso inks and their overprints: yellow, pink, orange (pink over yellow), light blue (blue dots),
green (blue dots over yellow).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .riso import Sketch, bez, ellipse_pts, mirror, path


@dataclass(frozen=True)
class Person:
    name: str
    hair: str                 # bald_tufts | bun | long | short | ponytail
    jaw: float = 1.0          # 1 = broad jaw; smaller = narrower chin
    crown: float = 1.24       # height of the top of the head above the eyes
    nose: float = 1.0         # nose size
    glasses: bool = False
    moustache: bool = False
    stubble: bool = False
    earrings: bool = False
    age: float = 0.0          # 0..1, how many wrinkles
    hair_grey: float = 0.0    # 0 dark .. 1 white
    garment: str = "tee"      # cardigan | scarf_top | blouse | polo | tee
    shoulders: float = 2.1    # half-width of the shoulders, in head units


GRANDPA = Person("Grandpa", "bald_tufts", jaw=1.0, nose=1.25, glasses=True, moustache=True, age=1.0, hair_grey=1.0,
                 garment="cardigan")
AUNT = Person("Aunt", "bun", jaw=0.9, crown=1.2, nose=0.95, earrings=True, age=0.45, hair_grey=0.15,
              garment="scarf_top", shoulders=2.2)
MOM = Person("Mom", "long", jaw=0.84, crown=1.18, nose=0.85, earrings=True, age=0.3, garment="blouse",
             shoulders=1.95)
DAD = Person("Dad", "short", jaw=1.02, crown=1.2, nose=1.05, stubble=True, age=0.35, hair_grey=0.35, garment="polo",
             shoulders=2.3)
PRIYA = Person("Priya", "ponytail", jaw=0.8, crown=1.16, nose=0.8, earrings=True, garment="tee", shoulders=1.85)

FAMILY = {p.name.upper(): p for p in (GRANDPA, AUNT, MOM, DAD, PRIYA)}

# Expression: brow lift per side (head units, negative = up), brow tilt (inner end up = worried), upper lid
# (0 wide .. 1 shut), smile (curve of a closed mouth), and the mouth shape when not talking.
EXPRESSIONS = {
    "neutral": dict(brow=(-0.0, -0.0), tilt=0.0, lid=0.25, mouth="smile", smile=0.25),
    "confused": dict(brow=(-0.14, -0.04), tilt=0.06, lid=0.0, mouth="o", smile=0.0),
    "surprised": dict(brow=(-0.16, -0.16), tilt=0.0, lid=0.0, mouth="o_big", smile=0.0),
    "beaming": dict(brow=(-0.12, -0.12), tilt=-0.04, lid=1.0, mouth="grin", smile=1.0),
    "gasp": dict(brow=(-0.2, -0.2), tilt=0.08, lid=0.0, mouth="gasp", smile=0.0),
    "flat": dict(brow=(0.04, 0.04), tilt=-0.02, lid=0.55, mouth="flat", smile=0.0),
    "happy": dict(brow=(-0.08, -0.08), tilt=0.0, lid=0.35, mouth="smile", smile=0.8),
    "excited": dict(brow=(-0.14, -0.14), tilt=0.02, lid=0.1, mouth="grin", smile=1.0),
    "asleep": dict(brow=(0.02, 0.02), tilt=0.0, lid=1.0, mouth="o_small", smile=0.0),
    "delighted": dict(brow=(-0.18, -0.18), tilt=0.0, lid=0.0, mouth="o_big", smile=0.6),
}


class Frame:
    """Head-unit to screen mapping for one person."""

    def __init__(self, cx, cy, R, turn=0.0):
        self.cx, self.cy, self.R, self.turn = cx, cy, R, turn

    def __call__(self, u, v, feature=True):
        shift = self.turn * 0.2 * self.R if feature else 0.0
        return (self.cx + u * self.R + shift, self.cy + v * self.R)

    def pts(self, uvs, feature=True):
        return [self(u, v, feature) for u, v in uvs]


def _head_outline(p: Person):
    T, J = p.crown, p.jaw
    chin = 1.36 if J >= 0.95 else 1.3
    left = path((0, -T), ((-0.62, -T), (-1.0, -0.69 * T), (-1.0, -0.19 * T)),
                ((-1.01, 0.5), (-0.8 * J, 1.08), (-0.36 * J, chin - 0.08)),
                ((-0.18 * J, chin - 0.01), (-0.07 * J, chin), (0, chin)), n=20)
    return left + mirror(left, 0)[::-1]


def person(sk: Sketch, p: Person, cx, cy, R, expr="neutral", mouth=0.0, gaze=(0.0, 0.0), turn=0.0, blink=False,
           bottom=1940.0):
    """A whole bust in the right order: hair behind, then the body, then the head."""
    back_hair(sk, p, cx, cy, R)
    torso(sk, p, cx, cy, R, bottom=bottom)
    head(sk, p, cx, cy, R, expr, mouth, gaze, turn, blink)


def back_hair(sk: Sketch, p: Person, cx, cy, R):
    f = Frame(cx, cy, R, 0)
    lw = max(2.4, R * 0.026)
    if p.hair == "long":  # falls behind the shoulders, narrower than the shoulders
        back = f.pts(path((0, -1.3), ((-0.9, -1.3), (-1.28, -0.6), (-1.3, 0.2)), ((-1.32, 1.2), (-1.32, 1.8), (-1.28, 2.3)),
                          ((-0.6, 2.45), (0.6, 2.45), (1.28, 2.3)), ((1.32, 1.8), (1.32, 1.2), (1.3, 0.2)),
                          ((1.28, -0.6), (0.9, -1.3), (0, -1.3)), n=16),
                     feature=False)
        _hair_fill(sk, back, p, lw)
    if p.hair == "ponytail":  # gathered at the back, hanging past the right shoulder
        tail = f.pts(path((0.55, -1.05), ((1.3, -1.15), (1.55, -0.3), (1.42, 0.6)),
                          ((1.38, 1.3), (1.25, 1.95), (0.98, 2.15)), ((0.88, 1.4), (1.0, 0.6), (0.82, -0.2)), n=14),
                     feature=False)
        _hair_fill(sk, tail, p, lw)
        sk.stroke(f.pts(bez((1.2, -0.6), (1.35, 0.2), (1.3, 1.0), (1.12, 1.7), 10), False), width=lw * 0.5,
                  ink="fill2")
    if p.hair == "bun":
        bun = f.pts(ellipse_pts(0.05, -1.42, 0.5, 0.42, 30), feature=False)
        _hair_fill(sk, bun, p, lw)


def head(sk: Sketch, p: Person, cx, cy, R, expr="neutral", mouth=0.0, gaze=(0.0, 0.0), turn=0.0, blink=False):
    f = Frame(cx, cy, R, turn)
    e = EXPRESSIONS[expr]
    lw = max(2.4, R * 0.026)
    outline = f.pts(_head_outline(p), feature=False)
    shade = lambda x, y: ((x - cx) / R * 0.42 + (y - cy) / R * 0.12 - 0.08)

    # -- Ears
    if p.hair not in ("long",):
        for side in (-1, 1):
            if turn * side < -0.5:
                continue
            ear = f.pts(path((side * 0.98, -0.19), ((side * 1.28, -0.33), (side * 1.33, 0.19), (side * 1.21, 0.4)),
                             ((side * 1.12, 0.6), (side * 0.98, 0.55), (side * 0.95, 0.43)), n=12), feature=False)
            sk.shape(ear + [f(side * 0.95, -0.15, False)], "skin", lw)
            sk.stroke(f.pts(bez((side * 1.06, -0.07), (side * 1.2, -0.05), (side * 1.19, 0.28), (side * 1.08, 0.35),
                                10), False), width=lw * 0.6)
            if p.earrings:
                ex, ey = f(side * 1.1, 0.68, False)
                sk.occlude(ellipse_pts(ex, ey, R * 0.07, R * 0.09))
                sk.solid(ellipse_pts(ex, ey, R * 0.07, R * 0.09), "fill2")
                sk.circle(ex, ey, R * 0.07, ry=R * 0.09, width=lw * 0.7)

    # -- Face
    sk.occlude(outline)
    sk.solid(outline, "skin")
    sk.halftone(outline, "accent", cell=max(7, R * 0.05), shade=shade)
    sk.stroke(outline + [outline[0]], width=lw * 1.15)
    if p.stubble:
        jaw = f.pts(path((-0.95, 0.35), ((-0.9, 0.95), (-0.4, 1.3), (0, 1.3)), n=12) +
                    path((0, 1.3), ((0.4, 1.3), (0.9, 0.95), (0.95, 0.35)), n=12)[1:] +
                    [(0.6, 0.62), (0, 0.78), (-0.6, 0.62)], feature=False)
        sk.halftone(jaw, "line", cell=max(6, R * 0.04), angle=45, shade=lambda x, y: 0.16)
    if p.hair == "bald_tufts":
        sk.erase([(x + (y - cy) * 0.6, y) for x, y in ellipse_pts(*f(-0.4, -0.95, False), R * 0.25, R * 0.1, 18)],
                 ["skin", "accent"])
    # Wrinkles
    if p.age > 0.6:
        for k, v in enumerate((-0.76, -0.63, -0.5)):
            sk.stroke(f.pts(bez((-0.37 + 0.03 * k, v + 0.03), (-0.19, v - 0.04), (0.19, v - 0.04),
                                (0.37 - 0.03 * k, v + 0.03), 12)), width=lw * 0.55)
    if p.age > 0.25:
        for side in (-1, 1):  # smile lines
            sk.stroke(f.pts(bez((side * 0.25, 0.62), (side * 0.34, 0.68), (side * 0.38, 0.78), (side * 0.37, 0.88), 8)),
                      width=lw * 0.5)

    # -- Eyes
    lid = 1.0 if blink else e["lid"]
    for side in (-1, 1):
        ex, ey = f(side * 0.467, 0.01)
        rx, ry = R * 0.16, R * 0.115
        if lid >= 0.95:
            if e["mouth"] == "grin" or expr == "beaming":  # happy closed eyes: arcs up
                sk.stroke(ellipse_pts(ex, ey + ry * 0.4, rx * 0.95, ry * 1.1, 14, math.pi * 1.1, math.pi * 1.9),
                          width=lw * 0.95)
            else:
                sk.stroke(ellipse_pts(ex, ey - ry * 0.2, rx * 0.95, ry * 0.8, 14, math.pi * 0.1, math.pi * 0.9),
                          width=lw * 0.95)
            continue
        white = ellipse_pts(ex, ey, rx, ry, 28)
        sk.occlude(white)
        px = ex + gaze[0] * rx * 0.45
        py = ey + gaze[1] * ry * 0.4
        sk.dot(px, py, R * 0.062)
        sk.erase(ellipse_pts(px - R * 0.022, py - R * 0.022, R * 0.02, R * 0.02, 10), ["line"])
        top = ey - ry * (1.25 - lid * 1.4)
        sk.stroke([(ex - rx * 1.1, ey - ry * 0.05)] + bez((ex - rx * 1.1, ey), (ex - rx * 0.6, top), (ex + rx * 0.6, top),
                                                          (ex + rx * 1.1, ey), 14)[1:], width=lw * 1.0)
        if lid > 0.2:  # the lid covers the top of the eye
            cover = bez((ex - rx * 1.1, ey), (ex - rx * 0.6, top), (ex + rx * 0.6, top), (ex + rx * 1.1, ey), 14)
            cover = cover + [(ex + rx * 1.2, ey - ry * 2), (ex - rx * 1.2, ey - ry * 2)]
            sk.occlude(cover)
            sk.solid(cover, "skin", offset=False)
        sk.stroke(white[3:12], width=lw * 0.55)  # lower lid
        if p.age > 0.4:
            sk.stroke(bez((ex - rx * 0.9, ey + ry * 1.5), (ex - rx * 0.3, ey + ry * 1.95), (ex + rx * 0.3, ey + ry * 1.95),
                          (ex + rx * 0.9, ey + ry * 1.45), 10), width=lw * 0.45)

    # -- Brows
    for i, side in enumerate((-1, 1)):
        lift = e["brow"][i]
        tilt = e["tilt"]
        inner, outer = (side * 0.2, -0.36 + lift - tilt), (side * 0.72, -0.36 + lift + tilt * 0.5)
        thick = 0.075 if p.name in ("Grandpa", "Dad") else 0.05
        brow = f.pts(path(inner, ((side * 0.38, inner[1] - 0.1), (side * 0.6, outer[1] - 0.1), outer),
                          ((side * 0.55, outer[1] + thick), (side * 0.35, inner[1] + thick * 0.7),
                           (inner[0], inner[1] + thick)), n=10))
        sk.occlude(brow)
        sk.solid(brow, "line", offset=False)
        if p.name == "Grandpa":
            for k in range(6):
                t = k / 5
                x, y = f(inner[0] + (outer[0] - inner[0]) * t, inner[1] + (outer[1] - inner[1]) * t - 0.05)
                sk.stroke([(x, y + R * 0.03), (x + side * R * 0.05, y - R * 0.05)], width=lw * 0.6, wobble=0.5)

    # -- Glasses
    if p.glasses:
        for side in (-1, 1):
            ex, ey = f(side * 0.467, 0.01)
            lens = _rrect(ex - R * 0.35, ey - R * 0.3, ex + R * 0.35, ey + R * 0.31, R * 0.22)
            sk.stroke(lens + [lens[0]], width=lw * 1.05)
            glare = [(ex + R * 0.1, ey - R * 0.27), (ex + R * 0.19, ey - R * 0.27), (ex + R * 0.31, ey - R * 0.08),
                     (ex + R * 0.24, ey - R * 0.06)]
            sk.erase(glare, ["skin", "accent"])
            sk.stroke([f(side * 0.82, -0.1), f(side * 0.98, -0.14, False)], width=lw * 0.9)
        sk.stroke(f.pts(bez((-0.12, -0.04), (-0.06, -0.12), (0.06, -0.12), (0.12, -0.04), 8)), width=lw)

    # -- Nose
    n = p.nose
    nose = f.pts(path((-0.06 * n, 0.1), ((-0.1 * n, 0.3), (-0.2 * n, 0.45), (-0.23 * n, 0.55)),
                      ((-0.28 * n, 0.72), (-0.08 * n, 0.78), (0, 0.75)),
                      ((0.1 * n, 0.8), (0.28 * n, 0.72), (0.22 * n, 0.56)), n=14))
    sk.occlude(nose + [f(0.06 * n, 0.1)])
    sk.solid(nose + [f(0.06 * n, 0.1)], "skin", offset=False)
    sk.halftone(nose + [f(0.06 * n, 0.1)], "accent", cell=max(7, R * 0.05), shade=shade)
    if p.name == "Grandpa":
        tip = f(0.02, 0.63)
        sk.halftone(ellipse_pts(*tip, R * 0.19, R * 0.12, 18), "accent", cell=max(6, R * 0.04), angle=45,
                    shade=lambda x, y: 0.55)
    sk.stroke(nose[14:], width=lw * 1.0)
    for side in (-1, 1):
        sk.stroke(f.pts(bez((side * 0.04, 0.72), (side * 0.08, 0.68), (side * 0.13, 0.69), (side * 0.16, 0.73), 6)),
                  width=lw * 0.6)

    # -- Mouth, and blush when happy
    _mouth(sk, f, e, mouth, R, lw, p)
    if e["smile"] >= 0.8:
        for side in (-1, 1):
            sk.halftone(ellipse_pts(*f(side * 0.6, 0.5), R * 0.17, R * 0.1, 18), "accent", cell=max(6, R * 0.04),
                        angle=45, shade=lambda x, y: 0.7)

    # -- Moustache
    if p.moustache:
        ml = path((0, 0.81), ((-0.17, 0.75), (-0.43, 0.74), (-0.55, 0.93)), ((-0.48, 0.96), (-0.33, 0.96), (-0.21, 0.93)),
                  ((-0.12, 0.91), (-0.05, 0.91), (0, 0.95)), n=12)
        for side in (-1, 1):
            ms = f.pts(ml if side < 0 else mirror(ml, 0))
            sk.occlude(ms)
            sk.stroke(ms, width=lw * 0.85)
            for k in range(6):
                x, y = f(side * (0.09 + k * 0.08), 0.84 + k * 0.007)
                sk.stroke([(x, y), (x + side * R * 0.03, y + R * 0.06)], width=lw * 0.4, wobble=0.4)

    # -- Hair in front
    _front_hair(sk, f, p, lw, R)


def _rrect(x0, y0, x1, y1, r):
    from .riso import round_rect_pts
    return round_rect_pts(x0, y0, x1, y1, r, 6)


def _hair_fill(sk: Sketch, pts, p: Person, lw):
    sk.occlude(pts)
    if p.hair_grey >= 0.9:
        sk.stroke(pts + [pts[0]], width=lw)
        return
    sk.solid(pts, "line", offset=False)


def _front_hair(sk: Sketch, f: Frame, p: Person, lw, R):
    if p.hair == "bald_tufts":
        for side in (-1, 1):
            tuft = f.pts(path((side * 0.93, -0.76), ((side * 1.25, -0.81), (side * 1.28, -0.52), (side * 1.12, -0.43)),
                              ((side * 1.33, -0.36), (side * 1.25, -0.07), (side * 1.06, -0.1)),
                              ((side * 1.2, 0.04), (side * 1.08, 0.19), (side * 0.98, 0.1)), n=12), feature=False)
            sk.occlude(tuft + [f(side * 0.98, -0.48, False)])
            sk.stroke(tuft, width=lw * 0.95)
        return
    T = p.crown
    # A cap of hair over the crown, with a parting; the hairline dips to the temples.
    cap = path((-1.04, 0.05), ((-1.12, -0.7), (-0.75, -T - 0.1), (0, -T - 0.08)),
               ((0.75, -T - 0.1), (1.12, -0.7), (1.04, 0.05)), n=18)
    if p.hair == "short":
        hairline = path((1.0, -0.3), ((0.85, -0.62), (0.45, -0.72), (0.1, -0.76)),
                        ((-0.3, -0.8), (-0.8, -0.66), (-1.0, -0.3)), n=14)
        cap = path((-1.02, -0.2), ((-1.1, -0.9), (-0.7, -T - 0.14), (0, -T - 0.12)),
                   ((0.7, -T - 0.14), (1.1, -0.9), (1.02, -0.2)), n=18)
    else:
        hairline = path((1.04, 0.05), ((0.98, -0.45), (0.6, -0.78), (0.12, -0.8)),
                        ((0.05, -0.66), (-0.35, -0.62), (-0.7, -0.68)),
                        ((-0.92, -0.45), (-1.0, -0.2), (-1.04, 0.05)), n=12)
    shape = f.pts(cap + hairline[1:], feature=False)
    _hair_fill(sk, shape, p, lw)
    sk.stroke(shape + [shape[0]], width=lw)
    # Sheen: a pale curved stripe across the dark hair
    if p.hair_grey < 0.9:
        sheen = f.pts(path((-0.62, -0.98), ((-0.4, -1.16), (-0.05, -1.22), (0.25, -1.16)), n=10) +
                      path((0.22, -1.12), ((-0.05, -1.17), (-0.4, -1.11), (-0.6, -0.95)), n=10), feature=False)
        sk.erase(sheen, ["line"])


def _mouth(sk: Sketch, f: Frame, e, m, R, lw, p: Person):
    mx, my = f(0, 1.0 if p.moustache else 0.97)
    shape = e["mouth"]
    if m > 0.08:  # talking: an open mouth sized by loudness, keeping the expression's corners
        w = R * (0.2 + 0.08 * e["smile"])
        h = R * (0.05 + 0.2 * m)
        pts = ellipse_pts(mx, my + h * 0.3, w, h, 24)
        if e["smile"] > 0.5:
            pts = [(x, max(y, my - h * 0.1)) for x, y in pts]
        sk.occlude(pts)
        sk.solid(pts, "line", offset=False)
        sk.halftone(ellipse_pts(mx, my + h * 0.7, w * 0.6, h * 0.4, 16), "accent", cell=max(5, R * 0.03),
                    shade=lambda x, y: 0.9)
        return
    if shape in ("o", "o_small", "o_big", "gasp"):
        rx = R * {"o": 0.09, "o_small": 0.06, "o_big": 0.14, "gasp": 0.17}[shape]
        ry = rx * (1.2 if shape != "gasp" else 1.35)
        pts = ellipse_pts(mx, my + ry * 0.4, rx, ry, 22)
        sk.occlude(pts)
        sk.solid(pts, "line", offset=False)
        sk.halftone(ellipse_pts(mx, my + ry, rx * 0.6, ry * 0.4, 14), "accent", cell=max(5, R * 0.03),
                    shade=lambda x, y: 0.85)
    elif shape == "grin":
        w = R * 0.34
        pts = bez((mx - w, my - R * 0.04), (mx - w * 0.6, my + R * 0.3), (mx + w * 0.6, my + R * 0.3), (mx + w, my - R * 0.04), 18)
        sk.occlude(pts)
        sk.solid(pts, "line", offset=False)
        sk.erase([(mx - w * 0.8, my - R * 0.02), (mx + w * 0.8, my - R * 0.02), (mx + w * 0.7, my + R * 0.06),
                  (mx - w * 0.7, my + R * 0.06)], ["line"])  # teeth
        sk.halftone(ellipse_pts(mx, my + R * 0.17, w * 0.45, R * 0.06, 14), "accent", cell=max(5, R * 0.03),
                    shade=lambda x, y: 0.9)
        sk.stroke(pts, width=lw)
    elif shape == "flat":
        sk.stroke([(mx - R * 0.17, my + R * 0.04), (mx + R * 0.17, my + R * 0.03)], width=lw)
    else:  # closed smile
        s = e["smile"]
        sk.stroke(bez((mx - R * 0.2, my), (mx - R * 0.08, my + R * 0.1 * s), (mx + R * 0.08, my + R * 0.1 * s),
                      (mx + R * 0.2, my), 12), width=lw)


# ----------------------------------------------------------------------------------------------------------------
# Bodies


def torso(sk: Sketch, p: Person, cx, cy, R, bottom=1940.0, turn=0.0):
    """Neck, shoulders and clothes, from a head drawn at (cx, cy, R); call before `head`."""
    f = Frame(cx, cy, R, 0)
    sw = p.shoulders
    neck = f.pts([(-0.34, 0.95), (0.34, 0.95), (0.37, 1.72), (-0.37, 1.72)])
    sk.shape(neck, "skin", R * 0.024)
    sk.halftone(neck, "accent", cell=max(7, R * 0.05), shade=lambda x, y: 0.45 - (y - f(0, 0.95)[1]) / (R * 1.6))
    left = path((0, 1.68), ((-0.6, 1.7), (-1.2, 1.82), (-sw * 0.8, 2.15)),
                ((-sw * 1.02, 2.5), (-sw * 1.06, 3.4), (-sw * 1.1, 4.5)), n=18)
    body = f.pts(left, False) + [(f(-sw * 1.1, 0, False)[0], bottom), (f(sw * 1.1, 0, False)[0], bottom)] + \
        f.pts(mirror(left, 0), False)[::-1]
    body = [(x, min(y, bottom)) for x, y in body]
    lw = R * 0.026
    shade = lambda x, y: ((x - cx) / R * 0.25 - 0.1)
    g = p.garment
    main = {"cardigan": "fill2", "scarf_top": "fill", "blouse": None, "polo": "fill2", "tee": "fill"}[g]
    sk.occlude(body)
    if main:
        sk.solid(body, main)
    if g == "blouse":  # light blue: blue dots
        sk.halftone(body, "line", cell=max(7, R * 0.045), angle=15, shade=lambda x, y: 0.2)
    if g == "polo":  # green: blue dots over yellow
        sk.halftone(body, "line", cell=max(7, R * 0.045), angle=15, shade=lambda x, y: 0.28)
    if g == "tee":  # orange: yellow dots over pink
        sk.halftone(body, "fill2", cell=max(7, R * 0.045), angle=75, shade=lambda x, y: 0.75)
    sk.halftone(body, "accent", cell=max(8, R * 0.055), shade=shade)
    clip = lambda pts: [(x, y) for x, y in pts if y <= bottom]
    sk.stroke(clip(f.pts(left, False)), width=lw * 1.1)
    sk.stroke(clip(f.pts(mirror(left, 0), False)), width=lw * 1.1)
    if g == "cardigan":
        shirt = f.pts([(-0.4, 1.6), (0.4, 1.6), (0.28, 2.75), (0, 3.2), (-0.28, 2.75)])
        sk.shape(shirt, "fill", lw)
        for side in (-1, 1):
            sk.shape(f.pts([(0, 1.85), (side * 0.45, 1.62), (side * 0.33, 2.15)]), "fill", lw * 0.8)
        sk.stroke([f(0, 3.2), (f(0, 0)[0], bottom)], width=lw)
        for v in (3.6, 4.15, 4.7):
            if f(0, v)[1] < bottom - 10:
                bx, by = f(0.13, v)
                sk.occlude(ellipse_pts(bx, by, R * 0.06, R * 0.06))
                sk.circle(bx, by, R * 0.06, width=lw * 0.7)
    elif g == "scarf_top":  # a yellow scarf over one shoulder, with pink dots
        scarf = f.pts(path((-0.5, 1.65), ((-1.2, 1.75), (-1.6, 2.2), (-1.7, 4.6)), n=14) + [(-0.9, 4.6)] +
                      path((-0.9, 4.6), ((-0.7, 3.2), (-0.2, 2.2), (0.55, 1.75)), n=14)[1:], False)
        scarf = [(x, min(y, bottom)) for x, y in scarf]
        sk.shape(scarf, "fill2", lw)
        sk.halftone(scarf, "accent", cell=max(9, R * 0.07), angle=45, shade=lambda x, y: 0.35)
        sk.stroke(f.pts(bez((-0.6, 1.9), (-1.0, 2.4), (-1.25, 3.2), (-1.3, 4.3), 12), False), width=lw * 0.6)
        sk.stroke(f.pts(bez((-0.42, 1.68), (0, 1.95), (0.3, 1.9), (0.5, 1.7), 10), False), width=lw)
    elif g == "blouse":
        sk.stroke(f.pts(bez((-0.45, 1.68), (-0.2, 2.25), (0.2, 2.25), (0.45, 1.68), 12), False), width=lw)
        for v in (2.6, 3.1, 3.6):
            if f(0, v)[1] < bottom - 10:
                bx, by = f(0, v, False)
                sk.circle(bx, by, R * 0.045, width=lw * 0.6)
    elif g == "polo":
        for side in (-1, 1):
            sk.shape(f.pts([(0, 1.95), (side * 0.5, 1.62), (side * 0.62, 1.95), (side * 0.15, 2.15)], False), "fill2",
                     lw * 0.9)
        sk.stroke([f(0, 2.0, False), f(0, 2.75, False)], width=lw * 0.8)
        for v in (2.25, 2.55):
            bx, by = f(0.07, v, False)
            sk.circle(bx, by, R * 0.04, width=lw * 0.5)
    elif g == "tee":
        sk.stroke(f.pts(bez((-0.42, 1.66), (-0.2, 1.98), (0.2, 1.98), (0.42, 1.66), 12), False), width=lw)
    return body


def sleeve(sk: Sketch, pts, thick, ink="fill2", line_w=4.5):
    """An arm as a filled band between two outlines, along a path from the shoulder to the wrist."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        j0, j1 = max(i - 1, 0), min(i + 1, len(pts) - 1)
        tx, ty = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n * thick / 2, tx / n * thick / 2
        left.append((x + nx, y + ny))
        right.append((x - nx, y - ny))
    band = left + right[::-1]
    sk.occlude(band)
    sk.solid(band, ink)
    sk.stroke(left, width=line_w)
    sk.stroke(right, width=line_w)
    return band


def hand(sk: Sketch, x, y, s, kind="fist", angle=0.0, line_w=4.0):
    """A simple hand at (x, y), size s (about a palm width): fist | open | phone."""
    rot = lambda pts: [(x + (u * math.cos(angle) - v * math.sin(angle)) * s,
                        y + (u * math.sin(angle) + v * math.cos(angle)) * s) for u, v in pts]
    if kind == "open":
        palm = rot(path((-0.5, 0.5), ((-0.6, 0.0), (-0.55, -0.4), (-0.45, -0.5)), ((-0.42, -1.1), (-0.25, -1.15), (-0.2, -0.55)),
                        ((-0.18, -1.3), (0.02, -1.3), (0.03, -0.6)), ((0.08, -1.25), (0.28, -1.2), (0.25, -0.55)),
                        ((0.35, -1.0), (0.52, -0.9), (0.45, -0.4)), ((0.75, -0.55), (0.85, -0.35), (0.5, 0.0)),
                        ((0.45, 0.3), (0.3, 0.55), (-0.5, 0.5)), n=8))
    else:
        palm = rot(path((-0.5, 0.45), ((-0.65, 0.0), (-0.55, -0.55), (-0.1, -0.6)), ((0.35, -0.65), (0.6, -0.4), (0.55, 0.0)),
                        ((0.55, 0.4), (0.3, 0.55), (-0.5, 0.45)), n=10))
    sk.occlude(palm)
    sk.solid(palm, "skin", offset=False)
    sk.halftone(palm, "accent", cell=8, shade=lambda a, b: 0.25)
    sk.stroke(palm + [palm[0]], width=line_w)
    if kind == "fist":
        for k in range(3):
            v = -0.3 + k * 0.25
            sk.stroke(rot([(0.05, v), (0.3, v + 0.03), (0.52, v)]), width=line_w * 0.6)
    if kind == "phone":
        ph = rot([(-0.15, -1.35), (0.35, -1.3), (0.38, 0.2), (-0.12, 0.15)])
        sk.occlude(ph)
        sk.solid(ph, "line", offset=False)
        sk.stroke(ph + [ph[0]], width=line_w)
        sk.stroke(rot(path((-0.5, 0.3), ((-0.65, -0.2), (-0.4, -0.5), (-0.1, -0.45)), n=8)), width=line_w)
    return palm
