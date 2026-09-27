"""A small neighbourhood restaurant: three people side by side at one table, facing the camera (Episode 07).

World layout matches the living room couch so shots line up: seats at x 330 / 575 / 820 with hips at y 1130, the table
top at y ~1235 hides everyone's lap (like the couch front), floor from y 1380.

Set interface (used by kit.episode.scene): wall_color(time), back(c, time, t=, behind=, **kw), front(c, **kw).
"""

from __future__ import annotations

from .canvas import HEAVY, INK, MUSTARD, PAPER, TEAL, Canvas

SEATS = (330, 575, 820)
SEAT_Y = 1130

WALL_WARM = (226, 196, 160)
WOOD = (150, 110, 80)
CLOTH = (250, 246, 236)
NIGHT = (38, 48, 82)


def wall_color(time: str = "night"):
    return WALL_WARM


def _string_lights(c: Canvas, y: float):
    c.line([(-300, y), (140, y + 40), (575, y + 10), (1010, y + 40), (1450, y)], fill=INK, width=3)
    for i, x in enumerate(range(-240, 1420, 90)):
        dip = 40 * (1 - abs(((x + 300) % 435) / 217.5 - 1))
        c.circle(x, y + 12 + dip * 0.9, 11, fill=MUSTARD if i % 2 else (250, 214, 150), width=3)


def back(c: Canvas, time: str = "night", t: float = 0.0, behind=None, **_):
    c.rect(-2000, -2000, 3000, 1380, fill=WALL_WARM, outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=(120, 84, 60), outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    # Window onto the evening street, with the restaurant's name painted on the glass.
    c.rect(200, 560, 950, 900, fill=NIGHT, width=8)
    c.line([(575, 560), (575, 900)], width=7)
    c.text(575, 610, "BANGKOK KITCHEN", 44, fill=MUSTARD, weight=HEAVY)
    for sx, sy in ((300, 820), (420, 760), (720, 790), (860, 740)):
        c.circle(sx, sy, 5, fill=(240, 234, 210), outline=None)
    # Plants either side and a string of lights above.
    for px in (60, 1090):
        c.rect(px - 50, 1250, px + 50, 1380, fill=(190, 120, 80), width=6)
        for dx, dy, r in ((0, -60, 55), (-40, -20, 42), (42, -24, 44)):
            c.circle(px + dx, 1250 + dy, r, fill=TEAL, width=6)
    _string_lights(c, 470)
    if behind:
        behind(c)


def front(c: Canvas, **_):
    """The table, drawn over the seated characters' laps."""
    c.rect(90, 1225, 1060, 1390, fill=CLOTH, radius=10)
    c.rect(90, 1225, 1060, 1255, fill=(236, 228, 214), radius=10)
    for x in (230, 470, 700, 930):  # water glasses
        c.rect(x - 18, 1170, x + 18, 1236, fill=(210, 232, 240), width=5, radius=4)
    c.rect(560, 1188, 590, 1236, fill=PAPER, width=4)  # a small number stand
    c.text(575, 1210, "7", 22, weight=HEAVY)
