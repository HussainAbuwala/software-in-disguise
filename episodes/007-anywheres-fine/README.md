# Episode 07 — Anywhere's Fine

Status: final 29.1-second cut with Hussain's recorded reveal, approved 2026-09-26; scheduling next.
YouTube title: `Anywhere's Fine | Leader Election Explained`.

Three starving friends can't decide where to eat until Mira makes Jo the decider: leader election. The first episode
built on the Episode 4–6 analytics: a close-up first frame, speech and faces through the first 10 s (forty minutes
pass on a wall clock, not a card), a ~3 s reveal inside the scene, and a final gag after the reveal.

## Files

- `deliverables/episode-07-anywheres-fine-final.mp4`: **upload file**
- `deliverables/thumbnail.png`, `deliverables/subtitles.srt`
- `BRIEF.md`: premise, accuracy check, beat sheet, packaging for both platforms
- `render_episode.py` (the story and the in-scene reveal), `voices.py`, `prep_reveal.py`

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.mp4
../../.venv/bin/python render_episode.py
```
