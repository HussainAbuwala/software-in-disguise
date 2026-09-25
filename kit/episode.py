"""The episode framework: timeline, lip-sync, dialogue mixing, rendering and deliverables.

An episode subclasses `Episode` and supplies four things: `build_shots()` (the timeline), `sound_design(mix)`,
`thumbnail(path)`, and a `reveal_frame(t)` for the R1 reveal shot. Shots are plain functions `draw(ctx) -> Image`.
Everything else is shared, so a new episode's file contains only its story.
"""

from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import soundfile as sf
from PIL import Image

from . import cast
from . import living_room as room
from .canvas import INK, SCREEN, W, H, Camera, Canvas, finish, lerp, new_frame
from .cast import DEV, JO, MIRA, Look, Pose
from .overlays import bubble, mouth_point, promise
from .sound import SR, Mix, band, level, load_wav

FPS = 30
LOOKS = {"DEV": DEV, "MIRA": MIRA, "JO": JO}
SEEDS = {"DEV": 1, "MIRA": 3, "JO": 4}

# Seat bottom (world y 1380) sits just above the bottom 20% reserved for the Shorts UI.
TWO_SHOT = Camera(1.42, 598, 1080, 540, 1090)
WIDE = Camera(0.86, 335, 1150, 540, 1250)


def cam_lerp(a: Camera, b: Camera, k: float) -> Camera:
    return Camera(lerp(a.zoom, b.zoom, k), lerp(a.fx, b.fx, k), lerp(a.fy, b.fy, k), lerp(a.sx, b.sx, k), lerp(a.sy, b.sy, k))


@dataclass
class Line:
    key: str
    offset: float
    bubble: tuple | None = None  # (x, y, w) on screen; None = no bubble (e.g. TV audio)
    gain: float = 1.0
    speaker: str = ""
    text: str = ""
    start: float = 0.0
    audio: np.ndarray | None = None


@dataclass
class Shot:
    name: str
    dur: float
    draw: Callable
    lines: list[Line] = field(default_factory=list)
    start: float = 0.0


class Ctx:
    """What a shot's draw function needs for one frame."""

    def __init__(self, ep: "Episode", shot: Shot, t: float):
        self.ep, self.shot, self.t = ep, shot, t
        self.g = shot.start + t

    @property
    def k(self) -> float:
        """Progress through the shot, 0..1."""
        return self.t / max(self.shot.dur, 0.01)

    def mouth(self, who: str) -> float:
        env_ = self.ep.mouths.get(who)
        if env_ is None:
            return 0.0
        i = min(len(env_) - 1, int(self.g * FPS))
        return float(env_[i])

    def blink(self, who: str) -> bool:
        return cast.blinking(self.g, SEEDS[who])

    def breathe(self, period=3.2, amp=3.0, phase=0.0) -> float:
        return math.sin(2 * math.pi * (self.g / period + phase)) * amp

    def seated(self, who: str, facing: int, expr: str, **kw) -> Pose:
        x, y = room.DEV_SEAT if who == "DEV" else room.MIRA_SEAT
        pose = Pose(x, y, facing, expr, mouth=self.mouth(who), blink=self.blink(who), **kw)
        pose.extras.setdefault("breathe", self.breathe(phase=SEEDS[who] * 0.3))
        return pose

    def standing(self, who: str, x: float, feet: float, facing: int, expr: str, **kw) -> Pose:
        return Pose(x, feet, facing, expr, mouth=self.mouth(who), blink=self.blink(who), standing=True, **kw)

    def bubbles(self, c: Canvas, cam: Camera, poses: dict):
        started = [l for l in self.shot.lines if l.bubble and self.t >= l.offset]
        for line in started:
            if any(o.speaker == line.speaker and o.offset > line.offset for o in started):
                continue  # a newer line from the same speaker replaces this bubble
            x, y, w = line.bubble
            pose = poses.get(line.speaker)
            target = mouth_point(cam, pose) if pose else (x + w * 0.35 + 200, y + 600)
            bubble(c, line.speaker, line.text, x, y, w, target)


Cast = list[tuple[Look, Pose]]


def scene(ctx: Ctx, cam: Camera, *, time: str = "day", seated: Cast = (), standing: Cast = (), behind: Cast = (),
          sleepers: tuple[Pose, ...] = (), overlay: Callable | None = None, set=room, **room_kw) -> Image.Image:
    """A set (the living room by default) with characters. Draw order: set back, `behind` (e.g. behind the couch
    back), `seated`, set front (couch front / tables), `standing`, sleeping Z's, bubbles, `overlay(screen_canvas)`,
    promise line. A set module provides wall_color(time), back(c, time, t=, behind=, **kw) and front(c, **kw)."""
    img = new_frame(set.wall_color(time))
    c = Canvas(img, cam)
    draw_behind = (lambda cv: [cast.draw(cv, look, pose) for look, pose in behind]) if behind else None
    set.back(c, time, t=ctx.g, behind=draw_behind, **room_kw)
    for look, pose in seated:
        cast.draw(c, look, pose)
    set.front(c, **room_kw)
    for look, pose in standing:
        cast.draw(c, look, pose)
    for i, pose in enumerate(sleepers):
        dx, dy = (60, -230) if pose.facing > 0 else (-20, -240)
        cast.zzz(c, pose.x + dx, pose.y + dy, ctx.g, 0.5 * i, set.wall_color(time))
    screen = Canvas(img, SCREEN)
    poses = {look.name.upper(): pose for look, pose in (*behind, *seated, *standing)}
    ctx.bubbles(screen, cam, poses)
    if overlay:
        overlay(screen)
    if ctx.g < ctx.ep.promise_until:
        promise(screen, ctx.ep.promise_size)
    return img


class Episode:
    here: Path  # the episode folder
    final_name: str  # upload file name
    reveal_chunks = ["reveal-1", "reveal-2", "reveal-3", "reveal-4"]
    promise_until = 3.0
    promise_size = 44

    def __init__(self):
        self.dialogue_dir = self.here / "audio" / "dialogue"
        self.build = self.here / "build"
        self.deliverables = self.here / "deliverables"
        self.build.mkdir(exist_ok=True)
        self.deliverables.mkdir(exist_ok=True)
        self.meta = json.loads((self.here / "audio" / "dialogue.json").read_text())["lines"]
        self.hussain = next((p for ext in ("wav", "m4a", "mp3", "aiff")
                             if (p := self.here / "audio" / f"reveal-hussain.{ext}").exists()), None)
        self.build_reveal_audio()
        self.shots = self.build_shots()
        t = 0.0
        for shot in self.shots:
            shot.start = t
            for line in shot.lines:
                line.start = t + line.offset
            t += shot.dur
        self.duration = t
        self.mouths = self.build_mouths()

    # --- to implement per episode ----------------------------------------------------------------------------
    def build_shots(self) -> list[Shot]:
        raise NotImplementedError

    def sound_design(self, mix: Mix):
        raise NotImplementedError

    def thumbnail(self, path: Path):
        raise NotImplementedError

    def reveal_frame(self, t: float) -> Image.Image:
        raise NotImplementedError

    # --- helpers for build_shots -----------------------------------------------------------------------------
    def line(self, key, offset, bubble=None, gain=1.0) -> Line:
        m = self.meta[key]
        return Line(key, offset, bubble, gain, m["speaker"], m["text"], audio=level(load_wav(self.dialogue_dir / f"{key}.wav")))

    def dur(self, key) -> float:
        return self.meta[key]["duration"]

    def shot(self, prefix: str) -> Shot:
        return next(s for s in self.shots if s.name.startswith(prefix))

    def reveal_shot(self) -> Shot:
        return Shot("R1 reveal", self.reveal_dur, lambda ctx: ctx.ep.reveal_frame(ctx.t), self.reveal_lines)

    def build_reveal_audio(self):
        chunks = self.reveal_chunks
        gap, lead = 0.2, 0.1
        starts, t = [], lead
        for key in chunks:
            starts.append(t)
            t += self.dur(key) + gap
        stand_in_len = t - gap - lead
        texts = [self.meta[k]["text"] for k in chunks]
        timings = self.here / "audio" / "reveal-hussain.json"
        if self.hussain and timings.exists():
            # Prepared by prep_reveal.py: already denoised and trimmed, with measured phrase starts.
            audio = level(load_wav(self.hussain))
            captions = json.loads(timings.read_text())["captions"]
            self.reveal_lines = [Line("reveal-hussain", lead, speaker="HUSSAIN", text=" ".join(texts), audio=audio)]
            self.reveal_captions = [(lead + t, txt) for t, txt in captions]
            self.reveal_dur = lead + len(audio) / SR + 0.5
        elif self.hussain:
            # Unprepared recording: trim silence and spread the captions proportionally.
            wav = self.build / "reveal-hussain-48k.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(self.hussain), "-ac", "1", "-ar", str(SR),
                            "-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                                   "silenceremove=start_periods=1:start_threshold=-45dB,areverse", str(wav)], check=True)
            audio = level(load_wav(wav))
            scale = (len(audio) / SR) / stand_in_len
            self.reveal_lines = [Line("reveal-hussain", lead, speaker="HUSSAIN", text=" ".join(texts), audio=audio)]
            self.reveal_captions = [(lead + (s - lead) * scale, txt) for s, txt in zip(starts, texts)]
            self.reveal_dur = lead + len(audio) / SR + 0.5
        else:
            self.reveal_lines = [self.line(k, s) for k, s in zip(chunks, starts)]
            self.reveal_captions = list(zip(starts, texts))
            self.reveal_dur = t - gap + 0.5

    # --- shared machinery ------------------------------------------------------------------------------------
    def dialogue_lines(self):
        for shot in self.shots:
            for line in shot.lines:
                yield shot, line

    def build_mouths(self) -> dict:
        n = int(self.duration * FPS) + 2
        mouths = {}
        for _, line in self.dialogue_lines():
            if line.speaker not in LOOKS:
                continue
            arr = mouths.setdefault(line.speaker, np.zeros(n))
            a = line.audio
            win = SR // FPS
            rms = np.array([np.sqrt(np.mean(a[i:i + win] ** 2)) for i in range(0, len(a), win)])
            rms = rms / (rms.max() + 1e-9)
            vals = np.clip((rms - 0.12) / 0.55, 0, 1)
            i0 = int(line.start * FPS)
            for k, v in enumerate(vals):
                if i0 + k < n:
                    arr[i0 + k] = max(arr[i0 + k], v)
        for arr in mouths.values():  # light smoothing so the jaw doesn't flicker
            arr[1:] = np.maximum(arr[1:], arr[:-1] * 0.5)
        return mouths

    def mix(self) -> np.ndarray:
        mix = Mix(self.duration)
        for shot, line in self.dialogue_lines():
            wave = line.audio
            if line.speaker == "TV":
                wave = band(wave, 350, 3200)  # small TV speaker
            mix.add(wave, line.start, 0.9 * line.gain, dialogue=line.speaker != "TV")
        self.sound_design(mix)
        return mix.render()

    def write_subtitles(self, path: Path):
        entries = []
        for shot, line in self.dialogue_lines():
            if line.speaker in LOOKS:
                entries.append((line.start, line.start + len(line.audio) / SR + 0.2, f"{line.speaker}: {line.text}"))
        r1 = self.shot("R1")
        caps = self.reveal_captions
        for i, (start, text) in enumerate(caps):
            end = caps[i + 1][0] if i + 1 < len(caps) else r1.dur - 0.3
            entries.append((r1.start + start, r1.start + end, text))
        entries.sort()
        # Lines spoken together (starting within 0.6 s) share one two-line subtitle; otherwise a subtitle never runs
        # into the next one.
        merged = []
        for a, b, t in entries:
            if merged and a - merged[-1][0] < 0.6:
                pa, pb, pt = merged[-1]
                merged[-1] = (pa, max(pb, b), f"{pt}\n{t}")
            else:
                merged.append((a, b, t))
        entries = [(a, min(b, merged[i + 1][0]) if i + 1 < len(merged) else b, t) for i, (a, b, t) in enumerate(merged)]
        path.write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(entries)))

    def render(self):
        print(f"duration {self.duration:.2f}s  ({'Hussain recording' if self.hussain else 'stand-in narrator'})")
        for s in self.shots:
            print(f"  {s.start:6.2f}  {s.dur:4.2f}  {s.name}")

        audio = self.mix()
        sf.write(self.build / "mix.wav", np.stack([audio, audio], axis=1), SR)

        silent = self.build / "video-silent.mp4"
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                               "-preset", "medium", str(silent)], stdin=subprocess.PIPE)
        samples = []
        si = 0
        for n in range(round(self.duration * FPS)):
            g = n / FPS
            while si + 1 < len(self.shots) and g >= self.shots[si + 1].start:
                si += 1
            shot = self.shots[si]
            frame = shot.draw(Ctx(self, shot, g - shot.start))
            if frame.size != (W, H):
                frame = finish(frame)
            ff.stdin.write(frame.tobytes())
            if not samples or samples[-1][0] != shot.name:
                samples.append([shot.name, None, shot.start + shot.dur * 0.7])
            if samples[-1][1] is None and g >= samples[-1][2]:
                samples[-1][1] = frame
        ff.stdin.close()
        ff.wait()

        final = self.deliverables / self.final_name
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(self.build / "mix.wav"),
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", str(final)], check=True)

        cols, tw, th = 5, W // 5, H // 5
        frames = [f for _, f, _ in samples if f is not None]
        sheet = Image.new("RGB", (cols * tw, math.ceil(len(frames) / cols) * th), INK)
        for i, f in enumerate(frames):
            sheet.paste(f.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        sheet.save(self.build / "contact-sheet.png")
        self.write_subtitles(self.deliverables / "subtitles.srt")
        self.thumbnail(self.deliverables / "thumbnail.png")
        print(final)


def srt_time(t: float) -> str:
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
