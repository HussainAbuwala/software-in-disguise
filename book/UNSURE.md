# Hussain's review: entries marked unsure

Hussain went through the draft-3 list (`IDEATION.md`) and marked the entries he's not sure about. Nothing in
`IDEATION.md` or `MOMENTS.md` changes until we go through this list together.

**Buckets**

- **A — weak story:** the software concept is good, but the analogy or story is weak. Look for a better moment.
- **B — dull concept:** the concept itself isn't interesting enough for this book. Consider cutting it.

| # | Entry | Concept | Bucket | Notes |
| --- | --- | --- | --- | --- |
| 1.2 | "It said available when I checked!" | Race condition | A | |
| 1.3 | "I put eggs on the list!" | Lost update | A | |
| 1.4 | "Dinner moved to 8" | Eventual consistency | A | |
| 2.2 | The hallway dance | Livelock | A | |
| 4.1 | "Are they still coming?" | Timeout | A | |
| 4.2 | The good-morning message that didn't come | Heartbeat | A | |
| 4.4 | Three bouquets | Idempotency | A | |
| 4.5 | "Grandma arrives Tuesday at 3." | Data corruption (checksums) | A | |
| 5.1 | "Your name's on the list." | Authentication vs. authorization | A | |
| 5.2 | "Just water the plants." | Least privilege | A | |
| 5.3 | The dog-sitter's key still works | Revoking access | A | |
| 6.1 | "We saved twenty minutes moving in." | Technical debt | A | |
| 6.2 | Same breakfast, fewer steps | Refactoring | A | |
| 7.1 | "Only Jo knows how the printer works." | Single point of failure | A | |
| 7.2 | "Espresso's down. Filter coffee's up." | Graceful degradation | A | |
| 7.3 | "Good thing we took a photo." | Backup and restore | A | |

16 of the 32 entries are marked, all bucket A (labeled 2026-09-26): Hussain is happy with every concept, and the
work is finding better moments for them.

**Main reason: not relatable.** Hussain: relatability is what people will really like. The replacement test is a
moment most readers have lived, ideally with a person, a sensible rule or habit, and a visible way it backfires.

**Rule: no screens in the story** (Hussain, 2026-09-26). If the moment happens in an app, a website, an online order
or a shared digital list, the software is showing and the disguise fails. That was the problem with the eggs list
(1.3), the online flower order (4.4) and the online ticket purchase (1.2). The story has to work entirely offline.

## Decisions

| # | Concept | New moment | Decided |
| --- | --- | --- | --- |
| 1.4 | Eventual consistency | **"Wait, you didn't know?"** Big family news spreads relative by relative. At the family lunch half the table knows and half doesn't, and someone congratulates the one person who hadn't been told yet. By dessert everyone knows. | 2026-09-26 |
| 2.2 | Livelock | **"After you." "No, after you."** At a door, both hold it for the other. Both insist, both step back, both step forward, and nobody goes through. | 2026-09-26 |

Still open:

- **1.2 race condition.** Rejected so far: concert seat, milk bought twice, table booked twice, the same birthday gift,
  salty curry, last seat on the bus, parking spot, two waiters at one table.
- **1.3 lost update.** Rejected so far: eggs list, group food order, headcount, AC dial, rearranged living room.

The two accepted moments (1.4, 2.2) are both about how people talk and behave with each other. Most of the rejected
ones are logistics: objects, orders, purchases.

## Moment list, round 1 (2026-09-26)

A list of 27 everyday moments written with no concepts attached. Hussain ticked the ones that feel like real life;
concepts were mapped afterwards.

**Ticked:** 1 "Mom, where's the…?" · 2 Grandma's dish has no recipe · 5 "Did I already take my tablet?" (pill box) ·
7 extension cord on extension cord · 8 "I'll put it here for now" pile · 9 power cut, candlelit dinner on the gas stove
· 11 old flatmate still has a key · 12 message passed through the little brother · 13 photocopy of a photocopy · 15
"I'm five minutes away" · 20 "No naan today." "Roti then." · 22 passport vs. boarding pass · 26 the wrong queue
(Hussain: immigration lines for different people) · 27 the waiter reads your order back.

**Not ticked:** 3 Grandma's phone diary · 4 Grandpa not on the pickup list · 6 reorganized kitchen · 10 key under the
flowerpot · 14 "ten more minutes, then we order" · 16 friend stops coming to football · 17 neighbour's curtains · 18
nobody booked the hotel · 19 splitting the bill · 21 lift button · 23 old office ID card · 24 valet gets the whole
keyring · 25 only one teacher can work the projector.

**Proposed mapping (awaiting Hussain's OK):**

| # | Concept | Ticked moment(s) | Note |
| --- | --- | --- | --- |
| 7.1 | Single point of failure | 1 "Mom, where's the…?" | Everyone depends on one person |
| 7.3 | Backup | 2 Grandma's dish has no recipe | The only copy is in one head; the fix is a second copy |
| 4.4 | Idempotency | 5 the pill box | Each dose has its own slot, so "take today's tablet" can't happen twice |
| 6.1 | Technical debt | **8 the "for now" pile** ✅ | Chosen over 7 (extension cords), which Hussain didn't like |
| 7.2 | Graceful degradation | **9 power cut, candlelit dinner** ✅ | Side examples: the mic dies mid-speech, the substitute teacher's movie, "no naan, roti then" |
| 5.3 | Revoking access | 11 old flatmate's key | |
| 4.5 | Data corruption + verification | 12 the message via the little brother (problem), 27 the read-back (fix) | 13 photocopy as a sidebar |
| 4.1 | Timeout | **The bus that never comes** ✅ ("ten more minutes, then a rickshaw"; it arrives the moment you get in) | Replaces 15, whose joke is the unreliable estimate, not a deadline; 15 can be a side example |
| 5.1 | Authentication vs. authorization | 22 passport vs. boarding pass | |
| New | Fail fast / early validation | **26 the wrong queue: the government office** ✅ (two hours in line, then "you're missing one document, come back tomorrow") | Candidate new entry |

**No relatable moment yet:** 4.2 heartbeat, 5.2 least privilege, 6.2 refactoring (plus parked 1.2, 1.3).

**Parked (2026-09-26):** 1.2 and 1.3, to revisit later. Hussain: the options feel like the concept forced onto a story
rather than the other way round. Generating stories for a concept is concept-first, which the Core promise warns
against. Next time, start from moments, not concepts. Not marked: 1.1, 1.5, 2.1, 2.3, 2.4, 3.1–3.6, 4.3, 4.6, 5.4, 6.3, 6.4.

## Moment list, round 2 (2026-09-26)

**Ticked:** 29 rewriting messy notes before the exam · 31 the fire drill · 32 "Why?" until "Because I said so" · 35
medicines on top, snacks on the bottom (Hussain: households childproof in different ways) · 36 parents' secret language
· 37 each waiting for the other to apologize first · 42 keep what you use close (Hussain: in Canada, winter clothes go
into storage for the summer) · 43 the wardrobe sorted by type · 45 "Where should we eat?" "Anywhere's fine." · 46
hospital triage · 47 "Twenty-minute wait" because the kitchen can't keep up · 48 sale-day rush · 50 two "main
entrances" (Hussain: malls).

**Not ticked:** 28 school-trip head count · 30 memorized times tables · 33 Dad's Sunday call · 34 the house guest
reorganizing · 38 card to the old address · 39 two aunties and the seating chart · 40 "I'll get it!" collision · 41
three desserts at the potluck · 44 the dog's silence · 49 bakery ticket machine · 51 hotel key card.

**Proposed mapping (awaiting Hussain's OK):**

| For | Concept | Ticked moment | Note |
| --- | --- | --- | --- |
| 6.2 | Refactoring | 29 rewriting messy notes | Same content, easier to use; fills a gap |
| 5.2 | Least privilege | 35 childproofing | Kids reach what they need and nothing else; fills a gap |
| New | Caching (the useful side) | 42 seasonal wardrobe swap | Current season close at hand, the rest in storage, swapped when needs change; pairs with 1.1 |
| New | Security by obscurity vs. real encryption | 36 parents' secret language | Works until the kids learn the language: a secret method isn't a secret key |
| New | Consensus / choosing a leader | 45 "Where should we eat?" | Nobody decides until one person is made the decider |
| New | Priority queue | 46 hospital triage | Pairs with 2.3 (starvation) |
| New | Backpressure | 47 "Twenty-minute wait" | The kitchen slows the front door instead of drowning |
| New | Thundering herd | 48 sale-day rush | Promotes an alternate |
| New | Recursion and its base case | 32 "Why?" / "Because I said so" | Loose: the questions don't get smaller, but "because I said so" is a base case |
| New | Failure drills | 31 the fire drill | Practise recovery before you need it; chapter 7 |
| 2.1 alt | Deadlock | 37 waiting for the other to apologize | A more relatable, social version than the remote |
| ? | Unique IDs, or indexing | 50 two main entrances; 43 wardrobe by type | Needs Hussain's choice |

**Failed two or more rounds:** heartbeat (16, 17, 28, 33, 44 not ticked), race condition (40, 41 not ticked, plus two
earlier rounds), lost update (39 not ticked, plus two earlier rounds). Candidates to leave out of the first book.

**Hussain's feedback on round 2 (2026-09-26):**

- **Decided:** 43 wardrobe sorted by type → **indexing** ✅. 32 "Why?" → recursion: **dropped** (the mapping doesn't
  hold). Heartbeat, race condition and lost update: **left out of the first book** unless a relatable moment turns up.
- **42 caching, corrected by Hussain:** a cache holds a *copy* of the original, but summer and winter clothes are
  different items, so it isn't caching. What it actually shows is **hot and cold storage (tiering)**: move what you use
  now somewhere close, move the rest to cheap, far storage, and swap when needs change. A real software concept
  (archive storage for old photos and files). Awaiting OK.
- **Open questions:** 29 alternatives for refactoring; 36 (obscurity is niche); 46 triage (Hussain agrees that's what
  ERs do); 48 thundering herd and 31 failure drills (explained, awaiting decision); a better deadlock moment; 50 unique
  IDs (not mentioned).

**Decisions (2026-09-26, continued):**

- 42 seasonal wardrobe → **hot and cold storage (tiering)** ✅
- 36 parents' secret language (obscurity) → **skipped**
- 31 fire drill → **failure drills / chaos engineering** ✅
- Deadlock (2.1) → **the narrow lane** ✅ (two cars head-on on a one-lane road, each waiting for the other to reverse).
  Proposed sidebar: "no job without experience, no experience without a job" as a **circular dependency**. It's a loop
  of requirements rather than two people each holding something, so it's a side example, not the main story.
- Still open: 29 refactoring (exam notes explained again), 48 thundering herd (Hussain asked whether it's a real term:
  yes).
- 29 exam notes → **refactoring** ✅ · 48 sale-day rush → **thundering herd** ✅

## Status after the review (2026-09-26)

All 16 unsure entries are resolved: 13 have a new, relatable moment, and 3 (race condition, lost update, heartbeat)
are left out of the first book. New entries from rounds 1–2: fail fast, hot and cold storage, priority queue,
thundering herd, failure drills, indexing (all ✅), plus consensus (45) and backpressure (47), which were ticked but
not discussed. Next: re-sort everything into chapters as draft 4, after Hussain's go-ahead.
- 4.3 collision ("No, you go") → **skipped** (2026-09-26). 5.4 split brain: Hussain unsure about "Mom said no, Dad
  said yes"; looking at other moments.
- 5.4 split brain → **left out of the first book** (2026-09-26). The two-car road trip, the wedding families and the
  shift managers don't feel like life either. Joins race condition, lost update and heartbeat.

**Draft 4 follow-ups (2026-09-26):** 1.5 → **"Clean your room." (acceptance criteria)** ✅, replacing "ambiguous
requirements", which felt abstract; the haircut becomes a side example. 2.3 → **"I'll do it after these quick things."
(starvation, Hussain's busy-day idea)** ✅; the barber and the family dinner become side examples.

**Structure (2026-09-26):** Hussain chose the question chapters over a day-in-the-life structure ("better for
learning"), with sharper questions: nine chapters of 2–5 entries (draft 5 of `IDEATION.md`).
