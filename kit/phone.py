"""Crisp, realistic phone screens for the "glitch in a real app" format (from Episode 1's remake, 2026-10-05).

The people and sets are printed in the riso look; app screens must read as real apps, so they are drawn sharp in
the system UI font and laid over the print afterwards (never riso-textured). Apps are generic and unbranded.

A screen is a function `draw(d: ScreenDraw)` on a 390x844 point canvas (an iPhone's logical size); `phone()` renders
it at 3x, puts it in a phone body and pastes it, rotated, onto a finished frame.
"""

from __future__ import annotations

from typing import Callable

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SF = "/System/Library/Fonts/SFNS.ttf"
SCALE = 3
SW, SH = 390, 844

INK = (17, 17, 20)
GREY = (120, 120, 128)
LINE = (226, 226, 232)
BLUE = (10, 122, 255)
GREEN = (52, 199, 89)
ORANGE = (255, 149, 0)
BG = (242, 242, 247)
WHITE = (255, 255, 255)

_fonts: dict = {}


def sf(size: float, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    key = (round(size * SCALE), weight)
    if key not in _fonts:
        f = ImageFont.truetype(SF, key[0])
        f.set_variation_by_name(weight)
        _fonts[key] = f
    return _fonts[key]


class ScreenDraw:
    """Drawing in screen points (390 x 844)."""

    def __init__(self, bg=WHITE):
        self.img = Image.new("RGB", (SW * SCALE, SH * SCALE), bg)
        self.d = ImageDraw.Draw(self.img)

    def rect(self, x0, y0, x1, y1, fill, r=0, outline=None, width=1):
        self.d.rounded_rectangle([x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE], radius=r * SCALE, fill=fill,
                                 outline=outline, width=width * SCALE)

    def circle(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * SCALE, (cy - r) * SCALE, (cx + r) * SCALE, (cy + r) * SCALE], fill=fill)

    def line(self, pts, fill, width=1):
        self.d.line([(x * SCALE, y * SCALE) for x, y in pts], fill=fill, width=round(width * SCALE), joint="curve")

    def text(self, x, y, s, size, weight="Regular", fill=INK, anchor="la"):
        self.d.text((x * SCALE, y * SCALE), s, font=sf(size, weight), fill=fill, anchor=anchor)

    def status_bar(self, time="9:41", fill=INK):
        self.text(52, 22, time, 17, "Semibold", fill, "ma")
        for i in range(4):  # signal
            h = 4 + i * 2.6
            self.rect(292 + i * 5.5, 33 - h, 295.5 + i * 5.5, 33, fill, r=1)
        self.d.arc([316 * SCALE, 21 * SCALE, 334 * SCALE, 39 * SCALE], 225, 315, fill=fill, width=2 * SCALE)  # wifi
        self.d.arc([320 * SCALE, 25 * SCALE, 330 * SCALE, 35 * SCALE], 225, 315, fill=fill, width=2 * SCALE)
        self.rect(341, 23, 366, 35, None, r=3.5, outline=fill, width=1)  # battery
        self.rect(343, 25, 361, 33, fill, r=2)
        self.rect(367, 27, 369, 31, fill, r=1)


def phone(frame: Image.Image, cx: float, cy: float, width: float, draw: Callable[[ScreenDraw], None],
          angle: float = 0.0, body=(22, 22, 26)) -> None:
    """Render a screen into a phone body and paste it onto `frame`, centered at (cx, cy), `width` px wide."""
    sd = ScreenDraw()
    draw(sd)
    screen = sd.img
    bez = 14 * SCALE
    pw, ph = screen.width + 2 * bez, screen.height + 2 * bez
    dev = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dev)
    dd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=62 * SCALE, fill=body + (255,))
    mask = Image.new("L", screen.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, screen.width - 1, screen.height - 1], radius=50 * SCALE, fill=255)
    dev.paste(screen, (bez, bez), mask)
    dd.rounded_rectangle([pw / 2 - 62 * SCALE, bez + 11 * SCALE, pw / 2 + 62 * SCALE, bez + 47 * SCALE],
                         radius=18 * SCALE, fill=(0, 0, 0, 255))  # the camera island
    s = width / pw
    dev = dev.resize((round(pw * s), round(ph * s)), Image.LANCZOS)
    if angle:
        dev = dev.rotate(angle, resample=Image.BICUBIC, expand=True)
    # A print-like offset shadow in riso blue, so the crisp phone still sits in the printed world.
    shadow = Image.new("RGBA", dev.size, (24, 66, 156, 0))
    shadow.putalpha(dev.getchannel("A").point(lambda a: int(a * 0.35)))
    x, y = round(cx - dev.width / 2), round(cy - dev.height / 2)
    frame.paste(shadow, (x + 14, y + 16), shadow)
    frame.paste(dev, (x, y), dev)
