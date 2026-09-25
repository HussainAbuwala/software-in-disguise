# Episode 06 — We're Both on the First Floor

Status: final 30.7-second cut with Hussain's recorded reveal. Scheduled on YouTube
(https://youtube.com/shorts/EVcvuKnatMA) and Instagram for Fri 2026-09-25, 8:00 PM ET.

An off-by-one story in a two-floor café (the new `kit/cafe.py` set). It's the first episode built on the retention
findings: a short reveal (~6 s), a bigger promise card, and motion from the first frame.

## Files

- `deliverables/episode-06-were-both-on-the-first-floor-final.mp4`: **upload file**
- `deliverables/thumbnail.png`, `deliverables/subtitles.srt`
- `BRIEF.md`: premise, accuracy check, beat sheet, packaging for both platforms
- `reveal.py` (run it alone for a contact sheet), `render_episode.py` (the story), `voices.py`

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.m4a
../../.venv/bin/python render_episode.py
```
