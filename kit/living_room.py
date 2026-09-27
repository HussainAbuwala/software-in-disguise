"""The Dev/Mira/Jo living room. World coordinates are fixed so every episode's shots line up.

Layout (world units): couch spans x 100..1080, seat top y ~1230, floor from y 1380. The TV sits to the left of the
couch at x -320..0 with its power button at POWER_BUTTON. Seated characters sit at DEV_SEAT / MIRA_SEAT.
"""

from __future__ import annotations

import math

from .canvas import ALERT, FLOOR, INK, MUSTARD, PAPER, WALL, Canvas

TEAL_DARK = (32, 128, 116)

DEV_SEAT = (330, 1130)
MIRA_SEAT = (820, 1130)
POWER_BUTTON = (-45, 1163)
TV_SCREEN = (-283, 1002, -37, 1150)

COUCH = (150, 142, 132)
COUCH_DARK = (122, 115, 106)
WOOD = (150, 110, 80)

TIMES = {
    "day": dict(wall=WALL, floor=FLOOR, sky=[(160, 205, 222)]),
    "night": dict(wall=(176, 168, 158), floor=(150, 128, 104), sky=[(38, 48, 82)]),
    "morning": dict(wall=(244, 230, 210), floor=(204, 176, 142), sky=[(252, 222, 180)]),
    "evening": dict(wall=(236, 216, 192), floor=(192, 162, 128), sky=[(240, 168, 118)]),
}


def wall_color(time: str):
    return TIMES[time]["wall"]


RAIN_SKY = (120, 128, 140)


def _sky(c: Canvas, time: str, t: float):
    if time == "day":
        cx = 470 + (t * 6) % 200  # a slow cloud keeps the day frame alive
        for dx, r in ((0, 34), (38, 44), (80, 30)):
            c.circle(cx + dx, 680, r, fill=PAPER, outline=None)
    elif time == "night":
        c.circle(720, 640, 36, fill=(240, 234, 210), outline=None)
        c.circle(738, 628, 32, fill=TIMES["night"]["sky"][0], outline=None)
        for sx, sy in ((400, 620), (470, 700), (560, 610), (640, 760), (430, 800)):
            c.circle(sx, sy, 4, fill=(240, 234, 210), outline=None)
    elif time == "morning":
        c.chord(620, 780, 780, 940, 180, 360, fill=(250, 190, 90), outline=None)
    elif time == "evening":
        c.chord(440, 800, 600, 960, 180, 360, fill=(252, 214, 120), outline=None)  # the sun going down


def _rain(c: Canvas, x0, y0, x1, y1, t: float):
    c.rect(x0, y0, x1, y1, fill=RAIN_SKY)
    for i in range(26):  # falling streaks, wrapped inside the pane
        sx = x0 + 12 + (i * 53) % (x1 - x0 - 24)
        sy = y0 + ((i * 97 + t * 900) % (y1 - y0 - 40))
        c.line([(sx, sy), (sx - 8, sy + 34)], fill=(210, 220, 232), width=4)


def _window(c: Canvas, time: str, t: float, weather: str = "clear"):
    x0, y0, x1, y1 = 330, 560, 820, 880
    if weather == "rain":
        _rain(c, x0, y0, x1, y1, t)
    else:
        c.rect(x0, y0, x1, y1, fill=TIMES[time]["sky"][0])
        _sky(c, time, t)
    c.rect(x0, y0, x1, y1, width=7)
    c.line([(575, y0), (575, y1)], width=7)
    c.rect(300, 870, 850, 900, fill=PAPER)


def _picture(c: Canvas):
    c.rect(880, 600, 1010, 760, fill=PAPER)
    c.poly([(900, 740), (945, 660), (990, 740)], fill=(42, 157, 143), width=5)
    c.circle(965, 645, 14, fill=(227, 178, 60), width=4)


def _tv(c: Canvas, tv: str, t: float):
    c.rect(-320, 1175, 0, 1390, fill=WOOD)
    c.line([(-160, 1200), (-160, 1370)], width=5)
    c.rect(-295, 990, -25, 1175, fill=(40, 40, 44), radius=6)
    x0, y0, x1, y1 = TV_SCREEN
    if tv == "off":
        c.rect(x0, y0, x1, y1, fill=(62, 64, 70), width=4)
        c.line([(x0 + 30, y0 + 20), (x0 + 70, y0 + 20)], fill=(90, 92, 100), width=6)
    elif tv == "golf":
        c.rect(x0, y0, x1, y1, fill=(150, 200, 235), width=4)
        c.rect(x0, y0 + 80, x1, y1, fill=(110, 170, 90), outline=None)
        c.ellipse(x0 + 60, y0 + 95, x0 + 200, y0 + 135, fill=(140, 200, 110), outline=None)
        c.line([(x0 + 150, y0 + 115), (x0 + 150, y0 + 55)], width=4)
        c.poly([(x0 + 150, y0 + 55), (x0 + 185, y0 + 65), (x0 + 150, y0 + 75)], fill=(209, 73, 91), width=3)
        c.rect(x0, y0, x1, y1, width=4)
    button_on = tv != "off"
    c.circle(*POWER_BUTTON, 7, fill=(120, 220, 120) if button_on else (209, 73, 91), width=3)


CLOCK = (205, 700)
DOOR = (1390, 1600)  # front door x range, right of the couch (outside every camera used before Episode 07)


def _clock(c: Canvas, minutes: float):
    """Wall clock; `minutes` since midnight (19 * 60 = 7:00 PM)."""
    x, y = CLOCK
    c.circle(x, y, 66, fill=PAPER, width=8)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        c.line([(x + 50 * math.sin(a), y - 50 * math.cos(a)), (x + 58 * math.sin(a), y - 58 * math.cos(a))], width=5)
    ah = (minutes / 60 % 12) / 12 * 2 * math.pi
    am = (minutes % 60) / 60 * 2 * math.pi
    c.line([(x, y), (x + 30 * math.sin(ah), y - 30 * math.cos(ah))], width=9)
    c.line([(x, y), (x + 46 * math.sin(am), y - 46 * math.cos(am))], width=6)
    c.circle(x, y, 7, fill=INK, outline=None)


def _door(c: Canvas, open_: bool):
    d0, d1 = DOOR
    top = 820
    c.rect(d0 - 22, top - 22, d1 + 22, 1380, fill=WOOD)
    if open_:
        c.rect(d0, top, d1, 1380, fill=(70, 74, 96))  # the dark hallway outside
        c.poly([(d0, top), (d0 + 70, top + 30), (d0 + 70, 1360), (d0, 1380)], fill=(176, 132, 96))
    else:
        c.rect(d0, top, d1, 1380, fill=(176, 132, 96))
        c.circle(d0 + 30, 1110, 12, fill=MUSTARD, width=4)


CUPBOARD = (1000, 1240, 760)  # x0, x1, top; a tall two-door cupboard right of the couch (Episode 08)
BALL = (226, 128, 52)
SHIRT = (200, 60, 70)


def _teddy(c: Canvas, x, y, r):
    """A teddy bear's head peeking out."""
    fur, snout = (150, 100, 64), (214, 176, 130)
    for dx in (-0.75, 0.75):
        c.circle(x + dx * r, y - 0.72 * r, 0.36 * r, fill=fur, width=5)
    c.circle(x, y, r, fill=fur, width=6)
    c.ellipse(x - 0.42 * r, y + 0.05 * r, x + 0.42 * r, y + 0.62 * r, fill=snout, width=5)
    c.circle(x, y + 0.2 * r, 0.12 * r, fill=INK, outline=None)
    for dx in (-0.36, 0.36):
        c.circle(x + dx * r, y - 0.2 * r, 0.1 * r, fill=INK, outline=None)


def _ball(c: Canvas, x, y, r):
    c.circle(x, y, r, fill=BALL, width=6)
    c.line([(x - r, y), (x + r, y)], width=4)
    c.arc(x - r * 0.55, y - r, x + r * 0.55, y + r, 90, 270, width=4)
    c.arc(x - r * 0.55, y - r, x + r * 0.55, y + r, 270, 90, width=4)


def sneaker(c: Canvas, x, y, facing=1, color=(60, 64, 80), scale=1.0):
    """Side-view sneaker; (x, y) is the middle of the sole's bottom."""
    k, f = scale, facing
    c.rect(x - 58 * k, y - 18 * k, x + 58 * k, y, fill=PAPER, width=5, radius=8 * k)  # sole
    upper = [(x - 56 * k * f, y - 18 * k), (x - 50 * k * f, y - 62 * k), (x - 10 * k * f, y - 66 * k),
             (x + 20 * k * f, y - 44 * k), (x + 56 * k * f, y - 34 * k), (x + 58 * k * f, y - 18 * k)]
    c.poly(upper, fill=color, width=5)
    for i in range(3):  # laces
        lx = x + (-4 + i * 12) * k * f
        c.line([(lx, y - 58 * k + i * 6 * k), (lx + 10 * k * f, y - 50 * k + i * 6 * k)], fill=PAPER, width=4)


def _cupboard(c: Canvas, strain: float, sock: float):
    """`strain` 0..1 pushes the doors apart and lets the crammed stuff squeeze out: a teddy bear at the top, a shirt sleeve,
    a basketball, a sneaker at the bottom. `sock` 0..1 lets a sock dangle out of the gap."""
    x0, x1, top = CUPBOARD
    xm = (x0 + x1) / 2
    mid = (top + 1360) / 2
    c.rect(x0 - 12, top - 20, x1 + 12, 1380, fill=(120, 86, 62))
    gap = 16 * strain
    if gap > 1:
        c.rect(xm - gap, top + 20, xm + gap, 1350, fill=(52, 44, 40), outline=None)
    bow = 20 * strain
    for side in (-1, 1):
        inner = xm + side * gap
        outer = x0 if side < 0 else x1
        pts = [(outer, top), (inner, top + 10 * strain), (inner + side * bow, mid), (inner, 1350 - 10 * strain),
               (outer, 1360)]
        c.poly(pts, fill=WOOD)
        c.circle(inner - side * 24 + side * bow * 0.6, mid, 9, fill=MUSTARD, width=4)
    if strain <= 0.05:
        return
    # Stuff squeezing out through the gap, drawn over the door edges so it reads as spilling out.
    _teddy(c, xm + 4, top + 110, 46 * strain)
    c.limb([(xm, mid - 90), (xm + 30, mid - 20), (xm + 22, mid + 50)], SHIRT, 40 * strain)  # a shirt sleeve
    c.rect(xm + 22 - 24 * strain, mid + 44, xm + 22 + 24 * strain, mid + 64, fill=PAPER, width=5, radius=6)  # its cuff
    _ball(c, xm - 8, 1150, 44 * strain)
    sneaker(c, xm + 30, 1330, 1, scale=0.8 * strain)
    for side in (-1, 1):  # strain marks around the doors
        for dy in (-160, 0, 160):
            ex = (x0 - 30) if side < 0 else (x1 + 30)
            c.arc(ex - 18, mid + dy - 26, ex + 18, mid + dy + 26, 120 if side < 0 else -60, 240 if side < 0 else 60,
                  width=5)
    if sock > 0:  # hanging out of the gap over the left door, between the teddy and the sleeve
        sy = top + 175
        length = 90 * sock
        c.line([(xm - 12, sy), (xm - 50, sy + length)], fill=(236, 230, 220), width=26)
        c.line([(xm - 50, sy + length), (xm - 78, sy + length + 4)], fill=(236, 230, 220), width=26)
        c.line([(xm - 36, sy + length * 0.45 - 10), (xm - 20, sy + length * 0.45 + 4)], fill=ALERT, width=8)


def back(c: Canvas, time: str = "day", tv: str = "off", pizza: bool = False, t: float = 0.0, weather: str = "clear",
         behind=None, clock: float | None = None, door: str | None = None, cupboard: tuple | None = None, **_):
    """Everything behind the seated characters. `behind(c)` draws anyone standing behind the couch. `clock` (minutes
    since midnight) hangs a wall clock left of the window; `door` ("open" or "closed") draws the front door."""
    tod = TIMES[time]
    c.rect(-2000, -2000, 3000, 1380, fill=tod["wall"], outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=tod["floor"], outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    _window(c, time, t, weather)
    _picture(c)
    if clock is not None:
        _clock(c, clock)
    if door:
        _door(c, door == "open")
    if cupboard is not None:
        _cupboard(c, *cupboard)
    _tv(c, tv, t)
    if behind:
        behind(c)
    c.rect(140, 1000, 1040, 1240, fill=COUCH, radius=40)
    if pizza:
        c.rect(515, 1110, 665, 1228, fill=(196, 150, 100), width=6)
        c.rect(530, 1124, 650, 1214, fill=(214, 172, 124), width=4)


def _under_couch(c: Canvas, clutter: bool):
    """Short legs and the dark gap under the couch; with `clutter`, stuff shoved into the gap pokes out of it."""
    c.rect(120, 1322, 1060, 1380, fill=(64, 56, 50), outline=None)
    if clutter:
        c.rect(470, 1334, 700, 1374, fill=(196, 150, 100), width=5)  # a pizza box, edge on
        c.text(585, 1355, "PIZZA", 26, fill=ALERT, weight=8)
        sneaker(c, 800, 1384, -1, scale=0.8)  # heel sticking out
        c.limb([(930, 1330), (950, 1370), (1000, 1392)], TEAL_DARK, 34)  # a hoodie sleeve dangling out
        c.rect(985, 1378, 1030, 1404, fill=(24, 100, 90), width=5, radius=6)  # its cuff
    for x in (150, 1030):
        c.rect(x - 14, 1322, x + 14, 1382, fill=(90, 70, 56), width=5)


def front(c: Canvas, pizza: bool = False, clutter: bool = False, legs: bool = False, **_):
    """Couch seat front and arms, drawn over the seated characters' laps. `legs` lifts the couch on short legs so
    there's a visible gap underneath (Episode 08); `clutter` fills that gap."""
    if legs:
        _under_couch(c, clutter)
        c.rect(110, 1230, 1070, 1330, fill=COUCH_DARK, radius=34)
        c.rect(100, 1120, 200, 1334, fill=COUCH, radius=40)
        c.rect(980, 1120, 1080, 1334, fill=COUCH, radius=40)
    else:
        c.rect(110, 1230, 1070, 1380, fill=COUCH_DARK, radius=34)
        c.rect(100, 1120, 200, 1390, fill=COUCH, radius=40)
        c.rect(980, 1120, 1080, 1390, fill=COUCH, radius=40)
    if pizza:
        c.poly([(500, 1236), (680, 1236), (668, 1262), (512, 1262)], fill=(196, 150, 100), width=6)
        for cx, cy in ((550, 1246), (600, 1250), (630, 1244)):
            c.circle(cx, cy, 4, fill=(170, 110, 60), outline=None)
