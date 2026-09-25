"""Drawing surface with a camera, shared by every code-drawn episode.

World coordinates are fixed per set (the living room is always the same size), and each shot is only a camera
(zoom + focus). Everything is drawn supersampled and downscaled once per frame for smooth ink lines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SS = 2

FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
BOLD, DEMI, MEDIUM, HEAVY = 0, 2, 5, 8

# Series palette.
INK = (28, 26, 24)
PAPER = (255, 252, 245)
WALL = (238, 230, 214)
FLOOR = (196, 170, 138)
MUSTARD = (227, 178, 60)
TEAL = (42, 157, 143)
ALERT = (209, 73, 91)
GREY = (150, 142, 132)
LW = 7  # standard ink line width, world units

_fonts: dict = {}


def font(size: float, weight: int = BOLD) -> ImageFont.FreeTypeFont:
    key = (round(size * SS), weight)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_PATH, key[0], index=weight)
    return _fonts[key]


@dataclass
class Camera:
    zoom: float = 1.0
    fx: float = W / 2  # world point that lands on screen point (sx, sy)
    fy: float = H / 2
    sx: float = W / 2
    sy: float = H / 2

    def to_screen(self, x: float, y: float) -> tuple[float, float]:
        return (x - self.fx) * self.zoom + self.sx, (y - self.fy) * self.zoom + self.sy


SCREEN = Camera()


class Canvas:
    """Thin wrapper over ImageDraw that maps world coordinates through a camera."""

    def __init__(self, img: Image.Image, cam: Camera = SCREEN):
        self.img = img
        self.d = ImageDraw.Draw(img)
        self.cam = cam

    # Coordinate helpers --------------------------------------------------------------------------------------
    def w(self, v: float) -> int:
        return max(1, round(v * SS * self.cam.zoom))

    def p(self, x: float, y: float) -> tuple[int, int]:
        sx, sy = self.cam.to_screen(x, y)
        return round(sx * SS), round(sy * SS)

    def box(self, x0, y0, x1, y1):
        (a, b), (c, d) = self.p(x0, y0), self.p(x1, y1)
        return [min(a, c), min(b, d), max(a, c), max(b, d)]

    def pts(self, xy):
        return [self.p(x, y) for x, y in xy]

    # Primitives ----------------------------------------------------------------------------------------------
    def ellipse(self, x0, y0, x1, y1, fill=None, outline=INK, width=LW):
        self.d.ellipse(self.box(x0, y0, x1, y1), fill=fill, outline=outline, width=self.w(width) if outline else 0)

    def circle(self, cx, cy, r, **kw):
        self.ellipse(cx - r, cy - r, cx + r, cy + r, **kw)

    def rect(self, x0, y0, x1, y1, fill=None, outline=INK, width=LW, radius=0):
        b = self.box(x0, y0, x1, y1)
        wd = self.w(width) if outline else 0
        if radius:
            self.d.rounded_rectangle(b, radius=self.w(radius), fill=fill, outline=outline, width=wd)
        else:
            self.d.rectangle(b, fill=fill, outline=outline, width=wd)

    def poly(self, xy, fill=None, outline=INK, width=LW):
        pts = self.pts(xy)
        self.d.polygon(pts, fill=fill)
        if outline:
            self.d.line(pts + [pts[0]], fill=outline, width=self.w(width), joint="curve")

    def line(self, xy, fill=INK, width=LW, rounded=True):
        pts = self.pts(xy)
        wd = self.w(width)
        self.d.line(pts, fill=fill, width=wd, joint="curve")
        if rounded:
            r = wd / 2
            for x, y in (pts[0], pts[-1]):
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def limb(self, xy, fill, width, outline=INK, ink=5):
        """A thick sleeve/arm with an ink outline: outline stroke first, color stroke on top."""
        self.line(xy, fill=outline, width=width + ink * 2)
        self.line(xy, fill=fill, width=width)

    def arc(self, x0, y0, x1, y1, start, end, fill=INK, width=6):
        self.d.arc(self.box(x0, y0, x1, y1), start, end, fill=fill, width=self.w(width))

    def chord(self, x0, y0, x1, y1, start, end, fill=None, outline=INK, width=LW):
        self.d.chord(self.box(x0, y0, x1, y1), start, end, fill=fill, outline=outline, width=self.w(width) if outline else 0)

    def pieslice(self, x0, y0, x1, y1, start, end, fill=None, outline=INK, width=LW):
        self.d.pieslice(self.box(x0, y0, x1, y1), start, end, fill=fill, outline=outline, width=self.w(width) if outline else 0)

    def text(self, x, y, s, size, fill=INK, weight=BOLD, anchor="mm"):
        """Text scales with the camera, so it can live in the world (e.g. a TV logo) or on screen."""
        f = font(size * self.cam.zoom, weight)
        self.d.text(self.p(x, y), s, font=f, fill=fill, anchor=anchor)


def new_frame(color=WALL) -> Image.Image:
    return Image.new("RGB", (W * SS, H * SS), color)


def finish(img: Image.Image) -> Image.Image:
    return img.resize((W, H), Image.LANCZOS)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lid_chord_angles(level: float) -> tuple[float, float]:
    """Angles for a chord covering the top `level` (0..1) of an ellipse, for eyelids."""
    s0 = max(-0.999, min(0.999, level * 2 - 1))
    phi = math.degrees(math.asin(s0))
    return 180 - phi, 360 + phi
