"""Render Episode 06 (off-by-one) end to end.

    ../../.venv/bin/python voices.py
    ../../.venv/bin/python render_episode.py   # deliverables/episode-06-were-both-on-the-first-floor-final.mp4

Shared machinery lives in kit/episode.py and the two-floor café set in kit/cafe.py; this file is only the story.
First episode built on the retention findings: a 3-chunk (~6 s) reveal, a bigger promise line, and motion from frame 1.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import reveal  # noqa: E402
from kit import cafe, cast  # noqa: E402
from kit.canvas import ALERT, DEMI, HEAVY, MUSTARD, SCREEN, SS, Camera, Canvas, ease, finish, font, lerp, new_frame  # noqa: E402
from kit.cast import DEV, MIRA, Pose  # noqa: E402
from kit.episode import Ctx, Episode, Shot, cam_lerp, scene  # noqa: E402
import numpy as np  # noqa: E402

from kit.sound import ding, hum, murmur, noise, pad, pluck, slide_whistle, thump, tick  # noqa: E402

LOOKS = {"DEV": DEV, "MIRA": MIRA}
STAND_X = 540  # standing spot beside each table
SPLIT = Camera(0.864, 625, 1030, 540, 965)
SPLIT_PUSHED = Camera(0.9, 625, 1030, 540, 965)
DEV_UP_CLOSE = Camera(2.3, 610, 640, 540, 1000)
MIRA_G_CLOSE = Camera(2.3, 610, 1400, 540, 1000)
DEV_POINT = Camera(1.5, 540, 700, 540, 1000)
MIRA_POINT = Camera(1.5, 540, 1460, 540, 1000)
POINT_X = 700  # far enough from the sign/door that the pointing arm doesn't cross the face


def sit(ctx: Ctx, who: str, floor: str, expr: str, **kw) -> Pose:
    x, y = cafe.SEAT_UP if floor == "up" else cafe.SEAT_GROUND
    pose = Pose(x, y, 1, expr, mouth=ctx.mouth(who), blink=ctx.blink(who), hands=kw.pop("hands", "phone_ear"), **kw)
    pose.extras.setdefault("breathe", ctx.breathe(phase=0.3 if who == "MIRA" else 0.0))
    return pose


def stand(ctx: Ctx, who: str, x: float, floor_y: float, facing: int, expr: str, **kw) -> Pose:
    return ctx.standing(who, x, floor_y, facing, expr, hands=kw.pop("hands", "phone_ear"), **kw)


def cafe_scene(ctx: Ctx, cam: Camera, seated=(), standing=(), inside=(), elevator: float = 0.0, overlay=None):
    """`inside` is whoever rides in the elevator car (drawn between its glass and frame)."""
    return scene(ctx, cam, set=cafe, seated=seated, standing=standing, behind=inside, elevator=elevator,
                 overlay=overlay)


# Floor tags: explain the human side of the mix-up (floor numbering differs by country) at the moment the characters
# realize it, and keep them up while the swap plays out. The upper tag appears on Mira's "Oh! Upstairs!", the ground
# tag on Dev's "Oh! The entrance!".
FLOOR_TAGS = (("up", "1st floor in the UK & India"), ("ground", "1st floor in the US & Canada"))


def floor_tags(ctx: Ctx, cam: Camera):
    ep = ctx.ep
    realize = ep.shot("S07")
    since = {"up": ctx.g - (realize.start + 0.35), "ground": ctx.g - (realize.start + ep.dev_realize_at + 0.25)}

    def draw(c: Canvas):
        for floor, text in FLOOR_TAGS:
            k = since[floor] / 0.3
            if k <= 0:
                continue
            k = ease(k)
            floor_y = cafe.UP if floor == "up" else cafe.GROUND
            x, y = cam.to_screen(cafe.TABLE_X, floor_y - 95)
            w = font(38, HEAVY).getlength(text) / SS + 48
            y += (1 - k) * 20
            c.rect(x - w / 2, y - 31, x + w / 2, y + 31, fill=MUSTARD, width=6, radius=31)
            c.text(x, y, text, 38 * (0.8 + 0.2 * k), weight=HEAVY)

    return draw


def looking_around(ctx: Ctx, speed=1.3, phase=0.0) -> float:
    return math.sin((ctx.g + phase) * speed * math.pi)


# --- shots ----------------------------------------------------------------------------------------------------


def s01_both_first_floor(ctx: Ctx):
    cam = cam_lerp(SPLIT, SPLIT_PUSHED, ease(ctx.k))  # a slow push-in: the frame is moving from the first instant
    dev = sit(ctx, "DEV", "up", "annoyed", gaze=looking_around(ctx))
    mira = sit(ctx, "MIRA", "ground", "annoyed", gaze=looking_around(ctx, phase=0.6))
    return cafe_scene(ctx, cam, seated=[(DEV, dev), (MIRA, mira)])


def s02_dev_window(ctx: Ctx):
    return cafe_scene(ctx, DEV_UP_CLOSE, seated=[(DEV, sit(ctx, "DEV", "up", "determined"))])


def s03_mira_window(ctx: Ctx):
    return cafe_scene(ctx, MIRA_G_CLOSE, seated=[(MIRA, sit(ctx, "MIRA", "ground", "annoyed", gaze=1.0))])


def s04_waving(ctx: Ctx):
    wave = math.sin(ctx.t * 16)
    dev = stand(ctx, "DEV", STAND_X, cafe.UP, 1, "cheerful", hands="wave_phone", extras={"wave": wave})
    mira = stand(ctx, "MIRA", STAND_X, cafe.GROUND, 1, "cheerful" if ctx.t < 1.0 else "annoyed",
                 hands="wave_phone" if ctx.t >= 0.9 else "phone_ear", extras={"wave": -wave})
    return cafe_scene(ctx, SPLIT, standing=[(DEV, dev), (MIRA, mira)])


def s05_dev_sign(ctx: Ctx):
    target = (cafe.SIGN_UP[0] + 80, cafe.SIGN_UP[1] + 10)
    dev = stand(ctx, "DEV", POINT_X, cafe.UP, -1, "annoyed", hands="point_phone", reach=target)
    return cafe_scene(ctx, DEV_POINT, standing=[(DEV, dev)])


def s06_mira_door(ctx: Ctx):
    target = (cafe.DOOR[1] + 10, cafe.GROUND - 300)
    mira = stand(ctx, "MIRA", POINT_X, cafe.GROUND, -1, "annoyed", hands="point_phone", reach=target)
    return cafe_scene(ctx, MIRA_POINT, standing=[(MIRA, mira)])


def s07_realize(ctx: Ctx):
    """Each finally gets the other's counting ("Oh! Upstairs!" / "Oh! The entrance!"), then both politely say
    "Stay there, I'm coming!" at the same moment, which is what sends them both moving."""
    stay = ctx.t >= ctx.ep.stay_at
    mira_expr = "cheerful" if stay else ("shock" if ctx.t >= 0.1 else "annoyed")
    dev_expr = "cheerful" if stay else ("shock" if ctx.t >= ctx.ep.dev_realize_at else "annoyed")
    dev = stand(ctx, "DEV", STAND_X, cafe.UP, 1, dev_expr)
    mira = stand(ctx, "MIRA", STAND_X, cafe.GROUND, 1, mira_expr)
    return cafe_scene(ctx, SPLIT, standing=[(DEV, dev), (MIRA, mira)], overlay=floor_tags(ctx, SPLIT))


# The swap: Dev takes the stairs down while Mira takes the elevator up. They pass each other halfway, at the same
# height, each staring at the phone, and each arrives exactly where the other just was. The pass is slowed down
# (SLOW_FROM..SLOW_TO of path time plays at SLOW_RATE) so the near-miss reads as the joke, not a plot hole.
SLOW_FROM, SLOW_TO, SLOW_RATE = 0.85, 1.15, 0.3
SLOW_EXTRA = (SLOW_TO - SLOW_FROM) / SLOW_RATE - (SLOW_TO - SLOW_FROM)
SWAP = 2.6 + SLOW_EXTRA


def path_time(t: float) -> float:
    slow_end = SLOW_FROM + (SLOW_TO - SLOW_FROM) / SLOW_RATE
    if t < SLOW_FROM:
        return t
    if t < slow_end:
        return SLOW_FROM + (t - SLOW_FROM) * SLOW_RATE
    return SLOW_TO + (t - slow_end)


def dev_path(t: float) -> tuple[float, float, int]:
    (sx, sy), (bx, by) = cafe.STAIRS_TOP, cafe.STAIRS_BOTTOM
    if t < 0.45:
        return lerp(STAND_X, sx, t / 0.45), cafe.UP, 1
    if t < 1.5:
        k = (t - 0.45) / 1.05
        return lerp(sx, bx, k), lerp(sy, by, k), 1
    k = min(1.0, (t - 1.5) / 0.9)
    return lerp(bx, STAND_X, ease(k)), cafe.GROUND, -1


def mira_path(t: float) -> tuple[float, float, int, float, bool]:
    """(x, feet y, facing, elevator progress, inside the car)."""
    car_x = (cafe.SHAFT[0] + cafe.SHAFT[1]) / 2
    if t < 0.45:
        return lerp(STAND_X, car_x, t / 0.45), cafe.GROUND, -1, 0.0, False
    if t < 1.6:
        k = min(1.0, max(0.0, (t - 0.55) / 0.95))
        k = k * k * (3 - 2 * k)  # smoothstep: symmetric, so the car is halfway up exactly when Dev is halfway down
        return car_x, cafe.car_y(k) + cafe.CAR_H, 1, k, True
    k = min(1.0, (t - 1.6) / 0.8)
    return lerp(car_x, STAND_X, ease(k)), cafe.UP, 1, 1.0, False


def s08_swap(ctx: Ctx):
    t = path_time(ctx.t)
    dx, dy, df = dev_path(t)
    mx, my, mf, lift, inside = mira_path(t)
    walking = 0.0 if t > 2.4 else -abs(math.sin(t * math.pi * 4.5)) * 9
    dev = stand(ctx, "DEV", dx, dy, df, "determined", gaze_y=0.9, extras={"bob": walking})  # eyes down: oblivious
    mira = stand(ctx, "MIRA", mx, my, mf, "determined", gaze_y=0.9, extras={"bob": 0.0 if inside else walking})
    return cafe_scene(ctx, SPLIT, standing=[(DEV, dev)] + ([] if inside else [(MIRA, mira)]),
                      inside=[(MIRA, mira)] if inside else [], elevator=lift, overlay=floor_tags(ctx, SPLIT))


def s09_where(ctx: Ctx):
    after = ctx.t > ctx.ep.where_at
    dev = stand(ctx, "DEV", STAND_X, cafe.GROUND, 1, "neutral" if not after else "deadpan", gaze=looking_around(ctx, 1.1))
    mira = stand(ctx, "MIRA", STAND_X, cafe.UP, 1, "neutral" if not after else "deadpan", gaze=looking_around(ctx, 1.1, 0.5))
    return cafe_scene(ctx, SPLIT, standing=[(DEV, dev), (MIRA, mira)], elevator=1.0, overlay=floor_tags(ctx, SPLIT))


def s10_again(ctx: Ctx):
    t = ctx.t
    go = max(0.0, t - 0.45)
    dev_x = STAND_X + go * 420  # toward the foot of the stairs
    mira_x = STAND_X - go * 420  # toward the elevator
    bob = -abs(math.sin(t * math.pi * 4.5)) * 9 if go > 0 else 0.0
    dev = stand(ctx, "DEV", dev_x, cafe.GROUND, 1, "determined", extras={"bob": bob})
    mira = stand(ctx, "MIRA", mira_x, cafe.UP, -1, "determined", extras={"bob": bob})
    return cafe_scene(ctx, SPLIT, standing=[(DEV, dev), (MIRA, mira)], elevator=1.0)


# --- episode --------------------------------------------------------------------------------------------------


class Episode06(Episode):
    here = HERE
    final_name = "episode-06-were-both-on-the-first-floor-final.mp4"
    reveal_chunks = ["reveal-1", "reveal-2", "reveal-3"]
    promise_size = 64

    def reveal_frame(self, t: float):
        return reveal.render_frame(t, self.reveal_captions)

    def build_shots(self) -> list[Shot]:
        d = self.dur
        ln = self.line
        so_am_i = 0.15 + d("dev-waving") + 0.15
        self.dev_realize_at = 0.1 + d("mira-realize") + 0.1
        self.stay_at = self.dev_realize_at + d("dev-realize") + 0.15
        mira_here = 0.3
        self.where_at = mira_here + d("mira-im-here") + 0.3
        up_bubble, ground_bubble = (590, 360, 440), (590, 1010, 440)
        return [
            Shot("S01 both first floor", 0.1 + d("mira-first-floor") + 0.25, s01_both_first_floor,
                 [ln("mira-first-floor", 0.1, (560, 1000, 460))]),
            Shot("S02 Dev window table", 0.08 + d("dev-window-table") + 0.25, s02_dev_window,
                 [ln("dev-window-table", 0.08, (60, 420, 600))]),
            Shot("S03 Mira window table", 0.08 + d("mira-at-window") + 0.3, s03_mira_window,
                 [ln("mira-at-window", 0.08, (200, 380, 640))]),
            Shot("S04 waving", so_am_i + d("mira-so-am-i") + 0.35, s04_waving,
                 [ln("dev-waving", 0.15, up_bubble), ln("mira-so-am-i", so_am_i, ground_bubble)]),
            Shot("S05 Dev points at the 1", 0.1 + d("dev-sign-says-one") + 0.3, s05_dev_sign,
                 [ln("dev-sign-says-one", 0.1, (330, 300, 560))]),
            Shot("S06 Mira points at the door", 0.1 + d("mira-front-door") + 0.3, s06_mira_door,
                 [ln("mira-front-door", 0.1, (330, 330, 620))]),
            Shot("S07 realize", self.stay_at + 0.05 + d("dev-stay-there") + 0.2, s07_realize,
                 [ln("mira-realize", 0.1, ground_bubble), ln("dev-realize", self.dev_realize_at, up_bubble),
                  ln("mira-stay-there", self.stay_at, ground_bubble), ln("dev-stay-there", self.stay_at + 0.05, up_bubble)]),
            Shot("S08 swap", SWAP, s08_swap),
            Shot("S09 where", self.where_at + d("mira-where") + 0.75, s09_where,
                 [ln("dev-im-here", 0.1, ground_bubble), ln("mira-im-here", mira_here, up_bubble),
                  ln("mira-where", self.where_at, (590, 360, 300))]),
            self.reveal_shot(),
            Shot("S10 again (loops to S01)", 0.3 + d("mira-coming-down-loop") + 0.35, s10_again,
                 [ln("dev-coming-up-loop", 0.1, ground_bubble), ln("mira-coming-down-loop", 0.3, up_bubble)]),
        ]

    def sound_design(self, mix):
        s = self.shot
        story = [x for x in self.shots if not x.name.startswith("R1")]
        for x in story:  # café murmur and the odd cup clink
            mix.add(murmur(x.dur, seed=int(x.start * 7) + 3), x.start, 0.03)
        for when in (0.9, 6.3, 12.4):
            mix.add(tick(), when, 0.12)

        C3, G2, E3 = 130.81, 98.0, 164.81
        for when, f in ((0.0, C3), (0.4, G2)):
            mix.add(pluck(f, seed=int(f)), when, 0.2)

        s07, s08, s09 = s("S07"), s("S08"), s("S09")
        mix.add(ding(), s07.start + 0.12, 0.1)  # Mira's lightbulb
        mix.add(ding(), s07.start + self.dev_realize_at + 0.02, 0.1)  # Dev's lightbulb

        # The swap: footsteps down the stairs, the elevator hums up, two slide whistles cross, a ding on arrival.
        for i in range(10):
            step = 0.05 + i * 0.2
            if SLOW_FROM <= step < SLOW_FROM + (SLOW_TO - SLOW_FROM) / SLOW_RATE:
                continue  # hold the footsteps during the slow-motion pass
            mix.add(thump(i), s08.start + step + (SLOW_EXTRA if step >= SLOW_FROM else 0), 0.16)
        mix.add(hum(0.95 + SLOW_EXTRA), s08.start + 0.55, 0.06)
        slow_end = SLOW_FROM + (SLOW_TO - SLOW_FROM) / SLOW_RATE
        mix.add(slide_whistle(), s08.start + 0.3, 0.1)
        mix.add(slide_whistle()[::-1], s08.start + 0.35, 0.1)
        whoosh_len = slow_end - SLOW_FROM
        whoosh = noise(whoosh_len, 250, 3500, 91) * np.sin(np.pi * np.linspace(0, 1, int(whoosh_len * 48000))) ** 2
        mix.add(whoosh, s08.start + SLOW_FROM, 0.12)  # the slow-motion pass
        mix.add(ding(), s08.start + 1.55 + SLOW_EXTRA, 0.14)

        # "Where?" then a deflated womp-womp.
        where = s09.start + self.where_at
        mix.add(pluck(E3, 0.5, seed=21), where + 0.75, 0.22)
        mix.add(pluck(C3, 0.9, seed=22), where + 1.0, 0.22)

        r1 = s("R1")
        b = reveal.beats_for(self.reveal_captions)
        mix.add(pad(r1.dur), r1.start, 0.07)
        mix.add(ding(), r1.start + b["glow"], 0.12)

        s10 = s("S10")
        for i in range(4):
            mix.add(thump(i + 20), s10.start + 0.5 + i * 0.22, 0.14)
        mix.add(pluck(G2, seed=5), self.duration - 0.4, 0.2)  # leads into S01's opening pluck on the loop

    def thumbnail(self, path: Path):
        cam = Camera(0.95, 625, 1080, 540, 1160)
        img = new_frame(cafe.wall_color())
        c = Canvas(img, cam)
        cafe.back(c, elevator=0.0)
        cast.draw(c, DEV, Pose(*cafe.SEAT_UP, 1, "annoyed", hands="phone_ear"))
        cast.draw(c, MIRA, Pose(*cafe.SEAT_GROUND, 1, "annoyed", hands="phone_ear"))
        cafe.front(c)
        s = Canvas(img, SCREEN)
        s.text(540, 90, "SOFTWARE IN DISGUISE · 06", 34, weight=DEMI)
        s.rect(60, 140, 1020, 420, fill=MUSTARD, width=9, radius=20)
        s.text(540, 225, "WE'RE BOTH ON", 96, weight=HEAVY)
        s.text(540, 335, "THE 1ST FLOOR.", 96, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


if __name__ == "__main__":
    Episode06().render()
