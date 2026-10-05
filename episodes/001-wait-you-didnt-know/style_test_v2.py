"""Style test v2: one finished-quality frame in the risograph look (Grandpa, "…On what?", also the thumbnail).

v1 proved the look; this one pushes the drawing itself: faces and bodies built from curves instead of circles,
halftone-dot shading (the riso signature) with light from the window, overprinted inks, a lived-in background, and
a hand that actually grips the fork. Reuses the hand-drawn primitives from style_test.py.

Run: ../../.venv/bin/python style_test_v2.py  →  deliverables/style-b2-grandpa.png and style-b-compare.png
"""

from __future__ import annotations

import math

from PIL import Image, ImageChops, ImageDraw, ImageFont

from style_test import OUT, SS, STYLES, H, Sketch, W, composite, ellipse_pts, round_rect_pts

STYLE = "b-riso"


def bez(p0, p1, p2, p3, n=28):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def path(start, *segs, n=28):
    """A chain of cubic segments: path(p0, (c1, c2, p1), (c1, c2, p2), ...)."""
    pts, cur = [start], start
    for c1, c2, p in segs:
        pts += bez(cur, c1, c2, p, n)[1:]
        cur = p
    return pts


def mirror(pts, cx=540):
    return [(2 * cx - x, y) for x, y in pts]


def mask_of(pts) -> Image.Image:
    m = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(m).polygon([(x * SS, y * SS) for x, y in pts], fill=255)
    return m


def halftone(sk: Sketch, pts, ink="line", cell=13.0, angle=22.0, shade=lambda x, y: 0.5, max_r=0.62):
    """Riso halftone: a rotated dot grid inside the shape, each dot sized by the shade (0 light .. 1 dark)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    span = int(math.hypot(x1 - x0, y1 - y0) / cell / 2) + 2
    dots = Image.new("L", (W * SS, H * SS), 0)
    dr = ImageDraw.Draw(dots)
    for i in range(-span, span + 1):
        for j in range(-span, span + 1):
            u, v = i * cell, j * cell
            x, y = cx + u * ca - v * sa, cy + u * sa + v * ca
            if not (x0 - cell <= x <= x1 + cell and y0 - cell <= y <= y1 + cell):
                continue
            s = max(0.0, min(1.0, shade(x, y)))
            r = cell * max_r * math.sqrt(s)
            if r > 0.6:
                dr.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=255)
    sk.layers[ink] = ImageChops.lighter(sk.layer(ink), ImageChops.multiply(dots, mask_of(pts)))


def solid(sk: Sketch, pts, ink, offset=True):
    m = mask_of(pts)
    if offset:
        m = ImageChops.offset(m, 6 * SS, -4 * SS)
    sk.layers[ink] = ImageChops.lighter(sk.layer(ink), m)


def hairs(sk: Sketch, base, n, length, spread, angle, width=2.6, ink="line"):
    """Short pen flicks, for brows, moustache and the fringe of hair."""
    for k in range(n):
        t = k / max(1, n - 1)
        bx = base[0] + (t - 0.5) * spread
        by = base[1] + sk.rng.uniform(-4, 4)
        a = math.radians(angle + sk.rng.uniform(-14, 14))
        L = length * sk.rng.uniform(0.7, 1.15)
        sk.stroke([(bx, by), (bx + math.cos(a) * L * 0.5, by + math.sin(a) * L * 0.5 - 2),
                   (bx + math.cos(a) * L, by + math.sin(a) * L)], ink=ink, width=width, wobble=0.8, double=0)


def light(x, y):
    """Window light from the upper left: shade grows to the right and downward."""
    return (x - 300) / 700 + (y - 700) / 2600


def draw() -> Image.Image:
    sk = Sketch(STYLES[STYLE], seed=21)
    W2 = 540

    # ---------------- Background: wallpaper, window light, a framed photo, a shelf
    wall = [(0, 0), (W, 0), (W, H), (0, H)]
    stripe = lambda x, y: 0.16 if (int(x) // 60) % 2 == 0 else 0.0
    halftone(sk, wall, "fill2", cell=11, angle=0, shade=lambda x, y: stripe(x, y) * 0.8 + max(0, (x - 700) / 3000))
    # Window on the left: daylight (bare paper), a pink curtain
    win = [(-10, 130), (300, 130), (300, 585), (-10, 585)]
    sk.occlude(win)
    sk.stroke([(300, 130), (300, 585)], width=6)
    sk.stroke([(-10, 130), (300, 130)], width=6)
    sk.stroke([(150, 135), (150, 580)], width=4)
    sk.stroke([(0, 355), (296, 355)], width=4)
    curtain = path((300, 115), ((360, 260), (330, 420), (390, 640)), n=20) + [(330, 640), (262, 115)]
    sk.occlude(curtain)
    solid(sk, curtain, "accent")
    sk.stroke(curtain[:21], width=4)
    for k in range(3):
        sk.stroke(bez((290 + k * 18, 140), (300 + k * 18, 300), (300 + k * 18, 450), (320 + k * 18, 620), 12),
                  width=2.6)
    # Framed photo of the couple, top right
    fx0, fy0, fx1, fy1 = 760, 230, 1010, 520
    frame = round_rect_pts(fx0, fy0, fx1, fy1, 8, 3)
    sk.occlude(frame)
    solid(sk, frame, "fill")
    inner = round_rect_pts(fx0 + 24, fy0 + 24, fx1 - 24, fy1 - 24, 4, 3)
    sk.occlude(inner)
    halftone(sk, inner, "fill2", cell=9, angle=45, shade=lambda x, y: 0.35)
    sk.stroke(frame + [frame[0]], width=4.5)
    sk.stroke(inner + [inner[0]], width=3.2)
    for hx, hy in ((850, 360), (925, 362)):
        sk.circle(hx, hy, 26, width=3.2)
        sk.stroke(ellipse_pts(hx, hy + 92, 40, 52, 16, math.pi * 1.08, math.pi * 1.92), width=3.2)
    sk.stroke([(886, 330), (893, 318), (900, 330)], ink="accent", width=3)  # a tiny heart-ish flourish
    sk.stroke([(885, 228), (885, 170), (870, 160)], width=3)  # the nail and string
    # Shelf edge with a plant, left
    sk.stroke([(-10, 600), (310, 596)], width=6)
    pot = [(70, 596), (80, 516), (170, 516), (180, 596)]
    sk.occlude(pot)
    solid(sk, pot, "accent")
    sk.stroke(pot + [pot[0]], width=4)
    for a0, L in ((-120, 120), (-95, 150), (-70, 110), (-140, 90), (-50, 95)):
        a = math.radians(a0)
        sk.stroke([(125, 516), (125 + math.cos(a) * L * 0.5 + 10, 520 + math.sin(a) * L * 0.6),
                   (125 + math.cos(a) * L, 520 + math.sin(a) * L)], width=4)

    # ---------------- Body: shirt, cardigan, shoulders
    cardigan_l = path((540, 1215), ((420, 1220), (300, 1250), (215, 1330)), ((150, 1400), (110, 1600), (95, 1940)))
    cardigan = cardigan_l + [(985, 1940)] + mirror(cardigan_l)[::-1]
    sk.occlude(cardigan)
    solid(sk, cardigan, "fill2")
    halftone(sk, cardigan, "accent", cell=12, angle=22, shade=lambda x, y: (light(x, y) - 0.5) * 0.65)
    sk.stroke(cardigan_l)
    sk.stroke(mirror(cardigan_l))
    shirt = [(455, 1190), (625, 1190), (600, 1430), (540, 1520), (480, 1430)]
    sk.occlude(shirt)
    solid(sk, shirt, "fill")
    sk.stroke([(455, 1200), (480, 1430), (540, 1520)])
    sk.stroke([(625, 1200), (600, 1430), (540, 1520)])
    for side in (-1, 1):  # collar points
        c = [(540, 1238), (540 + side * 95, 1195), (540 + side * 70, 1300)]
        sk.occlude(c)
        solid(sk, c, "fill")
        sk.stroke(c + [c[0]], width=4)
    sk.stroke([(540, 1520), (540, 1940)])  # cardigan opening
    for by in (1600, 1720, 1840):
        sk.occlude(ellipse_pts(570, by, 13, 13))
        sk.circle(570, by, 13, width=3.5)

    # ---------------- Neck and head
    neck = [(470, 1080), (612, 1080), (618, 1215), (462, 1215)]
    sk.occlude(neck)
    solid(sk, neck, "skin")
    halftone(sk, neck, "accent", cell=10, shade=lambda x, y: 0.42 - (y - 1080) / 330)
    sk.stroke([(475, 1085), (466, 1212)])
    sk.stroke([(608, 1085), (616, 1212)])

    for side in (-1, 1):  # ears, behind the head
        ear = path((540 + side * 205, 820), ((540 + side * 268, 790), (540 + side * 280, 900),
                                             (540 + side * 255, 945)), ((540 + side * 235, 985),
                                                                        (540 + side * 205, 975), (540 + side * 200, 950)))
        sk.occlude(ear + [(540 + side * 200, 830)])
        solid(sk, ear + [(540 + side * 200, 830)], "skin")
        sk.stroke(ear)
        sk.stroke(bez((540 + side * 222, 845), (540 + side * 252, 850), (540 + side * 250, 920),
                      (540 + side * 226, 935), 14), width=3.2)

    head_l = path((540, 600), ((410, 600), (330, 680), (330, 810)), ((328, 960), (380, 1075), (470, 1112)),
                  ((505, 1128), (525, 1132), (540, 1132)))
    head = head_l + mirror(head_l)[::-1]
    sk.occlude(head)
    solid(sk, head, "skin")
    halftone(sk, head, "accent", cell=10, angle=22, shade=lambda x, y: (light(x, y) - 0.38) * 0.9)
    sk.stroke(head + [head[0]], width=6)
    # Head shine (paper showing through the skin)
    shine = ellipse_pts(455, 690, 52, 22, 20)
    shine = [(x + (y - 690) * 0.6, y) for x, y in shine]
    for ink in ("skin", "accent"):
        sk.layers[ink] = ImageChops.subtract(sk.layer(ink), mask_of(shine))
    # Forehead wrinkles
    for k, y in enumerate((700, 728, 756)):
        sk.stroke(bez((462 + 6 * k, y + 6), (500, y - 8), (580, y - 8), (618 - 6 * k, y + 6), 14), width=3.2)
    # Side hair: white fluffy tufts (outlines only, so the paper is the white)
    for side in (-1, 1):
        tuft = path((540 + side * 196, 700), ((540 + side * 262, 690), (540 + side * 268, 750),
                                              (540 + side * 236, 770)),
                    ((540 + side * 280, 785), (540 + side * 262, 845), (540 + side * 222, 840)),
                    ((540 + side * 252, 868), (540 + side * 226, 900), (540 + side * 205, 880)))
        sk.occlude(tuft + [(540 + side * 205, 760)])
        sk.stroke(tuft, width=4.5)
        hairs(sk, (540 + side * 236, 770), 4, 22, 30, 90 - side * 40, width=2.2)

    # Brows: bushy and raised (confused: the left one higher)
    for side, lift in ((-1, -26), (1, -8)):
        bx, by = 540 + side * 100, 778 + lift
        brow = path((bx - side * 62, by + 14), ((bx - side * 40, by - 18), (bx + side * 30, by - 26),
                                                 (bx + side * 70, by - 4)),
                    ((bx + side * 50, by + 6), (bx, by + 4), (bx - side * 62, by + 14)), n=16)
        sk.occlude(brow)
        solid(sk, brow, "line", offset=False)
        for k in range(7):  # ragged top edge
            t = k / 6
            x = bx - side * 55 + side * 120 * t
            y = by - 14 - 10 * math.sin(t * math.pi)
            sk.stroke([(x, y + 6), (x + side * 10, y - 10)], width=3.4, wobble=0.6, double=0)

    # Eyes behind round glasses, looking left (toward the aunt)
    for side in (-1, 1):
        ex, ey = 540 + side * 98, 862
        white = ellipse_pts(ex, ey, 34, 24, 28)
        sk.occlude(white)
        sk.stroke(white[14:] + white[:2], width=3.6)  # lower lid lighter
        sk.stroke(bez((ex - 38, ey - 2), (ex - 22, ey - 30), (ex + 22, ey - 30), (ex + 38, ey - 2), 16), width=4.4)
        sk.dot(ex - 14, ey + 2, 13)
        hl = ellipse_pts(ex - 18, ey - 3, 4.5, 4.5, 10)
        sk.layers["line"] = ImageChops.subtract(sk.layer("line"), mask_of(hl))
        sk.stroke(bez((ex - 30, ey + 36), (ex - 12, ey + 46), (ex + 12, ey + 46), (ex + 30, ey + 34), 12),
                  width=2.6)  # eye bag
        if side == 1:  # crow's feet on the shaded side
            for k in (-1, 0, 1):
                sk.stroke([(ex + 70, ey + k * 14), (ex + 88, ey + k * 20)], width=2.4)
        lens = round_rect_pts(ex - 74, ey - 62, ex + 74, ey + 66, 46, 6)
        sk.stroke(lens + [lens[0]], width=5.5)
        glare = [(ex + 22, ey - 58), (ex + 40, ey - 58), (ex + 66, ey - 18), (ex + 50, ey - 14)]
        for ink in ("accent", "skin"):
            sk.layers[ink] = ImageChops.subtract(sk.layer(ink), mask_of(glare))
    sk.stroke(bez((515, 852), (528, 836), (552, 836), (565, 852), 10), width=5)  # bridge
    for side in (-1, 1):
        sk.stroke([(540 + side * 172, 840), (540 + side * 205, 830)], width=4.5)

    # Nose: a big soft bulb with a pink tip
    nose = path((527, 880), ((520, 920), (500, 950), (492, 975)), ((480, 1010), (520, 1025), (540, 1018)),
                ((562, 1028), (598, 1012), (586, 978)), ((578, 950), (558, 920), (553, 880)), n=18)
    sk.occlude(nose)
    solid(sk, nose, "skin")
    halftone(sk, ellipse_pts(546, 992, 40, 26, 20), "accent", cell=8, angle=45, shade=lambda x, y: 0.55)
    sk.stroke(nose[18:], width=5)
    for side in (-1, 1):
        sk.stroke(bez((540 + side * 8, 1008), (540 + side * 18, 1000), (540 + side * 30, 1004),
                      (540 + side * 36, 1012), 8), width=3)

    # Moustache (white, bushy) and a small "o" mouth below it
    moustache_l = path((540, 1030), ((505, 1018), (450, 1016), (425, 1055)), ((440, 1062), (470, 1062), (495, 1056)),
                       ((515, 1052), (530, 1052), (540, 1060)), n=16)
    for side in (-1, 1):
        ms = moustache_l if side < 0 else mirror(moustache_l)
        sk.occlude(ms)
        sk.stroke(ms, width=4.5)
        for k in range(6):
            x = 540 + side * (18 + k * 17)
            sk.stroke([(x, 1036 + k * 1.5), (x + side * 6, 1050 + k * 1.5)], width=2.2, wobble=0.5, double=0)
    mouth = ellipse_pts(542, 1090, 20, 24, 24)
    sk.occlude(mouth)
    solid(sk, mouth, "line", offset=False)
    halftone(sk, ellipse_pts(542, 1102, 12, 9, 16), "accent", cell=6, shade=lambda x, y: 0.8)
    for side in (-1, 1):  # nose-to-mouth folds
        sk.stroke(bez((540 + side * 62, 1000), (540 + side * 92, 1030), (540 + side * 98, 1060),
                      (540 + side * 92, 1090), 12), width=3)

    # ---------------- Raised hand with the fork (his right hand, screen left)
    sleeve = path((100, 1940), ((150, 1700), (205, 1430), (270, 1285)), n=20)
    sleeve2 = path((330, 1310), ((295, 1450), (265, 1700), (300, 1940)), n=20)
    arm = sleeve + sleeve2 + [(100, 1940)]
    sk.occlude(arm)
    solid(sk, arm, "fill2")
    halftone(sk, arm, "accent", cell=12, angle=22, shade=lambda x, y: 0.22)
    sk.stroke(sleeve)
    sk.stroke(sleeve2)
    cuff = [(262, 1280), (338, 1306), (330, 1340), (252, 1312)]
    sk.occlude(cuff)
    solid(sk, cuff, "fill2")
    sk.stroke(cuff + [cuff[0]], width=4.5)
    # Fork, held upright, a piece of food on it
    sk.stroke([(318, 1205), (346, 1030)], width=7)
    for dx in (-15, -5, 5, 15):
        sk.stroke([(346 + dx * 0.95, 1032), (352 + dx, 975)], width=3.6)
    sk.stroke(bez((330, 1030), (338, 1045), (356, 1045), (364, 1032), 8), width=4)
    food = ellipse_pts(352, 985, 30, 22, 20)
    sk.occlude(food)
    solid(sk, food, "accent")
    halftone(sk, food, "line", cell=7, shade=lambda x, y: 0.18)
    sk.stroke(food + [food[0]], width=4)
    # Fist around the handle: knuckles, curled fingers, thumb over the top
    fist = path((262, 1290), ((240, 1250), (250, 1180), (285, 1165)), ((320, 1150), (360, 1165), (365, 1200)),
                ((372, 1240), (360, 1290), (330, 1300)), n=16)
    sk.occlude(fist + [(262, 1290)])
    solid(sk, fist + [(262, 1290)], "skin")
    halftone(sk, fist, "accent", cell=9, shade=lambda x, y: 0.25 + (x - 250) / 600)
    sk.stroke(fist + [(262, 1290)], width=5)
    for k in range(3):  # finger creases
        y = 1205 + k * 26
        sk.stroke(bez((300, y - 6), (320, y + 2), (345, y + 2), (362, y - 4), 8), width=3)
    thumb = path((282, 1180), ((300, 1150), (335, 1140), (348, 1160)), ((356, 1172), (340, 1185), (318, 1182)), n=10)
    sk.stroke(thumb, width=4.5)

    # ---------------- Speech bubble, the aunt's off-screen line, and the caption strip
    from style_test import bubble
    bubble(sk, (560, 1340, 1040, 1500), (640, 1130), "…On what?", 84)
    sk.text((560, 72), "Congratulations!!", "noteworthy", 58, "line", angle=3)
    sk.stroke([(118, 190), (40, 215)], width=4)  # the aunt's line comes from off-screen left
    sk.stroke([(122, 215), (48, 255)], width=4)
    return composite(sk, STYLE)


def main():
    img = draw()
    img.save(OUT / "style-b2-grandpa.png")
    v1 = Image.open(OUT / "style-b-riso.png")
    tw, th = 540, 960
    sheet = Image.new("RGB", (tw * 2 + 60, th + 110), (245, 245, 245))
    dr = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34, index=0)
    for i, (label, im) in enumerate((("v1 · rough test", v1), ("v2 · finished drawing", img))):
        x = 20 + i * (tw + 20)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, 90))
        dr.text((x + tw / 2, 45), label, font=f, fill=(30, 30, 30), anchor="mm")
    sheet.save(OUT / "style-b-compare.png")
    print("wrote", OUT / "style-b2-grandpa.png")


if __name__ == "__main__":
    main()
