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

## In development

### Episode 04 — Neither Roommate Would Let Go

- **Status:** Final 29.5 s cut rendered with Hussain's recorded reveal; waiting on voice approval, then publish
- **Concept:** Deadlock (hold-and-wait with a circular wait)
- **Story:** Dev holds the TV remote. Mira holds the only batteries. Neither will hand theirs over first; three hours later, still holding; next morning, asleep holding. Jo turns the TV on with its own button ("It has a button."). The TV shows golf, so the standoff resumes and the Short loops.
- **Format:** First fully code-drawn episode (shared `kit/`); introduces the recurring cast and their voices
- **Files:** [`episodes/004-neither-roommate-would-let-go`](episodes/004-neither-roommate-would-let-go)

## Concepts not yet used

This is an idea bank, not an approved schedule. Each premise still needs research and creative review. Every premise is written as a failure, because a mechanism working correctly has no conflict. Where possible, set it in the Dev and Mira apartment.

- The roommates' shared grocery list says "milk" twice and "eggs" zero times after both edit it offline — conflict resolution / lost update
- Dev keeps serving guests the snack list from last week's party; the snacks have changed — stale cache
- Mira asks Dev and Dev's sister separately for the car; both say yes to different people — split brain
- The apartment Wi-Fi goes down; everyone reconnects at the same instant and it goes down again — retry storm / thundering herd
- "Meet on the first floor" in a building where the ground floor is zero — off-by-one
- Dev and Mira meet in the hallway; both politely step aside, again and again — livelock
- Four cars arrive at a four-way stop at once; everyone yields to the right — circular wait / deadlock (a later sequel to Episode 4)
- A house key copied for a dog-sitter still works a year later — revoking access / permission expiry
- The group chat shows a reply before the question it answers — message ordering / eventual consistency
- A restaurant accepts more reservations than it has tables — overbooking and capacity planning
- The coat-check gives two coats the same ticket number — hash collision
