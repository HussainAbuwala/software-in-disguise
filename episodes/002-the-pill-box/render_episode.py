"""Render Episode 02 remake (idempotency, "the pill box") end to end.

    ../../.venv/bin/python voices.py
    ../../.venv/bin/python prep_reveal.py      # once Hussain's take exists: audio/source/reveal-hussain-raw.*
    ../../.venv/bin/python render_episode.py   # deliverables/episode-02-the-pill-box-final.mp4
    ../../.venv/bin/python render_episode.py --stills   # build/stills.png, one frame per beat, for layout checks

Shared machinery lives in kit/episode.py; this file is only the story. Book moment 9.5, with Mom instead of Grandpa.

Hook v2 (after the Episode 3 remake's 62.7% swipe-away): frame 1 is the danger itself (the pill at Mom's lips, Mira's
hand on her wrist), the voice is the first sound, the first shots are tight close-ups, and there's no promise card.

Story: "Mom! Stop!" She can't remember whether she took today's pill, and "one more, to be safe" is what she said
yesterday too; the strip shows three gone on a Tuesday. Mira slams down a Monday-to-Sunday box. Next morning:
"...Did I?" Wednesday's slot is empty, so she did; checking again and again changes nothing. Reveal (with one line
on why it matters: paying twice). Final gag, the limit: the box only works if the dose matches the day, and Mom takes
Thursday's now to save time, pill to her lips, which loops into "Mom! Stop!".
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from PIL import Image  # noqa: E402

from kit import cast, kitchen  # noqa: E402
from kit.canvas import (ALERT, DEMI, HEAVY, INK, MUSTARD, PAPER, SCREEN, TEAL, H, W, Camera, Canvas, ease,  # noqa: E402
                        finish, lerp, new_frame)
from kit.cast import MIRA, MOM, Pose  # noqa: E402
from kit.episode import Ctx, Episode, Shot, scene  # noqa: E402
from kit.living_room import _clock  # noqa: E402
from kit.overlays import caption, check_mark, dim, stamp  # noqa: E402
from kit.sound import click, pad, pluck, tape_rip, thump, tick, whoosh  # noqa: E402

FLOOR = 1380
MOM_X, MIRA_X = 330, 760
SEVEN_02 = 7 * 60 + 2
PILL_REST = (505, 1030)  # world: Mom's pill, held out at chest height
PILL_MOUTH = (398, 858)  # at her lips
BOX_AT = (548, 1152)  # world: bottom-centre of the pill box on the counter
BOX_S = 1.15
WOOD = (176, 128, 84)
LID = (168, 208, 236)
MON, TUE, WED, THU = 0, 1, 2, 3


# --- props -----------------------------------------------------------------------------------------------------


def pill(c: Canvas, x, y, s=1.0):
    c.rect(x - 26 * s, y - 13 * s, x + 26 * s, y + 13 * s, fill=PAPER, radius=13 * s, width=5)
    c.rect(x, y - 13 * s, x + 26 * s, y + 13 * s, fill=ALERT, radius=13 * s, width=5)


def slot_x(i: int, x=BOX_AT[0], s=BOX_S) -> float:
    w = 300 * s
    return x - w / 2 + (i + 0.5) * w / 7


def lid_top(y=BOX_AT[1], s=BOX_S) -> float:
    return y - 92 * s - 16 * s


def pill_box(c: Canvas, x=BOX_AT[0], y=BOX_AT[1], s=BOX_S, opened: dict | None = None, empty=(MON, TUE)):
    """Monday-to-Sunday organiser, bottom-centre at (x, y). `opened` maps a day to how far its lid is up (0..1); an
    open slot shows its pill, or a dark empty well."""
    opened = opened or {}
    w, h = 300 * s, 92 * s
    c.rect(x - w / 2, y - h, x + w / 2, y, fill=(244, 242, 236), radius=12 * s, width=6)
    cw = w / 7
    for i, day in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
        x0 = x - w / 2 + i * cw
        k = opened.get(i, 0.0)
        if k > 0.05:
            c.rect(x0 + 8 * s, y - h - 4 * s, x0 + cw - 8 * s, y - h + 44 * s, fill=(70, 70, 78), radius=6 * s, width=5)
            if i not in empty:
                pill(c, x0 + cw / 2, y - h + 22 * s, 0.62 * s)
        top, bot = y - h - 16 * s - 80 * s * k, y - h + 40 * s - 96 * s * k
        c.rect(x0 + 5 * s, top, x0 + cw - 5 * s, bot, fill=LID, radius=8 * s, width=5)
        c.text(x0 + cw / 2, (top + bot) / 2, day, 21 * s * (1 - 0.25 * k), weight=HEAVY)


def blister_strip(c: Canvas, cx, cy, s=1.0, gone=3):
    """Top-down blister strip, 2 x 5, the first `gone` pockets pushed through."""
    w, h = 760 * s, 360 * s
    c.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill=(206, 210, 216), radius=26 * s, width=7)
    c.line([(cx - w / 2 + 20 * s, cy), (cx + w / 2 - 20 * s, cy)], fill=(176, 180, 188), width=4)
    for i in range(10):
        col, row = i % 5, i // 5
        px = cx - w / 2 + (col + 0.5) * w / 5
        py = cy - h / 4 + row * h / 2
        if i < gone:
            jag = [(px + 50 * s * math.cos(a) * (0.8 + 0.2 * ((k * 7) % 3)), py + 62 * s * math.sin(a) * (0.8 + 0.2 * ((k * 5) % 3)))
                   for k, a in enumerate(j * math.pi / 6 for j in range(12))]
            c.poly(jag, fill=(96, 90, 92), width=5)
        else:
            c.ellipse(px - 50 * s, py - 62 * s, px + 50 * s, py + 62 * s, fill=(236, 238, 242), width=5)
            c.rect(px - 22 * s, py - 44 * s, px + 22 * s, py + 44 * s, fill=PAPER, radius=22 * s, width=5)
            c.rect(px - 22 * s, py, px + 22 * s, py + 44 * s, fill=ALERT, radius=22 * s, width=5)


def strip_insert(c: Canvas, point: float = 1.0):
    """Top-down counter with the strip, in 1080x1920 insert coordinates; Mira's finger comes in from the right."""
    c.rect(-400, -400, 1500, 2400, fill=WOOD, outline=None)
    for i in range(-2, 14):
        c.line([(-400, 180 * i + 40), (1500, 180 * i + 70)], fill=(160, 114, 74), width=5)
    blister_strip(c, 540, 860)
    c.text(540, 1085, "TAKE ONE DAILY", 40, fill=(90, 90, 96), weight=DEMI)
    tip = (lerp(900, 330, ease(point)), lerp(1300, 900, ease(point)))
    c.limb([(1400, 1500), (tip[0] + 90, tip[1] + 60)], MIRA.top, 70)
    cast.hand(c, tip[0] + 60, tip[1] + 40, MIRA, r=40)
    c.line([(tip[0] + 60, tip[1] + 40), tip], fill=MIRA.skin, width=22)


def pay_diagram(c: Canvas, y: float, k: float):
    """Why it matters, in one picture: PAY tapped twice -> charged once. Screen coordinates; fades in with k."""
    if k <= 0:
        return
    a = ease(k)
    y = y + 40 * (1 - a)
    c.rect(90, y, 990, y + 250, fill=PAPER, width=6, radius=30)
    c.rect(140, y + 70, 380, y + 180, fill=TEAL, width=6, radius=24)
    c.text(260, y + 125, "PAY", 56, fill=PAPER, weight=HEAVY)
    for i in range(2):  # two taps
        c.circle(335 + i * 34, y + 85 - i * 22, 20, fill=None, width=5)
    c.text(430, y + 125, "× 2", 50, weight=HEAVY, anchor="lm")
    c.line([(540, y + 125), (640, y + 125)], width=7)
    c.poly([(640, y + 105), (670, y + 125), (640, y + 145)], fill=INK)
    c.text(700, y + 95, "Charged", 44, weight=DEMI, anchor="lm")
    c.text(700, y + 155, "once", 52, fill=TEAL, weight=HEAVY, anchor="lm")
    check_mark(c, 900, y + 150, 34)


def day_calendar(c: Canvas, day: str, x0=566, y0=724, x1=662, y1=842):
    c.rect(x0, y0, x1, y1, fill=PAPER, width=6, radius=6)
    c.rect(x0, y0, x1, y0 + 26, fill=ALERT, width=6, radius=6)
    c.text((x0 + x1) / 2, (y0 + 26 + y1) / 2 + 2, day, 40, weight=HEAVY)


def kitchen_with_clock(minutes: float = SEVEN_02):
    """Mom's kitchen with the wall clock and a tear-off day calendar. `day` is the showing page; `tear` (0..1) rips
    the page before it (`was`) up and away."""

    def back(c, time="day", t=0.0, behind=None, day="TUE", was=None, tear=1.0, **kw):
        kitchen.back(c, time, t=t, behind=behind)
        _clock(c, minutes, (655, 640))
        day_calendar(c, day)
        if was and tear < 1.0:
            k = ease(tear)
            day_calendar(c, was, 566 + 30 * k, 724 - 140 * k, 662 + 30 * k, 842 - 236 * k)

    return SimpleNamespace(wall_color=kitchen.wall_color, back=back, front=kitchen.front)


KITCHEN = kitchen_with_clock()


# --- poses -----------------------------------------------------------------------------------------------------


def mom_pose(ctx: Ctx, expr: str, pill_at, gaze_y=0.3, gaze=0.6, **kw):
    return ctx.standing("MOM", MOM_X, FLOOR, 1, expr, hands="reach", reach=pill_at, gaze=gaze, gaze_y=gaze_y, **kw)


def mira_pose(ctx: Ctx, expr: str, hands="hips", **kw):
    return ctx.standing("MIRA", MIRA_X, FLOOR, -1, expr, hands=hands, **kw)


def pill_path(ctx: Ctx) -> tuple:
    """Mom's pill during S02: out in front, then up toward her lips."""
    k = ease((ctx.t - 0.3) / 1.4)
    return (lerp(PILL_REST[0], PILL_MOUTH[0], k), lerp(PILL_REST[1], PILL_MOUTH[1], k))


def box_drop(t: float, land: float) -> float:
    """Vertical offset of the pill box: falls in, lands at `land` (shot time), small bounce."""
    if t >= land:
        return -26 * math.exp(-(t - land) * 14) * abs(math.sin((t - land) * 30))
    return -900 * (1 - ease((t - (land - 0.28)) / 0.28)) if t > land - 0.28 else -2000


def flaps(t: float, start: float, period: float = 0.55, count: int = 5) -> float:
    """Lid height for a lid flipped open and shut `count` times from `start`; stays open after the last flip."""
    u = (t - start) / period
    if u <= 0:
        return 0.0
    if u >= count - 0.5:
        return 1.0
    return abs(math.sin(u * math.pi)) ** 0.6


# --- the episode -----------------------------------------------------------------------------------------------

CLOSE_MOM = (3.4, 360, 840, 500, 900)  # zoom, focus x, focus y, screen x, screen y (the loop point)
BOX_TWO = Camera(1.9, 545, 1000, 540, 1100)


class Episode02(Episode):
    here = HERE
    final_name = "episode-02-the-pill-box-final.mp4"
    reveal_chunks = ["reveal-1", "reveal-2", "reveal-3"]
    promise_until = 0.0  # hook v2: no promise card
    reveal_hold = 0.5
    land = 0.95  # S04: the box hits the counter on "this"
    flip_at = 1.15  # S05: Mira flips Wednesday's lid

    def build_shots(self):
        L = self.line
        return [
            Shot("S01 stop", 2.7, self.s01, [L("mira-stop", 0.0, (560, 220, 420, 1080, 1150)),
                                             L("mom-my-pill", 1.05, (60, 300, 480))]),
            Shot("S01b already", 1.35, self.s01b, [L("mira-already", 0.05, (80, 260, 520))]),
            Shot("S01c did I", 1.4, self.s01c, [L("mom-did-i", 0.05, (560, 300, 320))]),
            Shot("S02 to be safe", 4.15, self.s02, [L("mom-to-be-safe", 0.1, (80, 260, 560)),
                                                    L("mira-yesterday", 2.55, (440, 300, 560))]),
            Shot("S03 strip", 4.2, self.s03, [L("mira-three-gone", 0.15, (60, 200, 600, 1020, 1500)),
                                              L("mom-which-day", 2.1, (400, 1240, 600, 60, 1500))]),
            Shot("S04 the box", 2.6, self.s04, [L("mira-use-this", 0.1, (600, 200, 420))]),
            # Next morning (the window's brighter, the clock says 7:02 again).
            Shot("S05 next morning", 3.25, self.s05, [L("mom-did-i", 0.05, (60, 330, 320)),
                                                      L("mira-wednesday-empty", 1.35, (440, 250, 580))]),
            Shot("S06 ten times", 3.95, self.s06, [L("mom-forget-again", 0.05, (60, 260, 480)),
                                                   L("mira-ten-times", 1.65, (560, 190, 500))]),
            self.reveal_shot_held(),
            Shot("S07 Thursday", 2.15, self.s07, [L("mom-thursday", 0.05, (60, 280, 560))]),
            Shot("S07b saves time", 1.35, self.s07b, [L("mom-saves-time", 0.05, (60, 300, 380))]),
        ]

    def reveal_shot_held(self):
        return Shot("R1 reveal", self.reveal_dur + self.reveal_hold, lambda ctx: ctx.ep.reveal_frame(ctx.t),
                    self.reveal_lines)

    # Hook ----------------------------------------------------------------------------------------------------
    def close_mom(self, ctx, k0=0.0, k1=0.15):
        z, fx, fy, sx, sy = CLOSE_MOM
        return Camera(z + lerp(k0, k1, ease(ctx.k)), fx, fy, sx, sy)

    def s01(self, ctx):
        """Frame 1: tight on Mom, the pill at her lips; Mira's hand (from off-screen right) grabs her wrist."""
        grab = ease(ctx.t / 0.12)
        mom = mom_pose(ctx, "neutral" if ctx.t < 0.25 else "shock" if ctx.t < 1.05 else "annoyed", PILL_MOUTH,
                       gaze_y=0.0, gaze=1.0)
        mira = ctx.standing("MIRA", 660, FLOOR, -1, "angry", hands="reach",
                            reach=(lerp(470, 400, grab), lerp(900, 915, grab)))
        return scene(ctx, self.close_mom(ctx), set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)],
                     props=lambda c: pill(c, *PILL_MOUTH))

    def s01b(self, ctx):
        cam = Camera(lerp(3.2, 3.3, ease(ctx.k)), 740, 840, 580, 900)
        mira = mira_pose(ctx, "angry", hands="point", reach=(560, 900))
        return scene(ctx, cam, set=KITCHEN, standing=[(MIRA, mira)])

    def s01c(self, ctx):
        at = (470, 960)
        mom = mom_pose(ctx, "frazzled", at, gaze_y=0.7, gaze=0.8)
        return scene(ctx, self.close_mom(ctx, 0.0, 0.1), set=KITCHEN, standing=[(MOM, mom)],
                     props=lambda c: pill(c, *at))

    def s02(self, ctx):
        at = pill_path(ctx)
        yell = ctx.t > 2.55
        cam = Camera(lerp(1.55, 1.65, ease(ctx.k)), 520, 960, 540, 1150)
        mom = mom_pose(ctx, "shock" if yell else "determined", at, gaze_y=0.0)
        mira = mira_pose(ctx, "shock" if yell else "annoyed", hands="point" if yell else "hips", reach=(600, 900))
        return scene(ctx, cam, set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)], props=lambda c: pill(c, *at))

    def s03(self, ctx):
        img = new_frame(WOOD)
        strip_insert(Canvas(img, SCREEN), point=ctx.t / 1.0)
        ctx.bubbles(Canvas(img, SCREEN), SCREEN, {})
        return img

    def s04(self, ctx):
        mom = mom_pose(ctx, "shock" if ctx.t > self.land else "frazzled", PILL_MOUTH, gaze_y=0.4)
        mira = mira_pose(ctx, "determined", hands="reach", reach=(BOX_AT[0] + 90, BOX_AT[1] - 60))
        dy = box_drop(ctx.t, self.land)
        shake = 10 * math.exp(-(ctx.t - self.land) * 12) * math.sin(ctx.t * 90) if ctx.t > self.land else 0
        cam = Camera(1.75, 548, 1000 + shake, 540, 1150)

        def props(c):
            pill(c, *PILL_MOUTH)
            pill_box(c, BOX_AT[0], BOX_AT[1] + dy)

        return scene(ctx, cam, set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)], props=props)

    # The fix, next morning -----------------------------------------------------------------------------------
    def s05(self, ctx):
        k = ease((ctx.t - self.flip_at) / 0.2)
        lid_at = (slot_x(WED) + 10, lid_top() - 40 * k)
        mom = ctx.standing("MOM", MOM_X, FLOOR, 1, "frazzled" if k < 1 else "cheerful", hands="mug", gaze=0.9, gaze_y=0.8)
        mira = mira_pose(ctx, "determined", hands="reach", reach=lid_at) if ctx.t > 0.7 else mira_pose(ctx, "neutral")
        cam = Camera(lerp(1.9, 2.0, ease(ctx.k)), 545, 1000, 540, 1100)
        return scene(ctx, cam, set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)], day="WED", was="TUE",
                     tear=ctx.t / 0.35, props=lambda c: pill_box(c, opened={WED: k}, empty=(MON, TUE, WED)))

    def s06(self, ctx):
        """Mom checks again, and again: open, empty, shut. Checking changes nothing."""
        k = flaps(ctx.t, 0.35)
        mom = mom_pose(ctx, "unimpressed", (slot_x(WED) - 10, lid_top() - 40 * k), gaze=0.9, gaze_y=0.8)
        mira = mira_pose(ctx, "smug" if ctx.t > 1.65 else "neutral", hands="crossed")
        cam = Camera(lerp(2.0, 2.2, ease(ctx.k)), 545, 1010, 540, 1100)
        return scene(ctx, cam, set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)], day="WED",
                     props=lambda c: pill_box(c, opened={WED: k}, empty=(MON, TUE, WED)))

    def reveal_frame(self, t: float):
        if not hasattr(self, "_frozen"):
            done = self.shot("S06")
            clean = Shot(done.name, done.dur, done.draw)  # the same moment without its speech bubbles
            clean.start = done.start
            self._frozen = done.draw(Ctx(self, clean, done.dur - 0.01))
        img = dim(self._frozen, 0.45 * ease(t / 0.25))
        c = Canvas(img, SCREEN)
        c.text(60, 150, "SOFTWARE IN DISGUISE · 02", 30, fill=(236, 230, 220), weight=DEMI, anchor="lm")
        current = [text for start, text in self.reveal_captions if t >= start]
        if current:
            caption(c, 230, current[-1])
        c2, c3 = self.reveal_captions[1][0], self.reveal_captions[2][0]
        stamp(c, 470, "IDEMPOTENCY", (t - (c2 + 0.5)) / 0.2, size=78)
        pay_diagram(c, 1180, (t - c3) / 0.3)
        return img

    # Final gag: the limit. The box only works if the dose matches the day. -----------------------------------
    def s07(self, ctx):
        k = ease((ctx.t - 0.35) / 0.2)
        lift = ease((ctx.t - 1.0) / 0.6)
        at = (lerp(slot_x(THU), 470, lift), lerp(lid_top() + 30, 980, lift))
        mom = mom_pose(ctx, "cheerful", at, gaze=0.9, gaze_y=0.6)
        mira = mira_pose(ctx, "shock" if ctx.t > 1.2 else "smug", hands="crossed")
        cam = Camera(lerp(1.9, 2.1, ease(ctx.k)), 520, 1000, 540, 1100)

        def props(c):
            pill_box(c, opened={THU: k}, empty=(MON, TUE, WED) + ((THU,) if ctx.t > 0.9 else ()))
            if ctx.t > 0.9:
                pill(c, *at)

        return scene(ctx, cam, set=KITCHEN, standing=[(MOM, mom), (MIRA, mira)], props=props, day="WED")

    def s07b(self, ctx):
        """Back to frame 1's framing, pill rising to her lips: the loop cuts into Mira's hand and "Mom! Stop!"."""
        k = ease(ctx.t / 0.7)
        at = (lerp(470, PILL_MOUTH[0], k), lerp(960, PILL_MOUTH[1], k))
        mom = mom_pose(ctx, "cheerful" if ctx.t < 0.9 else "neutral", at, gaze_y=0.0, gaze=1.0)
        return scene(ctx, self.close_mom(ctx, 0.1, 0.0), set=KITCHEN, standing=[(MOM, mom)], day="WED",
                     props=lambda c: pill(c, *at))

    # Sound ---------------------------------------------------------------------------------------------------
    def sound_design(self, mix):
        s = self.shot
        mix.add(whoosh(0.25), 0.0, 0.12)  # the grab, under "Mom! Stop!" (the voice is the first thing heard)
        for when, f in ((0.95, 130.81), (1.3, 98.0)):
            mix.add(pluck(f, seed=int(f)), when, 0.16)
        for i in range(8):  # the kitchen clock, once the hook has landed
            mix.add(tick(), 1.0 + i * 0.5, 0.1)
        for name in ("S01b", "S01c", "S02", "S03"):
            mix.add(whoosh(0.2), s(name).start - 0.08, 0.08)
        s04 = s("S04")
        mix.add(whoosh(0.3), s04.start + self.land - 0.3, 0.14)
        mix.add(thump(), s04.start + self.land, 0.45)
        mix.add(pluck(164.81, 0.8, seed=33), s04.start + self.land + 0.05, 0.16)

        s05 = s("S05")
        mix.add(whoosh(0.35, seed=94), s05.start - 0.15, 0.12)  # time jump
        mix.add(tape_rip(0.35), s05.start + 0.02, 0.3)  # the calendar page
        for i in range(4):
            mix.add(tick(), s05.start + 0.05 + i * 0.5, 0.1)
        mix.add(click(), s05.start + self.flip_at + 0.15, 0.35)
        mix.add(pluck(196.0, 0.6, seed=41), s05.start + self.flip_at + 0.2, 0.12)
        s06 = s("S06")
        for i in range(5):  # every flip: open (click) and shut (click)
            mix.add(click(), s06.start + 0.35 + i * 0.55 + 0.08, 0.25)
            if i < 4:
                mix.add(click(), s06.start + 0.35 + (i + 1) * 0.55 - 0.05, 0.18)

        r1 = s("R1")
        mix.add(pad(r1.dur), r1.start, 0.08)
        mix.add(thump(2), r1.start + self.reveal_captions[1][0] + 0.5, 0.25)  # the stamp

        s07 = s("S07")
        mix.add(click(), s07.start + 0.45, 0.3)
        mix.add(pluck(164.81, 0.4, seed=12), s07.start + 1.2, 0.14)

    def thumbnail(self, path: Path):
        z, fx, fy, sx, sy = CLOSE_MOM
        cam = Camera(z * 0.9, fx, fy - 40, sx + 30, sy + 420)
        img = new_frame(kitchen.wall_color())
        c = Canvas(img, cam)
        KITCHEN.back(c)
        cast.draw(c, MOM, Pose(MOM_X, FLOOR, 1, "frazzled", standing=True, hands="reach", reach=PILL_MOUTH, gaze=1.0))
        pill(c, *PILL_MOUTH)
        s = Canvas(img, SCREEN)
        s.text(540, 90, "SOFTWARE IN DISGUISE · 02", 34, weight=DEMI)
        s.rect(60, 140, 1020, 420, fill=MUSTARD, width=9, radius=20)
        s.text(540, 225, "“DID I", 104, weight=HEAVY)
        s.text(540, 335, "TAKE IT?”", 104, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


def stills(ep: Episode02):
    names = [(s.name, s.start + s.dur * 0.7) for s in ep.shots] + [("frame 0", 0.0), ("last", ep.duration - 0.02)]
    frames = []
    for _, g in names:
        shot = next(s for s in reversed(ep.shots) if s.start <= g)
        f = shot.draw(Ctx(ep, shot, g - shot.start))
        frames.append(f if f.size == (W, H) else finish(f))
    tw, th, cols = W // 4, H // 4, 7
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (tw * cols, th * rows), INK)
    for i, f in enumerate(frames):
        sheet.paste(f.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(ep.build / "stills.png")
    print(ep.build / "stills.png", f"{ep.duration:.2f}s")


if __name__ == "__main__":
    ep = Episode02()
    stills(ep) if "--stills" in sys.argv else ep.render()
