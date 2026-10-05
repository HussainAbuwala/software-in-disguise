"""Cast sheet for "The Last Room" in the big-head style.

Run: ../../.venv/bin/python cast_sheet.py  →  deliverables/cast-sheet.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit.bighead import CLERK, LATA, MEENA, PRIYA, PAPER, Pen, character, finish, new_frame  # noqa: E402

OUT = Path(__file__).parent / "deliverables"

POSES = [
    (MEENA, "furious", (0.8, 0), "point", "Meena · furious"),
    (MEENA, "triumphant", (0, 0), "hands_up", "Meena · \"Mine!\""),
    (LATA, "smug", (-0.8, 0), "crossed", "Lata · smug"),
    (LATA, "shocked", (0, 0), "rest", "Lata · \"Twice?!\""),
    (CLERK, "deadpan", (0, 0.3), "rest", "Clerk · deadpan"),
    (PRIYA, "explaining", (0.3, 0), "phone", "Priya · explaining"),
]


def main():
    OUT.mkdir(exist_ok=True)
    tiles = []
    for i, (c, expr, gaze, arm, label) in enumerate(POSES):
        img = new_frame(PAPER)
        p = Pen(img, boil=i)
        character(p, c, 540, 760, 300, expr, gaze=gaze, arm=arm, bottom=1500)
        tiles.append((label, finish(img).crop((90, 260, 990, 1500))))
    tw, th = 450, 620
    sheet = Image.new("RGB", (3 * (tw + 20) + 20, 2 * (th + 70) + 20), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 28, index=0)
    for i, (label, img) in enumerate(tiles):
        x, y = 20 + (i % 3) * (tw + 20), 20 + (i // 3) * (th + 70)
        dr.text((x + tw / 2, y + 22), label, font=f, fill=(30, 30, 30), anchor="mm")
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, y + 50))
    sheet.save(OUT / "cast-sheet.png")
    print("wrote", OUT / "cast-sheet.png")


if __name__ == "__main__":
    main()
