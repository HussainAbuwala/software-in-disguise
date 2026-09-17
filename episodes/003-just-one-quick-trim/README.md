# Episode 03 — Just One Quick Trim

Status: final 50.8-second cut and YouTube package complete. Unpublished. The human story uses static images; the technical reveal animates only queue cards.

## Review files

- `deliverables/episode-03-just-one-quick-trim-final.mp4` — final upload file
- `deliverables/payoff-preview.mp4` — punchline and reaction excerpt
- `deliverables/reveal-animation.mp4` — standalone printer-queue explanation
- `deliverables/thumbnail.png` — final YouTube cover
- `deliverables/safe-zone-preview.png` — conservative shared Shorts/Reels text boundary
- `deliverables/subtitles.srt` — dialogue subtitles
- `audio/auditions/comparison-reel.wav` — all voice candidates and chemistry scenes
- `audio/auditions/chemistry-P1-restrained.wav` — pairing used in the cut
- `audio/auditions/chemistry-P2-warmer.wav` — alternate pairing
- `audio/casting.md` — neutral IDs, source voices, rationale, and approval status
- `REVIEW.md` — production and technical review
- `LEARNINGS.md` — reusable creative and production lessons

## Premise

A groom arrives for a haircut before his wedding. A friendly barber repeatedly serves supposedly tiny jobs first. After three interruptions and a message that the wedding car is waiting, the groom offers his own quick request: “What if you just cut the front? That's quick.”

The closing reveal uses an imagined printer queue: a 20-page report never prints because new one-page jobs repeatedly jump ahead. A final fair-rule state gives the report its turn. This makes the impact visible while keeping the technical explanation brief. The example is explicitly hypothetical; it does not claim that ordinary printers always prioritize one-page jobs.

## Format

The human story uses static original illustrations and hard cuts. The final explanation adds a simple code-drawn animation of queue cards changing order. Text, phone UI, clock labels, captions, and reveal graphics are deterministic overlays. Sound carries activity between stills: shop ambience, entrance bell, clippers, a phone vibration, dialogue, paper cues, and sparse original musical tones.

## Reproduction

Requirements: Python with Pillow, NumPy, SoundFile and `kokoro-onnx`; FFmpeg and ffprobe. Set `KOKORO_MODEL_DIR` to a folder containing `kokoro.onnx` and `voices.bin`.

1. Run `voices.py` to regenerate candidates and final dialogue.
2. Run `render_episode.py` to build overlays, synthesize the original soundscape, animate the printer queue, mix audio, write subtitles, and create the thumbnail.

Voice model weights are not committed. Generated image prompts and output provenance are recorded in `art/prompts.json`.
