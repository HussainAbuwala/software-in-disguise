# Episode 08 — You Said You Cleaned

Status: first full cut (23.1 s) with Hussain's recorded reveal, awaiting review.
YouTube title: `You Said You Cleaned | Acceptance Criteria Explained`.

"You said you cleaned!" "I did!" Everything is under the couch and jammed in the cupboard, until Mira writes down what
"clean" means: acceptance criteria. Tests the Episode 7 lesson: frame 1 is a visible problem plus an accusing line.

## Files

- `deliverables/episode-08-you-said-you-cleaned-final.mp4`: **upload file**
- `deliverables/thumbnail.png`, `deliverables/subtitles.srt`
- `BRIEF.md`: premise, accuracy check, beat sheet, packaging for both platforms
- `render_episode.py` (the story and the in-scene reveal), `voices.py`, `prep_reveal.py`

## Reproduce

```bash
../../.venv/bin/python voices.py
../../.venv/bin/python prep_reveal.py      # cleans and trims audio/source/reveal-hussain-raw.mp4
../../.venv/bin/python render_episode.py
```
