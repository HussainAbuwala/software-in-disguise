"""Character options (2026-10-05): the same first frame with three kinds of characters.

1. Open Peeps: hand-drawn by an illustrator (Pablo Stanley, CC0), assembled from parts (kit/peeps.py)
2. Big heads: simple cartoon characters drawn in code, few details (in the spirit of the "Oversimplified" channel)
3. Cats: the family as animals, drawn in code

The set is kept plain and flat so only the characters differ; the phones are the same crisp screens.

Run: ../../.venv/bin/python character_options.py  →  deliverables/chars-*.png and chars-options.png
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from format_test import confirmation  # noqa: E402
from kit.peeps import bust  # noqa: E402
from kit.phone import phone  # noqa: E402

OUT = Path(__file__).parent / "deliverables"
W, H, S = 1080, 1920, 2  # drawn at 2x, downsampled

INK = (29, 27, 31)
WALL = (247, 236, 214)
DESK = (183, 116, 74)
RED = (226, 76, 58)
YELLOW = (242, 193, 78)
GOLD = (236, 184, 52)
SKIN1, SKIN2 = (196, 135, 92), (168, 110, 72)
HAIR = (31, 28, 33)
WHITE = (255, 255, 255)
HAND = "/System/Library/Fonts/Noteworthy.ttc"
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"


class Pen:
    def __init__(self, img):
        self.d = ImageDraw.Draw(img)
        self.lw = 9

    def ell(self, cx, cy, rx, ry, fill, lw=None, outline=INK):
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill,
                       outline=outline if lw != 0 else None, width=(lw or self.lw) * S)

    def poly(self, pts, fill, lw=None, outline=INK):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=None)
        if lw != 0:
            self.line(pts + [pts[0]], INK if outline is None else outline, lw or self.lw)

    def line(self, pts, fill=INK, lw=None):
        self.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=round((lw or self.lw) * S), joint="curve")
        r = (lw or self.lw) * S / 2
        for x, y in (pts[0], pts[-1]):
            self.d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=fill)

    def arc(self, cx, cy, rx, ry, a0, a1, fill=INK, lw=None):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
               for a in [a0 + (a1 - a0) * i / 24 for i in range(25)]]
        self.line(pts, fill, lw)

    def rrect(self, x0, y0, x1, y1, r, fill, lw=None):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill, outline=INK,
                                 width=(lw or self.lw) * S)

    def text(self, xy, s, size, path=HAND, index=1, fill=INK):
        self.d.text((xy[0] * S, xy[1] * S), s, font=ImageFont.truetype(path, size * S, index=index), fill=fill,
                    anchor="mm")


def set_and_bubble(p: Pen, text="That's MY room."):
    p.d.rectangle([0, 0, W * S, 1040 * S], fill=WALL)
    for x in range(0, W, 90):  # quiet wallpaper stripes
        p.d.rectangle([x * S, 0, (x + 30) * S, 1040 * S], fill=(242, 228, 202))
    p.rrect(330, 70, 750, 160, 16, RED)
    p.text((540, 116), "RECEPTION", 50, AVENIR, 8, WHITE)


def desk_and_key(p: Pen):
    p.d.rectangle([0, 1040 * S, W * S, 1200 * S], fill=DESK)
    p.line([(0, 1040), (W, 1040)], INK, 8)
    p.ell(520, 1080, 22, 22, GOLD, 6)
    p.line([(542, 1080), (612, 1080)], INK, 8)
    p.line([(592, 1080), (592, 1098)], INK, 6)
    p.line([(606, 1080), (606, 1094)], INK, 6)
    p.rrect(500, 1106, 558, 1146, 6, (250, 245, 232), 5)
    p.text((529, 1126), "204", 22, AVENIR, 8)


def speech(p: Pen, box, tail, text, size=60):
    x0, y0, x1, y1 = box
    tx = (x0 + x1) / 2 + (tail[0] - (x0 + x1) / 2) * 0.35
    p.poly([(tx - 32, y1 - 6), tail, (tx + 32, y1 - 6)], WHITE)
    p.rrect(x0, y0, x1, y1, 44, WHITE)
    p.d.polygon([((tx - 26) * S, (y1 - 10) * S), ((tx + 26) * S, (y1 - 10) * S), (tx * S, (y1 + 4) * S)], fill=WHITE)
    p.text(((x0 + x1) / 2, (y0 + y1) / 2), text, size)


def finish(img: Image.Image) -> Image.Image:
    img = img.resize((W, H), Image.LANCZOS)
    phone(img, 290, 1500, 370, confirmation("MH-48213"), angle=4)
    phone(img, 790, 1500, 370, confirmation("MH-48214"), angle=-4)
    return img


# ----------------------------------------------------------------------------------------------------------------
# 1. Open Peeps


def option_peeps() -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), WALL)
    p = Pen(img)
    set_and_bubble(p)
    a = bust(body="polka-dot-jacket", head="bun", face="angry", skin="#c4875c", clothes="#e2543f",
             height=1560)
    b = bust(body="sweater", head="long", face="suspicious", accessory="glasses", skin="#a86e48",
             clothes="#f2c14e", height=1500)
    b = ImageOps.mirror(b)
    img.paste(a, (-40 * S, 300 * S), a)
    img.paste(b, (560 * S, 330 * S), b)
    desk_and_key(p)
    speech(p, (40, 215, 560, 335), (300, 400), "That's MY room.")
    return finish(img)


# ----------------------------------------------------------------------------------------------------------------
# 2. Big heads


def bighead(p: Pen, cx, cy, r, skin, look, toward):
    g = toward * 0.09 * r
    # body, small under a big head
    p.poly([(cx - r * 0.95, 1060), (cx - r * 0.8, cy + r * 0.95), (cx + r * 0.8, cy + r * 0.95), (cx + r * 0.95, 1060)],
           RED if look == "bun" else YELLOW)
    if look == "long":  # hair behind
        p.rrect(cx - r * 1.12, cy - r * 0.9, cx + r * 1.12, cy + r * 1.5, r * 0.6, HAIR)
    p.ell(cx, cy, r, r * 1.05, skin)
    # hair cap with a middle parting
    cap = [(cx - r * 1.02, cy - r * 0.15)]
    for a in range(190, 351, 8):
        cap.append((cx + r * 1.04 * math.cos(math.radians(a)), cy - r * 0.05 + r * 1.1 * math.sin(math.radians(a))))
    cap += [(cx + r * 1.02, cy - r * 0.15), (cx + r * 0.5, cy - r * 0.62), (cx, cy - r * 0.78), (cx - r * 0.5, cy - r * 0.62)]
    p.poly(cap, HAIR, lw=6)
    p.line([(cx, cy - r * 1.12), (cx, cy - r * 0.8)], skin, 6)
    if look == "bun":
        p.ell(cx, cy - r * 1.2, r * 0.38, r * 0.3, HAIR, 6)
        for side in (-1, 1):  # grey streaks
            p.arc(cx + side * r * 0.45, cy - r * 0.55, r * 0.45, r * 0.4, 200 if side < 0 else 250, 290 if side < 0 else 340,
                  (150, 146, 150), 6)
    # eyes
    for side in (-1, 1):
        ex = cx + side * r * 0.34
        p.ell(ex, cy + r * 0.05, r * 0.2, r * 0.25, WHITE, 6)
        p.ell(ex + g, cy + r * 0.1, r * 0.1, r * 0.11, INK, 0)
        p.ell(ex + g - r * 0.03, cy + r * 0.06, r * 0.03, r * 0.03, WHITE, 0)
        # angry brows: inner end low
        p.line([(cx + side * r * 0.14, cy - r * 0.16), (cx + side * r * 0.55, cy - r * 0.3)], INK, 16)
        if look == "long":
            p.ell(ex, cy + r * 0.07, r * 0.27, r * 0.3, None, 7)
    if look == "long":
        p.line([(cx - r * 0.07, cy + r * 0.05), (cx + r * 0.07, cy + r * 0.05)], INK, 7)
    p.arc(cx + toward * r * 0.04, cy + r * 0.48, r * 0.09, r * 0.09, 100, 260 if toward > 0 else 280, INK, 6)  # nose
    p.arc(cx, cy + r * 0.83, r * 0.2, r * 0.1, 200, 340, INK, 8)  # frown
    for side in (-1, 1):
        p.ell(cx + side * r * 1.0, cy + r * 0.42, r * 0.07, r * 0.07, GOLD, 5)


def option_bigheads() -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), WALL)
    p = Pen(img)
    set_and_bubble(p)
    bighead(p, 285, 660, 215, SKIN1, "bun", 1)
    bighead(p, 800, 690, 205, SKIN2, "long", -1)
    desk_and_key(p)
    speech(p, (40, 215, 560, 335), (260, 420), "That's MY room.")
    return finish(img)


# ----------------------------------------------------------------------------------------------------------------
# 3. Cats


def cat(p: Pen, cx, cy, r, fur, stripe, look, toward):
    g = toward * 0.08 * r
    p.poly([(cx - r * 1.0, 1060), (cx - r * 0.75, cy + r * 0.85), (cx + r * 0.75, cy + r * 0.85), (cx + r * 1.0, 1060)],
           RED if look == "scarf" else YELLOW)
    for side in (-1, 1):  # ears
        p.poly([(cx + side * r * 0.25, cy - r * 0.85), (cx + side * r * 0.85, cy - r * 1.25), (cx + side * r * 0.92, cy - r * 0.35)],
               fur, 8)
        p.poly([(cx + side * r * 0.42, cy - r * 0.78), (cx + side * r * 0.78, cy - r * 1.05), (cx + side * r * 0.8, cy - r * 0.5)],
               (236, 150, 150), 0)
    p.ell(cx, cy, r * 1.08, r * 0.95, fur)
    if stripe:
        for k in (-1, 0, 1):
            p.line([(cx + k * r * 0.18, cy - r * 0.92), (cx + k * r * 0.14, cy - r * 0.62)], stripe, 12)
    p.ell(cx, cy + r * 0.42, r * 0.42, r * 0.3, (250, 244, 236), 0)  # muzzle
    for side in (-1, 1):
        ex = cx + side * r * 0.4
        p.ell(ex, cy + r * 0.0, r * 0.22, r * 0.2, (190, 214, 92), 6)
        p.ell(ex + g, cy + r * 0.02, r * 0.05, r * 0.16, INK, 0)  # slit pupil
        # half-shut angry lid
        p.d.chord([(ex - r * 0.24) * S, (cy - r * 0.22) * S, (ex + r * 0.24) * S, (cy + r * 0.22) * S], 180, 360, fill=fur)
        p.line([(ex - side * r * 0.24, cy - r * 0.02), (ex + side * r * 0.24, cy - r * 0.12)], INK, 9)
        for k in (-1, 0, 1):  # whiskers
            p.line([(cx + side * r * 0.42, cy + r * (0.45 + 0.08 * k)), (cx + side * r * 1.15, cy + r * (0.38 + 0.16 * k))],
                   INK, 4)
    p.poly([(cx - r * 0.09, cy + r * 0.3), (cx + r * 0.09, cy + r * 0.3), (cx, cy + r * 0.4)], (226, 110, 128), 4)
    p.arc(cx - r * 0.09, cy + r * 0.58, r * 0.09, r * 0.07, 200, 340, INK, 6)
    p.arc(cx + r * 0.09, cy + r * 0.58, r * 0.09, r * 0.07, 200, 340, INK, 6)
    if look == "glasses":
        for side in (-1, 1):
            p.ell(cx + side * r * 0.4, cy, r * 0.29, r * 0.27, None, 8)
        p.line([(cx - r * 0.11, cy - r * 0.02), (cx + r * 0.11, cy - r * 0.02)], INK, 7)
    else:  # earrings on the ears, and a flower
        p.ell(cx - r * 0.86, cy - r * 0.32, r * 0.07, r * 0.07, GOLD, 5)
        p.ell(cx + r * 0.86, cy - r * 0.32, r * 0.07, r * 0.07, GOLD, 5)


def option_cats() -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), WALL)
    p = Pen(img)
    set_and_bubble(p)
    cat(p, 290, 690, 215, (232, 146, 72), (186, 98, 40), "scarf", 1)
    cat(p, 795, 715, 205, (150, 150, 160), None, "glasses", -1)
    desk_and_key(p)
    speech(p, (40, 215, 560, 335), (270, 430), "That's MY room.")
    return finish(img)


def main():
    OUT.mkdir(exist_ok=True)
    options = [("Open Peeps (hand-drawn library)", option_peeps()), ("Big heads (code)", option_bigheads()),
               ("Cats (code)", option_cats())]
    for name, img in zip(("peeps", "bigheads", "cats"), (o[1] for o in options)):
        img.save(OUT / f"chars-{name}.png")
    tw, th = 486, 864
    sheet = Image.new("RGB", (3 * (tw + 20) + 20, th + 100), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(AVENIR, 30, index=0)
    for i, (label, img) in enumerate(options):
        x = 20 + i * (tw + 20)
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, 80))
        dr.text((x + tw / 2, 42), label, font=f, fill=(30, 30, 30), anchor="mm")
    sheet.save(OUT / "chars-options.png")
    print("wrote", OUT / "chars-options.png")


if __name__ == "__main__":
    main()
