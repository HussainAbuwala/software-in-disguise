"""A two-floor café seen in cross-section, one floor stacked on the other (made for the 9:16 frame).

World layout: building x 0..1250. Upper floor surface y UP=1000, ground floor surface y GROUND=1760, roof ROOF=300.
A glass elevator runs up the left side, the stairs run down the right side from the upper floor to the ground floor.
Both floors have an identical window table at the same x, which is the joke of Episode 06.

Set interface (used by kit.episode.scene): wall_color(time), back(c, time, t=, behind=, **kw), front(c, **kw).
`behind` draws whoever is inside the elevator car (between the glass and the frame).
"""

from __future__ import annotations

from .canvas import INK, MUSTARD, PAPER, TEAL, Canvas

ROOF, UP, GROUND = 300, 1000, 1760
SLAB = 60
WIDTH = 1250

SHAFT = (30, 250)  # elevator shaft x range
CAR_H = 600
CAR_UP = UP - CAR_H  # car top y when stopped at the upper floor
CAR_GROUND = GROUND - CAR_H
STAIRS_TOP = (870, UP)
STAIRS_BOTTOM = (1225, GROUND)

SEAT_X = 590
TABLE_X = 740
SEAT_UP = (SEAT_X, UP - 230)  # seated hip positions
SEAT_GROUND = (SEAT_X, GROUND - 230)
SIGN_UP = (375, UP - 575)  # the "1" sign on the upper floor
SIGN_GROUND = (375, GROUND - 575)  # the "G" sign, in the same spot on the ground floor (above the entrance)
DOOR = (300, 450)  # entrance door x range, ground floor

WALL_UP = (241, 228, 206)
WALL_GROUND = (234, 216, 192)
WOOD = (150, 110, 80)
SKY = (160, 205, 222)
GLASS = (210, 232, 240)


def wall_color(time: str = "day"):
    return SKY


def _window(c: Canvas, x0, x1, floor):
    y0, y1 = floor - 600, floor - 290
    c.rect(x0, y0, x1, y1, fill=SKY)
    c.circle(x0 + 90, y0 + 110, 40, fill=PAPER, outline=None)
    c.circle(x0 + 140, y0 + 100, 52, fill=PAPER, outline=None)
    c.rect(x0, y0, x1, y1, width=7)
    c.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], width=7)
    c.rect(x0 - 20, y1, x1 + 20, y1 + 24, fill=PAPER)


def _lamp(c: Canvas, x, ceiling):
    c.line([(x, ceiling), (x, ceiling + 90)], width=4)
    c.chord(x - 45, ceiling + 70, x + 45, ceiling + 150, 180, 360, fill=MUSTARD, width=5)


def _sign(c: Canvas, x, y, label):
    c.circle(x, y, 58, fill=TEAL, width=7)
    c.text(x, y + 2, label, 70, fill=PAPER, weight=8)


def _stairs(c: Canvas):
    (x0, y0), (x1, y1) = STAIRS_TOP, STAIRS_BOTTOM
    n = 10
    steps = []
    for i in range(n):
        xa = x0 + (x1 - x0) * i / n
        xb = x0 + (x1 - x0) * (i + 1) / n
        ya = y0 + (y1 - y0) * i / n
        yb = y0 + (y1 - y0) * (i + 1) / n
        steps += [(xa, ya), (xb, ya), (xb, yb)]
    c.poly([(x0, y0)] + steps + [(x1, y1 + 10), (x0, y0 + 60)], fill=(196, 170, 138))
    c.line([(x0 - 10, y0 - 150), (x1 - 10, y1 - 150)], fill=WOOD, width=10)  # handrail
    for i in range(0, n + 1, 3):
        px = x0 + (x1 - x0) * i / n
        py = y0 + (y1 - y0) * i / n
        c.line([(px, py), (px - 10, py - 150)], fill=WOOD, width=6)


def _chair(c: Canvas, seat):
    """Chair seen from the side: back, seat and two legs. Seated characters cover most of it."""
    x, y = seat
    floor = y + 230
    c.rect(x - 85, y - 150, x - 60, y + 40, fill=WOOD, radius=8)
    c.rect(x - 85, y + 30, x + 50, y + 52, fill=WOOD, radius=6)
    for lx in (x - 78, x + 36):
        c.line([(lx, y + 52), (lx, floor)], fill=WOOD, width=12)


def car_y(k: float) -> float:
    """Car top y for elevator progress k: 0 = ground floor, 1 = upper floor."""
    return CAR_GROUND + (CAR_UP - CAR_GROUND) * k


def back(c: Canvas, time: str = "day", t: float = 0.0, behind=None, elevator: float = 1.0, **_):
    # Street and sky around the building.
    c.rect(-3000, GROUND, 4500, 5000, fill=(170, 168, 162), outline=None)
    c.line([(-3000, GROUND), (4500, GROUND)], width=7)
    # Upper floor.
    c.rect(0, ROOF, WIDTH, UP, fill=WALL_UP)
    c.rect(0, UP - 26, WIDTH, UP, fill=(200, 170, 130), outline=None)
    _window(c, 470, 850, UP)
    _lamp(c, 660, ROOF)
    _sign(c, *SIGN_UP, "1")
    # Floor slab between the floors (open above the stairwell).
    c.rect(0, UP, STAIRS_TOP[0], UP + SLAB, fill=WOOD)
    # Ground floor.
    c.rect(0, UP + SLAB, WIDTH, GROUND, fill=WALL_GROUND)
    c.rect(STAIRS_TOP[0], UP, WIDTH, UP + SLAB, fill=WALL_GROUND, outline=None)
    c.rect(0, GROUND - 26, WIDTH, GROUND, fill=(200, 170, 130), outline=None)
    _window(c, 560, 850, GROUND)
    _lamp(c, 660, UP + SLAB)
    _sign(c, *SIGN_GROUND, "G")
    # Entrance door with daylight behind the glass.
    d0, d1 = DOOR
    c.rect(d0, GROUND - 440, d1, GROUND, fill=GLASS, width=7)
    c.line([((d0 + d1) / 2, GROUND - 440), ((d0 + d1) / 2, GROUND)], width=6)
    c.rect(d0 - 10, GROUND - 510, d1 + 10, GROUND - 450, fill=INK, outline=None, radius=8)
    c.text((d0 + d1) / 2, GROUND - 480, "ENTRANCE", 30, fill=PAPER, weight=0)
    _stairs(c)
    # Elevator shaft and glass car.
    s0, s1 = SHAFT
    c.rect(s0, ROOF, s1, GROUND, fill=(214, 206, 196), width=7)
    for y in (UP - 620, GROUND - 620):  # landing openings
        c.rect(s0 + 14, y, s1 - 14, y + 620, fill=(226, 220, 212), outline=None)
    cy = car_y(elevator)
    c.rect(s0 + 20, cy, s1 - 20, cy + CAR_H, fill=GLASS, width=6)
    if behind:
        behind(c)
    c.rect(s0 + 20, cy, s1 - 20, cy + CAR_H, width=9)
    c.line([(s0 + 20, cy + CAR_H * 0.55), (s1 - 20, cy + CAR_H * 0.55)], fill=(150, 170, 180), width=5)
    # Building outline and roof.
    c.rect(0, ROOF, WIDTH, GROUND, width=9)
    c.rect(-30, ROOF - 50, WIDTH + 30, ROOF, fill=(120, 96, 80))
    _chair(c, SEAT_UP)
    _chair(c, SEAT_GROUND)


def _table(c: Canvas, floor):
    top = floor - 190
    c.line([(TABLE_X, top), (TABLE_X, floor)], width=16)
    c.ellipse(TABLE_X - 70, floor - 20, TABLE_X + 70, floor + 6, fill=INK, outline=None)
    c.ellipse(TABLE_X - 125, top - 22, TABLE_X + 125, top + 22, fill=PAPER, width=7)
    c.rect(TABLE_X + 30, top - 70, TABLE_X + 80, top - 10, fill=PAPER, radius=8, width=6)  # coffee cup
    c.arc(TABLE_X + 70, top - 60, TABLE_X + 100, top - 28, 270, 90, width=6)


def front(c: Canvas, **_):
    _table(c, UP)
    _table(c, GROUND)
