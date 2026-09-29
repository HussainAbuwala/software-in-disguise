"""Mira's desk corner (added for Episode 03's remake): a desk by the window, a wall clock, and a door on the right.

World layout: floor y 1380. Mira sits at SEAT facing right, the desk in front of her (top at DESK_TOP), the notepad
flat on it and a wedding invitation standing at its far end. The door (x DOOR) is where people lean in; the sign
spot (SIGN_AT) is on the wall between the desk and the door.

Set interface (used by kit.episode.scene): wall_color(time), back(c, time, t=, behind=, **kw), front(c, **kw).
"""

from __future__ import annotations

from .canvas import ALERT, HAND, HEAVY, INK, MUSTARD, PAPER, Canvas, ease
from .living_room import TIMES, _clock

SEAT = (470, 1110)  # seated pose point (shoulders); the hip sits ~170 lower, on the chair
DESK = (600, 930)  # desk top x range
DESK_TOP = 1236
PEN_AT = (700, DESK_TOP - 6)  # where the pen meets the notepad
CLOCK_AT = (720, 690)
DOOR = (1060, 1260)
SIGN_AT = (905, 900)
WOOD = (150, 110, 80)
DESK_WOOD = (176, 128, 88)


def wall_color(time: str = "day"):
    return TIMES[time]["wall"]


def _window(c: Canvas, time: str, t: float):
    x0, y0, x1, y1 = 70, 600, 330, 900
    c.rect(x0, y0, x1, y1, fill=TIMES[time]["sky"][0])
    if time == "night":
        c.circle(260, 660, 30, fill=(240, 234, 210), outline=None)
        c.circle(275, 650, 27, fill=TIMES["night"]["sky"][0], outline=None)
        for sx, sy in ((120, 650), (170, 760), (230, 820), (300, 740)):
            c.circle(sx, sy, 4, fill=(240, 234, 210), outline=None)
    elif time == "morning":
        c.chord(140, 780, 270, 910, 180, 360, fill=(250, 190, 90), outline=None)
    elif time == "evening":
        c.chord(130, 800, 260, 930, 180, 360, fill=(252, 214, 120), outline=None)
    c.rect(x0, y0, x1, y1, width=7)
    c.line([(200, y0), (200, y1)], width=7)
    c.rect(50, 890, 350, 916, fill=PAPER)


def _door(c: Canvas, open_: bool):
    d0, d1 = DOOR
    top = 820
    c.rect(d0 - 22, top - 22, d1 + 22, 1380, fill=WOOD)
    if open_:
        c.rect(d0, top, d1, 1380, fill=(70, 74, 96))
        c.poly([(d1, top), (d1 - 60, top + 30), (d1 - 60, 1360), (d1, 1380)], fill=(176, 132, 96))
    else:
        c.rect(d0, top, d1, 1380, fill=(176, 132, 96))
        c.circle(d0 + 30, 1110, 12, fill=MUSTARD, width=4)


def wall_sign(c: Canvas, lines: tuple, k: float = 1.0):
    """A handwritten sheet taped to the wall. `k` 0..1 swings it up into place as it's taped."""
    if k <= 0:
        return
    x, y = SIGN_AT
    w, h = 170, 210
    drop = (1 - ease(k)) * 40
    c.rect(x - w / 2, y - h / 2 + drop, x + w / 2, y + h / 2 + drop, fill=PAPER, width=5)
    for dx in (-w / 2 + 18, w / 2 - 18):  # tape strips at the top corners
        c.rect(x + dx - 22, y - h / 2 - 12 + drop, x + dx + 22, y - h / 2 + 12 + drop, fill=(236, 226, 180), width=3)
    first, *rest = lines
    c.text(x, y - h / 2 + 56 + drop, first, 56, fill=ALERT, weight=HAND)
    for i, line in enumerate(rest):
        c.text(x, y - h / 2 + 122 + i * 42 + drop, line, 32, weight=HAND)


def _chair(c: Canvas):
    x, y = SEAT
    seat_y = y + 172
    c.rect(x - 100, y - 20, x - 74, seat_y + 10, fill=WOOD, radius=8)  # back
    c.rect(x - 100, seat_y, x + 90, seat_y + 22, fill=WOOD, radius=6)
    for lx in (x - 92, x + 80):
        c.line([(lx, seat_y + 22), (lx, 1380)], fill=WOOD, width=12)


def back(c: Canvas, time: str = "day", t: float = 0.0, behind=None, clock: float | None = None, door: str | None = None,
         sign: tuple | None = None, legs=None, **_):
    """Wall, window, clock, door and chair. `legs(c)` draws the seated character's legs (under the desk);
    `behind(c)` draws anyone behind the desk."""
    tod = TIMES[time]
    c.rect(-2000, -2000, 3000, 1380, fill=tod["wall"], outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=tod["floor"], outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    _window(c, time, t)
    if clock is not None:
        _clock(c, clock, CLOCK_AT)
    if door:
        _door(c, door == "open")
    if sign:
        wall_sign(c, *sign)
    _chair(c)
    if legs:
        legs(c)
    if behind:
        behind(c)


def invitation(c: Canvas, x: float, y: float, scale: float = 1.0):
    """A wedding invitation standing on the desk; (x, y) is its bottom center."""
    k = scale
    w, h = 150 * k, 150 * k
    c.rect(x - w / 2, y - h, x + w / 2, y, fill=(252, 244, 228), width=5)
    c.rect(x - w / 2 + 10 * k, y - h + 10 * k, x + w / 2 - 10 * k, y - 10 * k, outline=MUSTARD, width=4)
    c.text(x, y - h + 42 * k, "PRIYA", 30 * k, weight=HEAVY)
    c.text(x, y - h + 76 * k, "& SAM", 30 * k, weight=HEAVY)
    for dx in (-12, 12):  # two rings
        c.circle(x + dx * k, y - 38 * k, 14 * k, outline=MUSTARD, width=5)


def front(c: Canvas, notepad: bool = True, invite: bool = True, **_):
    """The desk, drawn over the seated character's legs, with the notepad lying on it and the invitation."""
    x0, x1 = DESK
    for lx in (x0 + 30, x1 - 30):
        c.rect(lx - 12, DESK_TOP, lx + 12, 1380, fill=DESK_WOOD, width=6)
    c.rect(x0, DESK_TOP, x1, DESK_TOP + 28, fill=DESK_WOOD, width=7)
    if notepad:  # lying flat, seen almost edge-on: a thin wedge of paper
        c.poly([(620, DESK_TOP), (770, DESK_TOP), (754, DESK_TOP - 14), (636, DESK_TOP - 14)], fill=PAPER, width=5)
    if invite:
        invitation(c, 815, DESK_TOP)
    c.line([(x0, DESK_TOP), (x1, DESK_TOP)], fill=INK, width=7)
