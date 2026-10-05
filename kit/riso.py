"""Risograph-zine drawing for code-drawn episodes (from Episode 1's remake, 2026-10-04).

Everything is drawn "by hand": strokes wobble along their length and overshoot their ends, circles overshoot where
they close, fills print slightly off the lines (a second riso drum never lines up), shading is halftone dots, and
the paper has grain. Inks overprint (multiply), so pink over yellow makes orange, as on a real riso.

Each ink is a coverage mask; `Sketch.occlude` erases everything behind a foreground shape before it is drawn, and
`composite` prints the masks onto paper. A Sketch is seeded per drawing; animating with a new seed every other frame
("on twos") makes the lines boil like hand-drawn animation.
"""

from __future__ import annotations

import math
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
SS = 2

PAPER = (246, 239, 224)
INKS = {
    "line": (24, 66, 156),      # riso blue: line art, text, deep shadow
    "accent": (255, 72, 140),   # fluorescent pink: shading dots, accents
    "fill": (255, 96, 160),     # pink fill
    "fill2": (255, 214, 40),    # yellow fill
    "skin": (240, 172, 128),    # skin, medium
    "skin2": (214, 144, 100),   # skin, deeper
    "label": (24, 66, 156),
    "good": (24, 66, 156),
}
PRINT_ORDER = ["skin", "skin2", "fill2", "fill", "accent", "line", "label", "good"]

# Looks the same drawing code can print in (2026-10-05 style comparison). "riso" is the default.
LOOKS = {
    "riso": dict(paper=PAPER, inks=INKS, grain=True, offset=(6, -4), wobble=1.0, width=1.0, shading="dots"),
    # Clean ink line and flat colour with two-tone (cel) shading, like a newspaper or New Yorker cartoon.
    "clean": dict(paper=(251, 249, 245), grain=False, offset=(0, 0), wobble=0.12, width=0.75, shading="cel",
                  inks={"line": (34, 30, 32), "accent": (196, 96, 84), "fill": (226, 112, 96), "fill2": (240, 192, 88),
                        "skin": (222, 166, 124), "skin2": (192, 132, 92), "label": (34, 30, 32), "good": (34, 30, 32)}),
    # Bold comic: heavy black ink, Ben-Day dots for shading, bright primaries.
    "comic": dict(paper=(253, 251, 244), grain=False, offset=(0, 0), wobble=0.35, width=1.7, shading="dots",
                  dot_scale=1.5, inks={"line": (12, 12, 14), "accent": (196, 84, 62), "fill": (230, 52, 48),
                                       "fill2": (252, 210, 34), "skin": (226, 168, 124), "skin2": (198, 138, 96), "label": (12, 12, 14),
                                       "good": (12, 12, 14)}),
}
LOOK = dict(LOOKS["riso"])


def use(name: str):
    """Switch every drawing that follows to another look."""
    LOOK.clear()
    LOOK.update(LOOKS[name])

SUPP = "/System/Library/Fonts/Supplemental/"
FONTS = {
    "hand": ("/System/Library/Fonts/Noteworthy.ttc", 1),
    "mono": ("/Library/Fonts/IBM-Plex-Mono/IBMPlexMono-Bold.otf", 0),
    "bradley": (SUPP + "Bradley Hand Bold.ttf", 0),
}
_font_cache: dict = {}


def font(name: str, size: float) -> ImageFont.FreeTypeFont:
    key = (name, round(size * SS))
    if key not in _font_cache:
        path, index = FONTS[name]
        _font_cache[key] = ImageFont.truetype(path, key[1], index=index)
    return _font_cache[key]


# ----------------------------------------------------------------------------------------------------------------
# Geometry helpers


def bez(p0, p1, p2, p3, n=28):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def path(start, *segs, n=28):
    """A chain of cubic segments: path(p0, (c1, c2, p1), (c1, c2, p2), ...)."""
    pts, cur = [start], start
    for c1, c2, p in segs:
        pts += bez(cur, c1, c2, p, n)[1:]
        cur = p
    return pts


def mirror(pts, cx):
    return [(2 * cx - x, y) for x, y in pts]


def ellipse_pts(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(a0, a1, n)]


def round_rect_pts(x0, y0, x1, y1, r, n=8):
    pts = []
    for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            t = math.radians(a + 90 * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def _resample(pts, step):
    out = [pts[0]]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        d = math.hypot(xb - xa, yb - ya)
        n = max(1, int(d / step))
        for i in range(1, n + 1):
            out.append((xa + (xb - xa) * i / n, ya + (yb - ya) * i / n))
    return out


def mask_of(pts) -> Image.Image:
    m = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in pts], fill=255)
    return m


# ----------------------------------------------------------------------------------------------------------------
# The sketch


class Sketch:
    def __init__(self, seed: int = 7, wobble: float = 1.6, width: float = 5.5):
        self.rng = random.Random(seed)
        self.wobble = wobble * LOOK["wobble"]
        self.width = width
        self.layers: dict[str, Image.Image] = {}

    def layer(self, ink: str) -> Image.Image:
        if ink not in self.layers:
            self.layers[ink] = Image.new("L", (W * SS, H * SS), 0)
        return self.layers[ink]

    def occlude(self, pts):
        poly = [(x * SS, y * SS) for x, y in pts]
        for im in self.layers.values():
            ImageDraw.Draw(im).polygon(poly, fill=0)

    def erase(self, pts, inks=None):
        """Remove ink inside a shape (highlights, glare): the paper shows through."""
        m = mask_of(pts)
        for ink in inks or list(self.layers):
            if ink in self.layers:
                self.layers[ink] = ImageChops.subtract(self.layers[ink], m)

    def _wobble_fn(self, amp):
        r = self.rng
        f = [r.uniform(0.5, 0.9), r.uniform(1.6, 2.4), r.uniform(4.0, 6.0)]
        p = [r.uniform(0, 6.28) for _ in f]
        return lambda s: amp * (math.sin(f[0] * s + p[0]) + 0.5 * math.sin(f[1] * s + p[1])
                                + 0.22 * math.sin(f[2] * s + p[2])) / 1.72

    def stroke(self, pts, ink="line", width=None, wobble=None, double=0.0, overshoot=4.0):
        width = (width or self.width) * LOOK["width"]
        wobble = self.wobble if wobble is None else wobble * LOOK["wobble"]
        self._stroke_once(pts, ink, width, wobble, overshoot)
        if double and self.rng.random() < double:
            self._stroke_once(pts, ink, width * 0.55, wobble * 1.6, overshoot * 1.5)

    def _stroke_once(self, pts, ink, width, wobble, overshoot):
        pts = _resample(pts, 5.0)
        if len(pts) < 2:
            return
        (x0, y0), (x1, y1) = pts[0], pts[1]
        d = math.hypot(x1 - x0, y1 - y0) or 1
        pts.insert(0, (x0 - (x1 - x0) / d * overshoot, y0 - (y1 - y0) / d * overshoot))
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        d = math.hypot(x1 - x0, y1 - y0) or 1
        pts.append((x1 + (x1 - x0) / d * overshoot, y1 + (y1 - y0) / d * overshoot))
        off = self._wobble_fn(wobble)
        wv = self._wobble_fn(0.18)
        out, s = [], 0.0
        for i, (x, y) in enumerate(pts):
            j0, j1 = max(i - 1, 0), min(i + 1, len(pts) - 1)
            tx, ty = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
            n = math.hypot(tx, ty) or 1
            if i:
                s += math.hypot(x - pts[i - 1][0], y - pts[i - 1][1]) / 60
            o = off(s)
            out.append((x - ty / n * o, y + tx / n * o, width * (1 + wv(s))))
        dr = ImageDraw.Draw(self.layer(ink))
        for (xa, ya, wa), (xb, yb, wb) in zip(out, out[1:]):
            w = (wa + wb) / 2 * SS
            dr.line([(xa * SS, ya * SS), (xb * SS, yb * SS)], fill=255, width=max(1, round(w)))
            r = w / 2
            dr.ellipse([xb * SS - r, yb * SS - r, xb * SS + r, yb * SS + r], fill=255)

    def circle(self, cx, cy, r, ink="line", width=None, ry=None, over=0.35):
        ry = ry or r
        a0 = self.rng.uniform(0, 6.28)
        n = max(24, int(r * 0.5))
        pts = [(cx + r * math.cos(a0 + t), cy + ry * math.sin(a0 + t)) for t in np.linspace(0, 2 * math.pi + over, n)]
        self.stroke(pts, ink, width, overshoot=0)

    def dot(self, cx, cy, r, ink="line"):
        dr = ImageDraw.Draw(self.layer(ink))
        jx, jy = self.rng.uniform(0.88, 1.08), self.rng.uniform(0.88, 1.08)
        dr.ellipse([(cx - r * jx) * SS, (cy - r * jy) * SS, (cx + r * jx) * SS, (cy + r * jy) * SS], fill=255)

    def solid(self, pts, ink, offset=True):
        """A flat riso fill, printed slightly off the line art."""
        m = mask_of(pts)
        dx, dy = LOOK["offset"]
        if offset and (dx or dy):
            m = ImageChops.offset(m, dx * SS, dy * SS)
        self.layers[ink] = ImageChops.lighter(self.layer(ink), m)

    def halftone(self, pts, ink="accent", cell=11.0, angle=22.0, shade=lambda x, y: 0.5, max_r=0.62):
        """Riso halftone: a rotated dot grid inside the shape, each dot sized by shade (0 light .. 1 dark)."""
        if LOOK["shading"] == "cel":
            return self._cel(pts, ink, shade)
        cell = cell * LOOK.get("dot_scale", 1.0)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        a = math.radians(angle)
        ca, sa = math.cos(a), math.sin(a)
        span = int(math.hypot(x1 - x0, y1 - y0) / cell / 2) + 2
        dots = Image.new("L", (W * SS, H * SS), 0)
        dr = ImageDraw.Draw(dots)
        for i in range(-span, span + 1):
            for j in range(-span, span + 1):
                u, v = i * cell, j * cell
                x, y = cx + u * ca - v * sa, cy + u * sa + v * ca
                if not (x0 - cell <= x <= x1 + cell and y0 - cell <= y <= y1 + cell):
                    continue
                s = max(0.0, min(1.0, shade(x, y)))
                r = cell * max_r * math.sqrt(s)
                if r > 0.6:
                    dr.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=255)
        self.layers[ink] = ImageChops.lighter(self.layer(ink), ImageChops.multiply(dots, mask_of(pts)))

    def _cel(self, pts, ink, shade, step=4.0, threshold=0.3, tone=130):
        """Two-tone shading: a flat tint wherever the shade passes a threshold."""
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, x1, y0, y1 = int(min(xs)), int(max(xs)) + 1, int(min(ys)), int(max(ys)) + 1
        gx, gy = np.meshgrid(np.arange(x0, x1, step), np.arange(y0, y1, step))
        try:
            s = np.asarray(shade(gx, gy), float) * np.ones_like(gx, float)
        except Exception:
            s = np.vectorize(lambda x, y: float(shade(x, y)))(gx, gy)
        small = Image.fromarray(((s > threshold) * tone).astype(np.uint8))
        big = small.resize((max(1, round((x1 - x0) * SS)), max(1, round((y1 - y0) * SS))), Image.NEAREST)
        big = big.filter(ImageFilter.GaussianBlur(SS * 1.5)).point(lambda v: tone if v > tone / 2 else 0)
        canvas = Image.new("L", (W * SS, H * SS), 0)
        canvas.paste(big, (x0 * SS, y0 * SS))
        self.layers[ink] = ImageChops.lighter(self.layer(ink), ImageChops.multiply(canvas, mask_of(pts)))

    def hairs(self, base, n, length, spread, angle, width=2.6, ink="line"):
        """Short pen flicks for brows, moustaches and loose hair."""
        for k in range(n):
            t = k / max(1, n - 1)
            bx = base[0] + (t - 0.5) * spread
            by = base[1] + self.rng.uniform(-4, 4)
            a = math.radians(angle + self.rng.uniform(-14, 14))
            L = length * self.rng.uniform(0.7, 1.15)
            self.stroke([(bx, by), (bx + math.cos(a) * L * 0.5, by + math.sin(a) * L * 0.5 - 2),
                         (bx + math.cos(a) * L, by + math.sin(a) * L)], ink=ink, width=width, wobble=0.8)

    def shape(self, pts, fill=None, line_w=None, offset=True, closed=True):
        """Occlude, fill and outline a closed shape: the common case."""
        self.occlude(pts)
        if fill:
            self.solid(pts, fill, offset)
        self.stroke(pts + ([pts[0]] if closed else []), width=line_w)

    def text(self, xy, s, fname, size, ink="line", anchor="mm", angle=0.0):
        f = font(fname, size)
        l, t, r, b = f.getbbox(s)
        pad = 20 * SS
        im = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
        ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=255)
        if angle:
            im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        x, y = xy[0] * SS, xy[1] * SS
        if anchor == "mm":
            x, y = x - im.width / 2, y - im.height / 2
        elif anchor == "lm":
            x, y = x - pad, y - im.height / 2
        lay = self.layer(ink)
        region = lay.crop((int(x), int(y), int(x) + im.width, int(y) + im.height))
        lay.paste(ImageChops.lighter(region, im), (int(x), int(y)))

    def text_width(self, s, fname, size):
        l, _, r, _ = font(fname, size).getbbox(s)
        return (r - l) / SS


# ----------------------------------------------------------------------------------------------------------------
# Overlays


def bubble(sk: Sketch, box, tail_to, text, size, fname="hand", ink="line", k: float = 1.0):
    """A speech bubble; k < 1 pops it in (scaled about its tail side)."""
    x0, y0, x1, y1 = box
    if k < 1:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        s = 0.6 + 0.4 * k
        x0, x1 = cx + (x0 - cx) * s, cx + (x1 - cx) * s
        y0, y1 = cy + (y0 - cy) * s, cy + (y1 - cy) * s
        size *= s
    pts = round_rect_pts(x0, y0, x1, y1, 46)
    cx = (x0 + x1) / 2
    tx = cx + (tail_to[0] - cx) * 0.35
    edge = y0 + 2 if tail_to[1] < y0 else y1 - 2
    tail = [(tx - 34, edge), tail_to, (tx + 34, edge)]
    sk.occlude(pts)
    sk.occlude(tail)
    sk.stroke(pts + [pts[0]], width=sk.width * 1.1)
    sk.stroke(tail, width=sk.width * 1.1)
    sk.text((cx, (y0 + y1) / 2), text, fname, size, ink, angle=sk.rng.uniform(-1.5, 1.5))


def tag(sk: Sketch, x, y, lines, size, ink="label", fill="fill2", angle=0.0):
    """A small mono name tag (the disguise coming off)."""
    w = max(sk.text_width(s, "mono", size) for s in lines) + 34
    h = len(lines) * size * 1.25 + 24
    x0, y0 = x - w / 2, y - h / 2
    pts = round_rect_pts(x0, y0, x0 + w, y0 + h, 12, 4)
    sk.occlude(pts)
    if fill:
        sk.solid(pts, fill)
    sk.stroke(pts + [pts[0]], ink=ink, width=sk.width * 0.75)
    for i, s in enumerate(lines):
        sk.text((x, y0 + 12 + size * 1.25 * (i + 0.5)), s, "mono", size, ink, angle=angle)


# ----------------------------------------------------------------------------------------------------------------
# Paper and printing

_paper_cache: dict = {}


def paper() -> np.ndarray:
    if "p" not in _paper_cache:
        rng = np.random.default_rng(3)
        base = np.ones((H * SS, W * SS, 3)) * np.array(PAPER, float)
        base += rng.normal(0, 5.0, (H * SS, W * SS, 1))
        _paper_cache["p"] = base
    return _paper_cache["p"]


def composite(sk: Sketch, seed: int = 11) -> Image.Image:
    """Print the ink masks onto paper (multiply, with riso grain) and downsample."""
    out = paper().copy() if LOOK["grain"] else np.ones((H * SS, W * SS, 3), np.float32) * np.array(LOOK["paper"],
                                                                                                    np.float32)
    rng = np.random.default_rng(seed)
    for ink in PRINT_ORDER:
        if ink not in sk.layers:
            continue
        a = np.asarray(sk.layers[ink], np.float32) / 255
        if LOOK["grain"]:
            grain = rng.random(a.shape, dtype=np.float32)
            a = a * np.clip(0.78 + grain * 0.3, 0, 1) * (0.9 if ink in ("fill", "fill2", "skin", "skin2") else 1)
        color = np.array(LOOK["inks"][ink], np.float32) / 255
        out = out * (1 - a[..., None] * (1 - color))
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    return img.resize((W, H), Image.LANCZOS)
