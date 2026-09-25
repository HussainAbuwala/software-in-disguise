"""Episode 06 reveal graphic (R1): two ways of numbering the same two floors.

Three spoken chunks, kept short on purpose (Episode 1's retention graph lost half its viewers during a long reveal):
  1 "That's an off-by-one error."                    -> title; Dev upstairs, Mira downstairs, "1 apart"
  2 "Computers count from zero, people from one."    -> CODE labels 0 / 1, then PEOPLE labels 1st / 2nd;
                                                        both "first floors" light up
  3 "One slip means a skipped item, or a crash."     -> a list in code [0] [1] [2]: counting from 1 skips "milk",
                                                        and one step past the end, [3], crashes
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from kit.canvas import ALERT, DEMI, HAND, HEAVY, INK, MUSTARD, PAPER, SCREEN, SS, TEAL, W, H, Canvas, ease, finish, font  # noqa: E402

BG = (244, 239, 230)
WALL = (241, 228, 206)
X0, X1 = 360, 720  # building
UPPER = (500, 800)
LOWER = (800, 1100)


def beats_for(captions) -> dict:
    c1, c2, c3 = (start for start, _ in captions)
    return {"title": c1 + 0.1, "apart": c1 + 0.7, "zero": c2 + 0.1, "one": c2 + 1.3, "glow": c2 + 2.2,
            "list": c3 + 0.05, "skip": c3 + 0.9, "crash": c3 + 1.7}


def _pin(c: Canvas, x, y, fill, label):
    c.circle(x, y, 52, fill=fill, width=7)
    c.circle(x, y - 14, 16, fill=PAPER, width=5)
    c.pieslice(x - 30, y + 2, x + 30, y + 58, 180, 360, fill=PAPER, width=5)
    c.rect(x - 60, y + 60, x + 60, y + 100, fill=INK, outline=None, radius=20)
    c.text(x, y + 80, label, 28, fill=PAPER)


def _label(c: Canvas, x, y, text, k, color=INK, size=64, weight=HEAVY):
    if k <= 0:
        return
    c.text(x, y + (1 - ease(k)) * 30, text, size * (0.7 + 0.3 * ease(k)), fill=color, weight=weight)


def render_frame(t: float, captions) -> Image.Image:
    b = beats_for(captions)
    img = Image.new("RGB", (W * SS, H * SS), BG)
    c = Canvas(img, SCREEN)
    c.text(80, 170, "SOFTWARE IN DISGUISE · 06", 30, weight=DEMI, anchor="lm")
    k = ease((t - b["title"]) / 0.3)
    if k > 0:
        c.text(540, 330, "OFF-BY-ONE", 110 + (1 - k) * 30, fill=ALERT, weight=HEAVY)

    # The two floors.
    for (y0, y1), fill in ((UPPER, WALL), (LOWER, (234, 216, 192))):
        c.rect(X0, y0, X1, y1, fill=fill, width=8)
        c.rect(X0 + 210, y0 + 60, X1 - 40, y0 + 170, fill=(160, 205, 222), width=6)  # window
    c.rect(X0 - 30, UPPER[0] - 40, X1 + 30, UPPER[0], fill=(120, 96, 80), width=7)  # roof
    c.line([(X0 - 120, LOWER[1]), (X1 + 120, LOWER[1])], width=8)  # street
    _pin(c, X0 + 110, UPPER[1] - 110, MUSTARD, "DEV")
    _pin(c, X0 + 110, LOWER[1] - 110, TEAL, "MIRA")

    # "1 apart" bracket between them.
    ka = ease((t - b["apart"]) / 0.35)
    if ka > 0:
        x = X0 + 175
        c.line([(x, UPPER[1] - 110), (x + 26, UPPER[1] - 110), (x + 26, LOWER[1] - 110), (x, LOWER[1] - 110)], fill=ALERT, width=8)
        px, py = x + 110, (UPPER[1] + LOWER[1]) / 2 - 110
        c.rect(px - 80, py - 28, px + 80, py + 28, fill=PAPER, outline=ALERT, width=5, radius=28)
        c.text(px, py, "1 apart", 34 * (0.6 + 0.4 * ka), fill=ALERT, weight=HEAVY)

    # Computers count from zero (right side), people count from one (left side).
    kz = (t - b["zero"]) / 0.3
    if kz > 0:
        c.text(840, UPPER[0] - 30, "CODE", 30, fill=(125, 115, 105), weight=DEMI)
    _label(c, 840, (UPPER[0] + UPPER[1]) / 2, "1", kz)
    _label(c, 840, (LOWER[0] + LOWER[1]) / 2, "0", kz - 0.3)
    ko = (t - b["one"]) / 0.3
    if ko > 0:
        c.text(240, UPPER[0] - 30, "PEOPLE", 30, fill=(125, 115, 105), weight=DEMI)
    _label(c, 240, (UPPER[0] + UPPER[1]) / 2, "2nd", ko, size=58)
    _label(c, 240, (LOWER[0] + LOWER[1]) / 2, "1st", ko - 0.3, size=58)

    # Both "first floors" light up: Dev's (code's 1) and Mira's (people's 1st).
    if t >= b["glow"]:
        for x, y in ((840, (UPPER[0] + UPPER[1]) / 2), (240, (LOWER[0] + LOWER[1]) / 2)):
            c.circle(x, y, 62, outline=ALERT, width=8)
        if t < b["list"]:
            c.text(540, 1160, 'both "first floor"', 44, fill=ALERT, weight=HAND)

    # A list in code. Counting from 1 skips the first item; one step past the end crashes.
    kl = ease((t - b["list"]) / 0.35)
    if kl > 0:
        for i, name in enumerate(("milk", "eggs", "bread", "")):
            x = 250 + i * 150
            empty = not name
            if empty and t < b["crash"]:
                continue
            c.rect(x, 1150, x + 130, 1230, fill=(250, 226, 226) if empty else PAPER, width=6, radius=12,
                   outline=ALERT if empty else INK)
            c.text(x + 65, 1190, name or "?", 34, weight=HAND, fill=ALERT if empty else INK)
            c.text(x + 65, 1262, f"[{i}]", 32 * kl, fill=ALERT, weight=HEAVY)
        if t >= b["skip"]:
            c.line([(255, 1160), (375, 1222)], fill=ALERT, width=8)
            c.text(315, 1115, "skipped!", 34, fill=ALERT, weight=HAND)
        if t >= b["crash"]:
            c.text(765, 1115, "crash!", 34, fill=ALERT, weight=HAND)

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
    return finish(img)


if __name__ == "__main__":
    caps = [(0.1, "That's an off-by-one error."), (1.96, "Computers count from zero, people from one."),
            (4.88, "One slip means a skipped item, or a crash.")]
    frames = [render_frame(t, caps) for t in (0.9, 2.6, 4.4, 5.1, 6.0, 7.2)]
    sheet = Image.new("RGB", (W // 3 * 3, H // 3 * 2))
    for i, f in enumerate(frames):
        sheet.paste(f.resize((W // 3, H // 3)), ((i % 3) * (W // 3), (i // 3) * (H // 3)))
    out = Path(__file__).resolve().parent / "build"
    out.mkdir(exist_ok=True)
    sheet.save(out / "reveal-contact-sheet.png")
    print(out / "reveal-contact-sheet.png")
