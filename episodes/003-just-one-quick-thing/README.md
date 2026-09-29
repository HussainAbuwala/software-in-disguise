# Episode 03 (remake) — Just One Quick Thing

Status: published on YouTube Sun 2026-09-27 (https://youtube.com/shorts/o2DTWqOxXnY); Instagram posted by Hussain from
the app.
Title: `Just One Quick Thing | Starvation Explained`. Replaces the published "Just One Quick Trim", which goes private
on YouTube when this one is live.

"Just one quick thing." The sofa, Mom, the laundry. At 11:58 PM the wedding speech is still blank: starvation. Tests
naming the concept in frame 1 ("Software concept: STARVATION, explained with everyday life") and a follow line at the
end.

## Files

- `deliverables/episode-03-just-one-quick-thing-final.mp4`: **upload file**
- `deliverables/thumbnail.png`, `deliverables/subtitles.srt`
- `BRIEF.md`: premise, accuracy check, beat sheet, the two tests, packaging for both platforms
- `render_episode.py` (the story and the in-scene reveal), `voices.py`, `prep_reveal.py`
- `audio/audition/`: the Mom voice audition (Hussain picked mom-E)

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.*
../../.venv/bin/python render_episode.py   # add --stills for one PNG per shot
```
