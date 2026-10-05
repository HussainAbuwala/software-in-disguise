"""Open Peeps busts (Pablo Stanley, CC0: https://www.openpeeps.com/), composed from the parts in assets/open-peeps.

Layout and tinting follow PeepStudio's composer (github.com/Hantuhan/peepstudio, lib/peeps): a 1136x1533 bust canvas
with the body, head, face and accessories at fixed offsets. Parts are black ink on white; the head's "🎨-Background"
becomes skin, its ink becomes hair; white areas of the face and body become skin; a body's background becomes the
clothing colour.
"""

from __future__ import annotations

import io
import os
import re
from pathlib import Path

from PIL import Image

os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")
import cairosvg  # noqa: E402

ATOMS = Path(__file__).resolve().parents[1] / "assets" / "open-peeps"
CANVAS = (1136, 1533)
BODY_AT, HEAD_AT = (147, 639), (372, 180)
FACE_OFF, FACIAL_HAIR_OFF, ACCESSORY_OFF = (159, 186), (123, 338), (47, 241)


def _group(svg: str) -> str:
    start = svg.find("<g")
    if start == -1:
        m = re.search(r"<svg[^>]*>([\s\S]*?)</svg>", svg)
        return m.group(1) if m else ""
    return svg[start:svg.rfind("</g>") + 4]


def _bg(group: str, color: str) -> str:
    return re.sub(r'(<path\b[^>]*\bid="🎨-Background"[^>]*?)\bfill="[^"]*"', rf'\1fill="{color}"', group)


def _white_to(group: str, color: str) -> str:
    def sub(m):
        tag = m.group(0)
        if 'id="🎨-Background"' in tag:
            return tag
        return re.sub(r'\bfill="(#fff|#ffffff)"', f'fill="{color}"', tag, count=1, flags=re.I)
    return re.sub(r"<path\b[^>]*>", sub, group, flags=re.I)


def _ink(group: str, color: str) -> str:
    return re.sub(r'\b(fill|stroke)="(#000000|#000|#231f20)"', rf'\1="{color}"', group, flags=re.I)


def bust(body="button-shirt", head="bun", face="calm", accessory=None, facial_hair=None, skin="#c98d63",
         hair="#1d1b1f", clothes="#e9563f", ink="#1d1b1f", height=900) -> Image.Image:
    read = lambda kind, name: (ATOMS / kind / f"{name}.svg").read_text()
    body_g = _group(read("body", body))
    # Clothing: the body's background layer if it has one, otherwise its white areas are the clothes.
    body_g = _bg(body_g, clothes) if 'id="🎨-Background"' in body_g else _white_to(body_g, clothes)
    body_g = _white_to(body_g, skin)
    head_g = _group(read("head", head))
    head_g = _ink(_bg(head_g, skin), hair) if 'id="🎨-Background"' in head_g else _white_to(head_g, skin)
    face_g = _white_to(_group(read("face", face)), skin)
    parts = [(BODY_AT, body_g), (HEAD_AT, head_g), ((HEAD_AT[0] + FACE_OFF[0], HEAD_AT[1] + FACE_OFF[1]), face_g)]
    if facial_hair:
        parts.append(((HEAD_AT[0] + FACIAL_HAIR_OFF[0], HEAD_AT[1] + FACIAL_HAIR_OFF[1]),
                      _ink(_group(read("facial-hair", facial_hair)), hair)))
    if accessory:
        parts.append(((HEAD_AT[0] + ACCESSORY_OFF[0], HEAD_AT[1] + ACCESSORY_OFF[1]), _group(read("accessories", accessory))))
    inner = "".join(f'<g transform="translate({x},{y})">{g}</g>' for (x, y), g in parts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS[0]} {CANVAS[1]}" '
           f'width="{CANVAS[0]}" height="{CANVAS[1]}">{inner}</svg>')
    svg = re.sub(r'#231f20|#000000\b|#000\b', ink, svg)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_height=height)
    return Image.open(io.BytesIO(png)).convert("RGBA")
