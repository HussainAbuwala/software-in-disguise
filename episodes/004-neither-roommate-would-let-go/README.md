# Episode 04 — Neither Roommate Would Let Go

Status: final 29.5-second cut with Hussain's recorded reveal. Ready to publish once the cast voices are approved by
ear.

This is the first episode made entirely without image generation. Every frame is drawn in code by the shared
character kit in [`kit/`](../../kit), so the recurring cast (Dev, Mira, Jo) and their living room look identical in
every episode.

## Files

- `deliverables/episode-04-neither-roommate-would-let-go-final.mp4`: **upload file**
- `deliverables/thumbnail.png`: Shorts cover (`NOBODY LETS GO.`)
- `deliverables/subtitles.srt`: dialogue and reveal subtitles
- `deliverables/reveal-graphic.mp4`: standalone reveal animation (review only)
- `BRIEF.md`: premise, accuracy check, beat sheet, packaging
- `audio/casting.md`: permanent cast voices and why
- `build/contact-sheet.png`: one frame per shot (regenerated each render, not committed)

## Reproduce

```bash
../../.venv/bin/python voices.py          # Kokoro dialogue → audio/dialogue/
../../.venv/bin/python render_episode.py  # frames + sound design + mix → deliverables/
```

The shared machinery (timeline, lip-sync, mixing, rendering) is in `kit/episode.py`, which was extracted from
this episode's original renderer and verified to reproduce it frame- and sample-identically. Requires Pillow, NumPy,
SoundFile and kokoro-onnx in the repo's `.venv`, plus FFmpeg. Set `KOKORO_MODEL_DIR` to a
folder containing `kokoro.onnx` and `voices.bin` (defaults to the Episode 01 model folder). A render takes about
90 seconds.

## Hussain's reveal

The raw voice note is kept in `audio/source/reveal-hussain-raw.m4a`. `prep_reveal.py` cleans it with
`kit/clean_voice.py`, trims it to the spoken words, and writes `audio/reveal-hussain.wav` plus
`audio/reveal-hussain.json`. The JSON holds measured phrase start times, so captions, arrows, pulse and relabel land
on the actual words.

- **Cleanup:** 75 Hz high-pass, FFT denoise learned from the silence before the first word, a soft gate, and a
  15 kHz low-pass. Background noise went from −48 dBFS to about −62 to −65 dBFS in the pauses. Speech level and tone
  are unchanged.
- **Trim:** 1.76–8.75 s of the raw take, cutting a lip click and a breath before "That's".

For a new take, replace the raw file, re-measure the phrase times in `prep_reveal.py`, then run
`prep_reveal.py` and `render_episode.py`.

## Sound design

All sound is synthesized in `render_episode.py`; there are no downloaded samples.

- **Standoff:** Karplus-Strong bass plucks on each cut, like a duel.
- **Time passing:** clock ticks under the first card, fridge hum at night, birdsong in the morning.
- **Sleep:** alternating snores (a low rattle for Dev, a whistle for Mira).
- **Jo's entrance:** footsteps, the button click, a TV power-on, then quiet golf commentary that ducks under dialogue.
- **Punchline:** a surprise stab when they wake. After "It has a button." there is silence, then a slide whistle
  over the blank stare.
- **Reveal:** a soft Cmaj9 pad, with a single pluck when the red highlight laps the deadlock cycle.
- **Loop:** the last pluck leads into the opening pluck when the Short replays.

Final mix is loudness-normalized to about −15 LUFS with −1.5 dBTP peaks.
