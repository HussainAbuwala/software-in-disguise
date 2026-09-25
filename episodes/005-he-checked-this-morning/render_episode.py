"""Render Episode 05 (stale cache) end to end.

    ../../.venv/bin/python voices.py           # once, or after changing lines
    ../../.venv/bin/python render_episode.py   # deliverables/episode-05-he-checked-this-morning-final.mp4

Shared machinery lives in kit/episode.py; this file is only the story.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import reveal  # noqa: E402
from kit import cast  # noqa: E402
from kit import living_room as room  # noqa: E402
from kit.canvas import (  # noqa: E402
    ALERT, DEMI, HEAVY, MUSTARD, SCREEN, SS, Camera, Canvas, ease, finish, lerp, new_frame,
)
from kit.cast import DEV, JO, MIRA, Pose  # noqa: E402
from kit.episode import Ctx, Episode, Shot, scene  # noqa: E402
from kit.overlays import card, memory_note  # noqa: E402
from kit.sound import (  # noqa: E402
    crumple, ding, door_thunk, drip, gulp, hum, pad, pluck, rain, sad_trombone, scribble, thump, thunder, tick, tonk,
)

MIRA_STAND = (800, 1480)
JO_BEHIND_FEET = 1330  # walking behind the couch
KITCHEN = (2400, 1480)  # a spot far from the living room where the fridge-POV shots are staged
WEATHER = "rain"  # it rains all day in the present; the flashbacks happen at a sunny 7:02 and 8:15

NOTE_POP = 0.35  # seconds after a line starts that Dev's memory note pops up

# Two-shot framed lower than kit's TWO_SHOT: Mira stands, so the heads need headroom for bubbles and Dev's note.
LOW_TWO = Camera(1.42, 598, 1080, 540, 1240)


def head_top(cam: Camera, pose: Pose) -> tuple[float, float]:
    """Screen point just above a character's head, where thought dots start."""
    f = pose.facing
    if pose.standing:
        return cam.to_screen(pose.x + f * 40, pose.y - 660)
    return cam.to_screen(pose.x + f * 50, pose.y - 205)


def dev_phone(ctx: Ctx, **kw) -> Pose:
    return ctx.seated("DEV", 1, kw.pop("expr", "phone"), hands="phone", **kw)


def mira_standing(ctx: Ctx, expr="annoyed", hands="carton", **kw) -> Pose:
    return ctx.standing("MIRA", *MIRA_STAND, -1, expr, hands=hands, **kw)


def note_for(ctx: Ctx, line_key: str, text: str, pose: Pose, cam: Camera, x: float, y: float):
    """Overlay that pops Dev's memory note shortly after his line in this shot starts."""
    line = next(l for l in ctx.shot.lines if l.key == line_key)
    k = (ctx.t - line.offset - NOTE_POP) / 0.35
    return lambda c: memory_note(c, head_top(cam, pose), x, y, text, "7:02 AM", k)


def flash(img: Image.Image, a: float) -> Image.Image:
    if a <= 0.01:
        return img
    return Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), min(0.9, a))


# --- shots ----------------------------------------------------------------------------------------------------


def s01_empty_carton(ctx: Ctx):
    drop = (ctx.t - 0.55) * 900 if 0.55 <= ctx.t < 0.85 else None
    shake = math.sin(ctx.t * 38) * 7 if ctx.t < 0.5 else 0.0
    extras = {"shake": shake} | ({"drop": drop} if drop is not None else {})
    mira = mira_standing(ctx, extras=extras)
    return scene(ctx, LOW_TWO, weather=WEATHER, seated=[(DEV, dev_phone(ctx))], standing=[(MIRA, mira)])


def s02_dev_checked(ctx: Ctx):
    cam = Camera(2.3, 350, 1010, 540, 1080)
    dev = dev_phone(ctx)
    return scene(ctx, cam, weather=WEATHER, seated=[(DEV, dev)],
                 overlay=note_for(ctx, "dev-i-checked", "MILK", dev, cam, 590, 560))


FRIDGE_CAM = Camera(2.5, KITCHEN[0], 910, 540, 860)
SHELF_CARTON = (800, 1252)  # carton center on the shelf, screen space
CARTON_SCALE = 2.6


def tilted_carton(img: Image.Image, center: tuple[float, float], angle: float):
    """Draw the milk carton rotated about its center (degrees counterclockwise), in screen space."""
    layer = Image.new("RGBA", (400 * SS, 560 * SS), (0, 0, 0, 0))
    half = (110 + 34 + 8) * CARTON_SCALE / 2
    cast.milk_carton(Canvas(layer, Camera(1.0, 0, 0, 200, 280)), 0, half, scale=CARTON_SCALE)
    if abs(angle) > 0.5:
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    x, y = round(center[0] * SS - layer.width / 2), round(center[1] * SS - layer.height / 2)
    img.paste(layer, (x, y), layer)


def fridge_pov(ctx: Ctx, who: str, pose: Pose, carton=(SHELF_CARTON, 0.0), arm_to=None, note=None):
    """Looking out from inside the fridge: shelves frame the face, the milk carton in the foreground.

    `carton` is (screen center, tilt angle). `arm_to` draws the character's near arm reaching into the fridge to a
    screen point (the pose should use hands="far_rest")."""
    cam = FRIDGE_CAM
    img = new_frame((236, 222, 196))
    c = Canvas(img, cam)
    c.rect(KITCHEN[0] - 1200, 1300, KITCHEN[0] + 1200, 1400, fill=(206, 186, 150), outline=None)  # counter
    for i in range(6):  # tiled backsplash
        c.line([(KITCHEN[0] - 1200, 560 + i * 90), (KITCHEN[0] + 1200, 560 + i * 90)], fill=(222, 206, 176), width=5)
    look = {"DEV": DEV, "JO": JO}[who]
    cast.draw(c, look, pose)
    s = Canvas(img, SCREEN)
    # Fridge interior: walls around the edge, a light, a glass shelf with food on it.
    wall = (226, 236, 242)
    s.rect(-10, -10, 130, 1930, fill=wall, width=8)
    s.rect(950, -10, 1090, 1930, fill=wall, width=8)
    s.rect(-10, -10, 1090, 150, fill=wall, width=8)
    s.rect(420, 100, 660, 150, fill=(255, 248, 210), width=6, radius=20)  # light
    s.rect(-10, 1470, 1090, 1930, fill=wall, width=8)
    s.rect(60, 1540, 1020, 1860, fill=(214, 232, 222), width=7, radius=30)  # vegetable drawer
    s.rect(400, 1580, 680, 1620, fill=(190, 212, 200), width=5, radius=20)
    s.rect(-10, 1440, 1090, 1480, fill=(200, 222, 232), width=6)  # glass shelf edge
    s.rect(170, 1270, 330, 1450, fill=(214, 90, 70), width=7, radius=20)  # jar of jam
    s.rect(160, 1230, 340, 1280, fill=(240, 240, 240), width=7, radius=10)
    s.rect(380, 1350, 500, 1445, fill=(250, 214, 110), width=7, radius=10)  # butter
    tilted_carton(img, *carton)
    if arm_to:
        f = pose.facing
        shoulder = cam.to_screen(pose.x + f * 58, pose.y - 490 + 60)
        s.limb([shoulder, ((shoulder[0] + arm_to[0]) / 2 + 40, (shoulder[1] + arm_to[1]) / 2 + 60), arm_to],
               look.top, 38 * cam.zoom, ink=12)
        s.circle(*arm_to, 22 * cam.zoom, fill=look.skin, width=12)
    if note:
        note(s)
    return img


def s03a_dev_fridge(ctx: Ctx):
    nod = math.sin(min(1.0, max(0.0, (ctx.t - 0.35) / 0.3)) * math.pi) * 14
    pose = Pose(*KITCHEN, 1, "confident" if ctx.t > 0.35 else "neutral", blink=ctx.blink("DEV"), standing=True,
                hands="rest", gaze=0.5, gaze_y=0.8, head_dy=nod)
    cam = FRIDGE_CAM
    note = lambda c: memory_note(c, head_top(cam, pose), 600, 230, "MILK", "7:02 AM", (ctx.t - 0.55) / 0.35)
    return fridge_pov(ctx, "DEV", pose, note=note)


def card_702(ctx: Ctx):
    img = s03a_dev_fridge(Ctx(ctx.ep, ctx.shot, 0.0))
    card(Canvas(img, SCREEN), "7:02 AM", ctx.t)
    return img


DRINK_AT = (790, 930)  # carton center while Jo drinks: spout at Jo's mouth, bottom up and to the right
DRINK_ANGLE = 115


def s03b_jo_fridge(ctx: Ctx):
    """Jo takes the milk, drinks it straight from the carton, and puts the empty carton back."""
    t = ctx.t
    reach = None
    if t < 0.3:  # Jo eyes the milk
        center, angle = SHELF_CARTON, 0.0
    elif t < 0.55:  # grab and raise to mouth
        k = ease((t - 0.3) / 0.25)
        center = (lerp(SHELF_CARTON[0], DRINK_AT[0], k), lerp(SHELF_CARTON[1], DRINK_AT[1], k))
        angle, reach = DRINK_ANGLE * k, True
    elif t < 1.2:  # drinking: the carton tips a little further with each gulp
        glug = math.sin((t - 0.55) * 2 * math.pi / 0.2) * 5
        center, angle, reach = DRINK_AT, DRINK_ANGLE + 6 * (t - 0.55) + glug, True
    elif t < 1.45:  # back onto the shelf
        k = ease((t - 1.2) / 0.25)
        center = (lerp(DRINK_AT[0], SHELF_CARTON[0], k), lerp(DRINK_AT[1], SHELF_CARTON[1], k))
        angle, reach = lerp(DRINK_ANGLE + 4, 0, k), True
    else:  # let go; the empty carton rocks
        bounce = 18 * math.sin((t - 1.45) * 30) * math.exp(-(t - 1.45) * 8)
        center, angle = (SHELF_CARTON[0], SHELF_CARTON[1] - max(0.0, bounce)), bounce * 0.4
    drinking = 0.55 <= t < 1.2
    pose = Pose(*KITCHEN, 1, "cheerful" if t > 1.45 else "deadpan", blink=drinking or ctx.blink("JO"),
                standing=True, hands="far_rest" if reach else "rest", gaze=0.6, gaze_y=0.7,
                head_dy=-10 if drinking else 0)
    hand = (center[0] + 30, center[1] + 20) if reach else None
    return fridge_pov(ctx, "JO", pose, carton=(center, angle), arm_to=hand)


def card_815(ctx: Ctx):
    img = s03b_jo_fridge(Ctx(ctx.ep, ctx.shot, 0.0))
    card(Canvas(img, SCREEN), "8:15 AM", ctx.t)
    return img


MIRA_CLOSE = Camera(2.3, 800, 930, 540, 1010)


def s04_mira_jo(ctx: Ctx):
    return scene(ctx, MIRA_CLOSE, weather=WEATHER, standing=[(MIRA, mira_standing(ctx, hands="rest"))])


JO_STOP = 560  # Jo stops behind the middle of the couch: clear of Dev's note, visible between Dev and Mira


def s05_fast_asleep(ctx: Ctx):
    t = ctx.t
    walk = ease((t - 0.45) / 0.7)
    jo_x = lerp(1250, JO_STOP, walk) if t >= 0.45 else 1500
    walking = 0.45 <= t < 1.15
    jo = Pose(jo_x, JO_BEHIND_FEET, -1, "cheerful", mouth=ctx.mouth("JO"), blink=ctx.blink("JO"), standing=True,
              hands="wave_mug", extras={"wave": math.sin(t * 14) if t >= 1.1 else 0.0,
                                        "bob": -abs(math.sin(t * math.pi * 3.2)) * 8 if walking else 0.0})
    mira_gaze = max(-1.0, min(1.0, (jo_x - MIRA_STAND[0]) / 250)) if t >= 0.45 else -1.0
    mira = mira_standing(ctx, hands="rest", gaze=mira_gaze)
    dev = dev_phone(ctx)
    return scene(ctx, LOW_TWO, weather=WEATHER, behind=[(JO, jo)], seated=[(DEV, dev)], standing=[(MIRA, mira)],
                 overlay=note_for(ctx, "dev-fast-asleep", "JO: zzz", dev, LOW_TWO, 40, 560))


def s06_mira_rain(ctx: Ctx):
    return scene(ctx, MIRA_CLOSE, weather=WEATHER, standing=[(MIRA, mira_standing(ctx, hands="rest", gaze=-1))])


SUNNY_CAM = Camera(1.9, 470, 900, 540, 1020)


def s07_sunny(ctx: Ctx):
    dev = dev_phone(ctx)
    img = scene(ctx, SUNNY_CAM, weather=WEATHER, seated=[(DEV, dev)],
                overlay=note_for(ctx, "dev-sunny", "SUNNY", dev, SUNNY_CAM, 540, 1010))
    ft = ctx.ep.flash_at - ctx.shot.start
    a = 0.0
    for off, strength in ((0.0, 0.85), (0.14, 0.6)):
        if ctx.t >= ft + off:
            a = max(a, strength * math.exp(-(ctx.t - ft - off) * 10))
    return flash(img, a)


def s08_sunny_at_seven(ctx: Ctx):
    cam = Camera(2.6, 345, 1000, 540, 1090)
    return scene(ctx, cam, weather=WEATHER, seated=[(DEV, dev_phone(ctx))])


def s08b_mira_stare(ctx: Ctx):
    mira = mira_standing(ctx, "unimpressed", hands="rest", gaze=-1)
    mira.blink = 0.5 <= ctx.t < 0.64
    return scene(ctx, MIRA_CLOSE, weather=WEATHER, standing=[(MIRA, mira)])


def s10_coffee(ctx: Ctx):
    dev = dev_phone(ctx)
    mira = mira_standing(ctx, hands="mug_up")
    return scene(ctx, LOW_TWO, weather=WEATHER, seated=[(DEV, dev)], standing=[(MIRA, mira)],
                 overlay=note_for(ctx, "dev-yep-checked", "COFFEE", dev, LOW_TWO, 40, 700))


# --- episode --------------------------------------------------------------------------------------------------


class Episode05(Episode):
    here = HERE
    final_name = "episode-05-he-checked-this-morning-final.mp4"

    def reveal_frame(self, t: float):
        if not hasattr(self, "_layers"):
            self._layers = (reveal.node_layer(0), reveal.node_layer(1))
        return reveal.render_frame(t, self._layers, self.reveal_captions)

    def build_shots(self) -> list[Shot]:
        d = self.dur
        sunny_end = 0.1 + d("dev-sunny")
        self.flash_offset = sunny_end + 0.02
        coffee_gap = 0.1 + d("mira-coffee") + 0.15
        return [
            Shot("S01 empty carton", 0.12 + d("mira-said-milk") + 0.35, s01_empty_carton,
                 [self.line("mira-said-milk", 0.12, (330, 420, 560))]),
            Shot("S02 I checked", 0.08 + d("dev-i-checked") + 0.75, s02_dev_checked,
                 [self.line("dev-i-checked", 0.08, (60, 380, 520))]),
            Shot("Card 7:02", 0.55, card_702),
            Shot("S03a Dev at fridge", 1.3, s03a_dev_fridge),
            Shot("Card 8:15", 0.55, card_815),
            Shot("S03b Jo at fridge", 1.95, s03b_jo_fridge),
            Shot("S04 Mira asks about Jo", 0.1 + d("mira-jo-asleep") + 0.3, s04_mira_jo,
                 [self.line("mira-jo-asleep", 0.1, (170, 380, 640))]),
            Shot("S05 fast asleep", 2.7, s05_fast_asleep,
                 [self.line("dev-fast-asleep", 0.15, (40, 330, 420)), self.line("jo-morning", 1.25, (380, 480, 340))]),
            Shot("S06 Mira asks about rain", 0.1 + d("mira-raining") + 0.3, s06_mira_rain,
                 [self.line("mira-raining", 0.1, (170, 380, 640))]),
            Shot("S07 sunny", sunny_end + 0.95, s07_sunny, [self.line("dev-sunny", 0.1, (60, 330, 460))]),
            Shot("S08 sunny at seven", 0.15 + d("dev-sunny-at-seven") + 0.3, s08_sunny_at_seven,
                 [self.line("dev-sunny-at-seven", 0.15, (60, 380, 620))]),
            Shot("S08b Mira stare", 1.05, s08b_mira_stare),
            self.reveal_shot(),
            Shot("S10 coffee (loops to S01)", coffee_gap + d("dev-yep-checked") + 0.5, s10_coffee,
                 [self.line("mira-coffee", 0.1, (420, 330, 480)), self.line("dev-yep-checked", coffee_gap, (40, 500, 440))]),
        ]

    @property
    def flash_at(self) -> float:
        return self.shot("S07").start + self.flash_offset

    def sound_design(self, mix):
        s = self.shot
        present = [x for x in self.shots if not x.name.startswith(("Card", "S03", "R1"))]
        for x in present:
            mix.add(rain(x.dur, seed=int(x.start * 10)), x.start, 0.035)

        s01, s02 = s("S01"), s("S02")
        C3, G2, E2 = 130.81, 98.0, 82.41
        for when, f in ((0.0, C3), (0.42, G2)):
            mix.add(pluck(f, seed=int(f)), when, 0.2)
        mix.add(drip(), s01.start + 0.8, 0.35)

        def note_sfx(shot, key):
            line = next(l for l in shot.lines if l.key == key)
            mix.add(ding(), line.start + NOTE_POP, 0.16)
            mix.add(scribble(0.3), line.start + NOTE_POP + 0.05, 0.08)

        note_sfx(s02, "dev-i-checked")
        for name in ("Card 7:02", "Card 8:15"):
            c = s(name)
            for i in range(2):
                mix.add(tick(), c.start + 0.05 + i * 0.22, 0.3)

        s03a, s03b = s("S03a"), s("S03b")
        mix.add(door_thunk(), s03a.start, 0.22)
        mix.add(hum(s03a.dur + s("Card 8:15").dur + s03b.dur), s03a.start, 0.04)
        mix.add(scribble(), s03a.start + 0.6, 0.12)
        mix.add(ding(), s03a.start + 0.55, 0.14)
        mix.add(door_thunk(2), s03b.start, 0.22)
        for i, off in enumerate((0.6, 0.8, 1.0)):
            mix.add(gulp(i), s03b.start + off, 0.14)
        mix.add(tonk(), s03b.start + 1.5, 0.4)
        mix.add(door_thunk(3), s03b.start + 1.85, 0.2)

        s05 = s("S05")
        note_sfx(s05, "dev-fast-asleep")
        for i in range(3):
            mix.add(thump(i), s05.start + 0.5 + i * 0.23, 0.14)

        note_sfx(s("S07"), "dev-sunny")
        mix.add(thunder(), self.flash_at + 0.05, 0.42)
        mix.add(sad_trombone(), s("S08b").start + 0.1, 0.16)

        r1 = s("R1")
        b = reveal.beats_for(self.reveal_captions)
        mix.add(pad(r1.dur), r1.start, 0.07)
        mix.add(ding(), r1.start + b["note"], 0.12)
        mix.add(crumple(), r1.start + b["expire"], 0.3)
        mix.add(ding(), r1.start + b["refresh"], 0.14)

        s10 = s("S10")
        note_sfx(s10, "dev-yep-checked")
        mix.add(pluck(E2, seed=5), self.duration - 0.42, 0.2)  # leads into S01's opening plucks on the loop

    def thumbnail(self, path: Path):
        cam = Camera(1.55, 590, 1060, 540, 1200)
        img = new_frame()
        c = Canvas(img, cam)
        room.back(c, "day", weather="rain")
        dev = Pose(*room.DEV_SEAT, 1, "phone", hands="phone")
        cast.draw(c, DEV, dev)
        room.front(c)
        cast.draw(c, MIRA, Pose(*MIRA_STAND, -1, "annoyed", standing=True, hands="carton"))
        s = Canvas(img, SCREEN)
        memory_note(s, head_top(cam, dev), 60, 700, "MILK", "7:02 AM", 1.0)
        s.text(540, 250, "SOFTWARE IN DISGUISE · 05", 34, weight=DEMI)
        s.rect(60, 330, 1020, 610, fill=MUSTARD, width=9, radius=20)
        s.text(540, 415, "HE CHECKED.", 104, weight=HEAVY)
        s.text(540, 530, "AT 7:02.", 104, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


if __name__ == "__main__":
    Episode05().render()
