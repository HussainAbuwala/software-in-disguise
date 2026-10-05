"""Format test (2026-10-05): the first frame of the "glitch in a real app" idea.

Two aunts, one wedding hotel, one room left: both booked it at 9:41 and both got a confirmation. People and set are
riso-printed; the phone screens are crisp and realistic (kit/phone.py). Note the booking IDs differ by one: the app
really did create two bookings.

Run: ../../.venv/bin/python format_test.py  →  deliverables/format-hybrid-frame1.png
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from kit.phone import BG, GREEN, GREY, INK, LINE, ORANGE, WHITE, BLUE, ScreenDraw, phone  # noqa: E402
from kit.riso import Sketch, bubble, composite, ellipse_pts, path, round_rect_pts  # noqa: E402
from kit.riso_cast import AUNT, EXPRESSIONS, MOM, person  # noqa: E402

OUT = Path(__file__).parent / "deliverables"

EXPRESSIONS.setdefault("glare", dict(brow=(0.06, 0.06), tilt=-0.09, lid=0.42, mouth="flat", smile=0.0))
AUNT2 = replace(MOM, name="Aunt2", glasses=True, garment="polo", age=0.5)


def confirmation(booking_id: str):
    def draw(d: ScreenDraw):
        d.rect(0, 0, 390, 844, BG)
        d.status_bar("9:41")
        d.text(20, 62, "‹ Bookings", 17, "Regular", BLUE)
        d.circle(195, 160, 44, GREEN)
        d.line([(175, 160), (189, 175), (216, 146)], WHITE, 7)
        d.text(195, 222, "Booking confirmed", 27, "Bold", INK, "ma")
        d.text(195, 260, "Marigold Hall & Rooms", 17, "Regular", GREY, "ma")
        d.rect(20, 302, 370, 572, WHITE, r=14)
        d.rect(36, 318, 186, 346, (255, 239, 214), r=8)
        d.text(111, 324, "Last room left!", 14, "Semibold", ORANGE, "ma")
        d.text(36, 362, "Deluxe Room 204", 21, "Semibold")
        d.text(36, 394, "Sat, Nov 14 · 1 night · 2 guests", 15, "Regular", GREY)
        d.line([(36, 436), (354, 436)], LINE, 1)
        for i, (k, v) in enumerate((("Booked", "Today, 9:41 PM"), ("Booking ID", booking_id), ("Paid", "$129.00"))):
            y = 452 + i * 36
            d.text(36, y, k, 16, "Regular", GREY)
            d.text(354, y, v, 16, "Semibold", INK, "ra")
        d.rect(20, 742, 370, 794, BLUE, r=14)
        d.text(195, 757, "View booking", 18, "Semibold", WHITE, "ma")
    return draw


def main():
    sk = Sketch(seed=31)
    # Reception: wall, a sign, the key board with one empty hook, the desk
    sk.halftone([(0, 0), (1080, 0), (1080, 1100), (0, 1100)], "fill2", cell=11, angle=0,
                shade=lambda x, y: 0.14 if (int(x) // 70) % 2 == 0 else 0.04)
    sign = round_rect_pts(330, 70, 750, 160, 14, 4)
    sk.shape(sign, "fill")
    sk.text((540, 115), "RECEPTION", "mono", 46, "line")
    # Desk top edge
    desk = [(0, 1040), (1080, 1040), (1080, 1190), (0, 1190)]
    sk.shape(desk, "fill", 5)
    # The two aunts, glaring at each other
    person(sk, AUNT, 280, 600, 165, "glare", gaze=(1.0, 0.1), turn=0.35, bottom=1045)
    person(sk, AUNT2, 800, 630, 160, "glare", gaze=(-1.0, 0.1), turn=-0.35, bottom=1045)
    bubble(sk, (40, 215, 560, 335), (250, 345), "That's MY room.", 58)
    # The one key, on the desk between them
    key = ellipse_pts(520, 1075, 22, 22, 20)
    sk.shape(key, "fill2", 4.5)
    sk.stroke([(540, 1075), (610, 1075)], width=7)
    sk.stroke([(590, 1075), (590, 1092)], width=5)
    sk.stroke([(604, 1075), (604, 1088)], width=5)
    tagp = round_rect_pts(500, 1100, 556, 1140, 6, 3)
    sk.shape(tagp, "fill", 3.5)
    sk.text((528, 1120), "204", "mono", 21, "line")
    img = composite(sk)
    # Crisp phones over the print: identical confirmations, IDs one apart
    phone(img, 290, 1490, 370, confirmation("MH-48213"), angle=4)
    phone(img, 790, 1490, 370, confirmation("MH-48214"), angle=-4)
    OUT.mkdir(exist_ok=True)
    img.save(OUT / "format-hybrid-frame1.png")
    print("wrote", OUT / "format-hybrid-frame1.png")


if __name__ == "__main__":
    main()
