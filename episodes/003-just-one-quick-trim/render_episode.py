from __future__ import annotations

from pathlib import Path
import json
import math
import subprocess

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
ART = ROOT / "art"
AUDIO = ROOT / "audio"
BUILD = ROOT / "build"
OUT = ROOT / "deliverables"
BUILD.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

W, H = 1080, 1920
FPS = 30
SR = 48000
SAFE_LEFT = 70
SAFE_RIGHT = 930
SAFE_TOP = 260
SAFE_BOTTOM = 1320
CAPTION_BOTTOM = 1240
FONT_REGULAR = "/System/Library/Fonts/Avenir Next.ttc"
FONT_BOLD = "/System/Library/Fonts/Avenir Next.ttc"
INK = (35, 31, 30)
CREAM = (247, 235, 210)
TEAL = (46, 85, 84)
GOLD = (224, 169, 65)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Avenir Next collection resolves to a readable default face on macOS.
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def fit_image(path: Path) -> Image.Image:
    return ImageOps.fit(Image.open(path).convert("RGB"), (W, H), method=Image.Resampling.LANCZOS)


def cover_gradient(im: Image.Image, top_strength: int = 0, bottom_strength: int = 0) -> Image.Image:
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    px = overlay.load()
    for y in range(H):
        a = 0
        if top_strength and y < 560:
            a = int(top_strength * (1 - y / 560) ** 1.5)
        if bottom_strength and y > 1300:
            a = max(a, int(bottom_strength * ((y - 1300) / 620) ** 1.4))
        if a:
            for x in range(W):
                px[x, y] = (20, 17, 15, a)
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def rounded_text_box(draw: ImageDraw.ImageDraw, xy, fill, radius=24, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def add_caption(im: Image.Image, speaker: str | None, text: str | None) -> Image.Image:
    if not text:
        return im
    out = im.convert("RGBA")
    shade = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rectangle((0, 1450, W, H), fill=(15, 13, 12, 92))
    out = Image.alpha_composite(out, shade)
    draw = ImageDraw.Draw(out)
    f = font(58, True)
    sfnt = font(28, True)
    lines = wrap(draw, text, f, 760)
    line_h = 72
    box_h = len(lines) * line_h + (48 if speaker else 20) + 56
    top = CAPTION_BOTTOM - box_h
    rounded_text_box(draw, (SAFE_LEFT, top, SAFE_RIGHT, CAPTION_BOTTOM), (248, 237, 214, 242), 28)
    if speaker:
        draw.text((SAFE_LEFT + 36, top + 32), speaker.upper(), font=sfnt, fill=TEAL)
        text_y = top + 72
    else:
        text_y = top + 38
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        draw.text(((W - (bbox[2] - bbox[0])) / 2, text_y), line, font=f, fill=INK)
        text_y += line_h
    return out.convert("RGB")


def add_time(im: Image.Image, value: str, y: int = 286) -> Image.Image:
    out = im.convert("RGBA")
    draw = ImageDraw.Draw(out)
    f = font(31, True)
    bbox = draw.textbbox((0, 0), value, font=f)
    x2 = SAFE_RIGHT
    x1 = x2 - (bbox[2] - bbox[0]) - 44
    rounded_text_box(draw, (x1, y, x2, y + 52), (35, 31, 30, 205), 20)
    draw.text((x1 + 22, y + 9), value, font=f, fill=CREAM)
    return out.convert("RGB")


def title_arrival(im: Image.Image) -> Image.Image:
    out = cover_gradient(im, top_strength=132)
    layer = out.convert("RGBA")
    draw = ImageDraw.Draw(layer)
    small = font(29, True)
    big = font(112, True)
    draw.text((SAFE_LEFT, 276), "SOFTWARE IN DISGUISE  ·  03", font=small, fill=(255, 244, 221))
    draw.text((SAFE_LEFT - 4, 326), "YOU'RE", font=big, fill=(255, 244, 221), stroke_width=2, stroke_fill=(40, 33, 28))
    draw.text((SAFE_LEFT - 4, 434), "NEXT.", font=big, fill=GOLD, stroke_width=2, stroke_fill=(40, 33, 28))
    return layer.convert("RGB")


def phone_frame(source: Image.Image) -> Image.Image:
    bg = source.resize((W, H)).filter(ImageFilter.GaussianBlur(4)).convert("RGBA")
    veil = Image.new("RGBA", bg.size, (22, 19, 18, 90))
    bg = Image.alpha_composite(bg, veil)
    draw = ImageDraw.Draw(bg)
    # Deterministic, unbranded phone close-up.
    phone = (142, 218, 938, 1684)
    rounded_text_box(draw, phone, (24, 26, 28, 255), 74, outline=(230, 220, 200, 210), width=5)
    screen = (170, 268, 910, 1628)
    rounded_text_box(draw, screen, (240, 232, 215, 255), 48)
    draw.rounded_rectangle((453, 292, 627, 314), radius=10, fill=(35, 33, 31, 240))
    draw.text((223, 382), "1:46 PM", font=font(34, True), fill=TEAL)
    draw.text((223, 508), "WEDDING CAR", font=font(34, True), fill=TEAL)
    rounded_text_box(draw, (214, 576, 866, 844), (255, 252, 244, 255), 34, outline=(208, 195, 170, 255), width=3)
    draw.text((258, 624), "Driver", font=font(31, True), fill=(105, 96, 86))
    draw.text((258, 696), "Outside", font=font(76, True), fill=INK)
    draw.text((258, 792), "Waiting by the entrance", font=font(30), fill=(105, 96, 86))
    draw.text((W // 2, 1525), "●", anchor="mm", font=font(36), fill=(80, 75, 70))
    return bg.convert("RGB")


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def lerp(start: float, end: float, amount: float) -> float:
    return start + (end - start) * amount


def draw_job_card(draw: ImageDraw.ImageDraw, x: float, y: float, width: int, height: int,
                  title: str, detail: str, fill, accent, status: str | None = None) -> None:
    x = int(x)
    y = int(y)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=24, fill=fill,
                           outline=(42, 37, 33), width=4)
    draw.rectangle((x, y, x + 14, y + height), fill=accent)
    draw.text((x + 30, y + 22), title, font=font(31, True), fill=INK)
    draw.text((x + 30, y + 65), detail, font=font(24), fill=(92, 82, 72))
    if status:
        draw.text((x + 30, y + height - 44), status, font=font(22, True), fill=accent)


def reveal_animation_frame(seconds: float) -> Image.Image:
    out = Image.new("RGB", (W, H), (241, 228, 200))
    draw = ImageDraw.Draw(out)
    # Paper texture and stable title field.
    for y in range(0, H, 12):
        shade = 235 + ((y // 12) % 2) * 2
        draw.line((0, y, W, y), fill=(shade, shade - 9, shade - 25), width=1)
    draw.text((SAFE_LEFT, 278), "STARVATION", font=font(100, True), fill=(151, 92, 26))
    draw.text((SAFE_LEFT, 386), "When one job never gets its turn.", font=font(39, True), fill=INK)
    draw.text((SAFE_LEFT, 476), "PRINT QUEUE", font=font(27, True), fill=TEAL)

    # Static printer at the front of the queue.
    px, py = 742, 548
    draw.rounded_rectangle((px, py + 72, px + 188, py + 250), radius=25,
                           fill=(61, 86, 84), outline=INK, width=5)
    draw.rectangle((px + 28, py, px + 160, py + 110), fill=(255, 250, 238), outline=INK, width=4)
    draw.line((px + 52, py + 35, px + 136, py + 35), fill=(118, 108, 96), width=4)
    draw.line((px + 52, py + 56, px + 124, py + 56), fill=(118, 108, 96), width=4)
    draw.rounded_rectangle((px + 26, py + 172, px + 162, py + 276), radius=12,
                           fill=(255, 250, 238), outline=INK, width=4)
    draw.text((px + 94, py + 131), "PRINT", anchor="mm", font=font(25, True), fill=CREAM)
    draw.line((SAFE_LEFT + 15, 718, px - 18, 718), fill=(116, 103, 88), width=5)
    draw.polygon([(px - 18, 718), (px - 42, 704), (px - 42, 732)], fill=(116, 103, 88))

    # The report remains in place as each tiny job passes it.
    report_progress = ease((seconds - 8.7) / 1.25)
    report_x = lerp(390, 560, report_progress)
    report_status = "YOUR TURN" if seconds >= 9.0 else "WAITING"
    draw_job_card(draw, report_x, 642, 270, 154, "YOUR REPORT", "20 pages",
                  (239, 185, 73), (141, 79, 25), report_status)

    arrivals = [(1.75, "ONE PAGE"), (3.75, "ONE PAGE"), (5.75, "ONE PAGE")]
    completed = 0
    for start, label in arrivals:
        local = seconds - start
        if local < 0:
            continue
        if local >= 1.65:
            completed += 1
            continue
        move_in = ease(local / 0.65)
        move_out = ease((local - 1.05) / 0.60)
        x = lerp(95, 580, move_in)
        x = lerp(x, 735, move_out)
        draw_job_card(draw, x, 662, 135, 116, label, "quick job",
                      (107, 169, 164), (36, 91, 89))

    # Printed one-page jobs accumulate as evidence of the unfair pattern.
    # Keep the completed jobs above the longest caption panel. The third card
    # ends at y=864, leaving a clear gap before the panel begins at y=876.
    draw.text((SAFE_LEFT, 778), "PRINTED FIRST", font=font(23, True), fill=(104, 91, 76))
    for index in range(completed):
        x = SAFE_LEFT + index * 112
        draw.rounded_rectangle((x, 816, x + 92, 864), radius=12,
                               fill=(107, 169, 164), outline=INK, width=3)
        draw.text((x + 46, 840), "1 PAGE", anchor="mm", font=font(17, True), fill=INK)

    # Once fairness is applied, the next small job waits behind the report.
    if seconds >= 8.7:
        draw.text((SAFE_LEFT, 542), "FAIR RULE: WAITING WORK GETS A TURN",
                  font=font(26, True), fill=(36, 91, 89))
        next_x = lerp(50, 228, ease((seconds - 8.9) / 0.8))
        draw_job_card(draw, next_x, 662, 135, 116, "ONE PAGE", "waits next",
                      (191, 211, 197), (36, 91, 89))

    if seconds < 1.45:
        caption = "That's starvation."
    elif seconds < 8.45:
        caption = "Imagine your report never printing because every new one-page job jumps ahead."
    else:
        caption = "Good software makes sure waiting work gets a turn."
    out = add_caption(out, None, caption)
    draw = ImageDraw.Draw(out)
    draw.text((SAFE_LEFT, 1282), "SOFTWARE IN DISGUISE  ·  03", font=font(24, True), fill=(94, 80, 66))
    return out


def render_reveal_animation(path: Path, duration: float) -> None:
    command = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
        "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", str(path)
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame_number in range(int(round(duration * FPS))):
        frame = reveal_animation_frame(frame_number / FPS)
        process.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("Reveal animation render failed")


base = {
    "arrival": fit_image(ART / "01-arrival.png"),
    "beard-arrives": fit_image(ART / "03-beard-arrives.png"),
    "beard-chair": fit_image(ART / "04-beard-chair.png"),
    "neckline-arrives": fit_image(ART / "05-neckline-arrives.png"),
    "neckline-chair": fit_image(ART / "06-neckline-chair.png"),
    "moustache-arrives": fit_image(ART / "07-moustache-arrives.png"),
    "payoff": fit_image(ART / "09-payoff.png"),
    "reaction": fit_image(ART / "10-reaction.png"),
}

# A fixed close composition for shot 2; it is a hard cut, not animated movement.
shot2 = ImageOps.fit(Image.open(ART / "01-arrival.png").convert("RGB"), (W, H),
                     method=Image.Resampling.LANCZOS, centering=(0.72, 0.49))

segments = [
    ("01-opening", 4.2, add_caption(add_time(title_arrival(base["arrival"]), "12:50 PM", 588), "Groom", "I'm getting married at two. Time for a haircut?")),
    ("02-promise", 3.1, add_caption(add_time(shot2, "12:50 PM"), "Barber", "Plenty of time. You're next.")),
    ("03-beard", 2.5, add_caption(base["beard-arrives"], "Customer", "Just a quick beard trim?")),
    ("03b-two-minutes", 1.9, add_caption(base["beard-arrives"], "Barber", "Two minutes.")),
    ("04-first-wait", 2.7, add_caption(base["beard-chair"], "Groom", "Sure.")),
    ("05-neckline", 2.7, add_caption(add_time(base["neckline-arrives"], "1:10 PM"), "Customer", "Just the neckline.")),
    ("05b-then-you", 2.5, add_caption(add_time(base["neckline-arrives"], "1:10 PM"), "Barber", "Then you're up.")),
    ("06-second-wait", 3.2, add_time(base["neckline-chair"], "1:18 PM")),
    ("07-moustache", 2.5, add_caption(add_time(base["moustache-arrives"], "1:30 PM"), "Customer", "Only the moustache.")),
    ("07b-one-minute", 2.7, add_caption(add_time(base["moustache-arrives"], "1:30 PM"), "Barber", "Won't take a minute.")),
    ("08-phone", 3.6, phone_frame(base["moustache-arrives"])),
    ("09-payoff", 4.2, add_caption(base["payoff"], "Groom", "What if you just cut the front? That's quick.")),
    ("10-reaction", 3.0, base["reaction"]),
    ("11-reveal", 12.0, reveal_animation_frame(0.0)),
]

timeline = []
cursor = 0.0
for name, duration, image in segments:
    path = BUILD / f"{name}.png"
    image.save(path, quality=95)
    timeline.append({"name": name, "start": cursor, "duration": duration, "image": str(path)})
    cursor += duration

TOTAL = cursor


def fade_envelope(n: int, attack: float = 0.01, release: float = 0.04) -> np.ndarray:
    env = np.ones(n, dtype=np.float32)
    a = min(n, int(attack * SR))
    r = min(n, int(release * SR))
    if a:
        env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] = np.linspace(1, 0, r)
    return env


rng = np.random.default_rng(303)
n = int((TOTAL + 0.1) * SR)
mix = np.zeros((n, 2), dtype=np.float32)

# Quiet continuous shop ambience: filtered-looking low noise plus distant electrical hum.
t = np.arange(n) / SR
noise = rng.normal(0, 1, n).astype(np.float32)
kernel = np.ones(1200, dtype=np.float32) / 1200
room = np.convolve(noise, kernel, mode="same") * 0.22
room += 0.004 * np.sin(2 * np.pi * 60 * t)
mix[:, 0] += room
mix[:, 1] += room * 0.97


def place_wave(wave: np.ndarray, start: float, gain: float = 1.0, pan: float = 0.0) -> None:
    idx = int(start * SR)
    if wave.ndim == 2:
        mono = wave.mean(axis=1)
    else:
        mono = wave
    if len(mono) + idx > len(mix):
        mono = mono[:len(mix) - idx]
    left = math.sqrt((1 - pan) / 2) * gain
    right = math.sqrt((1 + pan) / 2) * gain
    mix[idx:idx + len(mono), 0] += mono * left
    mix[idx:idx + len(mono), 1] += mono * right


def tone(freqs: list[float], seconds: float, amp: float = 0.12, decay: float = 3.0) -> np.ndarray:
    tt = np.arange(int(seconds * SR)) / SR
    sig = sum(np.sin(2 * np.pi * f * tt) for f in freqs) / len(freqs)
    return (sig * np.exp(-decay * tt) * fade_envelope(len(tt), 0.004, 0.08) * amp).astype(np.float32)


def clippers(seconds: float) -> np.ndarray:
    tt = np.arange(int(seconds * SR)) / SR
    carrier = 0.55 * np.sin(2 * np.pi * 118 * tt) + 0.3 * np.sin(2 * np.pi * 236 * tt)
    buzz = carrier + rng.normal(0, 0.25, len(tt))
    return (buzz * fade_envelope(len(tt), 0.08, 0.12) * 0.035).astype(np.float32)


# Door bells, clippers, phone vibration, and sparse original musical phrases.
for when in (0.08, 7.12, 14.18, 22.58):
    place_wave(tone([880, 1320], 0.7, 0.10, 4.2), when, pan=-0.45)
place_wave(clippers(2.1), 11.78, pan=0.45)
place_wave(clippers(2.6), 19.72, pan=0.45)
place_wave(clippers(2.4), 25.16, pan=0.45)
place_wave(tone([155, 165], 0.22, 0.13, 1.0), 28.45, pan=-0.15)
place_wave(tone([155, 165], 0.22, 0.13, 1.0), 28.78, pan=-0.15)
for when, note in [(4.25, 392), (4.62, 494), (5.02, 587)]:
    place_wave(tone([note, note * 2], 0.65, 0.025, 3.0), when, pan=-0.1)
for when, note in [(38.1, 294), (38.55, 370), (39.05, 440), (41.1, 587)]:
    place_wave(tone([note, note * 2], 1.3, 0.023, 2.2), when, pan=0.05)
# Quiet paper/queue cues for the explanatory animation.
for when in (40.55, 42.55, 44.55):
    place_wave(tone([720, 1040], 0.20, 0.035, 7.0), when, pan=0.25)
place_wave(tone([392, 494, 587], 0.80, 0.030, 2.8), 47.65, pan=0.05)


dialogue_starts = {
    "01-groom-opening": 0.72,
    "02-barber-promise": 4.48,
    "03-beard-request": 7.48,
    "04-barber-two-minutes": 10.02,
    "05-groom-sure": 12.05,
    "06-neckline-request": 14.62,
    "07-barber-then-you": 17.36,
    "08-moustache-request": 22.98,
    "09-barber-one-minute": 25.48,
    "10-groom-payoff": 31.92,
    "11-narrator-reveal": 39.18,
}

dialogue_meta = json.loads((AUDIO / "dialogue.json").read_text())
for line_id, start in dialogue_starts.items():
    wave, source_sr = sf.read(AUDIO / "dialogue" / f"{line_id}.wav", dtype="float32")
    if source_sr != SR:
        # ffmpeg performs the high-quality resample and writes a temporary WAV.
        converted = BUILD / f"{line_id}-48k.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(AUDIO / "dialogue" / f"{line_id}.wav"), "-ar", str(SR), "-ac", "1", str(converted)], check=True)
        wave, source_sr = sf.read(converted, dtype="float32")
    place_wave(wave, start, gain=0.92, pan=0)

# Conservative peak normalization before final loudness normalization.
peak = float(np.max(np.abs(mix)))
if peak > 0.92:
    mix *= 0.92 / peak
sf.write(BUILD / "mix-raw.wav", mix, SR)

subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(BUILD / "mix-raw.wav"),
    "-af", "loudnorm=I=-16:TP=-1.2:LRA=7", "-ar", str(SR), "-ac", "2", str(BUILD / "mix.wav")
], check=True)

# Build the static story first, then append the restrained queue animation.
concat = BUILD / "video-concat.txt"
lines = []
static_timeline = timeline[:-1]
static_total = sum(float(item["duration"]) for item in static_timeline)
for item in static_timeline:
    lines.append(f"file '{item['image']}'\n")
    lines.append(f"duration {item['duration']:.3f}\n")
lines.append(f"file '{static_timeline[-1]['image']}'\n")
concat.write_text("".join(lines))

subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
    "-t", f"{static_total:.3f}", "-r", str(FPS),
    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
    "-an", str(BUILD / "story-silent.mp4")
], check=True)

render_reveal_animation(OUT / "reveal-animation.mp4", float(timeline[-1]["duration"]))
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(BUILD / "story-silent.mp4"),
    "-i", str(OUT / "reveal-animation.mp4"),
    "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]",
    "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "17",
    "-pix_fmt", "yuv420p", str(BUILD / "video-silent.mp4")
], check=True)
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", str(BUILD / "video-silent.mp4"),
    "-i", str(BUILD / "mix.wav"), "-t", f"{TOTAL:.3f}", "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart",
    str(OUT / "short.mp4")
], check=True)


def srt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


subtitles = []
for i, (line_id, start) in enumerate(dialogue_starts.items(), 1):
    entry = dialogue_meta[line_id]
    end = start + float(entry["duration"])
    subtitles.append(f"{i}\n{srt_timestamp(start)} --> {srt_timestamp(end)}\n{entry['text']}\n")
(OUT / "subtitles.srt").write_text("\n".join(subtitles))
(ROOT / "storyboard.json").write_text(json.dumps({"duration": TOTAL, "segments": timeline, "dialogue_starts": dialogue_starts}, indent=2) + "\n")

# Thumbnail from the first waiting state; text is deterministic and readable.
thumb = cover_gradient(base["beard-chair"], top_strength=170, bottom_strength=35).convert("RGBA")
td = ImageDraw.Draw(thumb)
td.text((54, 82), "YOU'RE", font=font(112, True), fill=CREAM, stroke_width=3, stroke_fill=INK)
td.text((54, 190), "NEXT.", font=font(112, True), fill=GOLD, stroke_width=3, stroke_fill=INK)
td.text((58, 320), "SOFTWARE IN DISGUISE  ·  03", font=font(28, True), fill=CREAM)
thumb.convert("RGB").save(OUT / "thumbnail.png", quality=95)

# Review aid: the outlined rectangle is the conservative shared text-safe area
# used for both Shorts and Reels. It is not included in the final video.
safe = base["arrival"].convert("RGBA")
safe_overlay = Image.new("RGBA", safe.size, (0, 0, 0, 0))
safe_draw = ImageDraw.Draw(safe_overlay)
safe_draw.rectangle((SAFE_LEFT, SAFE_TOP, SAFE_RIGHT, SAFE_BOTTOM), fill=(80, 230, 130, 36), outline=(80, 230, 130, 255), width=8)
safe_draw.text((SAFE_LEFT + 24, SAFE_TOP + 20), "ESSENTIAL TEXT SAFE AREA", font=font(30, True), fill=(20, 90, 48, 255))
Image.alpha_composite(safe, safe_overlay).convert("RGB").save(OUT / "safe-zone-preview.png", quality=95)

print(json.dumps({"duration": TOTAL, "segments": len(segments), "output": str(OUT / "short.mp4")}, indent=2))
