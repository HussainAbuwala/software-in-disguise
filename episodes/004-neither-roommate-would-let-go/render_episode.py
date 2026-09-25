"""Render Episode 04 end to end: code-drawn shots, dialogue, sound design, captions, thumbnail.

    ../../.venv/bin/python voices.py           # once, or after changing lines
    ../../.venv/bin/python prep_reveal.py      # after replacing Hussain's raw reveal take
    ../../.venv/bin/python render_episode.py   # deliverables/episode-04-neither-roommate-would-let-go-final.mp4

The shared machinery (timeline, lip-sync, mixing, rendering, subtitles) lives in kit/episode.py; this file is only
the story: shots, sound design, and thumbnail.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import reveal  # noqa: E402
from kit import cast  # noqa: E402
from kit import living_room as room  # noqa: E402
from kit.canvas import ALERT, DEMI, HEAVY, MUSTARD, SCREEN, Camera, Canvas, ease, finish, lerp, new_frame  # noqa: E402
from kit.cast import DEV, JO, MIRA, Pose  # noqa: E402
from kit.episode import TWO_SHOT, WIDE, Ctx, Episode, Shot, cam_lerp  # noqa: E402
from kit.episode import scene as kit_scene  # noqa: E402
from kit.overlays import card  # noqa: E402
from kit.sound import chirp, click, hum, murmur, pad, pluck, slide_whistle, snore, thump, tick, tv_on  # noqa: E402


def scene(ctx: Ctx, cam: Camera, time: str, tv: str, pizza: bool, dev: Pose | None, mira: Pose | None,
          jo: Pose | None = None, sleepers: bool = False):
    seated = [(look, pose) for look, pose in ((DEV, dev), (MIRA, mira)) if pose]
    return kit_scene(ctx, cam, time=time, tv=tv, pizza=pizza, seated=seated, standing=[(JO, jo)] if jo else [],
                     sleepers=(dev, mira) if sleepers else ())


# --- shots ----------------------------------------------------------------------------------------------------


def s01_standoff(ctx: Ctx):
    return scene(ctx, TWO_SHOT, "day", "off", False,
                 ctx.seated("DEV", 1, "angry", hands="raise_remote"),
                 ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries"))


def s02_mira(ctx: Ctx):
    cam = Camera(2.2, 826, 1040, 540, 960)
    return scene(ctx, cam, "day", "off", False, None, ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries"))


def s03_insert(ctx: Ctx):
    """Close-up of Dev's hand gripping the empty remote. Drawn in screen space."""
    img = new_frame((150, 142, 132))
    c = Canvas(img, SCREEN)
    for i in range(-10, 30):  # couch fabric weave
        c.line([(i * 70, 0), (i * 70 - 900, 1920)], fill=(140, 132, 122), width=10, rounded=False)
    shake = math.sin(ctx.t * 45) * 4 if ctx.t > 0.1 else 0
    x0 = shake
    skin, sleeve = DEV.skin, DEV.top
    c.poly([(640, 1920), (1100, 1380), (1100, 1920)], fill=sleeve, width=8)
    c.ellipse(560 + x0, 1060, 900 + x0, 1440, fill=skin, width=8)  # palm behind the remote
    # Remote back, cover off.
    c.rect(400 + x0, 330, 680 + x0, 1380, fill=(60, 58, 56), radius=90, width=10)
    c.rect(452 + x0, 470, 628 + x0, 1030, fill=(222, 218, 210), radius=18, width=7)
    c.line([(540 + x0, 480), (540 + x0, 1020)], fill=(150, 145, 138), width=6)
    for sx in (496, 584):  # empty slots: flat contact at top, spring at bottom
        sx += x0
        c.rect(sx - 26, 490, sx + 26, 510, fill=(185, 185, 190), width=4)
        zig = [(sx + (-22 if i % 2 else 22), 1010 - i * 14) for i in range(7)]
        c.line(zig, fill=(150, 150, 158), width=7)
        c.text(sx, 560, "+" if sx - x0 < 540 else "−", 44, fill=(150, 145, 138), weight=HEAVY)
    for i, fy in enumerate((1110, 1180, 1250, 1320)):  # fingers wrap the right edge
        c.rect(610 + x0, fy, 740 + x0 - i * 8, fy + 64, fill=skin, radius=32, width=7)
    c.rect(356 + x0, 1080, 470 + x0, 1160, fill=skin, radius=40, width=7)  # thumb
    ctx.bubbles(c, SCREEN, {})
    return img


def s04_mira_smug(ctx: Ctx):
    cam = Camera(3.0, 830, 1020, 540, 1000)
    return scene(ctx, cam, "day", "off", False, None, ctx.seated("MIRA", -1, "smug", hands="clutch_batteries"))


def night_two_shot(ctx: Ctx, talking=True):
    k = ctx.t / max(ctx.shot.dur, 0.1)
    cam = cam_lerp(TWO_SHOT, Camera(1.6, 595, 1070, 540, 1060), k)
    return scene(ctx, cam, "night", "off", True,
                 ctx.seated("DEV", 1, "tired_angry", hands="raise_remote", raise_amt=0.55),
                 ctx.seated("MIRA", -1, "tired", hands="clutch_batteries"))


def card1(ctx: Ctx):
    img = night_two_shot(ctx)
    card(Canvas(img, SCREEN), "3 HOURS LATER", ctx.t)
    return img


def s05b_mira_tired(ctx: Ctx):
    cam = Camera(2.6, 826, 1030, 540, 980)
    return scene(ctx, cam, "night", "off", True, None, ctx.seated("MIRA", -1, "tired", hands="clutch_batteries"))


def asleep_poses(ctx: Ctx):
    dev = ctx.seated("DEV", 1, "asleep", hands="raise_remote", raise_amt=0.2, head_dx=18, head_dy=12)
    mira = ctx.seated("MIRA", -1, "asleep", hands="clutch_batteries", head_dx=-18, head_dy=12)
    dev.extras["breathe"] = ctx.breathe(2.4, 6, 0.0)
    mira.extras["breathe"] = ctx.breathe(2.4, 6, 0.5)
    dev.blink = mira.blink = False
    return dev, mira


def card2(ctx: Ctx):
    img = s06_asleep(ctx)
    card(Canvas(img, SCREEN), "NEXT MORNING", ctx.t)
    return img


def s06_asleep(ctx: Ctx):
    dev, mira = asleep_poses(ctx)
    return scene(ctx, TWO_SHOT, "morning", "off", True, dev, mira, sleepers=True)


JO_X, JO_FEET = 20, 1480
BUTTON_AT = 1.0


def s07_button(ctx: Ctx):
    t = ctx.t
    dev, mira = asleep_poses(ctx)
    walk = ease(t / 0.5)
    x = lerp(-260, JO_X, walk)
    bob = -abs(math.sin(t * math.pi * 5)) * 10 if t < 0.5 else 0
    if t < 0.6:
        jo = Pose(x, JO_FEET, 1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="mug", extras={"bob": bob})
    else:
        k = ease((t - 0.6) / 0.35)
        start = (JO_X - 80, 1150)
        reach = (lerp(start[0], room.POWER_BUTTON[0], k), lerp(start[1], room.POWER_BUTTON[1], k))
        jo = Pose(JO_X, JO_FEET, -1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="reach", reach=reach)
    tv = "golf" if t >= BUTTON_AT else "off"
    return scene(ctx, WIDE, "morning", tv, True, dev, mira, jo, sleepers=True)


def s08a_shock(ctx: Ctx):
    j = cast.jolt(ctx.t)
    dev = ctx.seated("DEV", -1, "shock", hands="raise_remote", head_dy=j)
    mira = ctx.seated("MIRA", -1, "shock", hands="clutch_batteries", head_dy=j * 0.8)
    jo = Pose(JO_X, JO_FEET, 1, "deadpan", blink=ctx.blink("JO"), standing=True, hands="mug")
    return scene(ctx, Camera(1.0, 400, 1150, 540, 1200), "morning", "golf", True, dev, mira, jo)


def s08b_jo(ctx: Ctx):
    jo = Pose(JO_X, JO_FEET, 1, "deadpan", mouth=ctx.mouth("JO"), blink=ctx.blink("JO"), standing=True, hands="mug")
    return scene(ctx, Camera(2.3, 30, 930, 540, 960), "morning", "golf", True, None, None, jo)


def s08c_stare(ctx: Ctx):
    both_blink = 0.55 <= ctx.t < 0.72  # a synchronized slow blink sells the silence
    dev = ctx.seated("DEV", -1, "neutral", hands="raise_remote", gaze=-1)
    mira = ctx.seated("MIRA", -1, "neutral", hands="clutch_batteries", gaze=-1)
    dev.blink = mira.blink = both_blink
    return scene(ctx, Camera(1.6, 580, 1060, 540, 1060), "morning", "golf", True, dev, mira)



def s10_golf(ctx: Ctx):
    k = ease(ctx.t / ctx.shot.dur)
    cam = cam_lerp(WIDE, Camera(1.3, 590, 1080, 540, 1100), k)
    looking_at_tv = ctx.t < 0.55
    if looking_at_tv:
        dev = ctx.seated("DEV", 1, "neutral", hands="raise_remote", gaze=-1)
        mira = ctx.seated("MIRA", -1, "unimpressed", hands="clutch_batteries", gaze=-1)
    else:
        dev = ctx.seated("DEV", 1, "determined", hands="raise_remote")
        mira = ctx.seated("MIRA", -1, "determined", hands="clutch_batteries")
    return scene(ctx, cam, "day", "golf", True, dev, mira)


class Episode04(Episode):
    here = HERE
    final_name = "episode-04-neither-roommate-would-let-go-final.mp4"

    def reveal_frame(self, t: float):
        if not hasattr(self, "_nodes"):
            self._nodes = (reveal.node_layer("story"), reveal.node_layer("software"))
        return reveal.render_frame(t, *self._nodes, captions=self.reveal_captions)

    def build_shots(self) -> list[Shot]:
        d = self.dur
        return [
            Shot("S01 standoff", max(1.8, 0.12 + d("dev-batteries-now") + 0.4), s01_standoff,
                 [self.line("dev-batteries-now", 0.12, (50, 470, 520))]),
            Shot("S02 Mira", max(1.5, 0.08 + d("mira-remote-first") + 0.35), s02_mira,
                 [self.line("mira-remote-first", 0.08, (120, 380, 560))]),
            Shot("S03 empty remote", 0.1 + d("dev-doesnt-work") + 0.4, s03_insert,
                 [self.line("dev-doesnt-work", 0.1, (80, 150, 920))]),
            Shot("S04 Mira smug", 0.1 + d("mira-why-holding") + 0.55, s04_mira_smug,
                 [self.line("mira-why-holding", 0.1, (170, 330, 740))]),
            Shot("Card 3 hours later", 0.75, card1),
            Shot("S05a night", 0.2 + d("dev-let-go") + 0.35, night_two_shot,
                 [self.line("dev-let-go", 0.2, (50, 430, 560))]),
            Shot("S05b Mira tired", 0.1 + d("mira-you-first") + 0.5, s05b_mira_tired,
                 [self.line("mira-you-first", 0.1, (230, 380, 520))]),
            Shot("Card next morning", 0.65, card2),
            Shot("S06 asleep", 2.0, s06_asleep),
            Shot("S07 button", 2.2, s07_button, [self.line("tv-golf-1", BUTTON_AT + 0.25, gain=0.2)]),
            Shot("S08a shock", 0.8, s08a_shock),
            Shot("S08b Jo", 0.1 + d("jo-button") + 0.45, s08b_jo, [self.line("jo-button", 0.1, (170, 330, 620))]),
            Shot("S08c stare", 1.1, s08c_stare),
            self.reveal_shot(),
            Shot("S10 golf (loops to S01)", 1.6, s10_golf, [self.line("tv-golf-2", 0.05, gain=0.2)]),
        ]

    def sound_design(self, mix):

        at = {s.name.split()[0]: s for s in self.shots}
        s01, s02, s03, s04 = at["S01"], at["S02"], at["S03"], at["S04"]
        E2, F2, Fs2, G2, B1 = 82.41, 87.31, 92.5, 98.0, 61.74
        # Standoff: low plucks on the cuts, like a duel.
        for when, f in ((0.0, E2), (0.45, B1), (0.9, E2), (s02.start, F2), (s03.start, E2), (s03.start + 0.5, G2),
                        (s04.start, Fs2), (s04.start + 0.6, F2)):
            mix.add(pluck(f, seed=int(f)), when, 0.2)
        mix.add(click(), s03.start + 0.08, 0.3)

        c1 = next(s for s in self.shots if s.name == "Card 3 hours later")
        for i in range(3):
            mix.add(tick(), c1.start + 0.05 + i * 0.22, 0.35)
        night = [s for s in self.shots if s.name.startswith("S05")]
        mix.add(hum(sum(s.dur for s in night) + c1.dur), c1.start, 0.05)

        c2 = next(s for s in self.shots if s.name == "Card next morning")
        s06, s07 = at["S06"], at["S07"]
        for i, off in enumerate((0.05, 0.4, 0.9, 1.5, 2.1, 2.4)):
            mix.add(chirp(40 + i), c2.start + off, 0.06)
        mix.add(snore(True), s06.start + 0.1, 0.22)
        mix.add(snore(False), s06.start + 1.0, 0.09)
        mix.add(snore(True), s07.start + 0.2, 0.18)

        for i, off in enumerate((0.1, 0.28, 0.46)):
            mix.add(thump(i), s07.start + off, 0.35)
        mix.add(click(), s07.start + BUTTON_AT, 0.45)
        mix.add(tv_on(), s07.start + BUTTON_AT + 0.02, 0.35)
        r1 = at["R1"]
        mix.add(murmur(r1.start - (s07.start + BUTTON_AT)), s07.start + BUTTON_AT, 0.03)

        s08a, s08c = at["S08a"], at["S08c"]
        mix.add(pluck(164.81, 0.6, seed=3) + pluck(233.08, 0.6, seed=4), s08a.start, 0.2)  # surprise stab
        mix.add(slide_whistle(), s08c.start + 0.25, 0.14)

        mix.add(pad(r1.dur), r1.start, 0.07)
        mix.add(pluck(329.63, 0.8, 0.99, seed=9), r1.start + reveal.beats_for(self.reveal_captions)["pulse"], 0.18)

        s10 = at["S10"]
        mix.add(murmur(s10.dur, 22), s10.start, 0.03)
        mix.add(pluck(B1, seed=2), self.duration - 0.45, 0.2)  # lands on the loop back into S01's first pluck

    def thumbnail(self, path: Path):
        cam = Camera(1.55, 580, 1060, 540, 1180)
        img = new_frame()
        c = Canvas(img, cam)
        room.back(c, "day", "off", False, 0)
        cast.draw(c, DEV, Pose(*room.DEV_SEAT, 1, "angry", hands="raise_remote"))
        cast.draw(c, MIRA, Pose(*room.MIRA_SEAT, -1, "smug", hands="clutch_batteries"))
        room.front(c)
        s = Canvas(img, SCREEN)
        s.text(540, 250, "SOFTWARE IN DISGUISE · 04", 34, weight=DEMI)
        s.rect(60, 340, 1020, 620, fill=MUSTARD, width=9, radius=20)
        s.text(540, 425, "NOBODY", 118, weight=HEAVY)
        s.text(540, 540, "LETS GO.", 118, fill=ALERT, weight=HEAVY)
        finish(img).save(path)


if __name__ == "__main__":
    Episode04().render()
