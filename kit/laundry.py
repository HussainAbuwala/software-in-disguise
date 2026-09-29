"""A laundry corner (added for Episode 03's remake): a front-loading washing machine and a basket.

World layout: floor y 1380; the machine spans MACHINE x, its round door centered at DOOR_C; the basket sits left of it.

Set interface (used by kit.episode.scene): wall_color(time), back(c, time, t=, behind=, **kw), front(c, **kw).
"""

from __future__ import annotations

from .canvas import ALERT, INK, PAPER, TEAL, Canvas

WALL = (206, 214, 222)
FLOOR = (176, 170, 164)
MACHINE = (560, 860, 960)  # x0, x1, top
DOOR_C = (710, 1190)
CLOTHES = [(200, 60, 70), (70, 120, 190), (227, 178, 60), (236, 230, 220), TEAL]


def wall_color(time: str = "night"):
    return WALL


def back(c: Canvas, time: str = "night", t: float = 0.0, behind=None, done: bool = True, **_):
    c.rect(-2000, -2000, 3000, 1380, fill=WALL, outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=FLOOR, outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    c.rect(560, 700, 900, 730, fill=PAPER, width=6)  # a shelf with detergent
    c.rect(600, 610, 670, 700, fill=TEAL, width=6, radius=8)
    c.rect(700, 640, 750, 700, fill=(230, 120, 60), width=6, radius=6)
    x0, x1, top = MACHINE
    c.rect(x0, top, x1, 1380, fill=(244, 244, 240), width=8, radius=16)
    c.line([(x0, top + 90), (x1, top + 90)], width=6)
    c.circle(x0 + 60, top + 45, 22, fill=(210, 210, 214), width=5)  # dial
    c.rect(x1 - 150, top + 22, x1 - 40, top + 68, fill=INK, radius=6, outline=None)  # display
    c.text(x1 - 95, top + 46, "END" if done else "0:02", 30, fill=ALERT if done else (120, 230, 140), weight=8)
    cx, cy = DOOR_C
    c.circle(cx, cy, 118, fill=(200, 204, 210), width=8)
    c.circle(cx, cy, 90, fill=(60, 66, 80), width=6)  # the drum, open and full
    for i, col in enumerate(CLOTHES[:4]):
        c.ellipse(cx - 70 + i * 30, cy - 10 + (i % 2) * 30, cx - 10 + i * 30, cy + 40 + (i % 2) * 30, fill=col, width=4)
    if behind:
        behind(c)


def basket(c: Canvas, x: float, y: float = 1380):
    c.poly([(x - 110, y - 150), (x + 110, y - 150), (x + 90, y), (x - 90, y)], fill=(214, 180, 120), width=7)
    for i in range(3):
        c.line([(x - 100 + i * 5, y - 110 + i * 40), (x + 100 - i * 5, y - 110 + i * 40)], fill=(170, 136, 86), width=5)
    for i, col in enumerate(CLOTHES):
        c.ellipse(x - 100 + i * 40, y - 190 + (i % 2) * 18, x - 30 + i * 40, y - 140, fill=col, width=4)


def front(c: Canvas, **_):
    basket(c, 250)
