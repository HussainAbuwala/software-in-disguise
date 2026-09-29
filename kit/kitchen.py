"""Mom's kitchen (added for Episode 03's remake), seen in the top half of a phone-call split screen.

World layout: floor y 1380, counter top at COUNTER_TOP along the back wall, a stove with a steaming pot, and upper
cabinets. Mom stands at MOM_AT in front of the counter.

Set interface (used by kit.episode.scene): wall_color(time), back(c, time, t=, behind=, **kw), front(c, **kw).
"""

from __future__ import annotations

import math

from .canvas import PAPER, Canvas

WALL = (214, 230, 214)
FLOOR = (200, 184, 160)
COUNTER_TOP = 1160
MOM_AT = (560, 1380)
CABINET = (226, 214, 190)
STEEL = (170, 174, 180)


def wall_color(time: str = "day"):
    return WALL


def back(c: Canvas, time: str = "day", t: float = 0.0, behind=None, **_):
    c.rect(-2000, -2000, 3000, 1380, fill=WALL, outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=FLOOR, outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    for i in range(-2, 6):  # tiled splashback
        for j in range(3):
            c.rect(i * 180 + (90 if j % 2 else 0), 920 + j * 80, i * 180 + 170 + (90 if j % 2 else 0), 990 + j * 80,
                   fill=(236, 240, 232), width=3)
    for x in (-40, 280, 760, 1080):  # upper cabinets
        c.rect(x, 560, x + 280, 820, fill=CABINET, width=7)
        c.circle(x + 250, 790, 9, fill=STEEL, width=4)
    c.rect(-2000, COUNTER_TOP, 3000, 1380, fill=CABINET, width=7)  # base cabinets
    c.rect(-2000, COUNTER_TOP - 26, 3000, COUNTER_TOP + 4, fill=(150, 140, 130), width=7)
    # Stove and a pot, steaming.
    c.rect(800, COUNTER_TOP - 34, 1060, COUNTER_TOP - 22, fill=(60, 60, 64), outline=None)
    c.rect(850, COUNTER_TOP - 150, 1010, COUNTER_TOP - 30, fill=STEEL, width=7, radius=10)
    c.rect(830, COUNTER_TOP - 162, 1030, COUNTER_TOP - 140, fill=(150, 154, 160), width=6, radius=8)
    for i in range(3):
        k = (t / 1.4 + i / 3) % 1.0
        sx = 890 + i * 45 + 14 * math.sin((t + i) * 3)
        c.circle(sx, COUNTER_TOP - 190 - k * 140, 16 + 10 * k, fill=PAPER, outline=None)
    if behind:
        behind(c)


def front(c: Canvas, **_):
    pass
