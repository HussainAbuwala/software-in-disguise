# Episode 05 — He Checked This Morning

Status: final 30.8-second cut with Hussain's recorded reveal. Scheduled for 2026-09-25 9:00 AM EDT:
https://youtube.com/shorts/oroEZpeOLDs

A stale-cache story in the Dev/Mira/Jo apartment, drawn entirely in code with the shared [`kit/`](../../kit).
Cast voices are the permanent ones from Episode 04 (see
[`../004-neither-roommate-would-let-go/audio/casting.md`](../004-neither-roommate-would-let-go/audio/casting.md)).

## Files

- `deliverables/episode-05-he-checked-this-morning-final.mp4`: **upload file**
- `deliverables/thumbnail.png`: Shorts cover (`HE CHECKED. AT 7:02.`)
- `deliverables/subtitles.srt`
- `BRIEF.md`: premise, accuracy check, beat sheet, packaging
- `reveal.py`: the cache diagram (`python reveal.py` writes a contact sheet to `build/`)
- `render_episode.py`: the story (shots, sound design, thumbnail). The shared machinery is in `kit/episode.py`.

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.m4a
../../.venv/bin/python render_episode.py
```

Takes about 90 seconds. Requires the repo `.venv` (Pillow, NumPy, SoundFile, kokoro-onnx) and FFmpeg.
