# Episode ledger

## On-camera format (from October 2026)

| # | Moment | Concept | Status | Link |
| --- | --- | --- | --- | --- |
| | | | | |

## Idea bank

Each idea starts from something on the viewer's own phone. All of them still need a check that the mapping is
accurate (see the Core promise in [`SERIES_GUIDE.md`](SERIES_GUIDE.md)).

| Kind | The moment | What's behind it |
| --- | --- | --- |
| Hidden feature | Gmail's Undo Send: the email never left | A send delay (holding queue) |
| Hidden feature | Instagram shows your post right away, even on bad Wi-Fi | Optimistic UI, then reconciling with the server |
| Hidden feature | "Typing…" appears, then vanishes without a message | Presence and heartbeats |
| Hidden feature | A site says "you've used this password before" | Hashing: it compares fingerprints, not your password |
| Everyday magic | Netflix starts blurry, then turns sharp | Adaptive bitrate streaming |
| Everyday magic | Search suggests the rest of your word as you type | Prefix lookup and debouncing |
| Everyday magic | Two people typing in one Google Doc never clash | Operational transforms / CRDTs |
| Glitch | The like count goes *down* when you refresh | Eventual consistency and caches |
| Glitch | Tapping Pay twice doesn't charge you twice (usually) | Idempotency keys |
| Glitch | Two people book the "last room" | Race condition (check-then-act) |
| Glitch | A group chat shows the reply before the question | Message ordering |
| Glitch | Everything breaks at once right after an outage ends | Retry storm / thundering herd |
| Glitch | The app says "updated" but your friend still sees the old version | Stale cache / TTL |

## Story-era Shorts (retired 2026-10-06)

These were code-drawn and cartoon stories with synthetic voices. They stay live on YouTube. Their sources and
renders were removed from the repo on 2026-10-06; they are in git history at `909a12c`. The analytics lessons are
in `SERIES_GUIDE.md` under "Carry over from the story era".

| Ep | Title | Concept | Link |
| --- | --- | --- | --- |
| 01R | We Both Booked the Last Room | Race condition | [YouTube](https://youtube.com/shorts/OeGX6GOu2dI) |
| 02R | Did I Take It? | Idempotency | [YouTube](https://youtube.com/shorts/uQi0gcv5R54) |
| 03R | Just One Quick Thing | Starvation | [YouTube](https://youtube.com/shorts/o2DTWqOxXnY) |
| 04 | Neither Roommate Would Let Go | Deadlock | [YouTube](https://youtube.com/shorts/ZZZFeXNJyp8) |
| 05 | He Checked This Morning | Stale cache | [YouTube](https://youtube.com/shorts/oroEZpeOLDs) |
| 06 | We're Both on the First Floor | Off-by-one | [YouTube](https://youtube.com/shorts/EVcvuKnatMA) |
| 07 | Anywhere's Fine | Leader election | [YouTube](https://youtube.com/shorts/YgS1JV5h7rY) |
| 08 | You Said You Cleaned | Acceptance criteria | [YouTube](https://youtube.com/shorts/h9lDr2ownpA) |

The original Episodes 1–3 were set to private when their remakes went live. Story-era results: about 1.1–1.3K views
each, 40–63% swiped away, 0.7–1.6% likes, and 0–3 subscribers per episode.
