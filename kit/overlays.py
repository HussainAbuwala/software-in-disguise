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


# --- added for Episode 07: the in-scene reveal ----------------------------------------------------------------


def dim(img, amount: float):
    """Darken a finished frame toward ink, for a freeze-frame reveal."""
    from PIL import Image

    return Image.blend(img, Image.new("RGB", img.size, INK), amount)


def leader_tag(c: Canvas, x: float, y: float, k: float):
    """A mustard "LEADER" tag with a small crown, popping in above someone's head (screen coordinates)."""
    if k <= 0:
        return
    s = 0.6 + 0.4 * ease(k)
    w, h = 250 * s, 78 * s
    y -= (1 - ease(k)) * 30
    c.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, fill=MUSTARD, width=6, radius=h / 2)
    c.text(x, y + 2, "LEADER", 46 * s, weight=HEAVY)
    cy = y - h / 2 - 12
    crown = [(x - 46 * s, cy), (x - 46 * s, cy - 44 * s), (x - 22 * s, cy - 20 * s), (x, cy - 52 * s),
             (x + 22 * s, cy - 20 * s), (x + 46 * s, cy - 44 * s), (x + 46 * s, cy)]
    c.poly(crown, fill=MUSTARD, width=6)


def dotted_arrow(c: Canvas, a: tuple[float, float], b: tuple[float, float], k: float, color=PAPER):
    """Dots from a to b (screen coordinates), drawn progressively as k goes 0 -> 1, with an arrowhead at the end."""
    if k <= 0:
        return
    k = ease(k)
    n = 9
    for i in range(int(n * k) + 1):
        f = i / n
        c.circle(lerp(a[0], b[0], f), lerp(a[1], b[1], f), 9, fill=color, width=4)
    if k > 0.95:
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        tip = (b[0] + ux * 26, b[1] + uy * 26)
        c.poly([tip, (b[0] - uy * 20, b[1] + ux * 20), (b[0] + uy * 20, b[1] - ux * 20)], fill=color, width=4)


def stamp(c: Canvas, y: float, text: str, k: float, size: float = 92):
    """The concept's name, stamped across the frame on a mustard strip (screen coordinates)."""
    if k <= 0:
        return
    s = 1.35 - 0.35 * ease(k)  # lands from slightly too big, like a rubber stamp
    size = size * s
    w = font(size, HEAVY).getlength(text) / 2 + 80
    c.rect(540 - w / 2, y - size * 0.75, 540 + w / 2, y + size * 0.75, fill=MUSTARD, width=8, radius=18)
    c.text(540, y + 2, text, size, weight=HEAVY)


def caption(c: Canvas, y: float, text: str, size: int = 50):
    """The narrator's current phrase, on a paper strip (screen coordinates)."""
    lines = wrap(text, size, 860)
    lh = size * 1.25
    h = lh * len(lines) + 44
    c.rect(80, y, 1000, y + h, fill=PAPER, width=6, radius=28)
    for i, line in enumerate(lines):
        c.text(540, y + 22 + lh * (i + 0.5), line, size, weight=DEMI)


# --- added for Episode 08 --------------------------------------------------------------------------------------


def checklist(c: Canvas, x: float, y: float, w: float, title: str, items: list[str], ticks: list[float],
              size: float = 50):
    """A handwritten list on paper (screen coordinates). `ticks[i]` (0..1) draws item i's tick mark in."""
    lh = size * 1.55
    h = 70 + size * 1.4 + lh * len(items) + 30
    c.rect(x + 10, y + 12, x + w + 10, y + h + 12, fill=(200, 190, 170), outline=None)  # shadow
    c.rect(x, y, x + w, y + h, fill=PAPER, width=6)
    for i in range(len(items) + 1):  # ruled lines
        ly = y + 60 + size * 1.4 + lh * i - lh * 0.1
        c.line([(x + 24, ly), (x + w - 24, ly)], fill=(190, 210, 230), width=3)
    c.text(x + 40, y + 34 + size * 0.7, title, size * 1.05, weight=HAND, anchor="lm")
    for i, item in enumerate(items):
        iy = y + 60 + size * 1.4 + lh * (i + 0.45)
        c.text(x + 110, iy, item, size, weight=HAND, anchor="lm")
        c.rect(x + 42, iy - size * 0.38, x + 42 + size * 0.76, iy + size * 0.38, width=4, radius=6)
        k = ticks[i] if i < len(ticks) else 0.0
        if k > 0:
            check_mark(c, x + 42 + size * 0.38, iy, size * 0.9 * (0.6 + 0.4 * ease(k)))
