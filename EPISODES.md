# Episode ledger

## On-camera format (from October 2026)

| # | Moment | Concept | Status | Link |
| --- | --- | --- | --- | --- |
| 001 | WhatsApp's grey and blue ticks | Acknowledgements (store-and-forward) | Brief drafted ([`episodes/001-whatsapp-ticks`](episodes/001-whatsapp-ticks/BRIEF.md)) | |

## Idea bank

Pick things nearly everyone did today. Each idea has to pass four checks:

- **Daily:** nearly everyone did it today.
- **Twist:** the real explanation contradicts what people assume. "Wait, *really*?" is what earns comments and shares.
- **Filmable:** it can be shown on Hussain's own phone.
- **True and short:** the mapping is accurate and fits in under 3 minutes (see the Core promise in
  [`SERIES_GUIDE.md`](SERIES_GUIDE.md)).

### Strongest picks

| Everyday thing | The twist | Concept |
| --- | --- | --- |
| WhatsApp's grey and blue ticks | One tick means the message reached WhatsApp's server, not your friend | Acknowledgements, store-and-forward |
| Authenticator codes | They work in airplane mode: the phone and the website each compute the code from a shared secret and the time | TOTP |
| Gmail's Undo Send | Nothing is unsent; Gmail waits a few seconds before sending | Delay queue |
| Red traffic lines in Google Maps | The red is other people's phones moving slowly on that road | Crowdsourced (anonymized) location data |
| Face ID | Your face never leaves the phone; a mathematical version is kept in a separate chip | On-device biometrics, secure enclave |
| Shazam | It matches a fingerprint of the loudest points in the sound, not the song | Audio fingerprinting, hash lookup |
| Notifications when the app is closed | The app isn't running; one connection from Apple or Google delivers for every app | Push notification services |
| YouTube or Netflix starting blurry, then sharp | The video is stored at several qualities and the player switches between them | Adaptive bitrate streaming |
| The "I'm not a robot" checkbox | The click barely matters; it judges how you got there | Risk analysis, bot detection |
| Searching "dog" in your photos | It finds your dog offline, because the phone recognized the photos itself | On-device image classification |

### Runner-ups

| Everyday thing | What's behind it |
| --- | --- |
| The Uber car jumping around the map | Location updates every few seconds, smoothed in between |
| "Typing…" appears, then vanishes | Presence events that expire |
| The Pay button greys out after one tap; a double tap doesn't charge twice | Idempotency |
| Instagram shows your post before it has uploaded | Optimistic UI |
| A site says "you've used this password before" | Hashing: it compares fingerprints, not passwords |
| Search suggests the rest of your word | Prefix lookup and debouncing |
| Two people typing in one Google Doc never clash | Operational transforms / CRDTs |
| The like count goes *down* when you refresh | Eventual consistency, caches |
| Two people book the "last room" | Race condition |

**Avoid:** "prices go up because you looked". It's tempting, but the popular explanation is mostly a myth and hard to
cover accurately.

### Series shape: "A day in your phone"

Order the first batch the way people use their phones: unlock with Face ID → WhatsApp ticks → Maps traffic on the
commute → Undo Send at work → Shazam at a café → Netflix at night. That gives a playlist, a reason to follow
("tomorrow: …"), and relatability every episode.

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
