"""Render Episode 08 (acceptance criteria, "You Said You Cleaned") end to end.

    ../../.venv/bin/python voices.py
    ../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.mp4
    ../../.venv/bin/python render_episode.py   # deliverables/episode-08-you-said-you-cleaned-final.mp4

Shared machinery lives in kit/episode.py; this file is only the story. Tests the Episode 7 lesson: frame 1 shows a
visible problem (the bulging cupboard, a sock poking out) under an accusing line ("You said you cleaned!").
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kit import cast, living_room as room  # noqa: E402
from kit.canvas import ALERT, DEMI, HEAVY, MUSTARD, SCREEN, Camera, Canvas, ease, finish, lerp, new_frame  # noqa: E402
from kit.cast import DEV, JO, MIRA, Pose  # noqa: E402
from kit.episode import Ctx, Episode, Shot, scene  # noqa: E402
from kit.overlays import caption, checklist, dim, stamp  # noqa: E402
from kit.sound import creak, ding, pad, pluck, scribble, thump, whoosh  # noqa: E402

LOOKS = {"DEV": DEV, "JO": JO, "MIRA": MIRA}
FLOOR = 1380
DEV_X, MIRA_X = 820, 1400  # the cupboard (x 1000-1240) stands between them

TWO = Camera(1.25, 1110, 900, 540, 1010)
UNDER = Camera(1.3, 960, 1080, 540, 1000)
DEV_CLOSE = Camera(2.4, 824, 830, 540, 1060)
CUP_CLOSE = Camera(1.9, 1120, 1070, 540, 1000)
MIRA_LIST = Camera(2.3, 1404, 800, 540, 640)

LIST_TITLE = "CLEAN ="
LIST_ITEMS = ["Floor clear", "Nothing under the couch", "Cupboard shuts"]


def room_scene(ctx: Ctx, cam: Camera, standing: dict, messy: bool, strain=1.0, sock=0.4, overlay=None):
    cup = (strain, sock) if messy else (0.0, 0.0)
    return scene(ctx, cam, time="day", standing=[(LOOKS[w], p) for w, p in standing.items()], cupboard=cup,
                 clutter=messy, legs=True, overlay=overlay)


def dev(ctx, expr, x=DEV_X, facing=1, **kw):
    return ctx.standing("DEV", x, FLOOR, facing, expr, **kw)


def mira(ctx, expr, x=MIRA_X, facing=-1, **kw):
    return ctx.standing("MIRA", x, FLOOR, facing, expr, **kw)


# --- shots ----------------------------------------------------------------------------------------------------


def s01_you_said(ctx: Ctx):
    """Frame 1: the problem is visible (the bulging cupboard, a sock poking out) under the accusation."""
    cam = Camera(lerp(1.25, 1.32, ease(ctx.k)), 1110, 900, 540, 1010)  # a slow push-in from the first frame
    return room_scene(ctx, cam, {"DEV": dev(ctx, "confident", hands="hips"),
                                 "MIRA": mira(ctx, "annoyed", hands="crossed")}, messy=True)


def s02_under_couch(ctx: Ctx):
    m = ctx.standing("MIRA", 1250, FLOOR, -1, "annoyed", hands="point", reach=(1090, 1190))
    return room_scene(ctx, UNDER, {"MIRA": m}, messy=True)


def s03_floor_clean(ctx: Ctx):
    return room_scene(ctx, DEV_CLOSE, {"DEV": dev(ctx, "smug", hands="hips")}, messy=True)


def s04_cupboard(ctx: Ctx):
    """The door strains; on "Closed." a sock pops out further."""
    pop = ctx.ep.pop_at
    strain = 1.0 + 0.15 * math.sin(ctx.t * 22) * (ctx.t < pop)
    sock = 0.4 if ctx.t < pop else min(1.0, 0.4 + (ctx.t - pop) * 4)
    return room_scene(ctx, CUP_CLOSE, {"DEV": dev(ctx, "confident", hands="hips"),
                                       "MIRA": mira(ctx, "unimpressed", hands="crossed")},
                      messy=True, strain=min(1.0, strain), sock=sock)


def list_overlay(ticks=(0.0, 0.0, 0.0), big=True):
    def draw(c: Canvas):
        if big:
            checklist(c, 150, 930, 780, LIST_TITLE, LIST_ITEMS, list(ticks), size=52)
            for x in (150, 930):  # Mira's hands holding it up
                c.circle(x, 1300, 34, fill=MIRA.skin, width=6)
        else:
            checklist(c, 520, 1030, 540, LIST_TITLE, LIST_ITEMS, list(ticks), size=36)
    return draw


def s05_clean_means(ctx: Ctx):
    return room_scene(ctx, MIRA_LIST, {"MIRA": mira(ctx, "determined", hands="far_rest")}, messy=True,
                      overlay=list_overlay())


def s06_that_clean(ctx: Ctx):
    k = ease(ctx.k)
    d = dev(ctx, "neutral" if ctx.k < 0.35 else "tired", hands="rest", head_dy=lerp(0, 14, k), gaze_y=0.6)
    return room_scene(ctx, DEV_CLOSE, {"DEV": d}, messy=True)


def s07_done(ctx: Ctx):
    """Hard cut: the room is actually tidy. Mira ticks every item on the list."""
    ep = ctx.ep
    ticks = [max(0.0, min(1.0, (ctx.t - at) / 0.15)) for at in ep.tick_at]
    return room_scene(ctx, TWO, {"DEV": dev(ctx, "cheerful", hands="hips"),
                                 "MIRA": mira(ctx, "neutral" if ticks[-1] < 1 else "cheerful", hands="far_rest")},
                      messy=False, overlay=list_overlay(ticks, big=False))


def s08_my_bed(ctx: Ctx):
    """The final gag: the list never mentioned Jo's room."""
    walk = min(1.0, ctx.t / 1.0)
    bob = -abs(math.sin(ctx.t * math.pi * 4.5)) * 9 if walk < 1 else 0.0
    jo = ctx.standing("JO", lerp(700, 900, ease(walk)), FLOOR, 1, "deadpan", hands="armful", extras={"bob": bob})
    d = dev(ctx, "neutral" if ctx.t < ctx.ep.list_at else "confident", x=1300, facing=-1, hands="rest")
    return room_scene(ctx, TWO, {"JO": jo, "DEV": d}, messy=False)


# --- episode --------------------------------------------------------------------------------------------------


class Episode08(Episode):
    here = HERE
    final_name = "episode-08-you-said-you-cleaned-final.mp4"
    reveal_chunks = ["reveal-1", "reveal-2"]
    promise_size = 64
    reveal_hold = 0.6

    def build_shots(self) -> list[Shot]:
        d, ln = self.dur, self.line
        did_at = 0.1 + d("mira-you-said") + 0.15
        closed_at = 0.1 + d("mira-cupboard") + 0.15
        self.pop_at = closed_at + 0.35
        self.tick_at = [0.1 + d("dev-done") + 0.25 + i * 0.4 for i in range(3)]
        self.list_at = 0.9 + d("jo-my-bed") + 0.15
        return [
            Shot("S01 you said you cleaned", did_at + d("dev-i-did") + 0.3, s01_you_said,
                 [ln("mira-you-said", 0.1, (560, 470, 460)), ln("dev-i-did", did_at, (40, 500, 300))]),
            Shot("S02 under the couch", 0.1 + d("mira-under-couch") + 0.25, s02_under_couch,
                 [ln("mira-under-couch", 0.1, (380, 330, 560))]),
            Shot("S03 the floor is clean", 0.08 + d("dev-floor-clean") + 0.25, s03_floor_clean,
                 [ln("dev-floor-clean", 0.08, (120, 420, 620))]),
            Shot("S04 and the cupboard", self.pop_at + 0.55, s04_cupboard,
                 [ln("mira-cupboard", 0.1, (560, 330, 440)), ln("dev-closed", closed_at, (60, 560, 300))]),
            Shot("S05 clean means this", 0.1 + d("mira-clean-means") + 0.6, s05_clean_means,
                 [ln("mira-clean-means", 0.1, (100, 250, 600))]),
            Shot("S06 oh that clean", 0.08 + d("dev-that-clean") + 0.4, s06_that_clean,
                 [ln("dev-that-clean", 0.08, (120, 420, 620))]),
            Shot("S07 done", self.tick_at[-1] + 0.6, s07_done, [ln("dev-done", 0.1, (40, 500, 300))]),
            Shot("R1 reveal", self.reveal_dur + self.reveal_hold, lambda ctx: ctx.ep.reveal_frame(ctx.t), self.reveal_lines),
            Shot("S08 on my bed (loops to S01)", self.list_at + d("dev-not-on-list") + 0.35, s08_my_bed,
                 [ln("jo-my-bed", 0.9, (40, 470, 550)), ln("dev-not-on-list", self.list_at, (610, 470, 430))]),
        ]

    # The reveal happens inside the scene: the tidy room freezes and dims, Hussain's voice names the idea, the ticked
    # list stays bright, and the term is stamped across the frame.
    def reveal_frame(self, t: float):
        if not hasattr(self, "_frozen"):
            done = self.shot("S07")
            self._frozen = done.draw(Ctx(self, done, done.dur - 0.01))
        (c1, _), (c2, _) = self.reveal_captions
        img = dim(self._frozen, 0.4 * ease(t / 0.25))
        c = Canvas(img, SCREEN)
        c.text(60, 150, "SOFTWARE IN DISGUISE · 08", 30, fill=(236, 230, 220), weight=DEMI, anchor="lm")
        current = [text for start, text in self.reveal_captions if t >= start]
        if current:
            caption(c, 230, current[-1])
        list_overlay((1.0, 1.0, 1.0), big=False)(c)
        stamp(c, 420, "ACCEPTANCE CRITERIA", (t - (c2 + 0.55)) / 0.2, size=68)
        return img

    def sound_design(self, mix):
        s = self.shot
        C3, G2, E3 = 130.81, 98.0, 164.81
        for when, f in ((0.0, C3), (0.4, G2)):
            mix.add(pluck(f, seed=int(f)), when, 0.18)
        mix.add(creak(0.8), 0.35, 0.22)  # the cupboard, straining from the first second

        s04 = s("S04")
        mix.add(creak(1.0, seed=96), s04.start + 0.05, 0.25)
        mix.add(thump(3), s04.start + self.pop_at, 0.3)  # the sock pops out
        mix.add(pluck(659.25, 0.4, seed=12), s04.start + self.pop_at + 0.02, 0.12)

        mix.add(scribble(0.6), s("S05").start + 0.05, 0.2)
        s06 = s("S06")
        mix.add(pluck(E3, 0.5, seed=32), s06.start + s06.dur - 0.5, 0.18)  # deflation
        mix.add(pluck(C3, 0.9, seed=33), s06.start + s06.dur - 0.25, 0.18)

        s07 = s("S07")
        mix.add(whoosh(), s07.start - 0.1, 0.2)
        for i, at in enumerate(self.tick_at):
            mix.add(ding(), s07.start + at, 0.12)
            mix.add(scribble(0.15, seed=40 + i), s07.start + at, 0.12)

        r1 = s("R1")
        mix.add(pad(r1.dur), r1.start, 0.06)

        s08 = s("S08")
        for i in range(4):  # Jo's footsteps
            mix.add(thump(i + 20), s08.start + 0.1 + i * 0.22, 0.12)
        mix.add(pluck(G2, seed=5), self.duration - 0.4, 0.2)  # leads into S01's opening pluck on the loop

    def thumbnail(self, path: Path):
        img = new_frame(room.wall_color("day"))
        c = Canvas(img, Camera(1.25, 1110, 880, 540, 1150))
        room.back(c, "day", cupboard=(1.0, 0.8))
        room.front(c, clutter=True, legs=True)
        cast.draw(c, DEV, Pose(DEV_X, FLOOR, 1, "confident", standing=True, hands="hips"))
        cast.draw(c, MIRA, Pose(MIRA_X, FLOOR, -1, "annoyed", standing=True, hands="crossed"))
        s = Canvas(img, SCREEN)
        s.text(540, 90, "SOFTWARE IN DISGUISE · 08", 34, weight=DEMI)
        s.rect(60, 140, 1020, 420, fill=MUSTARD, width=9, radius=20)
        s.text(540, 225, "“I DID", 104, weight=HEAVY)
        s.text(540, 335, "CLEAN.”", 104, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


if __name__ == "__main__":
    Episode08().render()
