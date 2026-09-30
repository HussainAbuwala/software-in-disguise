# Episode 02 (remake) — the pill box

Status: published on YouTube 2026-09-29 (https://youtube.com/shorts/uQi0gcv5R54); Instagram from the app. Replaces the
published "He Tried Not to Overdo the Apology" (21 views, old format) when it goes live.
Concept: idempotency (book moment 9.5, with Mom instead of Grandpa). Details and tests in `BRIEF.md`.

## Files

- `deliverables/episode-02-the-pill-box-final.mp4`: **upload file**
- `deliverables/thumbnail.png`, `deliverables/subtitles.srt`
- `deliverables/style-test-*.mp4`, `side-by-side.mp4`: the look test (current kit vs comic page; current won)
- `deliverables/hook-v2.mp4`: the first 16 s with the new hook, before the ending was written
- `render_episode.py` (the story), `voices.py`, `prep_reveal.py`

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.mp4
../../.venv/bin/python render_episode.py   # add --stills for a contact sheet
```
