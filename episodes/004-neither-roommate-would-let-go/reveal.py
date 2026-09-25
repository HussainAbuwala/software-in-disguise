"""Render the Episode 04 reveal graphic (R1): the deadlock cycle, then the same cycle relabeled as software.

Timed to Hussain's reveal line. Silent; audio is mixed in the full episode render (render_episode.py), which passes
the real caption start times so the arrows, pulse and relabel land on the spoken words.

    ../../.venv/bin/python reveal.py            # deliverables/reveal-graphic.mp4
    ../../.venv/bin/python reveal.py --sheet    # also build/reveal-contact-sheet.png
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "deliverables" / "reveal-graphic.mp4"
SHEET = HERE / "build" / "reveal-contact-sheet.png"

W, H, FPS, DURATION = 1080, 1920, 30, 7.5
SS = 2  # supersampling factor for smooth ink lines

FONT = "/System/Library/Fonts/Avenir Next.ttc"
BOLD_INDEX, DEMI_INDEX = 0, 2  # Avenir Next Bold, Demi Bold

PAPER = (244, 239, 230)
INK = (28, 26, 24)
MUSTARD = (227, 178, 60)
TEAL = (42, 157, 143)
GREY = (205, 198, 186)
ALERT = (209, 73, 91)

# Hussain's line, split into caption chunks with approximate start times (seconds).
CAPTIONS = [
    (0.00, "That's a deadlock."),
    (1.30, "Each one holds what the other needs,"),
    (3.60, "so both wait forever."),
    (5.30, "It's one reason apps freeze."),
]

# Cycle layout (1x coordinates). Content stays inside the Shorts safe zone:
# right 15% and bottom 20% hold no essential text.
NODES = {
    "dev": {"xy": (270, 560), "fill": MUSTARD, "story": ("DEV", "person"), "software": ("TASK A", "app")},
    "batteries": {"xy": (750, 560), "fill": GREY, "story": ("BATTERIES", "battery"), "software": ("FILE 2", "file")},
    "mira": {"xy": (750, 1100), "fill": TEAL, "story": ("MIRA", "person"), "software": ("TASK B", "app")},
    "remote": {"xy": (270, 1100), "fill": GREY, "story": ("REMOTE", "remote"), "software": ("FILE 1", "file")},
}
NODE_R = 125

# (from, to, label). Order traces the circular wait.
EDGES = [
    ("dev", "batteries", "wants"),
    ("batteries", "mira", "held by"),
    ("mira", "remote", "wants"),
    ("remote", "dev", "held by"),
]
EDGE_GROW = 0.35
PULSE_LAP = 0.7  # a red highlight travels the loop twice
RELABEL_LEN = 0.5


def beats_for(captions) -> dict:
    """Event times keyed to the four spoken chunks: title on chunk 1, arrows through chunk 2, pulse on
    "wait forever", relabel on "apps freeze"."""
    c1, c2, c3, c4 = (start for start, _ in captions)
    step = max(0.3, (c3 - 0.25 - (c1 + 0.7)) / 3)
    return {
        "title": c1 + 0.15,
        "edges": [c1 + 0.7 + i * step for i in range(4)],
        "pulse": c3 + 0.1,
        "relabel": c4,
    }


def font(size: int, index: int = BOLD_INDEX) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size * SS, index=index)


def s(v: float) -> int:
    return round(v * SS)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def text_center(draw: ImageDraw.ImageDraw, xy, text, fnt, fill):
    draw.text((s(xy[0]), s(xy[1])), text, font=fnt, fill=fill, anchor="mm")


def draw_icon(draw: ImageDraw.ImageDraw, shape: str, cx: float, cy: float):
    lw = s(7)
    if shape == "battery":
        for dx in (-34, 34):
            x = cx + dx
            draw.rounded_rectangle([s(x - 22), s(cy - 58), s(x + 22), s(cy + 38)], radius=s(8), fill=MUSTARD, outline=INK, width=lw)
            draw.rectangle([s(x - 9), s(cy - 72), s(x + 9), s(cy - 58)], fill=INK)
            draw.line([s(x - 22), s(cy - 30), s(x + 22), s(cy - 30)], fill=INK, width=s(5))
    elif shape == "remote":
        draw.rounded_rectangle([s(cx - 30), s(cy - 72), s(cx + 30), s(cy + 42)], radius=s(18), fill=(60, 58, 56), outline=INK, width=lw)
        draw.ellipse([s(cx - 12), s(cy - 58), s(cx + 12), s(cy - 34)], fill=ALERT)
        for row in range(3):
            for col in (-1, 1):
                x, y = cx + col * 12, cy - 18 + row * 20
                draw.ellipse([s(x - 6), s(y - 6), s(x + 6), s(y + 6)], fill=PAPER)
    elif shape == "file":
        draw.polygon([(s(cx - 40), s(cy - 66)), (s(cx + 16), s(cy - 66)), (s(cx + 40), s(cy - 42)), (s(cx + 40), s(cy + 50)), (s(cx - 40), s(cy + 50))], fill=PAPER, outline=INK, width=lw)
        draw.polygon([(s(cx + 16), s(cy - 66)), (s(cx + 16), s(cy - 42)), (s(cx + 40), s(cy - 42))], fill=INK)
        for row in range(4):
            y = cy - 26 + row * 18
            draw.line([s(cx - 24), s(y), s(cx + (24 if row < 3 else 4)), s(y)], fill=INK, width=s(5))
    elif shape == "app":
        draw.rounded_rectangle([s(cx - 58), s(cy - 58), s(cx + 58), s(cy + 44)], radius=s(10), fill=PAPER, outline=INK, width=lw)
        draw.line([s(cx - 58), s(cy - 30), s(cx + 58), s(cy - 30)], fill=INK, width=lw)
        for i, dx in enumerate((-40, -24, -8)):
            draw.ellipse([s(cx + dx - 5), s(cy - 49), s(cx + dx + 5), s(cy - 39)], fill=ALERT if i == 0 else INK)
        # Frozen app: a stalled progress bar.
        draw.rounded_rectangle([s(cx - 38), s(cy + 2), s(cx + 38), s(cy + 20)], radius=s(9), outline=INK, width=s(4))
        draw.rounded_rectangle([s(cx - 34), s(cy + 6), s(cx - 2), s(cy + 16)], radius=s(5), fill=INK)
    else:  # person: simple head-and-shoulders silhouette
        draw.ellipse([s(cx - 30), s(cy - 78), s(cx + 30), s(cy - 18)], fill=PAPER, outline=INK, width=lw)
        draw.pieslice([s(cx - 58), s(cy - 10), s(cx + 58), s(cy + 100)], 180, 360, fill=PAPER, outline=INK, width=lw)


def node_layer(label_key: str) -> Image.Image:
    """All four nodes with either story or software labels, on a transparent layer."""
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    label_font = font(40)
    for node in NODES.values():
        cx, cy = node["xy"]
        draw.ellipse([s(cx - NODE_R), s(cy - NODE_R), s(cx + NODE_R), s(cy + NODE_R)], fill=node["fill"], outline=INK, width=s(9))
        label, shape = node[label_key]
        draw_icon(draw, shape, cx, cy - 10)
        # Same pill width in both states so the label crossfade has no ghost edges.
        box_w = max(150, max(len(node[k][0]) for k in ("story", "software")) * 27 + 40)
        ly = cy + NODE_R + 8
        draw.rounded_rectangle([s(cx - box_w / 2), s(ly - 30), s(cx + box_w / 2), s(ly + 30)], radius=s(30), fill=INK)
        text_center(draw, (cx, ly), label, label_font, PAPER)
    return layer


def edge_points(a: str, b: str):
    (x1, y1), (x2, y2) = NODES[a]["xy"], NODES[b]["xy"]
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    pad = NODE_R + 22
    return (x1 + ux * pad, y1 + uy * pad), (x2 - ux * pad, y2 - uy * pad), (ux, uy)


def draw_edge(draw: ImageDraw.ImageDraw, a: str, b: str, label: str, progress: float, color):
    if progress <= 0:
        return
    (sx, sy), (ex, ey), (ux, uy) = edge_points(a, b)
    tx, ty = sx + (ex - sx) * progress, sy + (ey - sy) * progress
    draw.line([s(sx), s(sy), s(tx), s(ty)], fill=color, width=s(12))
    head = 34
    px, py = -uy, ux
    draw.polygon(
        [
            (s(tx + ux * 8), s(ty + uy * 8)),
            (s(tx - ux * head + px * head * 0.6), s(ty - uy * head + py * head * 0.6)),
            (s(tx - ux * head - px * head * 0.6), s(ty - uy * head - py * head * 0.6)),
        ],
        fill=color,
    )
    if progress > 0.6:
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        # Offset labels outward from the cycle's center so they never sit on the arrow.
        cx, cy = 510, 830
        ox, oy = mx - cx, my - cy
        n = math.hypot(ox, oy) or 1
        lx, ly = mx + ox / n * 48, my + oy / n * 48
        f = font(34, DEMI_INDEX)
        w = draw.textlength(label, font=f) / SS + 36
        draw.rounded_rectangle([s(lx - w / 2), s(ly - 26), s(lx + w / 2), s(ly + 26)], radius=s(26), fill=PAPER, outline=color, width=s(5))
        text_center(draw, (lx, ly), label, f, color)


def active_caption(t: float, captions=CAPTIONS) -> str:
    text = ""
    for start, chunk in captions:
        if t >= start:
            text = chunk
    return text


def render_frame(t: float, story_nodes: Image.Image, software_nodes: Image.Image, captions=CAPTIONS) -> Image.Image:
    beats = beats_for(captions)
    img = Image.new("RGBA", (W * SS, H * SS), PAPER + (255,))
    draw = ImageDraw.Draw(img)

    # Corner wordmark and concept title.
    draw.text((s(80), s(170)), "SOFTWARE IN DISGUISE · 04", font=font(30, DEMI_INDEX), fill=INK)
    title_in = ease((t - beats["title"]) / 0.3)
    if title_in > 0:
        size = 120 + (1 - title_in) * 40
        title = Image.new("RGBA", img.size, (0, 0, 0, 0))
        text_center(ImageDraw.Draw(title), (W / 2 - 50, 300), "DEADLOCK", font(round(size)), ALERT + (round(255 * title_in),))
        img.alpha_composite(title)

    # Arrows: grow in order, then a red highlight laps the loop.
    lap_t = t - beats["pulse"]
    hot = int(lap_t / (PULSE_LAP / 4)) % 4 if 0 <= lap_t < PULSE_LAP * 2 else -1
    for i, ((a, b, label), start) in enumerate(zip(EDGES, beats["edges"])):
        draw_edge(draw, a, b, label, ease((t - start) / EDGE_GROW), ALERT if i == hot else INK)

    # Nodes, crossfading from story labels to software labels.
    mix = ease((t - beats["relabel"]) / RELABEL_LEN)
    nodes = story_nodes if mix <= 0 else software_nodes if mix >= 1 else Image.blend(story_nodes, software_nodes, mix)
    img.alpha_composite(nodes)

    # Caption panel (above the bottom 20% reserve).
    caption = active_caption(t, captions)
    if caption:
        f = font(54)
        lines, line = [], ""
        for word in caption.split():
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=f) / SS > 780:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
        top = 1370
        panel_h = 40 + 70 * len(lines)
        draw.rounded_rectangle([s(90), s(top), s(900), s(top + panel_h)], radius=s(24), fill=(255, 252, 245), outline=INK, width=s(5))
        for i, text in enumerate(lines):
            text_center(draw, (495, top + 55 + 70 * i), text, f, INK)

    return img.convert("RGB").resize((W, H), Image.LANCZOS)


def main():
    story_nodes, software_nodes = node_layer("story"), node_layer("software")
    OUT.parent.mkdir(exist_ok=True)
    ffmpeg = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", str(FPS), str(OUT)],
        stdin=subprocess.PIPE,
    )
    samples = {0.1: None, 1.0: None, 2.8: None, 4.1: None, 5.55: None, 7.3: None}
    for n in range(round(DURATION * FPS)):
        t = n / FPS
        frame = render_frame(t, story_nodes, software_nodes)
        ffmpeg.stdin.write(frame.tobytes())
        for k in samples:
            if samples[k] is None and t >= k:
                samples[k] = frame
    ffmpeg.stdin.close()
    ffmpeg.wait()

    if "--sheet" in sys.argv:
        SHEET.parent.mkdir(exist_ok=True)
        thumbs = [f.resize((W // 3, H // 3)) for f in samples.values()]
        sheet = Image.new("RGB", (W // 3 * 3, H // 3 * 2), (0, 0, 0))
        for i, th in enumerate(thumbs):
            sheet.paste(th, ((i % 3) * (W // 3), (i // 3) * (H // 3)))
        sheet.save(SHEET)
    print(OUT)


if __name__ == "__main__":
    main()
