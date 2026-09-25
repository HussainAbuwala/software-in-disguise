# Software in Disguise

**Software in Disguise** is a YouTube Shorts series for **The Unplanned Stack**. Each episode begins as a funny, recognizable everyday story. Only near the end does it reveal the software concept that the audience has just watched play out.

The format is designed for both technical and nontechnical viewers: the story and joke must work without software knowledge, while the ending gives the situation a useful technical name and explanation.

## Current status

| Episode | Story | Software concept | Status |
| --- | --- | --- | --- |
| 01 | Two people buy the same concert seat | Race condition / check-then-act | Published on 2026-09-12 |
| 02 | One apology becomes three flower deliveries | Idempotency | Published on 2026-09-13 |
| 03 | A groom keeps losing his turn at the barbershop | Starvation | Published on 2026-09-17 |
| 04 | Two roommates, one remote, one set of batteries | Deadlock | Final cut ready; not yet published |

From Episode 4 the series follows the September 2026 revision in [`SERIES_GUIDE.md`](SERIES_GUIDE.md):

- The video opens on the conflict, with no title card.
- An on-screen line promises the payoff without naming it.
- Runtime is 20–30 seconds, and the ending loops back to the opening.
- Hussain records the reveal.
- A recurring cast (Dev, Mira, Jo) replaces a new set of characters each episode.
- Art is drawn in code by the shared character kit in `kit/`; no image generation.

## Start here next time

1. Read [`SERIES_GUIDE.md`](SERIES_GUIDE.md) before developing an idea.
2. Check [`EPISODES.md`](EPISODES.md) to avoid repeating a completed concept.
3. Copy [`templates/episode-brief.md`](templates/episode-brief.md) for the new episode.
4. Use GPT-6 Astra for the premise, technical mapping, comedy, script, pacing, and final creative judgment.
5. Delegate production implementation and routine revisions to GPT-5.6 Sol once the creative brief is stable.
6. Preserve the everyday hook until the closing software reveal, but promise in the first seconds that the reveal is coming.

## Repository layout

```text
kit/            Code-drawn character kit: cast, living room set, camera (Episode 4 onward)
episodes/       Completed episode records, sources, and deliverables
templates/      Briefs to copy when starting an episode
SERIES_GUIDE.md Creative rules and production workflow
EPISODES.md     Canonical episode ledger and future idea guardrails
```
