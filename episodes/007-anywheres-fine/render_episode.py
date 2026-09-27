"""Render Episode 07 (leader election, "Anywhere's Fine") end to end.

    ../../.venv/bin/python voices.py
    ../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.mp4
    ../../.venv/bin/python render_episode.py   # deliverables/episode-07-anywheres-fine-final.mp4

Shared machinery lives in kit/episode.py; this file is only the story. First episode built on the Episode 4-6
analytics: a close-up first frame, speech and faces through the first 10 s (time passes on a wall clock, not a card),
a ~3 s reveal inside the scene (freeze frame, "LEADER" tag, stamped term), and a final gag after the reveal.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kit import cast, living_room as room, restaurant  # noqa: E402
from kit.canvas import ALERT, DEMI, HEAVY, INK, MUSTARD, SCREEN, Camera, Canvas, ease, finish, lerp, new_frame  # noqa: E402
from kit.cast import DEV, JO, MIRA, Pose  # noqa: E402
from kit.episode import Ctx, Episode, Shot, cam_lerp, scene  # noqa: E402
from kit.overlays import caption, dim, dotted_arrow, leader_tag, stamp  # noqa: E402
from kit.sound import ding, growl, murmur, pad, pluck, tick, whoosh  # noqa: E402

LOOKS = {"DEV": DEV, "JO": JO, "MIRA": MIRA}
SEAT_X = {"DEV": 330, "JO": 575, "MIRA": 820}
FACING = {"DEV": 1, "JO": 1, "MIRA": -1}
SEAT_Y = 1130

# Tight framing throughout: faces must read at phone size (Episode 6's wide first frame lost the most swipes).
THREE = Camera(1.55, 575, 1015, 540, 1000)
THREE_PUSHED = Camera(1.65, 575, 1015, 540, 1000)
CLOCK_SHOT = Camera(1.4, 525, 1000, 540, 1030)  # wide enough for the wall clock at the left
TOWARD_JO = Camera(1.9, 660, 1015, 540, 1050)


def close(who: str) -> Camera:
    return Camera(2.6, SEAT_X[who], 1015, 540, 1060)


STAND_X = {"DEV": 840, "JO": 1040, "MIRA": 1240}
DOOR_CAM = Camera(1.3, 1180, 850, 540, 1000)

EVENING, LATER = 19 * 60, 19 * 60 + 40  # the wall clock: 7:00 PM, then 7:40 PM


def sit(ctx: Ctx, who: str, expr: str, sink: float = 0.0, **kw) -> Pose:
    """Seated on the couch (or at the restaurant table). `sink` slides them lower as hunger wins."""
    pose = Pose(SEAT_X[who], SEAT_Y + sink, kw.pop("facing", FACING[who]), expr, mouth=ctx.mouth(who),
                blink=ctx.blink(who), **kw)
    pose.extras.setdefault("breathe", ctx.breathe(phase={"DEV": 0.0, "JO": 0.5, "MIRA": 0.3}[who]))
    return pose


def couch(ctx: Ctx, cam: Camera, poses: dict, time="evening", clock=EVENING, **kw):
    return scene(ctx, cam, time=time, seated=[(LOOKS[w], p) for w, p in poses.items()], clock=clock, **kw)


def hungry(ctx: Ctx, sink: float, exprs=("tired", "tired", "tired"), gazes=(None, None, None)) -> dict:
    return {
        "DEV": sit(ctx, "DEV", exprs[0], sink, hands="belly", gaze=gazes[0]),
        "JO": sit(ctx, "JO", exprs[1], sink + 6, gaze=gazes[1]),
        "MIRA": sit(ctx, "MIRA", exprs[2], sink + 3, gaze=gazes[2]),
    }


# --- shots ----------------------------------------------------------------------------------------------------


def s01_where(ctx: Ctx):
    cam = cam_lerp(THREE, THREE_PUSHED, ease(ctx.k))  # moving from the first frame
    return couch(ctx, cam, hungry(ctx, 20, gazes=(1, -1, -1)))


def s02_dev(ctx: Ctx):
    return couch(ctx, close("DEV"), hungry(ctx, 20, gazes=(1, 1, -1)))


def s03_jo(ctx: Ctx):
    poses = hungry(ctx, 20, exprs=("tired", "deadpan", "tired"), gazes=(1, 1, -1))
    return couch(ctx, close("JO"), poses)


def s04_mira(ctx: Ctx):
    return couch(ctx, close("MIRA"), hungry(ctx, 20, gazes=(1, 1, -1)))


def s05_forty_minutes(ctx: Ctx):
    """Forty minutes pass on the wall clock while they keep deferring; the light drops and they slide lower."""
    k = min(1.0, ctx.t / 0.8)
    minutes = lerp(EVENING, LATER, ease(k))
    sink = lerp(20, 60, ease(k))
    time = "evening" if k < 0.5 else "night"
    return couch(ctx, CLOCK_SHOT, hungry(ctx, sink, gazes=(1, 1, -1)), time=time, clock=minutes)


def s06a_dev_thai(ctx: Ctx):
    poses = hungry(ctx, 60)
    poses["DEV"] = sit(ctx, "DEV", "cheerful", 30, head_dy=-10)
    return couch(ctx, close("DEV"), poses, time="night", clock=LATER)


def s06b_mira_if(ctx: Ctx):
    poses = hungry(ctx, 60, exprs=("cheerful", "tired", "neutral"))
    return couch(ctx, close("MIRA"), poses, time="night", clock=LATER)


def s06c_dev_deflates(ctx: Ctx):
    k = ease(ctx.k)
    poses = hungry(ctx, 60)
    poses["DEV"] = sit(ctx, "DEV", "neutral" if ctx.k < 0.6 else "tired", lerp(30, 70, k), head_dy=lerp(-10, 18, k))
    return couch(ctx, close("DEV"), poses, time="night", clock=LATER + 1)


def s07_mira_points(ctx: Ctx):
    cam = cam_lerp(THREE, TOWARD_JO, ease(ctx.k))
    poses = hungry(ctx, 60, exprs=("tired", "deadpan", "determined"), gazes=(1, 1, -1))
    poses["MIRA"] = sit(ctx, "MIRA", "determined", 10, hands="point", reach=(SEAT_X["JO"] + 110, 1085))
    poses["DEV"] = sit(ctx, "DEV", "shock", 40, hands="belly", gaze=1)
    return couch(ctx, cam, poses, time="night", clock=LATER + 2)


def s08a_jo_thai(ctx: Ctx):
    poses = hungry(ctx, 60, exprs=("shock", "deadpan", "determined"), gazes=(1, 0, -1))
    return couch(ctx, close("JO"), poses, time="night", clock=LATER + 2)


def door_frame(ctx: Ctx):
    """All three already at the open front door, shoes on: forty minutes of slumping, then instant readiness."""
    poses = {w: ctx.standing(w, STAND_X[w], 1380, 1, "cheerful") for w in ("DEV", "MIRA")}
    poses["JO"] = ctx.standing("JO", STAND_X["JO"], 1380, 1, "confident")
    return scene(ctx, DOOR_CAM, time="night", standing=[(LOOKS[w], p) for w, p in poses.items()],
                 clock=LATER + 2, door="open")


def s09_order(ctx: Ctx):
    """The final gag: at the restaurant, the next decision. Dev and Mira turn to Jo; Jo is not doing this every time."""
    turn = ease((ctx.t - ctx.ep.turn_at) / 0.5) if ctx.t > ctx.ep.turn_at else 0.0
    def menu():
        return dict(hands="menu", extras={"menu_y": -10})

    poses = {
        "DEV": sit(ctx, "DEV", "neutral", 0, gaze=lerp(0.2, 1, turn), gaze_y=lerp(1, 0, turn), **menu()),
        "JO": sit(ctx, "JO", "deadpan" if turn < 0.5 else "unimpressed", 0, gaze=0.0, gaze_y=lerp(1, 0, turn), **menu()),
        "MIRA": sit(ctx, "MIRA", "neutral", 0, gaze=lerp(-0.2, -1, turn), gaze_y=lerp(1, 0, turn), **menu()),
    }
    return scene(ctx, THREE, set=restaurant, seated=[(LOOKS[w], p) for w, p in poses.items()])


# --- episode --------------------------------------------------------------------------------------------------


class Episode07(Episode):
    here = HERE
    final_name = "episode-07-anywheres-fine-final.mp4"
    reveal_chunks = ["reveal-1", "reveal-2"]
    promise_size = 64
    reveal_hold = 0.6  # extra time on the stamped term before the final gag

    def build_shots(self) -> list[Shot]:
        d, ln = self.dur, self.line
        mira_b = (570, 440, 470)
        close_b = (100, 470, 640)
        easy_at = 0.5 + d("dev-whatever") + 0.15
        same_at = easy_at + d("mira-easy") + 0.15
        self.turn_at = 0.3 + d("mira-what-order") + 0.15
        not_at = self.turn_at + 0.6
        self.door_hold = 1.3
        return [
            Shot("S01 where should we eat", 0.1 + d("mira-where-eat") + 0.3, s01_where,
                 [ln("mira-where-eat", 0.1, mira_b)]),
            Shot("S02 Dev anywhere", 0.08 + d("dev-anywhere") + 0.2, s02_dev, [ln("dev-anywhere", 0.08, close_b)]),
            Shot("S03 Jo you pick", 0.08 + d("jo-you-pick") + 0.2, s03_jo, [ln("jo-you-pick", 0.08, close_b)]),
            Shot("S04 Mira don't mind", 0.08 + d("mira-dont-mind") + 0.25, s04_mira,
                 [ln("mira-dont-mind", 0.08, close_b)]),
            Shot("S05 forty minutes later", same_at + d("jo-same") + 0.35, s05_forty_minutes,
                 # Stacked to the right of the wall clock, so the forty minutes stay visible.
                 [ln("dev-whatever", 0.5, (230, 400, 760)), ln("mira-easy", easy_at, (600, 560, 440)),
                  ln("jo-same", same_at, (250, 740, 400))]),
            Shot("S06a Dev what about Thai", 0.08 + d("dev-thai") + 0.2, s06a_dev_thai, [ln("dev-thai", 0.08, close_b)]),
            Shot("S06b Mira if you want", 0.08 + d("mira-if-you-want") + 0.2, s06b_mira_if,
                 [ln("mira-if-you-want", 0.08, close_b)]),
            Shot("S06c Dev only if you want", 0.08 + d("dev-only-if-you") + 0.45, s06c_dev_deflates,
                 [ln("dev-only-if-you", 0.08, close_b)]),
            Shot("S07 Mira makes Jo the decider", 0.1 + d("mira-jo-choose") + 0.25, s07_mira_points,
                 [ln("mira-jo-choose", 0.1, (300, 420, 720))]),
            Shot("S08a Jo Thai", 0.08 + d("jo-thai") + 0.12, s08a_jo_thai, [ln("jo-thai", 0.08, (300, 520, 420))]),
            Shot("S08b at the door", self.door_hold, door_frame),
            Shot("R1 reveal", self.reveal_dur + self.reveal_hold, lambda ctx: ctx.ep.reveal_frame(ctx.t), self.reveal_lines),
            Shot("S09 what should we order (loops to S01)", not_at + d("jo-not-every-time") + 0.35, s09_order,
                 [ln("mira-what-order", 0.3, (440, 440, 600)), ln("jo-not-every-time", not_at, (100, 655, 580))]),
        ]

    # The reveal happens inside the scene: the doorway shot freezes and dims, Hussain's voice names the idea, a
    # "LEADER" tag pops over Jo with dotted arrows from Dev and Mira, and the term is stamped across the frame.
    def reveal_beats(self) -> dict:
        (c1, _), (c2, _) = self.reveal_captions
        return {"dim": 0.0, "tag": c2 + 0.35, "arrows": c2 + 0.55, "stamp": c2 + 0.75}

    def reveal_frame(self, t: float):
        if not hasattr(self, "_frozen"):
            door = self.shot("S08b")
            self._frozen = door.draw(Ctx(self, door, door.dur - 0.01))
        b = self.reveal_beats()
        img = dim(self._frozen, 0.38 * ease(t / 0.25))
        c = Canvas(img, SCREEN)
        c.text(60, 150, "SOFTWARE IN DISGUISE · 07", 30, fill=(236, 230, 220), weight=DEMI, anchor="lm")
        current = [text for start, text in self.reveal_captions if t >= start]
        if current:
            caption(c, 230, current[-1])
        head = {w: DOOR_CAM.to_screen(STAND_X[w] + 4, 1380 - 560) for w in STAND_X}
        jo_x, jo_y = head["JO"]
        tag_y = jo_y - 250
        dotted_arrow(c, (head["DEV"][0] + 40, head["DEV"][1] - 110), (jo_x - 150, tag_y + 20), (t - b["arrows"]) / 0.4)
        dotted_arrow(c, (head["MIRA"][0] - 40, head["MIRA"][1] - 110), (jo_x + 150, tag_y + 20), (t - b["arrows"]) / 0.4)
        leader_tag(c, jo_x, tag_y, (t - b["tag"]) / 0.25)
        stamp(c, 1400, "LEADER ELECTION", (t - b["stamp"]) / 0.2)
        return img

    def sound_design(self, mix):
        s = self.shot
        C3, G2, E3, C4, E4, G4 = 130.81, 98.0, 164.81, 261.63, 329.63, 392.0
        mix.add(growl(0.9), 0.02, 0.45)  # the first sound is a stomach
        for when, f in ((0.15, C3), (0.55, G2)):
            mix.add(pluck(f, seed=int(f)), when, 0.18)

        s05 = s("S05")
        for i in range(8):  # the clock racing through forty minutes
            mix.add(tick(), s05.start + 0.05 + i * 0.1, 0.12)
        mix.add(growl(1.2, seed=92), s05.start + 0.55, 0.55)

        mix.add(pluck(E3, 0.6, seed=31), s("S06a").start + 0.05, 0.2)  # hope
        s06c = s("S06c")
        mix.add(pluck(E3, 0.5, seed=32), s06c.start + s06c.dur - 0.45, 0.18)  # and deflation
        mix.add(pluck(C3, 0.9, seed=33), s06c.start + s06c.dur - 0.2, 0.18)
        mix.add(pluck(G2, 0.6, seed=34), s("S07").start + 0.1, 0.2)  # the point

        door = s("S08b")
        mix.add(whoosh(), door.start - 0.12, 0.22)
        for i, f in enumerate((C4, E4, G4)):  # a quick "ta-da"
            mix.add(pluck(f, 0.7, seed=40 + i), door.start + 0.04 + i * 0.07, 0.2)

        r1 = s("R1")
        b = self.reveal_beats()
        mix.add(pad(r1.dur), r1.start, 0.06)
        mix.add(ding(), r1.start + b["tag"], 0.12)

        s09 = s("S09")
        mix.add(murmur(s09.dur, seed=71), s09.start, 0.035)
        mix.add(pluck(G2, seed=5), self.duration - 0.4, 0.2)  # leads into S01's opening pluck on the loop

    def thumbnail(self, path: Path):
        img = new_frame(room.wall_color("evening"))
        c = Canvas(img, Camera(1.12, 575, 1040, 540, 1250))
        room.back(c, "evening", clock=LATER)
        for w in ("DEV", "JO", "MIRA"):
            cast.draw(c, LOOKS[w], Pose(SEAT_X[w], SEAT_Y + 30, FACING[w], "tired" if w != "JO" else "deadpan",
                                        hands="belly" if w == "DEV" else "rest"))
        room.front(c)
        s = Canvas(img, SCREEN)
        s.text(540, 90, "SOFTWARE IN DISGUISE · 07", 34, weight=DEMI)
        s.rect(60, 140, 1020, 420, fill=MUSTARD, width=9, radius=20)
        s.text(540, 225, "ANYWHERE'S", 104, weight=HEAVY)
        s.text(540, 335, "FINE.", 104, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


if __name__ == "__main__":
    Episode07().render()
