# Software in Disguise

**Software in Disguise** is a YouTube Shorts series for **The Unplanned Stack**. Each episode begins as a funny, recognizable everyday story. Only near the end does it reveal the software concept that the audience has just watched play out.

The format is designed for both technical and nontechnical viewers: the story and joke must work without software knowledge, while the ending gives the situation a useful technical name and explanation.

## Current status

| Episode | Story | Software concept | Status |
| --- | --- | --- | --- |
| 01 | Two people buy the same concert seat | Race condition / check-then-act | Published on 2026-09-12 |
| 02 | One apology becomes three flower deliveries | Idempotency | Produced for review; not published |

Episode 1 and its source material are archived under [`episodes/001-two-people-bought-the-same-concert-seat`](episodes/001-two-people-bought-the-same-concert-seat).

## Start here next time

1. Read [`SERIES_GUIDE.md`](SERIES_GUIDE.md) before developing an idea.
2. Check [`EPISODES.md`](EPISODES.md) to avoid repeating a completed concept.
3. Copy [`templates/episode-brief.md`](templates/episode-brief.md) for the new episode.
4. Use GPT-6 Astra for the premise, technical mapping, comedy, script, pacing, and final creative judgment.
5. Delegate production implementation and routine revisions to GPT-5.6 Sol once the creative brief is stable.
6. Preserve the everyday hook until the closing software reveal.

## Repository layout

```text
episodes/       Completed episode records, sources, and deliverables
templates/      Briefs to copy when starting an episode
SERIES_GUIDE.md Creative rules and production workflow
EPISODES.md     Canonical episode ledger and future idea guardrails
```

