"""Cast sheet for the Episode 1 remake: the family in the riso look, each in their key expression.

Run: ../../.venv/bin/python cast_sheet.py  →  deliverables/cast-sheet.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit.riso import Sketch, composite  # noqa: E402
from kit.riso_cast import AUNT, DAD, GRANDPA, MOM, PRIYA, person  # noqa: E402

OUT = Path(__file__).parent / "deliverables"

POSES = [
    (GRANDPA, "confused", (-0.6, 0.0), 0.0, '"…On what?"'),
    (GRANDPA, "delighted", (0.0, 0.0), 0.0, '"Oh!"'),
    (AUNT, "beaming", (0.0, 0.0), 0.0, '"Congratulations!!"'),
    (MOM, "gasp", (0.0, -0.2), 0.0, '"Oh my God!"'),
    (DAD, "flat", (0.3, 0.6), 0.0, '"Mm. Nice."'),
    (PRIYA, "excited", (0.2, 0.0), 0.0, '"I\'m engaged!"'),
]


def bust(who, expr, gaze, turn, seed):
    sk = Sketch(seed=seed)
    cx, cy, R = 540, 860, 210
    person(sk, who, cx, cy, R, expr, gaze=gaze, turn=turn, bottom=1700)
    return composite(sk).crop((40, 300, 1040, 1700))


def main():
    OUT.mkdir(exist_ok=True)
    tiles = []
    for i, (p, expr, gaze, turn, line) in enumerate(POSES):
        img = bust(p, expr, gaze, turn, seed=10 + i)
        img.save(OUT / f"cast-{p.name.lower()}-{expr}.png")
        tiles.append((f"{p.name} · {line}", img))
        print("drew", p.name, expr)
    tw, th = 500, 700
    cols = 3
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 20, 2 * (th + 70) + 20), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 30, index=0)
    for i, (label, img) in enumerate(tiles):
        x = 20 + (i % cols) * (tw + 20)
        y = 20 + (i // cols) * (th + 70)
        dr.text((x + tw / 2, y + 22), label, font=f, fill=(30, 30, 30), anchor="mm")
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, y + 50))
    sheet.save(OUT / "cast-sheet.png")
    print("wrote", OUT / "cast-sheet.png")


if __name__ == "__main__":
    main()
