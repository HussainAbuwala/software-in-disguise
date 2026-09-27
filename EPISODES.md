# Episode ledger

## Published

### Episode 01 — Two people bought the same concert seat

- **Status:** Published
- **Published:** 2026-09-12
- **Public title used/planned:** `Two People Bought the Same Concert Seat`
- **Series cover hook:** `TWO TICKETS. ONE SEAT.`
- **Concept:** Race condition, specifically the check-then-act pattern
- **Plain explanation:** Both buyers checked the seat while it was still available, before either purchase marked it sold.
- **Story:** Two concertgoers arrive with tickets for A12. A flashback shows both seeing the final available ticket and receiving confirmations. An usher offers a tiny stool; one asks whether it comes with emotional support. The ending maps the double booking to a race condition.
- **Format:** 30-second vertical voiced comic with original situational music and sound effects
- **Files:** [`episodes/001-two-people-bought-the-same-concert-seat`](episodes/001-two-people-bought-the-same-concert-seat)
- **Public URL:** Not recorded yet
- **Performance (2026-09-24):** 163 views. Best of the first three; the first frame already showed the conflict.

### Episode 02 — One apology. Three deliveries.

- **Status:** Published
- **Published:** 2026-09-13
- **Public title used:** `He Tried Not to Overdo the Apology`
- **Performance (2026-09-24):** 21 views. The opening showed a calm setup scene with no visible conflict.
- **Concept:** Idempotency / safely retrying the same intended order
- **Story:** An apology promises restraint. Missing confirmations lead the sender to retry twice, creating three flower deliveries.
- **Format:** Vertical illustrated limited animation with synthetic dialogue, audio-driven mouths, reactions, original music and sound effects
- **Files:** [`episodes/002-one-apology-three-deliveries`](episodes/002-one-apology-three-deliveries)

### Episode 03 — Just One Quick Trim

- **Status:** Published
- **Published:** 2026-09-17
- **Public title used:** `Just One Quick Trim | Starvation in Computers Explained`
- **Performance (2026-09-24):** 31 views. Runtime was 50.8 seconds, and nothing went wrong in the opening scene.
- **Series cover hook:** `YOU'RE NEXT.`
- **Concept:** Starvation in scheduling
- **Plain explanation:** Small jobs keep going first, so a bigger one may never finish—like a 20-page report that never prints because every new one-page job jumps ahead.
- **Story:** A groom arrives for a haircut before his wedding. The barber repeatedly serves tiny walk-in jobs first. When the wedding car arrives, the still-uncut groom asks how much it would cost to cut only the front.
- **Format:** Vertical illustrated story with static human scenes, a simple animated printer-queue reveal, synthetic dialogue, situation-specific sound, and original sparse music
- **Files:** [`episodes/003-just-one-quick-trim`](episodes/003-just-one-quick-trim)

## Publishing plan

| Episode | YouTube | Instagram |
| --- | --- | --- |
| 01–03 | Published | Not posted (old format) |
| 04 | Published 2026-09-24 ([link](https://youtube.com/shorts/ZZZFeXNJyp8)) | Scheduled Fri 2026-09-25, 12:00 PM ET (catch-up) |
| 05 | Published Fri 2026-09-25, 9:00 AM ET ([link](https://youtube.com/shorts/oroEZpeOLDs)) | Scheduled Fri 2026-09-25, 4:00 PM ET (catch-up) |
| 06 | Scheduled Fri 2026-09-25, 8:00 PM ET ([link](https://youtube.com/shorts/EVcvuKnatMA)) | Scheduled Fri 2026-09-25, 8:00 PM ET (same time) |

From Episode 6 on, both platforms go live at the same time.

**Titles changed 2026-09-26** to the "human hook | Concept Explained" format for search: Episode 4 `Neither Roommate
Would Let Go | Deadlock Explained`, Episode 5 `He Checked This Morning | Stale Cache Explained`, Episode 6 `We're Both on
the First Floor | Off-by-One Error Explained`. Compare their search-traffic share before and after.


## Retention baseline (read from YouTube Studio; Episodes 4–6 updated 2026-09-26)

| Episode | Views | Stayed to watch | Avg view duration | Where viewers leave |
| --- | --- | --- | --- | --- |
| 01 (old format, 31 s) | 162 | 23.1% | 0:22 (71%) | Holds through the story, then falls from about 65% to 30% over the last ~8 s (the reveal) |
| 02 (old format, 36 s) | 21 | 50.0% (tiny sample) | 0:16 (44%) | Steps down to about 45% within the first ~8 s of setup |
| 03 (old format, 51 s) | 32 | 35.5% | 0:19 (37%) | Falls to about 30% during the slow opening (3–12 s) |
| 04 (29.5 s) | 1,187 | 51.5% | 0:22 (73%) | Sharpest drop at 0:03–0:05 (the silent insert of the remote, as the promise card leaves); then a steady slide through the reveal to ~35% at the end |
| 05 (31 s) | 1,202 | 59.2% | 0:19 (61%) | Drops from ~108% to ~72% during 0:04–0:10 (time cards and a silent flashback); steepest fall at the reveal (0:19–0:23), ending at ~16% |
| 06 (31 s) | 1,123 | 41.7% | 0:26 (84%) | Most swipes of the three in the first seconds, but the story holds (~90% at 0:16, ~83% at 0:20); halves during the reveal (~80% → ~40%) |

Episodes 4–6 were read on 2026-09-26, about 1–2 days after publishing. Retention figures are read off the Studio
chart and are approximate. All three got about 93–96% of their views from the Shorts feed, and their views stopped
growing within about 4–12 hours at roughly 1.1–1.2K each: the feed tested each Short on a first audience and didn't
widen it. Subscribers: +3, +1, +2.

**What Episodes 4–6 show:**

- **The reveal is the main exit.** It's where each of Episodes 4–6 loses the most viewers after the opening, as
  Episode 1 did. Viewers who leave there also miss the loop tail, so there are fewer replays.
- **Silence and inserts early cost viewers.** Episode 5's time cards and wordless flashback (0:04–0:08) and Episode 4's
  silent insert (0:03) are the early drop points. Speech and faces held; cutaways without dialogue didn't.
- **Episode 6: weak hook, strong story.** 58% swiped away (the worst of the three), probably because the wide
  cross-section with two small figures on phones doesn't show the conflict at phone size. Those who stayed watched the
  most of any episode (84%).
- **Loops work.** Episodes 4 and 6 start above 100% retention, so some viewers replay them.
- **Versus the old format:** stayed-to-watch is up from 23% (Episode 1) to 42–59%.

## In development

### Episode 04 — Neither Roommate Would Let Go

- **Status:** Published by Hussain on 2026-09-24 (21 views in its first hour)
- **Concept:** Deadlock (hold-and-wait with a circular wait)
- **Story:** Dev holds the TV remote. Mira holds the only batteries. Neither will hand theirs over first; three hours later, still holding; next morning, asleep holding. Jo turns the TV on with its own button ("It has a button."). The TV shows golf, so the standoff resumes and the Short loops.
- **Format:** First fully code-drawn episode (shared `kit/`); introduces the recurring cast and their voices
- **Files:** [`episodes/004-neither-roommate-would-let-go`](episodes/004-neither-roommate-would-let-go)

### Episode 05 — He Checked This Morning

- **Status:** Scheduled on The Unplanned Stack for 2026-09-25 9:00 AM EDT
- **Public URL:** https://youtube.com/shorts/oroEZpeOLDs
- **Concept:** Stale cache (plus expiry / TTL as the fix)
- **Story:** Dev answers every question from what he saw at 7:02: milk (Jo finished it at 8:15), "Fast asleep" (Jo walks in saying "Morning!"), "Sunny" (thunder). Payoff: "It was sunny at seven." Loop: "Is there coffee?" "Yep. Checked."
- **Format:** Code-drawn (`kit/`); introduces Dev's memory note as a visual device; first episode that isn't about concurrency
- **Files:** [`episodes/005-he-checked-this-morning`](episodes/005-he-checked-this-morning)

### Episode 06 — We're Both on the First Floor

- **Status:** Scheduled on YouTube and Instagram for Fri 2026-09-25, 8:00 PM ET
- **Concept:** Off-by-one error (counting from zero vs. from one)
- **Story:** On the phone at identical window tables, Dev (upstairs, "1") and Mira (entrance level, "G") are each sure they're on the first floor. Each finally gets the other's count, both say "Stay there, I'm coming!", and they swap floors by stairs and elevator, passing in slow motion, still one apart. "Okay. I'm here." "…Where?"
- **Format:** New two-floor café set; first episode with the short (~6 s) reveal and the two-line promise card
- **Files:** [`episodes/006-were-both-on-the-first-floor`](episodes/006-were-both-on-the-first-floor)

### Episode 07 — Anywhere's Fine

- **Status:** Final cut approved by Hussain (29.1 s, his recorded reveal); scheduling next
- **Title:** `Anywhere's Fine | Leader Election Explained`
- **Concept:** Leader election (the usual fix for the consensus problem)
- **Story:** Dev, Mira and Jo, starving on the couch: "Where should we eat?" "Anywhere's fine." Forty minutes later,
  Mira makes Jo the decider: "Thai." They're at the door instantly. Final gag at the restaurant: "So… what should we
  order?" Jo: "I'm not doing this every time."
- **Format:** First episode built on the Episode 4–6 analytics: close-up first frame, speech through the first 10 s, a
  3–4 s reveal inside the scene, and a final gag after the reveal
- **Files:** [`episodes/007-anywheres-fine`](episodes/007-anywheres-fine)

## Concepts not yet used

This is an idea bank, not an approved schedule. Each premise still needs research and creative review. Premises start from a situation people have lived (see the Core promise in `SERIES_GUIDE.md`). The fuller, rated list is in `book/IDEATION.md`. Set each one wherever the situation happens; reusing an existing set is a bonus, not a requirement.

- The roommates' shared grocery list says "milk" twice and "eggs" zero times after both edit it offline — conflict resolution / lost update
- Mira asks Dev and Dev's sister separately for the car; both say yes to different people — split brain
- The apartment Wi-Fi goes down; everyone reconnects at the same instant and it goes down again — retry storm / thundering herd
- Dev and Mira meet in the hallway; both politely step aside, again and again — livelock
- Four cars arrive at a four-way stop at once; everyone yields to the right — circular wait / deadlock (a later sequel to Episode 4)
- A house key copied for a dog-sitter still works a year later — revoking access / permission expiry
- The group chat shows a reply before the question it answers — message ordering / eventual consistency
- A restaurant accepts more reservations than it has tables — overbooking and capacity planning
- The coat-check gives two coats the same ticket number — hash collision
