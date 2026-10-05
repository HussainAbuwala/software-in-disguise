"""Style test for the Episode 1 remake: one frame ("…On what?") in three hand-drawn looks.

The current kit draws smooth vector cartoons, which two viewers read as AI-made. Each style here draws every line by
"hand": strokes wobble along their length, circles overshoot where they close, and fills are hatched, misprinted or
scribbled. The composition is identical across styles so only the look is compared.

Run: ../../.venv/bin/python style_test.py  →  deliverables/style-{a,b,c}-*.png and style-sheet.png
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
SS = 2
OUT = Path(__file__).parent / "deliverables"

SUPP = "/System/Library/Fonts/Supplemental/"
FONTS = {
    "bradley": (SUPP + "Bradley Hand Bold.ttf", 0),
    "noteworthy": ("/System/Library/Fonts/Noteworthy.ttc", 1),
    "chalkduster": (SUPP + "Chalkduster.ttf", 0),
    "chalkboard": (SUPP + "ChalkboardSE.ttc", 2),
    "mono": ("/Library/Fonts/IBM-Plex-Mono/IBMPlexMono-Bold.otf", 0),
    "mono_med": ("/Library/Fonts/IBM-Plex-Mono/IBMPlexMono-Medium.otf", 0),
}
_font_cache: dict = {}


def font(name: str, size: float) -> ImageFont.FreeTypeFont:
    key = (name, round(size * SS))
    if key not in _font_cache:
        path, index = FONTS[name]
        _font_cache[key] = ImageFont.truetype(path, key[1], index=index)
    return _font_cache[key]


# ----------------------------------------------------------------------------------------------------------------
# Styles

STYLES = {
    "a-notebook": dict(
        label="A · Notebook doodle",
        paper=(250, 248, 241),
        inks={"line": (34, 52, 138), "accent": (200, 36, 48), "fill": (34, 52, 138), "fill2": (34, 52, 138),
              "label": (34, 52, 138), "good": (34, 52, 138), "skin": (34, 52, 138)},
        fill_mode="hatch",
        wobble=2.2, width=4.2, double=0.35,
        bubble_font="bradley", tag_font="mono",
    ),
    "b-riso": dict(
        label="B · Risograph zine",
        paper=(246, 239, 224),
        inks={"line": (24, 66, 156), "accent": (255, 72, 140), "fill": (255, 96, 160), "fill2": (255, 214, 40),
              "label": (24, 66, 156), "good": (24, 66, 156), "skin": (255, 190, 150)},
        fill_mode="riso",
        wobble=1.6, width=5.5, double=0.0,
        bubble_font="noteworthy", tag_font="mono",
    ),
    "c-chalk": dict(
        label="C · Chalkboard, dark mode",
        paper=(33, 39, 41),
        inks={"line": (236, 234, 226), "accent": (246, 120, 116), "fill": (240, 212, 112), "fill2": (130, 200, 230),
              "label": (128, 224, 146), "good": (128, 224, 146), "skin": (236, 234, 226)},
        fill_mode="scribble",
        wobble=2.0, width=5.0, double=0.5,
        bubble_font="chalkboard", tag_font="mono",
    ),
}


# ----------------------------------------------------------------------------------------------------------------
# Hand-drawn primitives


class Sketch:
    def __init__(self, style: dict, seed: int = 7):
        self.s = style
        self.rng = random.Random(seed)
        self.layers: dict[str, Image.Image] = {}

    # Layers are coverage masks per ink; foreground shapes erase what's behind them before drawing.
    def layer(self, ink: str) -> Image.Image:
        if ink not in self.layers:
            self.layers[ink] = Image.new("L", (W * SS, H * SS), 0)
        return self.layers[ink]

    def occlude(self, pts):
        poly = [(x * SS, y * SS) for x, y in pts]
        for im in self.layers.values():
            ImageDraw.Draw(im).polygon(poly, fill=0)

    def _wobble_fn(self, amp):
        r = self.rng
        f = [r.uniform(0.5, 0.9), r.uniform(1.6, 2.4), r.uniform(4.0, 6.0)]
        p = [r.uniform(0, 6.28) for _ in f]
        return lambda s: amp * (math.sin(f[0] * s + p[0]) + 0.5 * math.sin(f[1] * s + p[1])
                                + 0.22 * math.sin(f[2] * s + p[2])) / 1.72

    def stroke(self, pts, ink="line", width=None, wobble=None, double=None, overshoot=4.0):
        width = width or self.s["width"]
        wobble = self.s["wobble"] if wobble is None else wobble
        double = self.s["double"] if double is None else double
        self._stroke_once(pts, ink, width, wobble, overshoot)
        if double and self.rng.random() < double:
            self._stroke_once(pts, ink, width * 0.55, wobble * 1.6, overshoot * 1.5)

    def _stroke_once(self, pts, ink, width, wobble, overshoot):
        pts = _resample(pts, 5.0)
        if len(pts) < 2:
            return
        # Hands overshoot line ends a little.
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

    def circle(self, cx, cy, r, ink="line", width=None, ry=None, over=0.35, start=None):
        ry = ry or r
        a0 = self.rng.uniform(0, 6.28) if start is None else start
        n = max(24, int(r * 0.5))
        pts = [(cx + r * math.cos(a0 + t), cy + ry * math.sin(a0 + t))
               for t in np.linspace(0, 2 * math.pi + over, n)]
        self.stroke(pts, ink, width, overshoot=0)

    def dot(self, cx, cy, r, ink="line"):
        dr = ImageDraw.Draw(self.layer(ink))
        jitter = [self.rng.uniform(0.85, 1.1) for _ in range(2)]
        dr.ellipse([(cx - r * jitter[0]) * SS, (cy - r * jitter[1]) * SS, (cx + r * jitter[0]) * SS,
                    (cy + r * jitter[1]) * SS], fill=255)

    def fill(self, pts, ink="fill", angle=-35.0, gap=13.0):
        """Fill a closed shape in the style's way: pen hatching, a misregistered riso layer, or chalk scribble."""
        mode = self.s["fill_mode"]
        poly = [(x * SS, y * SS) for x, y in pts]
        mask = Image.new("L", (W * SS, H * SS), 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)
        if mode == "riso":
            dx, dy = 7 * SS, -5 * SS  # the second drum never lines up exactly
            mask = ImageChops.offset(mask, dx, dy)
            self.layers[ink] = ImageChops.lighter(self.layer(ink), mask)
            return
        hatch = Image.new("L", (W * SS, H * SS), 0)
        dr = ImageDraw.Draw(hatch)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        diag = math.hypot(x1 - x0, y1 - y0)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        a = math.radians(angle)
        ux, uy = math.cos(a), math.sin(a)
        k = -diag / 2
        width = 2.2 if mode == "hatch" else 6.5
        while k < diag / 2:
            jit = self.rng.uniform(-2, 2)
            px, py = cx - uy * (k + jit), cy + ux * (k + jit)
            dr.line([((px - ux * diag) * SS, (py - uy * diag) * SS), ((px + ux * diag) * SS, (py + uy * diag) * SS)],
                    fill=255 if mode == "hatch" else 150, width=round(width * SS))
            k += gap if mode == "hatch" else gap * 0.75
        hatch = ImageChops.multiply(hatch, mask)
        self.layers[ink] = ImageChops.lighter(self.layer(ink), hatch)

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


def _resample(pts, step):
    out = [pts[0]]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        d = math.hypot(xb - xa, yb - ya)
        n = max(1, int(d / step))
        for i in range(1, n + 1):
            out.append((xa + (xb - xa) * i / n, ya + (yb - ya) * i / n))
    return out


def ellipse_pts(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(a0, a1, n)]


def round_rect_pts(x0, y0, x1, y1, r, n=8):
    pts = []
    for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            t = math.radians(a + 90 * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


# ----------------------------------------------------------------------------------------------------------------
# Paper


def paper(style_key: str) -> Image.Image:
    st = STYLES[style_key]
    rng = np.random.default_rng(3)
    base = np.ones((H, W, 3)) * np.array(st["paper"], float)
    if style_key == "a-notebook":
        img = Image.fromarray(base.astype(np.uint8))
        dr = ImageDraw.Draw(img)
        for y in range(150, H, 58):
            dr.line([(0, y), (W, y)], fill=(176, 198, 226), width=2)
        dr.line([(118, 0), (118, H)], fill=(232, 150, 150), width=3)
        base = np.asarray(img, float)
        base += rng.normal(0, 2.0, (H, W, 1))
    elif style_key == "b-riso":
        base += rng.normal(0, 5.0, (H, W, 1))
    else:
        smudge = Image.fromarray((rng.random((H // 24, W // 24)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
        smudge = np.asarray(smudge.filter(ImageFilter.GaussianBlur(30)), float)[..., None] / 255
        base += (smudge - 0.5) * 22 + rng.normal(0, 3.0, (H, W, 1))
        # Faint half-erased chalk from an earlier lesson.
        ghost = Image.new("L", (W, H), 0)
        gd = ImageDraw.Draw(ghost)
        gd.text((140, 1700), "x = x + 1", font=ImageFont.truetype(FONTS["chalkduster"][0], 70), fill=255)
        gd.text((640, 230), "O(n)", font=ImageFont.truetype(FONTS["chalkduster"][0], 60), fill=255)
        ghost = np.asarray(ghost.filter(ImageFilter.GaussianBlur(6)), float)[..., None] / 255
        base += ghost * 16
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def composite(sk: Sketch, style_key: str) -> Image.Image:
    st = STYLES[style_key]
    bg = paper(style_key).resize((W * SS, H * SS), Image.BICUBIC)
    out = np.asarray(bg, float)
    rng = np.random.default_rng(11)
    order = ["skin", "fill2", "fill", "line", "label", "good", "accent"]
    for ink in order:
        if ink not in sk.layers:
            continue
        a = np.asarray(sk.layers[ink], float) / 255
        color = np.array(st["inks"][ink], float)
        if style_key == "c-chalk":
            # Chalk skips over the board's grain.
            grain = rng.random(a.shape)
            grain = np.asarray(Image.fromarray((grain * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),
                               float) / 255
            a = a * np.clip((grain - 0.28) * 3.2, 0, 1) * 0.95
            out = out * (1 - a[..., None]) + color * a[..., None]
        else:
            if style_key == "b-riso":
                grain = rng.random(a.shape)
                a = a * np.clip(0.78 + grain * 0.3, 0, 1) * (0.9 if ink in ("fill", "fill2", "skin") else 1)
            else:
                a = a * 0.93
            multiplied = out * color / 255
            out = out * (1 - a[..., None]) + multiplied * a[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    return img.resize((W, H), Image.LANCZOS)


# ----------------------------------------------------------------------------------------------------------------
# People, drawn frontal with simple features


def head(sk: Sketch, cx, cy, r, who, expr, gaze=(0.0, 0.0)):
    shape = ellipse_pts(cx, cy, r, r * 1.06)
    sk.occlude(shape)
    if sk.s["fill_mode"] == "riso":
        sk.fill(shape, "skin")
    # Hair behind the head
    if who == "mom":
        hair = [(cx - r * 1.05, cy - r * 0.2), (cx - r * 1.15, cy + r * 1.3), (cx - r * 0.6, cy + r * 1.35),
                (cx + r * 0.6, cy + r * 1.35), (cx + r * 1.15, cy + r * 1.3), (cx + r * 1.05, cy - r * 0.2)]
        sk.stroke(hair[:2] + [hair[2]])
        sk.stroke(hair[3:])
    sk.circle(cx, cy, r, ry=r * 1.06)
    ex, ey = r * 0.36, -r * 0.02
    gx, gy = gaze[0] * r * 0.09, gaze[1] * r * 0.09
    # Eyes
    if expr == "beaming":
        for sx in (-1, 1):
            sk.stroke(ellipse_pts(cx + sx * ex, cy + ey + r * 0.04, r * 0.13, r * 0.1, 10, math.pi, 2 * math.pi),
                      width=sk.s["width"] * 0.9)
    else:
        for sx in (-1, 1):
            sk.dot(cx + sx * ex + gx, cy + ey + gy, r * (0.075 if expr != "confused" else 0.06))
    # Brows
    lift = {"confused": -0.42, "beaming": -0.36, "happy": -0.3, "listen": -0.3}.get(expr, -0.3)
    for sx in (-1, 1):
        tilt = 0.07 * sx if expr == "confused" else 0
        b0 = (cx + sx * (ex - r * 0.16), cy + r * (lift + tilt))
        b1 = (cx + sx * (ex + r * 0.14), cy + r * (lift - 0.04 + (0.1 * sx if expr == "confused" and sx > 0 else 0)))
        sk.stroke([b0, ((b0[0] + b1[0]) / 2, min(b0[1], b1[1]) - r * 0.05), b1], width=sk.s["width"] * 0.9)
    # Nose
    sk.stroke([(cx + r * 0.02, cy + r * 0.05), (cx - r * 0.07, cy + r * 0.27), (cx + r * 0.06, cy + r * 0.3)],
              width=sk.s["width"] * 0.8)
    # Mouth
    my = cy + r * 0.55
    if expr == "beaming":
        m = ellipse_pts(cx, my - r * 0.06, r * 0.34, r * 0.28, 24, 0, math.pi)
        mouth = [(cx - r * 0.34, my - r * 0.06)] + m[::-1][::-1]
        sk.occlude(m)
        sk.stroke(m + [m[0]])
        sk.stroke([(cx - r * 0.33, my - r * 0.06), (cx + r * 0.33, my - r * 0.06)])
        if sk.s["fill_mode"] == "riso":
            sk.fill(m, "accent")
    elif expr == "confused":
        sk.circle(cx + r * 0.05, my + r * 0.04, r * 0.09, ry=r * 0.11)
    else:
        sk.stroke(ellipse_pts(cx, my - r * 0.18, r * 0.24, r * 0.16, 14, 0.35, math.pi - 0.35))
    # Cheeks (riso blush)
    if sk.s["fill_mode"] == "riso" and expr in ("beaming", "happy"):
        for sx in (-1, 1):
            sk.fill(ellipse_pts(cx + sx * r * 0.58, cy + r * 0.32, r * 0.14, r * 0.09, 16), "accent")

    # Hair and accessories in front
    if who == "grandpa":
        for sx in (-1, 1):  # side tufts
            for k in range(3):
                sk.stroke([(cx + sx * r * 0.93, cy - r * (0.25 - k * 0.14)),
                           (cx + sx * r * (1.12 + 0.03 * k), cy - r * (0.32 - k * 0.14))], width=sk.s["width"] * 0.8)
        for sx in (-1, 1):  # glasses
            sk.circle(cx + sx * ex, cy + ey, r * 0.21, width=sk.s["width"] * 0.85)
        sk.stroke([(cx - ex + r * 0.21, cy + ey), (cx + ex - r * 0.21, cy + ey)], width=sk.s["width"] * 0.8)
        for sx in (-1, 1):  # moustache
            sk.stroke([(cx, cy + r * 0.36), (cx + sx * r * 0.2, cy + r * 0.33), (cx + sx * r * 0.36, cy + r * 0.46)])
        sk.stroke(ellipse_pts(cx - r * 0.3, cy - r * 0.62, r * 0.18, r * 0.1, 8, math.pi * 1.1, math.pi * 1.7),
                  width=sk.s["width"] * 0.7)
    elif who == "aunt":
        bun = (cx + r * 0.1, cy - r * 1.32)
        sk.occlude(ellipse_pts(*bun, r * 0.44, r * 0.38))
        sk.circle(*bun, r * 0.44, ry=r * 0.38)
        cap = ellipse_pts(cx, cy - r * 0.05, r * 1.08, r * 1.12, 30, math.pi * 1.02, math.pi * 1.98)
        sk.stroke(cap)
        sk.stroke([(cx - r * 0.9, cy - r * 0.55), (cx - r * 0.15, cy - r * 0.78), (cx + r * 0.85, cy - r * 0.6)])
        if sk.s["fill_mode"] != "riso":
            sk.fill(cap + [(cx + r * 0.85, cy - r * 0.6), (cx - r * 0.15, cy - r * 0.78), (cx - r * 0.9, cy - r * 0.55)],
                    "line", angle=60, gap=10)
            sk.fill(ellipse_pts(*bun, r * 0.44, r * 0.38), "line", angle=60, gap=10)
        else:
            sk.fill(cap + [(cx + r * 0.85, cy - r * 0.6), (cx - r * 0.9, cy - r * 0.55)], "line")
            sk.fill(ellipse_pts(*bun, r * 0.44, r * 0.38), "line")
        for sx in (-1, 1):  # earrings
            sk.circle(cx + sx * r * 1.0, cy + r * 0.42, r * 0.08, ink="accent")
    elif who == "mom":
        cap = ellipse_pts(cx, cy - r * 0.05, r * 1.06, r * 1.12, 30, math.pi * 1.0, math.pi * 2.0)
        sk.stroke(cap)
        sk.stroke([(cx - r * 0.95, cy - r * 0.2), (cx - r * 0.1, cy - r * 0.8), (cx + r * 0.2, cy - r * 0.6),
                   (cx + r * 0.98, cy - r * 0.15)])
    elif who in ("dad", "fiance"):
        sk.stroke(ellipse_pts(cx, cy - r * 0.1, r * 1.04, r * 1.05, 24, math.pi * 1.05, math.pi * 1.95))
        sk.stroke([(cx - r * 0.95, cy - r * 0.35), (cx - r * 0.3, cy - r * 0.72), (cx + r * 0.4, cy - r * 0.62),
                   (cx + r * 0.95, cy - r * 0.35)])
    if who == "dad":
        sk.stroke(ellipse_pts(cx, cy + r * 0.25, r * 0.92, r * 0.85, 20, 0.15, math.pi - 0.15))  # beard
    elif who == "sister":
        sk.stroke(ellipse_pts(cx, cy - r * 0.05, r * 1.06, r * 1.1, 24, math.pi * 1.0, math.pi * 2.0))
        sk.stroke([(cx - r * 0.95, cy - r * 0.25), (cx + r * 0.3, cy - r * 0.85), (cx + r * 1.0, cy - r * 0.3)])
        tail = [(cx + r * 0.95, cy - r * 0.5), (cx + r * 1.55, cy - r * 0.1), (cx + r * 1.45, cy + r * 0.7),
                (cx + r * 1.05, cy + r * 0.2)]
        sk.stroke(tail)


def torso(sk: Sketch, cx, top, half_w, bottom, ink="fill", lean=0.0):
    pts = [(cx - half_w * 0.35 + lean, top), (cx - half_w * 0.95 + lean * 0.6, top + half_w * 0.35),
           (cx - half_w * 1.05, bottom), (cx + half_w * 1.05, bottom),
           (cx + half_w * 0.95 + lean * 0.6, top + half_w * 0.35), (cx + half_w * 0.35 + lean, top)]
    sk.occlude(pts)
    sk.fill(pts, ink)
    sk.stroke(pts[:3])
    sk.stroke(pts[3:])
    sk.stroke([pts[-1], ((pts[0][0] + pts[-1][0]) / 2, top + half_w * 0.18), pts[0]])  # neckline


def arm(sk: Sketch, pts, hand_r=16, ink="fill", thick=34):
    """A sleeve (two outlines around a filled band) ending in a round hand."""
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
    sk.fill(band, ink)
    sk.stroke(left)
    sk.stroke(right)
    hx, hy = pts[-1]
    sk.occlude(ellipse_pts(hx, hy, hand_r, hand_r))
    if sk.s["fill_mode"] == "riso":
        sk.fill(ellipse_pts(hx, hy, hand_r, hand_r), "skin")
    sk.circle(hx, hy, hand_r)


def bubble(sk: Sketch, box, tail_to, text, size, fname=None, ink="line"):
    x0, y0, x1, y1 = box
    fname = fname or sk.s["bubble_font"]
    pts = round_rect_pts(x0, y0, x1, y1, 46)
    cx = (x0 + x1) / 2
    tx = cx + (tail_to[0] - cx) * 0.35
    tail = [(tx - 34, y1 - 2), tail_to, (tx + 34, y1 - 2)]
    sk.occlude(pts)
    sk.occlude(tail)
    sk.stroke(pts + [pts[0]], width=sk.s["width"] * 1.1)
    sk.stroke(tail, width=sk.s["width"] * 1.1)
    sk.text((cx, (y0 + y1) / 2), text, fname, size, ink, angle=sk.rng.uniform(-2, 2))


def tag(sk: Sketch, x, y, lines, size, ink="label", box=True, angle=0.0):
    """A small name tag: the character's role in the system."""
    fname = sk.s["tag_font"]
    w = max(sk.text_width(s, fname, size) for s in lines) + 34
    h = len(lines) * size * 1.25 + 24
    x0, y0 = x - w / 2, y - h / 2
    pts = round_rect_pts(x0, y0, x0 + w, y0 + h, 12, 4)
    sk.occlude(pts)
    if box:
        if sk.s["fill_mode"] == "riso":
            sk.fill(pts, "fill2")
        sk.stroke(pts + [pts[0]], ink=ink, width=sk.s["width"] * 0.75)
    for i, s in enumerate(lines):
        sk.text((x, y0 + 12 + size * 1.25 * (i + 0.5)), s, fname, size, ink, angle=angle)


# ----------------------------------------------------------------------------------------------------------------
# The frame


def draw_frame(style_key: str) -> Image.Image:
    sk = Sketch(STYLES[style_key])
    chalk = style_key == "c-chalk"

    # Far end of the table: the couple; Mom (left) and Dad (right) a little nearer.
    # Couple
    torso(sk, 478, 610, 62, 700, "fill2")
    head(sk, 478, 545, 50, "sister", "happy", (-0.5, 0.4))
    torso(sk, 600, 615, 62, 700, "fill")
    head(sk, 600, 548, 50, "fiance", "happy", (-0.6, 0.4))
    # Sister's raised hand with the ring
    arm(sk, [(440, 660), (408, 615), (404, 572)], 13, "fill2", thick=18)
    sk.circle(404, 556, 7, ink="accent", width=3.4)
    for a in range(4):  # sparkle
        t = a * math.pi / 2 + math.pi / 4
        sk.stroke([(372 + 10 * math.cos(t), 540 + 10 * math.sin(t)), (372 + 22 * math.cos(t), 540 + 22 * math.sin(t))],
                  ink="accent", width=3.4, double=0)
    torso(sk, 300, 770, 78, 880, "fill2", lean=10)
    head(sk, 300, 690, 62, "mom", "happy", (0.6, 0.5))
    torso(sk, 790, 770, 78, 880, "fill")
    head(sk, 790, 690, 62, "dad", "listen", (-0.7, 0.5))

    # The table, receding: near edge at the bottom of the frame.
    table = [(385, 740), (700, 740), (850, 1940), (230, 1940)]
    sk.occlude(table)
    if not chalk:
        sk.fill(table, "fill2" if sk.s["fill_mode"] == "riso" else "line", angle=20, gap=34)
    sk.stroke([table[0], table[1]])
    sk.stroke([table[1], table[2]])
    sk.stroke([table[3], table[0]])
    # Dishes
    for (px, py, pr) in ((440, 830, 44), (645, 830, 44), (360, 1330, 82), (720, 1330, 82)):
        sh = ellipse_pts(px, py, pr, pr * 0.42)
        sk.occlude(sh)
        sk.circle(px, py, pr, ry=pr * 0.42)
        sk.circle(px, py, pr * 0.62, ry=pr * 0.26, width=sk.s["width"] * 0.7)
    py0 = 1175
    body = [(440, py0), (452, py0 + 85), (628, py0 + 85), (640, py0)]
    sk.occlude(body)
    if sk.s["fill_mode"] != "hatch":
        sk.fill(body, "accent" if sk.s["fill_mode"] == "riso" else "fill")
    sk.stroke(body)
    sk.occlude(ellipse_pts(540, py0, 100, 38))
    sk.circle(540, py0, 100, ry=38)
    for k in (-1, 0, 1):  # steam
        x = 540 + k * 44
        sk.stroke([(x, py0 - 50), (x - 12, py0 - 75), (x + 9, py0 - 100), (x - 5, py0 - 122)], width=sk.s["width"] * 0.8)

    # Near left: the aunt, leaning in toward Grandpa, beaming.
    torso(sk, 175, 1390, 165, 1940, "fill", lean=30)
    arm(sk, [(270, 1470), (385, 1488), (478, 1405)], 24, "fill")
    head(sk, 175, 1250, 122, "aunt", "beaming")
    # Near right: Grandpa, fork in the air.
    torso(sk, 905, 1380, 165, 1940, "fill2", lean=-20)
    sk.stroke([(742, 1250), (742, 1150)], width=sk.s["width"] * 0.9)  # fork handle
    arm(sk, [(812, 1470), (712, 1430), (738, 1268)], 24, "fill2")
    for dx in (-10, 0, 10):
        sk.stroke([(742 + dx, 1150), (742 + dx, 1112)], width=sk.s["width"] * 0.7)
    sk.occlude(ellipse_pts(742, 1112, 17, 14))
    sk.circle(742, 1112, 17, ry=14)
    if sk.s["fill_mode"] == "riso":
        sk.fill(ellipse_pts(742, 1112, 17, 14), "fill2")
    head(sk, 905, 1235, 125, "grandpa", "confused", (-0.6, 0.0))

    # Speech bubbles
    bubble(sk, (22, 900, 572, 1030), (190, 1068), "Congratulations!!", 60)
    bubble(sk, (606, 935, 1058, 1060), (900, 1100), "…On what?", 64)

    # Role tags
    small = 27
    tag(sk, 540, 440, ["PRIMARY"], small + 4)
    tag(sk, 260, 575, ["replica", "synced"], small)
    tag(sk, 830, 575, ["replica", "synced"], small)
    tag(sk, 210, 1700, ["replica · synced"], 31)
    tag(sk, 830, 1720, ["replica", "last sync: 3 days ago"], 31, ink="accent")
    # STALE READ stamp
    sx, sy = 830, 1830
    tag(sk, sx, sy, ["STALE READ"], 50, ink="accent", angle=6)

    # Header
    hand = sk.s["bubble_font"]
    sk.text((W / 2, 200), "Sunday lunch.", hand, 56, "line", angle=-1.5)
    sk.text((W / 2, 290), "Priya got engaged on Friday.", hand, 38, "line", angle=0.8)
    return composite(sk, style_key)


def main():
    OUT.mkdir(exist_ok=True)
    frames = []
    for key, st in STYLES.items():
        img = draw_frame(key)
        img.save(OUT / f"style-{key}.png")
        frames.append((st["label"], img))
        print("wrote", OUT / f"style-{key}.png")
    # Contact sheet: the three side by side at phone-preview size.
    tw, th = 540, 960
    sheet = Image.new("RGB", (tw * 3 + 80, th + 110), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34, index=0)
    for i, (label, img) in enumerate(frames):
        x = 20 + i * (tw + 20)
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, 90))
        dr.text((x + tw / 2, 45), label, font=f, fill=(30, 30, 30), anchor="mm")
    sheet.save(OUT / "style-sheet.png")
    print("wrote", OUT / "style-sheet.png")


if __name__ == "__main__":
    main()
