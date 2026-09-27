# Software in Disguise — Book ideation (draft 5, 2026-09-26)

Draft 5 comes out of Hussain's review of draft 3 (`UNSURE.md`). Sixteen entries he was unsure about were reworked by
starting from everyday moments he recognized, not from concepts: 13 got new moments, 8 new concepts came in, and 7
concepts are left out of the first book. Draft 5 also swaps two entries ("Clean your room", the busy day) and splits
the book into nine sharper question chapters. Every entry is explained in [`MOMENTS.md`](MOMENTS.md).

## The idea

> *You've already lived it. Programmers just have a name for it.*

Everyday situations often behave the way software does. Readers recognize a moment from their own lives, and they
learn a piece of software vocabulary without feeling taught. Recognition comes first and humor is a bonus. The full
version is the Core promise in `SERIES_GUIDE.md`.

## How entries are chosen (learned in the review)

1. **Moments first.** Write lists of everyday moments with no software attached. Hussain ticks the ones that feel like
   real life, and only then are concepts mapped onto them. Stories written to fit a concept felt forced every time.
2. **Relatable beats accurate-but-invented.** If no real moment fits a concept after two rounds, the concept waits.
3. **No screens in the story.** If the moment happens in an app, a website, an online order or a digital list, the
   software is showing and the disguise fails. Phones can be props; the behavior must happen offline.
4. **Social moments work best.** How people behave with each other (news spreading at lunch, "After you" at a door)
   landed far better than logistics (orders, purchases, seats, parking).

## Reader and promise

- **Primary reader:** curious adults who don't code and enjoy illustrated nonfiction.
- **Likely buyer:** someone in tech buying for a partner, parent or friend.
- **Welcome but secondary:** PMs, designers and new developers (an index and a comparison page per chapter).
- **Positioning to test:** *An illustrated collection of everyday mix-ups, clever shortcuts and familiar frustrations
  that reveal how software behaves. No coding required.*
- **Emotional promise:** *You'll start noticing these patterns everywhere.*
- **Title:** *Software in Disguise*. Subtitle to test: *Everyday life, explained through software comics*, with *You've
  already lived it. Programmers just have a name for it.* on the cover or back.

## Chapters: nine specific questions

Each chapter is a question a reader might ask. Underneath, each is a real area of software, which is how textbooks
group ideas: related concepts sit side by side, so a chapter-end page can compare them. Hussain chose this over a
day-in-the-life structure because it's better for learning. The software area column can become an index or map at
the back of the book.

| # | Chapter | The question underneath | Software area | Entries | Chapter-end comparison |
| --- | --- | --- | --- | --- | --- |
| 1 | **"Is that still true?"** | Why is my information out of date? | Caching and consistency | 2 | Old copy vs. not-yet-arrived news |
| 2 | **"That's not what I meant!"** | Why do we understand the same thing differently? | Communication and specifications | 3 | Counted differently, defined differently, changed in transit |
| 3 | **"Why is nobody moving?"** | Why does everyone get stuck? | Concurrency and coordination | 5 | Frozen, busy, deferring, abandoned, or waiting too long |
| 4 | **"When is it my turn?"** | Who decides who goes next? | Scheduling | 3 | Quickest first, most urgent first, everyone limited |
| 5 | **"Why is this line so long?"** | Why do crowds and queues jam? | Queues, traffic and scaling | 5 | Which fix for which kind of queue |
| 6 | **"How do we save time?"** | Which shortcuts help, and at what cost? | Performance | 5 | Each shortcut and the price it pays |
| 7 | **"Who's allowed in?"** | Who may do what? | Security and access | 3 | Who you are, how much, for how long |
| 8 | **"Can we change it without breaking it?"** | How do people change things safely? | Software maintenance | 4 | Debt, refactoring, regression, rehearsal |
| 9 | **"What if something goes wrong?"** | How do we recover, or make mistakes harmless? | Reliability | 5 | Depend, degrade, restore, practise, repeat safely |

**35 entries**, 2–5 per chapter. If a two-entry chapter feels thin, chapters 1 and 2 can merge back into one.
**★** marks strong candidates for a Short: a problem visible from the first frame, faces and speech throughout, and a
short reveal.

## The contents (moment → concept)

### 1. "Is that still true?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 1.1 | "I checked this morning." | Stale cache | Reusing an answer from earlier instead of looking again; convenient until the world changes | ✅ Ep 5 |
| 1.2 | "Wait, you didn't know?" | Eventual consistency | Family news reaches each relative at a different time; by dessert, everyone knows | ★ |

### 2. "That's not what I meant!"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 2.1 | "We're both on the first floor." | Off-by-one | One counts floors from 0, the other from 1, so they're exactly one apart | ✅ Ep 6 |
| 2.2 | "Clean your room." | Acceptance criteria | "Done!" means everything under the bed; a checklist of what "clean" means settles it | ★ |
| 2.3 | The message via your little brother, and the waiter's read-back | Data corruption and checking | Messages change as they're passed along; reading it back catches the change before it matters | ★ |

Side example for 2.2: "Just a little shorter" at the hairdresser, fixed by bringing a photo.

### 3. "Why is nobody moving?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 3.1 | The narrow lane | Deadlock | Two cars head-on on a one-lane road; each holds its half and waits for the other to reverse | ★ |
| 3.2 | "After you." "No, after you." | Livelock | Both keep politely yielding, in sync, so nobody goes through the door | ★ |
| 3.3 | "Where should we eat?" "Anywhere's fine." | Consensus and choosing a leader | Everyone defers, so nobody decides until one person is made the decider | ★ |
| 3.4 | The jacket saving a seat | Lock without a lease | A claim whose owner has vanished never expires | |
| 3.5 | The bus that never comes | Timeout | "Ten more minutes, then a rickshaw": a deadline, then a fallback. The bus arrives as you leave | ★ |

Sidebar for 3.1: "No job without experience, no experience without a job" (circular dependency).
Side example for 3.5: "I'm five minutes away" (why you can't trust the estimate).
3.2 and 3.3 make a natural pair: at the door everyone yields, at dinner everyone defers.

### 4. "When is it my turn?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 4.1 | "I'll do it after these quick things." | Starvation | Every quick task goes first, so the big one (the wedding speech) never gets its turn | ★ |
| 4.2 | ER triage | Priority queue | Whoever is worse off goes first, not whoever arrived first | ★ |
| 4.3 | "One 'are we there yet?' every 10 minutes" | Rate limiting | A cap on how often one person can ask protects the parent's attention | ★ |

Side examples for 4.1: the barber and the quick walk-ins (Episode 3), and trying to get a word in at family dinner.

### 5. "Why is this line so long?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 5.1 | "This till's open!" | Load balancing | Someone sends each new arrival to whichever till is free | |
| 5.2 | Four cooks, one oven | Bottleneck | One shared stage limits the whole meal; more helpers don't help | |
| 5.3 | "Twenty-minute wait" (with empty tables) | Backpressure | The overwhelmed kitchen slows the front door instead of drowning | |
| 5.4 | Sale-day rush | Thundering herd | Everyone waiting for the same moment arrives at once and overwhelms the shop | |
| 5.5 | The government office | Fail fast | Two hours in line to hear "you're missing one document"; check at the door instead | ★ |

### 6. "How do we save time?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 6.1 | "I need that shirt tomorrow." | Batching | Waiting for a full load saves washes, but the first shirt waits for the rest | |
| 6.2 | "Your usual?" | Prefetching | Made before you ask saves time, and it's wasted when the guess is wrong | |
| 6.3 | "We'll buzz you when it's ready." | Asynchronous work | Order now, sit down, get buzzed later; nobody stands at the counter | |
| 6.4 | Winter clothes into storage for the summer | Hot and cold storage | Keep what you use now close, store the rest cheaply, swap when the season changes | |
| 6.5 | The wardrobe sorted by type | Indexing | Organized so you go straight to what you need, at the cost of putting things back in the right place | |

### 7. "Who's allowed in?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 7.1 | Passport and boarding pass | Authentication vs. authorization | The passport proves who you are; the boarding pass says which plane and seat | |
| 7.2 | Childproofing | Least privilege | Kids can reach what they need and nothing else | |
| 7.3 | The old flatmate still has a key | Revoking access | Access stays valid until someone takes it back | |

### 8. "Can we change it without breaking it?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 8.1 | "I'll just put it here for now." | Technical debt | Each shortcut saves a minute; the pile costs ten every time you look for something | ★ |
| 8.2 | Rewriting messy notes before the exam | Refactoring | Same content, nothing new, reorganized so every revision is easier | |
| 8.3 | "I fixed the squeak." | Regression | Fixing one thing breaks another that used to work | |
| 8.4 | The dress rehearsal | Staging environment | Try it all in a realistic copy first; some things still only show up on the day | |

### 9. "What if something goes wrong?"

| # | The moment | Concept | How it maps | Short? |
| --- | --- | --- | --- | --- |
| 9.1 | "Mom, where's the…?" | Single point of failure | Everyone depends on one person; when she's away, the house falls apart | ★ |
| 9.2 | The power cut, dinner by candlelight | Graceful degradation | The fridge and fan stop, but the gas stove works, so the essentials carry on | ★ |
| 9.3 | Grandma's recipe that only exists in her head | Backup | The only copy is in one place; the fix is writing it down, and changes made later won't be in it | |
| 9.4 | The fire drill | Failure drills (chaos engineering) | Practise the emergency on a normal day, and find the locked door before it matters | |
| 9.5 | The pill box | Idempotency | Each dose has its own slot, so "take today's tablet" can't happen twice | ★ |

Side examples for 9.2: the mic dies mid-speech, the substitute teacher's movie, "No naan? Roti then."

## If we need to trim (35 → 32)

1. **Indexing (6.5) becomes a sidebar of 6.4.** Both are wardrobe scenes, so one spread can carry both.
2. **Backpressure (5.3) becomes a sidebar of 5.2.** The overwhelmed kitchen is the bottleneck, and the "twenty-minute
   wait" is how the restaurant protects it.
3. **Load balancing (5.1) becomes a sidebar of 5.4.** Chapter 5 is among the most crowded, and the till is the least
   surprising of its moments.

## Not in the first book

| Concept | Why |
| --- | --- |
| Race condition, lost update, heartbeat, split brain | No relatable moment after two or more rounds (the attempts are listed in `UNSURE.md`) |
| Collision and random backoff | Skipped by Hussain |
| Security by obscurity | Skipped: niche term |
| Recursion | The "Why?" / "Because I said so" mapping doesn't hold |

**Alternates** (still possible): hash collision, binary search, knapsack, reply-all amplification, missed dependency,
unique IDs (two "main entrances").

**Parked earlier:** restarting a device, fridge clean-out as garbage collection, duplicate coat tickets, the cinema
row, chat reply before question, Wi-Fi reconnect storm, fake bank caller, charger adapter, wedding vows as two-phase
commit, mailbox as public-key encryption.

## Page format (to prototype, not decided)

- Compare a **two-page entry** (short comic plus compact reveal) with a **four-page entry** (story spread, then reveal,
  real example and boundary note).
- The reveal: about 80–130 words, one diagram, one real software consequence and one short "where the analogy breaks"
  note.
- Shorts and book share scripts and art, but a Short is **adapted** for print, not exported.

## Cast

Dev, Mira and Jo anchor the world, and the situation decides who else appears: family (Mom, Grandma, Grandpa, a
little brother), friends, strangers, staff. Nobody has a fixed teaching job, and some characters get things right
(5.1, 6.3, 9.2). Parents, grandparents and non-technical characters are never the punchline; the situation is.

## The gap (quick check, not proven)

| Book | What it does | How we differ |
| --- | --- | --- |
| *Algorithms to Live By* (Christian & Griffiths) | Prose; algorithms as life strategies | Comics, and systems behavior rather than only algorithms |
| *Once Upon an Algorithm* (Erwig, MIT Press) | Prose; computing through famous stories | Moments from the reader's own life, with a recurring cast |
| *CODE* (Petzold), *How Computers Really Work*, *How to Speak Machine* (Maeda) | Prose or hands-on guides to computing | Not comprehensive; wins on observation and reading pleasure |
| *The Cartoon Guide to the Computer* (Gonick), *Grokking Algorithms* | Illustrated explanations of computing and algorithms | Original sequential stories from everyday life, no exercises |
| Wizard Zines (Julia Evans) | Comics for working developers | For people who don't program |

A plausible space at the intersection of everyday adult comedy, sequential storytelling and software behavior. It's a
hypothesis that a sample has to prove.

## Next steps

- [ ] Hussain's review of draft 5 (the trim list)
- [ ] Pick the next two Shorts from the ★ moments, after the retention fixes are in `SERIES_GUIDE.md`
- [ ] Rough print prototypes of three entries: 1.1 stale cache, 6.2 prefetching, 9.5 the pill box; try one in both
      page formats
- [ ] 6–10 readers, mostly non-technical and not channel viewers (prompts in `IDEATION_REVIEW.md` section 9)
- [ ] Technical review of actual scripts and diagrams (the quality gate in `MOMENTS.md`)
- [ ] Price the chosen format in KDP's calculator before expanding

## Future ideas

- **"___ in Disguise" as a brand** (economics, psychology, physics). Earn it with software first.
- Keep collecting moments: any everyday situation that feels like a glitch goes into `UNSURE.md`'s moment lists.
