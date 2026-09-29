"""Render Episode 03 remake (starvation, "Just One Quick Thing") end to end.

    ../../.venv/bin/python voices.py
    ../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.*
    ../../.venv/bin/python render_episode.py   # deliverables/episode-03-just-one-quick-thing-final.mp4
    ../../.venv/bin/python render_episode.py --stills   # build/still-*.png, one per shot, for layout checks

Shared machinery lives in kit/episode.py; this file is only the story. Two tests: frame 1 names the concept
("Software concept: STARVATION, explained with everyday life"), breaking the hide-the-term rule for one episode, and a
follow line over the last beat. Every quick thing is shown being done (the sofa, Mom on a split-screen call, the
laundry); the speech waits on the desk, and the page itself is shown top-down.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from kit import cast, kitchen, laundry, living_room as room, study  # noqa: E402
from kit.canvas import ALERT, DEMI, HEAVY, INK, MUSTARD, PAPER, SCREEN, Camera, Canvas, ease, finish, lerp, new_frame  # noqa: E402
from kit.cast import DEV, JO, MIRA, MOM, Pose, seated_legs  # noqa: E402
from kit.episode import Ctx, Episode, Shot, scene  # noqa: E402
from kit.overlays import bubble, caption, dim, mouth_point, page_closeup, stamp  # noqa: E402
from kit.sound import band, beep, buzz, murmur, pad, pluck, scrape, scribble, tape_rip, thump, tick, whoosh  # noqa: E402

FLOOR = 1380
TITLE = "Priya's wedding speech"
SIGN = ("9–11", "SPEECH", "ONLY")

# Minutes since midnight. The clock appears from the second quick thing on.
SIX_40, EIGHT_15, NINE_20, MIDNIGHT_ISH, NINE_AM = 18 * 60 + 40, 20 * 60 + 15, 21 * 60 + 20, 23 * 60 + 58, 9 * 60

DESK_TWO = Camera(1.35, 790, 1080, 540, 1230)  # Mira at the desk + someone at the sign / door on the right
DESK_LOW = Camera(1.5, 660, 1080, 540, 1640)  # Mira at the desk, in the bottom half of the split screen
KITCHEN_HIGH = Camera(1.35, 600, 1000, 540, 560)  # Mom, in the top half
DESK_WIDE = Camera(1.3, 780, 1080, 540, 1200)  # Mira and Jo in the doorway
CARRY = Camera(1.3, 640, 1000, 540, 1100)
SIGN_CAM = Camera(1.6, 950, 960, 540, 1100)  # Mira at the wall, pressing the sign up
LAUNDRY = Camera(1.45, 560, 1040, 540, 1060)


def mira_at_desk(ctx: Ctx, expr: str, pen: bool = True, **kw) -> Pose:
    extras = {"pen": (ctx.g * 0.9) % 1.0 if pen else 0.0, "pen_down": pen}
    extras.update(kw.pop("extras", {}))
    hands = kw.pop("hands", "write")
    return Pose(*study.SEAT, 1, expr, mouth=ctx.mouth("MIRA"), blink=ctx.blink("MIRA"), hands=hands,
                reach=study.PEN_AT, extras=extras, **kw)


def desk_scene(ctx: Ctx, cam: Camera, time: str, mira: Pose, standing=(), clock=None, door="closed", sign=None,
               overlay=None):
    return scene(ctx, cam, set=study, time=time, seated=[(MIRA, mira)], standing=standing, overlay=overlay,
                 legs=lambda c: seated_legs(c, MIRA, mira), clock=clock, door=door, sign=sign)


# --- shots ----------------------------------------------------------------------------------------------------


def s01_quick_thing(ctx: Ctx):
    """Frame 1: the card names the concept. Mira writing Priya's speech (the invitation on the desk), Dev leaning in."""
    cam = Camera(lerp(1.55, 1.62, ease(ctx.k)), 675, 1080, 540, 1250)
    m = mira_at_desk(ctx, "annoyed", pen=ctx.t < 1.2)
    d = ctx.standing("DEV", 960, FLOOR, -1, "pleading", head_dx=-22, head_dy=16)
    return desk_scene(ctx, cam, "evening", m, [(DEV, d)], door="open")


def s02_sofa(ctx: Ctx):
    """Quick thing 1: carrying the sofa with Dev."""
    wob = 14 * math.sin(ctx.t * 7)
    m = ctx.standing("MIRA", 300, FLOOR, 1, "tired_angry", hands="carry")
    d = ctx.standing("DEV", 980, FLOOR, -1, "cheerful", hands="carry")
    sofa = lambda c: room.sofa_lifted(c, 380, 900, 1135, tilt=wob)  # noqa: E731
    return scene(ctx, CARRY, time="evening", standing=[(MIRA, m), (DEV, d)], props=sofa, couch=False, clock=SIX_40)


def s03_mom(ctx: Ctx):
    """Quick thing 2: Mom calls. Split screen, Mom in her kitchen on top, Mira at the desk below. Her "one quick
    thing" is "did you eat?", and then the clock spins from 8:15 to 9:20 while she keeps talking."""
    ep = ctx.ep
    jump = max(0.0, min(1.0, (ctx.t - ep.jump_at) / ep.jump_dur))
    if jump > 0:  # the chatter replaces the spoken lines' bubbles
        ctx = Ctx(ep, Shot(ctx.shot.name, ctx.shot.dur, ctx.shot.draw, [], ctx.shot.start), ctx.t)
    mom = ctx.standing("MOM", *kitchen.MOM_AT, 1, "cheerful", hands="phone_ear")
    if jump > 0:
        mom.mouth = max(0.0, math.sin(ctx.t * 23)) * 0.8
    top = scene(ctx, KITCHEN_HIGH, set=kitchen, standing=[(MOM, mom)])
    if jump > 0:
        bubble(Canvas(top, SCREEN), "MOM", "…and another thing…", 600, 90, 440, mouth_point(KITCHEN_HIGH, mom))
    on_phone = ctx.t >= 0.2
    m = mira_at_desk(ctx, "tired" if jump > 0 else "neutral", pen=not on_phone,
                     hands="phone_ear" if on_phone else "write", head_dy=14 * ease(jump), gaze_y=0.5 * jump)
    bottom = desk_scene(ctx, DESK_LOW, "night", m, clock=lerp(EIGHT_15, NINE_20, ease(jump)))
    img = top.copy()
    half = img.height // 2  # frames are supersampled; screen y 960 is the middle
    img.paste(bottom.crop((0, half, bottom.width, bottom.height)), (0, half))
    Canvas(img, SCREEN).line([(-10, 960), (1090, 960)], fill=INK, width=8)
    return img


def s04_laundry(ctx: Ctx):
    """Quick thing 3: the washing machine is done."""
    m = ctx.standing("MIRA", 420, FLOOR, 1, "tired", hands="armful" if ctx.t > 0.45 else "rest")
    return scene(ctx, LAUNDRY, set=laundry, time="night", standing=[(MIRA, m)])


def s05_page(ctx: Ctx):
    """Top-down: the page is still blank."""
    img = new_frame(PAPER)
    c = Canvas(img, SCREEN)
    page_closeup(c, TITLE, pen=True)
    ctx.bubbles(c, SCREEN, {})
    return img


def s06_midnight(ctx: Ctx):
    """11:58. A beat of silence."""
    cam = Camera(lerp(1.8, 1.9, ease(ctx.k)), 620, 900, 540, 1000)
    m = mira_at_desk(ctx, "frazzled", pen=False, gaze_y=0.6)
    return desk_scene(ctx, cam, "night", m, clock=MIDNIGHT_ISH + min(1.0, ctx.t))


def s07_jo(ctx: Ctx):
    """Jo from the doorway: none of them was wrong; the rule was."""
    m = mira_at_desk(ctx, "frazzled", pen=False)
    j = ctx.standing("JO", 1080, FLOOR, -1, "deadpan")
    return desk_scene(ctx, DESK_WIDE, "night", m, [(JO, j)], clock=MIDNIGHT_ISH + 1, door="open")


def s08_sign(ctx: Ctx):
    """The fix: Mira reserves time for the big job. She presses the sheet onto the wall herself."""
    k = max(0.0, min(1.0, (ctx.t - 0.1) / 0.4))
    x, y = study.SIGN_AT
    lift = (1 - ease(k)) * 40  # her hands rise with the sheet
    m = ctx.standing("MIRA", 1110, FLOOR, -1, "determined", hands="press", reach=(x + 78, y - 88 + lift),
                     extras={"press_offset": (0, 170)})  # right of the sign, pressing its right edge
    return scene(ctx, SIGN_CAM, set=study, time="night", standing=[(MIRA, m)], clock=MIDNIGHT_ISH + 2,
                 door="closed", sign=(SIGN, k))


def s09_dear(ctx: Ctx):
    """9 AM, top-down: finally writing."""
    img = new_frame(PAPER)
    page_closeup(Canvas(img, SCREEN), TITLE, "Dear Priya,", k=ctx.t / (ctx.shot.dur * 0.85), t=ctx.t)
    return img


def follow_line(k: float):
    def draw(c: Canvas):
        if k <= 0:
            return
        y = lerp(120, 200, ease(min(1.0, k * 3)))
        c.rect(90, y, 990, y + 170, fill=PAPER, width=6, radius=34)
        c.text(540, y + 55, "Your life is full of software.", 46, weight=DEMI)
        c.text(540, y + 118, "Follow for the next one.", 46, fill=ALERT, weight=HEAVY)
    return draw


def s10_nine_am(ctx: Ctx):
    """Dev walks in, reads the sign, and asks anyway (loops to S01)."""
    ep = ctx.ep
    walk = min(1.0, ctx.t / 0.6)
    bob = -abs(math.sin(ctx.t * math.pi * 5)) * 8 if walk < 1 else 0.0
    reading = 0.55 <= ctx.t < ep.ask_at - 0.05
    d = ctx.standing("DEV", lerp(1220, 1070, ease(walk)), FLOOR, -1, "neutral" if reading else "pleading",
                     head_dx=-22 * walk, head_dy=16 * walk, gaze_y=-0.9 if reading else None, extras={"bob": bob})
    m = mira_at_desk(ctx, "determined" if ctx.t < ep.ask_at + 0.3 else "annoyed", pen=ctx.t < ep.ask_at + 0.3)
    return desk_scene(ctx, DESK_TWO, "morning", m, [(DEV, d)], clock=NINE_AM, door="open", sign=(SIGN, 1.0),
                      overlay=follow_line((ctx.t - ep.follow_at) / 1.0))


# --- episode --------------------------------------------------------------------------------------------------


class Episode03(Episode):
    here = HERE
    final_name = "episode-03-just-one-quick-thing-final.mp4"
    reveal_chunks = ["reveal-1", "reveal-2"]
    promise_size = 56
    promise_until = 3.4
    promise_lines = ("Software concept:", "STARVATION", "explained with everyday life.")
    reveal_hold = 0.6

    def build_shots(self) -> list[Shot]:
        d, ln = self.dur, self.line
        writing_at = 0.1 + d("dev-quick-thing") + 0.1
        self.yes_at = 0.3
        mom_at = self.yes_at + d("mira-yes-mom") + 0.1
        self.jump_at = mom_at + d("mom-quick") + 0.15
        self.jump_dur = 1.2
        laundry_at = 0.6
        self.ask_at = 1.0
        self.follow_at = self.ask_at - 0.2
        first_at = 0.1 + d("jo-every-one") + 0.1
        up = (540, -300)  # off-screen speaker above the frame
        return [
            Shot("S01 just one quick thing", writing_at + d("mira-writing") + 0.3, s01_quick_thing,
                 [ln("dev-quick-thing", 0.1, (540, 470, 480)), ln("mira-writing", writing_at, (30, 700, 500))]),
            Shot("S02 the sofa", 0.1 + d("dev-two-minutes") + 0.75, s02_sofa,
                 [ln("dev-two-minutes", 0.1, (560, 380, 440))]),
            Shot("S03 mom calls", self.jump_at + self.jump_dur + 0.25, s03_mom,
                 [ln("mom-quick", mom_at, (600, 90, 440)), ln("mira-yes-mom", self.yes_at, (420, 1200, 360))]),
            Shot("S04 laundry", laundry_at + d("mira-laundry") + 0.3, s04_laundry,
                 [ln("mira-laundry", laundry_at, (80, 380, 520))]),
            Shot("S05 the page is blank", 0.3 + d("mira-wedding") + 0.3, s05_page,
                 [ln("mira-wedding", 0.3, (160, 60, 760, *up))]),
            Shot("S06 11:58", 1.0, s06_midnight),
            Shot("S07 jo: they always went first", first_at + d("jo-went-first") + 0.4, s07_jo,
                 [ln("jo-every-one", 0.1, (420, 420, 600)), ln("jo-went-first", first_at, (420, 420, 600))]),
            Shot("R1 reveal", self.reveal_dur + self.reveal_hold, lambda ctx: ctx.ep.reveal_frame(ctx.t), self.reveal_lines),
            Shot("S08 the sign", 0.45 + d("mira-nine-sharp") + 0.3, s08_sign,
                 [ln("mira-nine-sharp", 0.45, (420, 330, 520))]),
            Shot("S09 dear priya", 1.1, s09_dear),
            Shot("S10 nine am (loops to S01)", self.ask_at + d("dev-quick-thing") + 0.25, s10_nine_am,
                 [ln("dev-quick-thing", self.ask_at, (560, 470, 460))]),
        ]

    # The reveal happens inside the scene: 11:58, Mira and the clock (S06, no bubbles) freeze and dim, Hussain's voice
    # explains, and the term (already named in frame 1) is stamped across the frame.
    def reveal_frame(self, t: float):
        if not hasattr(self, "_frozen"):
            s06 = self.shot("S06")
            self._frozen = s06.draw(Ctx(self, s06, 0.3))
        (_, _), (c2, _) = self.reveal_captions
        img = dim(self._frozen, 0.4 * ease(t / 0.25))
        c = Canvas(img, SCREEN)
        c.text(60, 150, "SOFTWARE IN DISGUISE · 03", 30, fill=(236, 230, 220), weight=DEMI, anchor="lm")
        current = [text for start, text in self.reveal_captions if t >= start]
        if current:
            caption(c, 230, current[-1])
        stamp(c, 410, "STARVATION", (t - (c2 + 0.45)) / 0.2)
        return img

    def sound_design(self, mix):
        s = self.shot
        C3, G2, E3 = 130.81, 98.0, 164.81
        for when, f in ((0.0, C3), (0.4, G2)):
            mix.add(pluck(f, seed=int(f)), when, 0.18)
        mix.add(scribble(1.0), 0.05, 0.12)  # Mira writing under Dev's opening line

        s02 = s("S02")
        mix.add(whoosh(), s02.start - 0.1, 0.15)
        mix.add(scrape(s02.dur), s02.start, 0.22)

        s03 = s("S03")
        mix.add(buzz(1), s03.start, 0.3)
        chatter = s03.dur - self.jump_at
        mix.add(band(murmur(chatter, seed=23), 400, 3000), s03.start + self.jump_at, 0.3)  # Mom, still going
        for i in range(int(self.jump_dur / 0.07)):  # the clock spinning forward
            mix.add(tick(), s03.start + self.jump_at + i * 0.07, 0.12)

        s04 = s("S04")
        mix.add(beep(3), s04.start + 0.02, 0.22)

        s05 = s("S05")
        for i in range(int((s05.dur + s("S06").dur) / 0.5)):
            mix.add(tick(), s05.start + 0.05 + i * 0.5, 0.25)
        s06 = s("S06")
        mix.add(pluck(E3, 0.6, seed=32), s06.start + s06.dur - 0.45, 0.14)

        r1 = s("R1")
        mix.add(pad(r1.dur), r1.start, 0.06)

        s08 = s("S08")
        mix.add(tape_rip(), s08.start + 0.1, 0.2)
        mix.add(thump(4), s08.start + 0.58, 0.12)

        mix.add(scribble(1.0, seed=35), s("S09").start + 0.05, 0.18)

        s10 = s("S10")
        mix.add(scribble(0.8, seed=36), s10.start + 0.05, 0.1)
        for i in range(3):  # Dev's footsteps
            mix.add(thump(i + 20), s10.start + 0.08 + i * 0.2, 0.12)
        mix.add(pluck(G2, seed=5), self.duration - 0.4, 0.2)  # leads into S01's opening pluck on the loop

    def thumbnail(self, path: Path):
        img = new_frame(study.wall_color("evening"))
        cam = Camera(1.5, 690, 1060, 540, 1300)
        c = Canvas(img, cam)
        m = Pose(*study.SEAT, 1, "annoyed", hands="write", reach=study.PEN_AT)
        study.back(c, "evening", door="open", legs=lambda cv: seated_legs(cv, MIRA, m))
        cast.draw(c, MIRA, m)
        study.front(c)
        cast.draw(c, DEV, Pose(960, FLOOR, -1, "pleading", standing=True, head_dx=-22, head_dy=16))
        s = Canvas(img, SCREEN)
        s.text(540, 90, "SOFTWARE IN DISGUISE · 03", 34, weight=DEMI)
        s.rect(60, 140, 1020, 420, fill=MUSTARD, width=9, radius=20)
        s.text(540, 225, "“JUST ONE", 104, weight=HEAVY)
        s.text(540, 335, "QUICK THING.”", 104, fill=ALERT, weight=HEAVY)
        finish(img).save(path)

    def stills(self):
        """One frame per shot (at 70% through it), for checking layout without a full render."""
        for f in self.build.glob("still-*.png"):
            f.unlink()
        for i, shot in enumerate(self.shots):
            for frac in ((0.02, 0.7) if i == 0 else (0.7,)):
                img = shot.draw(Ctx(self, shot, shot.dur * frac))
                if img.size != (1080, 1920):
                    img = finish(img)
                img.save(self.build / f"still-{i:02d}-{frac:.2f}.png")
        self.thumbnail(self.build / "still-thumb.png")


if __name__ == "__main__":
    ep = Episode03()
    if "--stills" in sys.argv:
        for sh in ep.shots:
            print(f"  {sh.start:6.2f}  {sh.dur:4.2f}  {sh.name}")
        print(f"duration {ep.duration:.2f}s")
        ep.stills()
    else:
        ep.render()
