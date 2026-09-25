"""Episode 05 reveal graphic (R1): Dev's memory is a cache, the fridge is the source of truth.

Beats follow the four spoken chunks:
  1 "That's a stale cache."                           -> title
  2 "An answer saved once, and never checked again."  -> Mira asks, Dev answers from his note, never checks the fridge
  3 "It's why a site can show you yesterday's price." -> relabel: YOU / CACHE / DATABASE, milk -> prices
  4 "Good caches expire."                             -> the note is stamped EXPIRED and the arrow now checks the source
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from kit.canvas import (  # noqa: E402
    ALERT, DEMI, HAND, HEAVY, INK, MUSTARD, PAPER, SCREEN, SS, TEAL, W, H, Canvas, ease, finish, font, lerp,
)
from kit.overlays import check_mark, cross_mark, memory_note  # noqa: E402

BG = (244, 239, 230)
GREY = (205, 198, 186)
NODE_R = 115

FRIDGE = (700, 610)
MIRA = (230, 1120)
DEV = (700, 1120)
NOTE = (270, 740)  # top-left of Dev's memory note
NOW = (430, 610)  # the fridge's current value


def _person(c: Canvas, cx, cy):
    c.circle(cx, cy - 48, 30, fill=PAPER, width=7)
    c.pieslice(cx - 58, cy - 8, cx + 58, cy + 102, 180, 360, fill=PAPER, width=7)


def _fridge(c: Canvas, cx, cy):
    c.rect(cx - 45, cy - 75, cx + 45, cy + 70, fill=PAPER, radius=12, width=7)
    c.line([(cx - 45, cy - 22), (cx + 45, cy - 22)], width=6)
    c.line([(cx + 28, cy - 60), (cx + 28, cy - 38)], width=7)
    c.line([(cx + 28, cy - 6), (cx + 28, cy + 30)], width=7)


def _database(c: Canvas, cx, cy):
    for y in (cy + 40, cy + 5):
        c.chord(cx - 55, y - 18, cx + 55, y + 18, 0, 180, fill=PAPER, width=7)
    c.rect(cx - 55, cy - 50, cx + 55, cy + 40, fill=PAPER, outline=None)
    c.line([(cx - 55, cy - 50), (cx - 55, cy + 40)], width=7)
    c.line([(cx + 55, cy - 50), (cx + 55, cy + 40)], width=7)
    c.arc(cx - 55, cy - 13, cx + 55, cy + 23, 0, 180, width=6)
    c.arc(cx - 55, cy + 22, cx + 55, cy + 58, 0, 180, width=7)
    c.ellipse(cx - 55, cy - 68, cx + 55, cy - 32, fill=PAPER, width=7)


def _note_icon(c: Canvas, cx, cy):
    c.poly([(cx - 50, cy - 50), (cx + 50, cy - 50), (cx + 50, cy + 25), (cx + 25, cy + 50), (cx - 50, cy + 50)], fill=(255, 226, 120), width=7)
    c.poly([(cx + 50, cy + 25), (cx + 25, cy + 25), (cx + 25, cy + 50)], fill=(230, 196, 90), width=5)
    for i in range(3):
        c.line([(cx - 32, cy - 26 + i * 22), (cx + 26 - i * 14, cy - 26 + i * 22)], width=5)


NODES = {
    "fridge": (FRIDGE, GREY, ("FRIDGE", _fridge), ("DATABASE", _database)),
    "mira": (MIRA, TEAL, ("MIRA", _person), ("YOU", _person)),
    "dev": (DEV, MUSTARD, ("DEV", _person), ("CACHE", _note_icon)),
}


def node_layer(state: int) -> Image.Image:
    """Nodes plus the fridge's current value, for state 0 (story) or 1 (software)."""
    img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    c = Canvas(img, SCREEN)
    for (cx, cy), fill, *labels in NODES.values():
        label, icon = labels[state]
        c.circle(cx, cy, NODE_R, fill=fill, width=9)
        icon(c, cx, cy)
        bw = max(170, max(len(l[0]) for l in labels) * 28 + 44)
        ly = cy + NODE_R + 6
        c.rect(cx - bw / 2, ly - 30, cx + bw / 2, ly + 30, fill=INK, outline=None, radius=30)
        c.text(cx, ly, label, 40, fill=PAPER)
    # The fridge's value right now.
    x, y = NOW
    c.line([(x + 120, y), (FRIDGE[0] - NODE_R, y)], width=6)
    c.rect(x - 130, y - 70, x + 120, y + 70, fill=PAPER, width=6, radius=18)
    c.text(x - 5, y - 38, "RIGHT NOW", 26, fill=(125, 115, 105), weight=DEMI)
    if state == 0:
        c.text(x - 20, y + 18, "no milk", 50, weight=HAND)
        cross_mark(c, x + 85, y + 18, 40)
    else:
        c.text(x, y + 16, "$12", 64, weight=HEAVY)
    return img


def arrow(c: Canvas, a, b, k: float, color=INK, dashed=False, width=11):
    if k <= 0:
        return
    (x1, y1), (x2, y2) = a, b
    tx, ty = lerp(x1, x2, k), lerp(y1, y2, k)
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    if dashed:
        n = int(math.hypot(tx - x1, ty - y1) // 34)
        for i in range(n):
            s0, s1 = i * 34, i * 34 + 20
            c.line([(x1 + ux * s0, y1 + uy * s0), (x1 + ux * s1, y1 + uy * s1)], fill=color, width=width)
    else:
        c.line([(x1, y1), (tx, ty)], fill=color, width=width)
    px, py, hd = -uy, ux, 32
    c.poly([(tx + ux * 6, ty + uy * 6), (tx - ux * hd + px * hd * 0.6, ty - uy * hd + py * hd * 0.6),
            (tx - ux * hd - px * hd * 0.6, ty - uy * hd - py * hd * 0.6)], fill=color, outline=None)


def pill(c: Canvas, x, y, text, color=INK, size=34):
    w = font(size, DEMI).getlength(text) / SS + 40
    c.rect(x - w / 2, y - 26, x + w / 2, y + 26, fill=PAPER, outline=color, width=5, radius=26)
    c.text(x, y, text, size, fill=color, weight=DEMI)


def beats_for(captions) -> dict:
    c1, c2, c3, c4 = (start for start, _ in captions)
    return {"title": c1 + 0.1, "ask": c2, "note": c2 + 0.35, "answer": c2 + 0.8, "never": c2 + 1.7,
            "relabel": c3, "expire": c4 + 0.35, "refresh": c4 + 1.05}


def render_frame(t: float, layers, captions) -> Image.Image:
    b = beats_for(captions)
    img = Image.new("RGBA", (W * SS, H * SS), BG + (255,))
    c = Canvas(img, SCREEN)
    c.text(80, 170, "SOFTWARE IN DISGUISE · 05", 30, weight=DEMI, anchor="lm")
    k = ease((t - b["title"]) / 0.3)
    if k > 0:
        c.text(470, 330, "STALE CACHE", 104 + (1 - k) * 30, fill=ALERT, weight=HEAVY)

    # Arrows under the nodes.
    arrow(c, (MIRA[0] + NODE_R + 10, 1085), (DEV[0] - NODE_R - 14, 1085), ease((t - b["ask"]) / 0.35))
    arrow(c, (DEV[0] - NODE_R - 10, 1160), (MIRA[0] + NODE_R + 14, 1160), ease((t - b["answer"]) / 0.35))
    expired = t >= b["expire"]
    never_k = ease((t - b["never"]) / 0.4)
    arrow(c, (DEV[0], DEV[1] - NODE_R - 10), (FRIDGE[0], FRIDGE[1] + NODE_R + 50), never_k,
          color=TEAL if expired else (150, 140, 130), dashed=not expired)

    mix = ease((t - b["relabel"]) / 0.45)
    story, software = layers
    nodes = story if mix <= 0 else software if mix >= 1 else Image.blend(story, software, mix)
    img.alpha_composite(nodes)

    if t >= b["ask"] + 0.25:
        pill(c, (MIRA[0] + DEV[0]) / 2, 1040, "milk?" if mix < 0.5 else "price?")
    if t >= b["answer"] + 0.25:
        answer = "yes!" if mix < 0.5 else ("$12!" if t >= b["refresh"] else "$10!")
        pill(c, (MIRA[0] + DEV[0]) / 2, 1205, answer)
    if never_k >= 1:
        if expired:
            pill(c, FRIDGE[0], 880, "checks again", TEAL)
        else:
            pill(c, FRIDGE[0], 880, "never checks", ALERT)

    # Dev's note: pops in, flips to the software value at the relabel, then expires.
    flip = (t - b["relabel"]) / 0.4
    note_k = min(1.0, max(0.0, (t - b["note"]) / 0.5))
    if 0 <= flip < 1:
        note_k *= 0.35 + 0.65 * abs(math.cos(math.pi * flip))
    software_note = flip >= 0.5
    refreshed = t >= b["refresh"]
    if refreshed:  # after expiring, the next answer comes fresh from the source
        text, stamp = "$12", "just now"
        note_k = min(1.0, (t - b["refresh"]) / 0.35)
    elif software_note:
        text, stamp = "$10", "yesterday"
    else:
        text, stamp = "MILK", "7:02 AM"
    memory_note(c, (DEV[0] - 80, DEV[1] - 90), *NOTE, text, stamp, note_k, expired=expired and not refreshed)

    # Captions, above the bottom 20% reserve.
    text = ""
    for start, chunk in captions:
        if t >= start:
            text = chunk
    if text:
        lines, line = [], ""
        for word in text.split():
            trial = f"{line} {word}".strip()
            if font(54).getlength(trial) / SS > 780:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
        top = 1390
        c.rect(90, top, 900, top + 40 + 70 * len(lines), fill=(255, 252, 245), width=5, radius=24)
        for i, ln in enumerate(lines):
            c.text(495, top + 55 + 70 * i, ln, 54)
    return finish(img.convert("RGB"))


if __name__ == "__main__":  # quick contact sheet of the reveal alone
    caps = [(0.1, "That's a stale cache."), (1.7, "An answer saved once, and never checked again."),
            (4.9, "It's why a site can show you yesterday's price."), (7.8, "Good caches expire.")]
    layers = (node_layer(0), node_layer(1))
    frames = [render_frame(t, layers, caps) for t in (0.8, 2.6, 4.2, 5.6, 8.5, 9.5)]
    sheet = Image.new("RGB", (W // 3 * 3, H // 3 * 2))
    for i, f in enumerate(frames):
        sheet.paste(f.resize((W // 3, H // 3)), ((i % 3) * (W // 3), (i // 3) * (H // 3)))
    out = Path(__file__).resolve().parent / "build"
    out.mkdir(exist_ok=True)
    sheet.save(out / "reveal-contact-sheet.png")
    print(out / "reveal-contact-sheet.png")
