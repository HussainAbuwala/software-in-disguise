"""Screen-space overlays: the payoff promise line, time cards, and speech bubbles."""

from __future__ import annotations

import math

from .canvas import ALERT, DEMI, HAND, HEAVY, INK, MUSTARD, PAPER, TEAL, W, Camera, Canvas, ease, font, lerp
from .cast import Pose


def promise(c: Canvas, size: int = 44):
    """The payoff promise line. Episodes 04-05 use one small line (size 44); Episode 06 onward uses a larger, bolder
    two-line card (size 60+) so it registers in the first second."""
    text = "Programmers have a name for this."
    if size <= 44:
        f = font(size, DEMI)
        w = c.d.textlength(text, font=f) / 2 + 64
        c.rect(540 - w / 2, 230, 540 + w / 2, 318, fill=PAPER, radius=44, width=5)
        c.text(540, 274, text, size, weight=DEMI)
        return
    lines = ("Programmers have", "a name for this.")
    f = font(size, HEAVY)
    w = max(c.d.textlength(l, font=f) for l in lines) / 2 + 90
    lh = size * 1.15
    top, h = 190, lh * 2 + 50
    c.rect(540 - w / 2, top, 540 + w / 2, top + h, fill=MUSTARD, radius=36, width=7)
    for i, l in enumerate(lines):
        c.text(540, top + 25 + lh * (i + 0.5), l, size, weight=HEAVY)


def card(c: Canvas, text: str, k: float):
    """Time card: a mustard strip that snaps in."""
    y = lerp(-120, 380, ease(k * 3))
    c.rect(-20, y, W + 20, y + 150, fill=MUSTARD, width=8)
    c.text(540, y + 75, text, 76, weight=HEAVY)


def wrap(text: str, size: int, width: float) -> list[str]:
    f = font(size)
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if f.getlength(trial) / 2 > width and line:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line]


def bubble(c: Canvas, speaker: str, text: str, x: float, y: float, w: float, target: tuple[float, float]):
    lines = wrap(text, 52, w - 70)
    h = 64 + 64 * len(lines)
    # Tail toward the speaker, capped so it never covers the face.
    bx, by = x + w * 0.35, y + h
    dx, dy = target[0] - bx, target[1] - by
    dist = math.hypot(dx, dy) or 1
    length = min(dist - 40, 120)
    tip = (bx + dx / dist * length, by + dy / dist * length)
    c.poly([(bx - 26, by - 6), (bx + 26, by - 6), tip], fill=PAPER, width=6)
    c.rect(x, y, x + w, y + h, fill=PAPER, radius=38, width=6)
    c.line([(bx - 22, by - 3), (bx + 22, by - 3)], fill=PAPER, width=9, rounded=False)
    c.text(x + 36, y + 36, speaker, 30, fill=(125, 115, 105), weight=DEMI, anchor="lm")
    for i, line in enumerate(lines):
        c.text(x + 36, y + 88 + 64 * i, line, 52, anchor="lm")


def mouth_point(cam: Camera, pose: Pose) -> tuple[float, float]:
    f = pose.facing
    if pose.standing:
        hx, hy = pose.x + f * 4, pose.y - 560
    else:
        hx, hy = pose.x + f * 6 + pose.head_dx, pose.y - 115 + pose.head_dy
    return cam.to_screen(hx + f * 20, hy + 46)


NOTE_YELLOW = (255, 226, 120)


def check_mark(c: Canvas, x, y, size=40, color=TEAL):
    c.line([(x - size * 0.5, y), (x - size * 0.1, y + size * 0.4), (x + size * 0.55, y - size * 0.45)], fill=color, width=size * 0.2)


def cross_mark(c: Canvas, x, y, size=40, color=ALERT):
    h = size * 0.45
    c.line([(x - h, y - h), (x + h, y + h)], fill=color, width=size * 0.2)
    c.line([(x - h, y + h), (x + h, y - h)], fill=color, width=size * 0.2)


def memory_note(c: Canvas, head: tuple[float, float], x: float, y: float, text: str, stamp: str, k: float = 1.0,
                mark: str = "check", expired: bool = False):
    """A thought bubble holding a sticky note: what the character *remembers*, with when they last checked.

    `head` is the screen point the thought dots rise from; (x, y) is the note's top-left; `k` (0..1) pops it in.
    """
    if k <= 0:
        return
    k = ease(k * 1.6)
    w, h = max(300, font(54, HAND).getlength(text) / 2 + 130), 190
    # Thought dots from the head toward the note.
    tx, ty = x + w * 0.3, y + h
    for i, r in enumerate((10, 15, 21)):
        f = (i + 1) / 4
        c.circle(lerp(head[0], tx, f), lerp(head[1], ty, f), r * k, fill=PAPER, width=4)
    cx, cy = x + w / 2, y + h / 2
    sw, sh = w * k, h * k
    fill = (214, 210, 200) if expired else NOTE_YELLOW
    c.rect(cx - sw / 2 + 8, cy - sh / 2 + 10, cx + sw / 2 + 8, cy + sh / 2 + 10, fill=(200, 190, 170), outline=None)  # shadow
    c.rect(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2, fill=fill, width=5)
    if k < 0.95:
        return
    ink = (150, 144, 136) if expired else INK
    c.text(x + 34, y + 70, text, 54, fill=ink, weight=HAND, anchor="lm")
    tw = font(54, HAND).getlength(text) / 2
    if expired:
        c.line([(x + 26, y + 74), (x + 44 + tw, y + 66)], fill=ALERT, width=7)
        c.text(x + 34, y + 140, "EXPIRED", 40, fill=ALERT, weight=HEAVY, anchor="lm")
        return
    mx = min(x + 34 + tw + 42, x + w - 36)
    (check_mark if mark == "check" else cross_mark)(c, mx, y + 68, 44)
    c.text(x + 34, y + 140, stamp, 38, fill=(150, 70, 60), weight=HAND, anchor="lm")
