"""The Dev/Mira/Jo living room. World coordinates are fixed so every episode's shots line up.

Layout (world units): couch spans x 100..1080, seat top y ~1230, floor from y 1380. The TV sits to the left of the
couch at x -320..0 with its power button at POWER_BUTTON. Seated characters sit at DEV_SEAT / MIRA_SEAT.
"""

from __future__ import annotations

from .canvas import INK, PAPER, WALL, FLOOR, Canvas

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


def back(c: Canvas, time: str = "day", tv: str = "off", pizza: bool = False, t: float = 0.0, weather: str = "clear",
         behind=None):
    """Everything behind the seated characters. `behind(c)` draws anyone standing behind the couch."""
    tod = TIMES[time]
    c.rect(-2000, -2000, 3000, 1380, fill=tod["wall"], outline=None)
    c.rect(-2000, 1380, 3000, 4000, fill=tod["floor"], outline=None)
    c.line([(-2000, 1380), (3000, 1380)], width=7)
    _window(c, time, t, weather)
    _picture(c)
    _tv(c, tv, t)
    if behind:
        behind(c)
    c.rect(140, 1000, 1040, 1240, fill=COUCH, radius=40)
    if pizza:
        c.rect(515, 1110, 665, 1228, fill=(196, 150, 100), width=6)
        c.rect(530, 1124, 650, 1214, fill=(214, 172, 124), width=4)


def front(c: Canvas, pizza: bool = False, **_):
    """Couch seat front and arms, drawn over the seated characters' laps."""
    c.rect(110, 1230, 1070, 1380, fill=COUCH_DARK, radius=34)
    c.rect(100, 1120, 200, 1390, fill=COUCH, radius=40)
    c.rect(980, 1120, 1080, 1390, fill=COUCH, radius=40)
    if pizza:
        c.poly([(500, 1236), (680, 1236), (668, 1262), (512, 1262)], fill=(196, 150, 100), width=6)
        for cx, cy in ((550, 1246), (600, 1250), (630, 1244)):
            c.circle(cx, cy, 4, fill=(170, 110, 60), outline=None)
