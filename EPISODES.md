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

## Produced for review

### Episode 02 — One apology. Three deliveries.

- **Status:** Full 35.4-second voiced cut produced for review; not published
- **Working title:** `He Tried Not to Overdo the Apology`
- **Concept:** Idempotency / safely retrying the same intended order
- **Story:** An apology promises restraint. Missing confirmations lead the sender to retry twice, creating three flower deliveries.
- **Format:** Vertical illustrated limited animation with synthetic dialogue, audio-driven mouths, reactions, original music and sound effects
- **Files:** [`episodes/002-one-apology-three-deliveries`](episodes/002-one-apology-three-deliveries)

### Episode 03 — Just One Quick Trim

- **Status:** Final 50.8-second voiced cut and YouTube metadata rendered; not published
- **Working title:** `Just One Quick Trim`
- **Series cover hook:** `YOU'RE NEXT.`
- **Concept:** Starvation in scheduling
- **Plain explanation:** Small jobs keep going first, so a bigger one may never finish—like a 20-page report that never prints because every new one-page job jumps ahead.
- **Story:** A groom arrives for a haircut before his wedding. The barber repeatedly serves tiny walk-in jobs first. When the wedding car arrives, the still-uncut groom asks how much it would cost to cut only the front.
- **Format:** Vertical illustrated story with static human scenes, a simple animated printer-queue reveal, synthetic dialogue, situation-specific sound, and original sparse music
- **Files:** [`episodes/003-just-one-quick-trim`](episodes/003-just-one-quick-trim)

## Concepts not yet used

This is an idea bank, not an approved schedule. Each premise still needs research and creative review.

- A busy café reuses a recently prepared order — caching
- A bakery serves customers in arrival order — queue / FIFO
- A building key opens only certain rooms — authorization and permissions
- A group passes a message through unreliable friends — networking and retries
- A restaurant accepts more reservations than tables — overbooking and capacity planning
- Several people edit the same shared list — conflict resolution / optimistic concurrency
- A coat-check ticket retrieves the right coat — keys and lookup tables
- A household keeps duplicate emergency supplies — redundancy and fault tolerance
