# Episode 01 — Two people bought the same concert seat

## Status

Published on 2026-09-12. The public URL has not yet been recorded in this repository.

## Creative record

- **Opening:** `SOFTWARE IN DISGUISE`, `EPISODE 01`, `TWO TICKETS. ONE SEAT.`
- **Story:** Two concertgoers discover that both tickets say A12. A flashback shows both buying the last available ticket. The usher's alternative is a tiny stool, prompting: “Does it come with emotional support?”
- **Reveal:** `A RACE CONDITION` — both buyers checked availability before either booking marked the seat sold.
- **Art direction:** Bold black-ink comic, halftone texture, mustard/purple/teal palette, expressive adult characters.
- **Characters:** Man with brown skin, curly black hair, mustard jacket; woman with brown skin, purple-black bob, hoop earrings, purple jacket; usher with black bun, white shirt, and black vest.
- **Audio:** Short synthetic dialogue plus scene-specific cues: tension during the dispute, brighter booking notes, silence for the shocked reaction, uncertain notes under the seat, a comic sting for the stool, and a resolving motif for the reveal.

The initial cut felt like a static slideshow. The published version improved it through tighter 30-second pacing, alternating close-ups and stacked panels, reactions, speaker tails, voices, and music that changes with the story.

## Packaging

- **Recommended/public title:** `Two People Bought the Same Concert Seat`
- **Description lead:** `A funny real-life example of a race condition, explained through a concert ticket disaster.`
- **Description hashtags:** `#SoftwareInDisguise #RaceCondition #Programming`
- **Search tags:** `race condition, race condition explained, race condition example, software engineering, software concepts, programming explained, programming for beginners, computer science, concurrency, double booking, double booked seat, concert tickets, software comedy, programmer humor, tech humor, Software in Disguise, The Unplanned Stack`

## Files

- `deliverables/short.mp4` — final 30-second 1080×1920 video
- `deliverables/thumbnail.png` — vertical Shorts cover
- `assets/page1.png`, `assets/page2.png` — generated four-panel comic pages
- `audio/*.wav` — individual voice lines
- `audio/dialogue.json` — dialogue, voice IDs, and measured durations
- `audio/qa.json` — audio checks
- `audio/SOURCE-LICENSES.md` — voice-model sources and licenses
- `voices.py` — regenerate dialogue using local Kokoro weights
- `render.py` — recreate the final video, music, and sound effects

## Reproduction

Requirements: Python, `kokoro-onnx`, Pillow, NumPy, SoundFile, FFmpeg, and ffprobe.

Place `kokoro.onnx` and `voices.bin` in the repository-level ignored `models/` folder, or set `KOKORO_MODEL_DIR` to their directory. Run `voices.py` only when dialogue changes, then run `render.py` from this episode directory.

The voice sources and official download references are documented in `audio/SOURCE-LICENSES.md`. Large model files are intentionally excluded from Git.

