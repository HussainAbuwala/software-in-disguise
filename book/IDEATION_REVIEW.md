# Software in Disguise — independent editorial review

**Reviewed:** 25 September 2026  
**Draft:** `IDEATION.md`, draft 2, with `MOMENTS.md`, `SERIES_GUIDE.md`, and `EPISODES.md` as supporting context.  
**Perspective:** prospective nontechnical reader, book editor, technical reviewer, and potential gift buyer.

**Editorial priority, incorporating Hussain's clarification:** make excellent content for an everyday audience. Relatability comes first; the reader should not need an existing interest in programming. Better analogies and replacement topics are welcome, even when that means removing items from the original bank.

This is a review of the proposed book, not a rewrite of the source documents. Reader reactions below are editorial hypotheses, not findings from audience interviews. I have not assessed finished artwork or watched the videos. External research was limited to selected technical checks, adjacent-book descriptions, and Amazon print economics; this is not a market-demand study.

## 1. Verdict: develop a small book prototype before committing to forty concepts

The idea has a strong, repeatable pleasure: “I recognize that situation—and now I have a name for it.” That is a credible foundation for an illustrated book. The strongest assets are the situation-first rule, the accessible promise, and the opportunity for a recurring cast to make technical ideas feel personal.

The draft is currently more convincing as a **series engine** than as a **book proposition**. It explains where many episodes will come from, but leaves three questions insufficiently answered: who actively wants this book, what they gain beyond forty terms, and why reading several entries together stays rewarding.

My recommendation is to develop it as **an illustrated collection for curious adults who do not code**, with tech-adjacent readers and beginners as secondary audiences. Let it offer pleasure and useful recognition rather than a miniature computer-science course. Aim for the strongest 24–30 entries initially; earn additional pages through quality, not a promised number on the cover.

The five most consequential changes are:

1. Separate the intended reader from the likely purchaser, especially for gifts.
2. Repair the analogies where the story teaches the wrong mechanism.
3. Give the collection variety and progression beyond repeated mishaps.
4. Test an actual print reading experience before fixing the page count.
5. Validate interest in owning the book separately from interest in watching Shorts.

## 2. What is already working—and should survive revision

**Keep the central line.** “You've already lived it. Programmers just have a name for it” is memorable and friendly. It lowers the barrier to entry without promising that the reader will learn to program. Treat it as a playful invitation: some terms also belong to mathematics, operations, and other fields.

**Keep situations ahead of terminology.** Stale information, a queue that never advances, a forgotten reservation, and contradictory messages carry their own tension. That is much more inviting than opening with a definition.

**Keep the distinction between recognition and humor.** A story can be satisfying without a punchline. Warmth, surprise, or a well-observed frustration can carry a page. Forced jokes would weaken the book.

**Keep the limits of each analogy.** The “where the analogy breaks” note can build trust. Make it brief and useful. It should refine a basically correct story; it cannot repair a story whose central mechanism is wrong.

**Keep a shared world.** Dev, Mira, and Jo can make the collection feel authored. Their relationships and changing roles matter more than the size of the reusable asset library.

## 3. Audience and purchase appeal

“Adults who don't program” describes a very large group, most of whom have no particular reason to buy software vocabulary. Narrow the motivation before narrowing the demographics.

| Reader or buyer | Likely attraction | Main risk | Recommendation |
| --- | --- | --- | --- |
| Curious adult who enjoys illustrated nonfiction | Recognizing familiar patterns and learning something surprising | The software reveal feels like homework | Primary reader; every story must reward this person |
| Developer buying for a partner, friend, or parent | A shared joke and an approachable window into their work | The gift feels like an assignment to understand the developer | Strong buyer hypothesis; test the recipient's response separately |
| PM, designer, or colleague working with engineers | Remembering unfamiliar terms | Explanations feel too shallow to use at work | Secondary reader; provide an index and optional notes |
| Beginning developer or CS student | Memorable anchors for new concepts | Expectation of a systematic foundation or study guide | Welcome them without making exam or curriculum promises |

The gift positioning needs particular care. “So what do you actually do all day?” promises a view of software work, but this bank mostly explains system behavior. Coding, debugging, reviews, requirements, and working with other people are much less visible. Either soften that sales line or add a small amount of material about making and changing software. Do not imply the current selection explains the whole profession.

Suggested positioning to test:

> An illustrated collection of everyday mix-ups, clever shortcuts, and familiar frustrations that reveal how software behaves. No coding required.

Keep *Software in Disguise* as the working title. For a subtitle, test **“Everyday life, explained through software comics.”** Retain the current promise line on the cover or back cover. Avoid locking “40” into the subtitle before the shortlist is proven.

The emotional promise should be: **“You'll start noticing these patterns everywhere.”** That gives readers a reason to care beyond remembering terminology.

### Apply a stricter everyday-reader test

“Easy to picture once explained” is weaker than “I've been there.” Keep those as separate judgments. A cinema full of people recursively asking their row number can be pictured, but does not sound like something people normally do. Laundry waiting for a full load needs almost no explanation.

Before naming a concept, the reader should understand who wants what and why the result is frustrating, useful, or surprising. Avoid premises that require invented rules solely to reproduce a technical mechanism. A familiar setting alone does not make an unfamiliar behavior relatable.

Do not treat the current recognition dots as audience evidence. Test them across the people you hope will read the book. Four-way stops, VIP wristbands, printed dictionaries, workplace email, and wedding rehearsals are not equally familiar across countries, ages, or lifestyles. You do not need every scene to be universal; you need enough accessible scenes that readers consistently feel included. Show any essential local convention in the drawing.

Use plain titles such as “Your usual?” and “I need that shirt tomorrow.” Save terms like prefetching and batching for the reveal. Avoid “you already understand distributed systems” as a promise: recognizing one pattern is the pleasure, and the book need not inflate it into expertise.

In the reader test, show the comic without its software explanation first. Ask whether it feels observed or invented, and whether it is worth reading on its own. Then reveal the connection and check whether it adds satisfaction. Passing only the technical half is not enough.

## 4. Make it a book people want to keep reading

### Build progression without turning it into a course

Chapters by life area are approachable, but the current grouping is uneven: “Keeping in touch” has eleven entries, “Trust and safety” has three, and “Big days” contains office printers and chargers. Those labels feel partly dictated by the remaining inventory.

My preferred structure is a set of human questions, with different settings inside each section:

| Working section | Reader's question | Candidate moments |
| --- | --- | --- |
| “But I checked!” | Why is the information wrong? | #1 stale cache, #3 lost update, #15 counting conventions, #25 delayed updates |
| “Why is nobody moving?” | Why does everyone get stuck? | #2 deadlock, #10 livelock, #17 starvation, #12 abandoned reservation |
| “Can we make this easier?” | Which shortcuts help, and what do they cost? | #13 load balancing, #18 prefetching, revised #6 batching, #14 search |
| “Did you get my message?” | What happens when we cannot tell what happened? | #24 timeout, #23 retries, #28 idempotency, #27 corruption |
| “Who can do what?” | How do trust and permissions work? | #33 identity/permissions, #34 access expiry, revised #26 conflicting authority |
| “What if something changes?” | How do we change things and recover? | #9 regression, #35 dependency on one person, #40 rehearsal, revised #38 recovery |

These are organizing hypotheses, not a final contents page. If you retain life-area chapters, keep the same progression within them and rename “Big days” to fit its contents.

A dip-in book does not need a continuous plot. It does need rhythm. Avoid long runs where everybody waits, everybody miscommunicates, or every apparent solution fails. Deliberately alternate mishaps, useful designs, and trade-offs. Some characters should get things right.

### Give the cast personalities rather than fixed teaching jobs

Dev should not always be wrong; Jo should not always arrive with the answer. Let each be capable in one situation and fallible in another. Establish enough relationship context to make an interaction legible without requiring readers to remember earlier chapters.

Use callbacks as a bonus: the stale milk answer can return later when somebody decides to verify it. Avoid turning every parent, grandparent, or nontechnical person into a punchline. The joke should usually be the situation or the rule people are following.

### Add value beyond the videos

The book can offer things Shorts cannot: diagrams readers can inspect, comparisons between easily confused ideas, recurring visual details, and a concept index. A short chapter-ending comparison of deadlock, livelock, and starvation would be more useful than giving every neighboring term another full story.

Give each entry one concrete software consequence: a shopping-cart update disappearing, an order being duplicated, or a page serving yesterday's information. Readers need the bridge back to software, not just a label pasted onto a joke.

## 5. Review of all 41 proposed moments

**Keep** means a strong candidate, subject to scripting and accuracy review. **Revise** means the premise has value but the mapping or staging needs work. **Merge** means use as a supporting example or comparison. **Park** means omit from the first prototype unless a stronger treatment emerges. These are editorial decisions, not measurements of popularity.

| # | Moment / concept | Decision | Specific editorial note |
| --- | --- | --- | --- |
| 1 | Checked this morning / stale cache | Keep | Excellent opener. Show why reusing an answer is convenient before its age becomes a problem. Expiry limits staleness; it does not guarantee current information. |
| 2 | Remote and batteries / deadlock | Keep | Clear visual conflict. Make each person's goal and held resource explicit so this is more than general stubbornness. |
| 3 | Missing eggs / lost update | Keep | Show the two starting copies and the overwrite. Otherwise readers may infer forgetting, failed sync, or deletion. |
| 4 | Clothes chair / technical debt | Revise | Show the continuing cost of the shortcut. Avoid equating technical debt with laziness or every postponed chore. |
| 5 | “Are we there yet?” / rate limiting | Keep | Simple rule, visible enforcement. Make the exhausted parent's limited attention the resource being protected. |
| 6 | Grocery bags / batching | Revise | The trade-off must visibly come from waiting to form a batch. Multiple trips can also delay items; the current outcome is not automatic. |
| 7 | Restarting a device | Park | Already literally a software situation, so the “disguise” adds little. Could become a brief aside; restarting does not erase all persistent state or solve every failure. |
| 8 | Fridge clean-out / garbage collection | Revise | A name label is not the same as reachability. Unclaimed does not necessarily mean unused. A better reference-tracing mechanism is needed. |
| 9 | Cabinet fix breaks clearance / regression | Keep | Clear cause and effect. Use “regression” as the main concept; not every side effect is a regression. |
| 10 | Hallway dance / livelock | Keep | One of the best visual premises. Define left/right from a consistent viewpoint and show movement without progress. |
| 11 | Four-way stop / circular wait | Merge | Better alongside #2 as a larger waiting cycle. Traffic conventions also vary, so explain the scene's rule rather than assuming universality. |
| 12 | Jacket reserves seat forever / lease | Keep | Strong story. Distinguish a reservation expiring from a waiting person deciding to leave. Briefly acknowledge the returning owner's stale claim. |
| 13 | Newly opened checkout / load balancing | Keep | Useful positive counterweight. Show work being distributed and the dispatcher making the choice. |
| 14 | Searching a movie / binary search | Revise | The reader must know whether each sampled scene is before or after the target. Time order alone does not supply that knowledge. |
| 15 | First-floor disagreement / off-by-one | Keep, narrow label | Good recognition. This illustrates a mismatch in counting conventions, one route to an off-by-one error, not the definition of all off-by-one bugs. |
| 16 | Two people, one seat / race condition | Keep | Show both checking before either reserves. Duplicate tickets alone could have several unrelated causes. |
| 17 | Quick walk-ins / starvation | Keep | Strong stakes and escalation. Show the scheduling rule repeatedly postponing the larger job, rather than merely a long wait. |
| 18 | Barista predicts order / prefetching | Keep | A warm character moment and a genuine trade-off. Preparing a drink is broader speculative work; tie the software reveal specifically to fetching data early. |
| 19 | Duplicate coat tickets / hash collision | Revise substantially | Duplicate identifiers are not enough to demonstrate hashing. Keep as key–value lookup, or show different keys mapping to one bucket. |
| 20 | Cinema row / recursion | Park | The mechanism works if the base case and returning answers are shown, but the behavior feels invented for the lesson. Low recognition weakens the promise. |
| 21 | “Text me when home” / heartbeat | Revise or merge | A single expected arrival message is a completion notification. A heartbeat requires recurring check-ins; otherwise use this under timeout. |
| 22 | Simultaneous talking / collision and backoff | Keep | Strong recognition. Show unequal pauses resolving the repetition. Limit the software claim to relevant shared-channel protocols. |
| 23 | Ten unanswered calls / retry backoff | Keep | The current story shows retries without backoff. Add increasing waits to demonstrate the proposed solution; endless retries are not the lesson. |
| 24 | Waiting for a friend / timeout | Keep | Establish an expected reply or arrival and a deadline. A timeout tells you how long you waited, not what happened to the friend. |
| 25 | Dinner-time update / eventual consistency | Keep | Make copies of the plan eventually converge. Delayed reading alone is a loose stand-in; conflicting new updates introduce a separate problem. |
| 26 | Asking the other parent / split brain | Revise | Show an agreed shared decision being made independently because the decision-makers cannot coordinate. Ordinary disagreement is not sufficient. |
| 27 | Family message chain / corruption | Keep | Strong familiar premise. Choose corruption as the central concept; checksum detection can be the reveal's supporting idea, not a second unexplained lesson. |
| 28 | Repeated flowers / idempotency | Keep | Make it the same intended order retried after missing confirmation. Three deliberate new purchases should legitimately produce three bouquets. |
| 29 | Reply before question / ordering | Revise | A memorable image, but do not imply every familiar chat app behaves this way. A clearly fictional service or mixed delivery routes can avoid that claim. |
| 30 | Reply-all avalanche / broadcast storm | Keep, qualify | Strong office recognition. It resembles traffic amplification; distinguish it from a literal network-layer broadcast storm. |
| 31 | Wi-Fi reconnects / thundering herd | Replace setting | It is already software and needs an unexplained fragile router. Try a crowd rushing a desk the instant it reopens, if observed behavior supports it. |
| 32 | Fake bank caller / social engineering | Merge or park | Worth knowing, but this is already the actual security attack. Low surprise for this particular premise; avoid padding a thin chapter with it. |
| 33 | ID and VIP wristband / authentication vs. authorization | Keep | One of the strongest teaching pairs. Have staff match a named guest to an ID; checking age alone is an eligibility check. |
| 34 | Old dog-sitter key / access revocation | Keep | Familiar and consequential. Distinguish revoking existing access from granting access that expires automatically. |
| 35 | Only Jo knows / single point of failure | Keep | Good human stakes. Use “bus factor of one” as an optional team term; bus factor is a measure, not a synonym for every single point of failure. |
| 36 | Charger adapter / compatibility | Revise | Currently a hardware example. An adapter bridges interfaces; backward compatibility concerns newer systems continuing to support older uses. Choose one. |
| 37 | Full suitcase / knapsack | Keep, simplify | Show competing usefulness and capacity clearly. Physical shape complicates packing beyond a simple knapsack model; weight allowance may map more cleanly. |
| 38 | Parking photo and spare key / backups and replication | Revise substantially | Two scenes and several ideas are bundled together. Choose recovering a lost original, then distinguish a retained backup from a continuously updated replica. |
| 39 | Wedding vows / two-phase commit | Park or rebuild | Two people saying yes are not the two phases. The scene needs preparation followed by a separate coordinated decision. High explanation cost for this audience. |
| 40 | Wedding rehearsal / staging | Keep | Accessible positive design. A rehearsal approximates reality; show one difference that it cannot test. Avoid claiming failures there never matter. |
| 41 | Airline overbooking / overcommitment | Keep | Good trade-off and a useful contrast with #16: deliberate oversubscription versus accidental double allocation. Treat unfair consequences with empathy. |

### The five analogy repairs I would prioritize

**#19 — coat check:** Choose between a simple lookup story and a collision story. For hashing, two distinct full identifiers must be sent to the same storage bucket by a rule; matching the full identifier then distinguishes them. Two copies of ticket 147 instead demonstrate identifier duplication. Java's hash-code contract explicitly permits different objects to share a hash code, which supports this distinction. [Oracle: Object.hashCode](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html#hashCode--)

**#21 — heartbeat:** Keep the lovely human concern, but decide what it teaches. “Text me when you arrive” works for an expected completion message and a timeout. Repeated “still here” check-ins work for heartbeat monitoring. Missing a check-in raises suspicion; it does not prove failure. [RabbitMQ: heartbeats](https://www.rabbitmq.com/docs/heartbeats)

**#39 — two-phase commit:** “Two phases” means prepare, then commit or abort—not asking two participants. Prepared participants may remain waiting for a decision. If preserving that mechanism makes the wedding unnatural, drop the concept from the first book. A simpler scene is more valuable than impressive terminology. [PostgreSQL: PREPARE TRANSACTION](https://www.postgresql.org/docs/current/sql-prepare-transaction.html)

**#4 — technical debt:** The strongest part of the clothes-chair scene is that yesterday's convenience makes today's task slower. Emphasize that continuing cost. Avoid moralizing: software debt can come from reasonable choices or later learning, not just careless shortcuts. [Martin Fowler: Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html)

**#38 — backups:** A parking photo is primarily an external memory aid. A spare key illustrates redundancy and separate placement, but does not teach the difference between backup and replication. A recoverable older copy of something accidentally overwritten would make the recovery purpose clearer. Do not teach that keeping multiple live copies automatically protects against every kind of loss.

### The parked mini-examples also need an accuracy pass

The bathroom lock is a strong supporting mutex example. The kitchen ticket rail can illustrate a queue if service order is clear. GPS rerouting is already computing, and “shortest” may mean travel time rather than distance. Driving without seeing the engine gives a useful abstraction example, but could also be framed as an interface; choose the wording carefully.

The mailbox analogy for public-key encryption needs more care than a tiny box permits. A slot anyone can use illustrates asymmetric access, but does not itself show encryption. Do not let the reader conclude that anyone can unlock the mailbox using a public key. Park it unless the illustration can make the intended correspondence unambiguous.

## 6. Topic balance: make every added entry earn its place

The bank leans heavily toward concurrency, waiting, retries, and distributed coordination. That is a distinctive strength, but it creates overlap. Deadlock/circular wait, collision/retry backoff, heartbeat/timeout, and cache/consistency/lost updates must each contribute a different reader insight.

Do not add every missing CS topic to make the book “complete.” Instead, gather lived scenes in a few underrepresented areas. These are prompts for observation, not approved analogies:

| Situation worth collecting | Possible lens | Why it could help |
| --- | --- | --- |
| “Make it a little bigger”—but both people mean different things | Ambiguous requirements | Shows software work beginning with understanding what somebody wants |
| A recipe works for four people and falls apart when cooking for forty | Scaling and bottlenecks | Adds a trade-off with a clear visual escalation; the specific limiting step must be visible |
| A kitchen is rearranged so every later meal takes fewer steps | Refactoring | Positive change to the process while preserving the intended result |
| A failed cake can only be explained if somebody recorded what changed | Logging and diagnosis | Shows why evidence matters when fixing a problem; avoid equating logs with complete observability |
| A café can still serve drip coffee when its espresso machine breaks | Graceful degradation | A system coping usefully rather than collapsing completely |

Three strong replacements would improve the book more than ten extra terms. If a scene needs an elaborate invented rule to fit its concept, return to collecting moments.

### Stronger replacement analogies to develop

These are proposed scenes, not claims that your audience has experienced them. They should still pass recognition and accuracy testing. Prefer the ones drawn from something you or a reader actually observed.

**Batching: “I need that shirt tomorrow.”** One person waits until there is a full laundry load; another needs a particular shirt washed tonight. Waiting uses fewer wash cycles, but the early item waits longer. The comic can show the same shirt waiting as the basket slowly fills. This is a cleaner batching trade-off than carrying grocery bags because the accumulation delay is visible. Boundary: not every item waits longer, and real systems can release a batch when it reaches a size limit or a time limit. **I would replace #6 with this.**

**Technical debt: “We saved twenty minutes moving in.”** To finish a move quickly, somebody skips labeling the boxes. Over the next week, every search for one object requires reopening several boxes. The time saved once creates repeated costs; labeling now would take effort but make later searches easier. This is more specific than generic untidiness. Keep the chair if its character comedy is better, but give it this same “shortcut, repeated cost, possible repair” structure. **Test against #4.**

**Heartbeat: the daily check-in.** Two friends living in different cities exchange a brief message every morning. A sequence of days establishes the rhythm; then one morning's message is missing. Concern leads to a call, and the explanation might simply be a flat phone battery. It preserves uncertainty and warmth while making recurrence explicit. Do not manufacture a frightening accident for the payoff. **Replace #21 if heartbeat deserves its own entry; otherwise keep the arrival-text scene under timeout.**

**Hash collision: “There are two Patels in the P tray.”** At an event, name badges are organized into trays by the first letter of the surname. Patel and Perez both lead to P; the volunteer still checks the full name inside the tray. Different keys share a bucket without being the same key. Initial-letter grouping is a deliberately simple stand-in for a hash function, and uneven tray sizes can show why the grouping rule matters. This is closer to a real familiar process than inventing duplicate coat tickets. **Replace #19 if you want hashing; retain the original coat check for simple lookup.**

**Binary search: a word in a printed dictionary.** Open around the middle, compare the page's words with the target alphabetically, and discard the irrelevant half. The order comparison is explicit and repeatable. It is mechanically stronger than movie scrubbing, although probably less relatable to some younger readers. A sorted printed attendee list can serve the same role. **Choose this only if readers recognize the activity; do not keep binary search just for syllabus coverage.**

**Recovery from backup: the recipe card that gets ruined.** A treasured handwritten recipe is damaged during cooking. Someone previously photographed it and kept the photo separately, so the recipe can be recovered. The story has an emotional reason to preserve information and a visible restoration. Boundary: changes made after the photograph are missing from that backup. **Replace the parking-photo/spare-key bundle in #38.**

**Thundering herd: the service desk reopens.** A queue has dispersed while a desk is closed. When the shutter rises, everyone rushes forward together and the attendant cannot serve anyone efficiently. Show the shared trigger and sudden burst, not just a busy crowd. A numbered queue then illustrates one possible admission strategy. **Replace the Wi-Fi setting in #31, but compare with #13 and keep both only if readers learn distinctly different things.**

**Recursion: counting a whole family for a reunion.** The organizer asks each family branch for its total; each person asks their own children for their branch totals, adds them and themselves, then reports upward. Someone with no children simply reports one. The drawing can show the question traveling down a tree and counts returning up. Boundary: count everyone exactly once and use a deliberately simple family tree. This is more plausible than a cinema row full of people who do not know their row number, but it still needs a human story. **A candidate to test, not an automatic rescue of #20.**

I would not force replacements for garbage collection or two-phase commit yet. Both are interesting, but a first volume can be excellent without them. Difficulty finding an honest, recognizable scene is useful selection evidence.

### New topics I would put ahead of several current candidates

These additions would broaden the reader's picture of software from “things get stuck or messages go wrong” to “people design systems, make changes, and handle imperfect conditions.” The examples are starting premises; the software connection must survive scripting.

| Priority | Scene to develop | Topic and exact connection | Why it earns consideration / boundary |
| --- | --- | --- | --- |
| High | The espresso machine fails, but the café still serves drip coffee and pastries | Graceful degradation: preserve a useful subset of service | A positive resilience story. The remaining service must not depend on the failed machine. |
| High | “The recipe worked for four!” Four cooks are ready, but every dish still needs the one oven | Bottleneck: one constrained stage limits the whole operation | Visual and broadly recognizable. More helpers do not expand oven capacity; distinguish this from every kind of scaling problem. |
| High | A shop accepts a repair and gives you a claim ticket; you leave instead of standing there until it is fixed | Asynchronous work: acceptance and completion happen separately | Introduces a useful design choice. Show where the completed result goes and how you find out it is ready. |
| High | The plant-waterer only needs the balcony, but gets the key that opens every room | Least privilege: grant only the access needed for the job | Complements #34: scope of permission versus duration. It can be a sidebar to #33 if a full entry repeats too much. |
| High | The kitchen is reorganized; tomorrow's breakfast is the same, but the process is easier to maintain | Refactoring: change internal organization while preserving intended external behavior | Shows constructive software work. Keep changing the recipe or adding a new dish out of this example. |
| Medium | “Cut it short.” Both people agree, but picture different haircuts | Requirements ambiguity: agreement on words is not agreement on expected behavior | Directly supports the “what developers do” angle. The remedy is a shared example or measurable expectation, not blaming the customer. |
| Medium | A new table-service routine is tried on two café tables before all tables use it | Gradual rollout: observe a change with limited real exposure | Adds a useful contrast to rehearsal. A small trial can miss problems; it does not prove the full rollout will succeed. |
| Medium | Two dinner cooks each think the other is bringing the one shared ingredient | Dependency planning: several tasks depend on one prerequisite | A strong everyday failure if based on a real incident. Do not label ordinary forgetfulness a dependency graph without showing what is blocked. |

For the initial bank, I would promote graceful degradation, bottlenecks, asynchronous work, and refactoring ahead of restarting devices, the current recursion story, the current two-phase-commit story, and the direct phishing example. Those swaps add range and positive design without increasing the entry count.

Keep APIs, AI, blockchain, encryption, and other fashionable or familiar labels out unless a strong scene earns them. A book's topic list is not improved merely by adding currently recognizable keywords.

### A proposed 28-entry editorial shortlist

This is my strongest current direction, not a production commitment. A revised entry stays only if its replacement scene works; do not treat 28 as a quota.

| Theme | Candidate entries |
| --- | --- |
| Information and memory — 5 | #1 stale cache; #3 lost update; #15 counting conventions; #25 eventual consistency; #38 recipe backup |
| Sharing time and resources — 5 | #2 deadlock; #10 livelock; #17 starvation; #12 reservation lease; #5 rate limiting |
| Making work flow — 5 | #13 load balancing; #6 laundry batching; #18 prefetching; new oven bottleneck; new repair-shop asynchronous work |
| Messages and uncertainty — 4 | #24 timeout; #22 collision/backoff; #28 idempotency; #27 corruption |
| Trust and permission — 3 | #33 authentication/authorization; #34 revocation/expiry; revised #26 split brain |
| Change and resilience — 6 | #4 technical debt; #9 regression; #35 single point of failure; #40 rehearsal/staging; new refactoring; new graceful degradation |

Use #23 retry backoff as supporting material for #28, least privilege alongside #33, and #11 circular wait alongside #2. Keep repaired hashing, knapsack, and overcommitment as strong alternates. If readers find the shortlist too coordination-heavy, substitute one of those for a weaker repeated waiting/messaging story.

### A quality gate for “best content”

For each finished premise, write four sentences privately: **what the person wants; what rule or constraint drives the scene; which exact software behavior matches; what the reader must not infer.** If these do not align, revise before drawing.

Then assess five things: recognition, visual clarity, technical fidelity, human payoff, and contribution to the collection. A technically wrong analogy fails regardless of how funny it is. A correct but lifeless one returns to the bank. A good story that repeats an earlier lesson becomes a supporting example. The strongest content is the smallest set in which every entry contributes a distinct pleasure or insight.

## 7. Page design: resolve the three-page problem early

Two comic pages plus one explanation page is a reasonable content budget, but an awkward repeated print unit. A spread is two facing pages. Repeating three-page entries alternates the starting side, so successive two-page comics cannot all be intact facing spreads without additional layout decisions.

The arithmetic is also worth making explicit: 41 entries at three pages occupy 123 pages before chapter openers, introduction, glossary, and other material. The proposed 120–150 pages can accommodate that only toward its upper end, with limited room for expansion.

Prototype two approaches:

| Format | Advantage | Risk |
| --- | --- | --- |
| Two-page entry: short comic plus compact reveal | Easy to browse; economical | Dialogue and diagrams may become cramped |
| Four-page entry: story spread, then explanation and supporting material | Room for expressions, a real example, and limits | More pages; temptation to pad simple ideas |

A promising starting plan is 28 four-page entries: 112 content pages plus roughly 16–24 pages for the rest. This is a planning example, not a target to force every story into. A mix of two- and four-page entries is also possible once the layout system is tested.

There is a trade-off between placing the reveal on the same spread and hiding it until a page turn. Print readers scan ahead. A two-page entry may sacrifice surprise for convenience; a four-page entry can preserve it. Test which matters more instead of importing the Shorts reveal rule unchanged.

For the reveal, try roughly 80–130 words, one legible diagram, and one short boundary note as a starting constraint. “You've seen this too” should appear only when the extra cases clarify the concept. Three more weak analogies will make a strong entry worse.

Replace “render a print page for every episode” with **“save reusable art and script material; adapt selected episodes for print.”** Vertical video framing, timed reveals, voices, and loop endings do not automatically produce good comics. Early episodes also need a consistent book art style. Judge the result at actual printed size, particularly faces, speech bubbles, diagram labels, and the gutter.

## 8. Selling on Amazon: a few decisions affect the idea itself

### Keep the market-gap claim provisional

The comparison table is a useful starting point, but “not exactly like these five books” is not evidence of demand. The differentiation must be visible in a sample spread: adult situations, original sequential comics, and a satisfying software connection.

Correct the Gonick title to *The Cartoon Guide to the Computer*. His official description includes software programming, so the comparison should not reduce that book to hardware alone. Recheck the other titles and avoid broad audience claims such as “often for kids” without looking at the individual books. [Larry Gonick: book description](https://www.larrygonick.com/titles/science/the-cartoon-guide-to-the-computer/)

Compare potential substitutes by reader promise, tone, illustration density, depth, and gift appeal. The buyer may be choosing between this book and another entertaining illustrated nonfiction gift, not another computing title.

Additional adjacent works make the competitive picture more useful:

| Work | What the primary description establishes | Implication for this book |
| --- | --- | --- |
| *Grokking Algorithms* | An illustrated introduction to algorithms with explanations and exercises. [Manning](https://livebook.manning.com/book/grokking-algorithms/foreword) | “Illustrated and approachable” is not sufficient differentiation. Your everyday stories and freedom from implementation exercises need to be visible. |
| *How Computers Really Work* | A hands-on guide spanning circuits, programming, operating systems, and the internet. [No Starch Press](https://nostarch.com/how-computers-really-work) | Avoid competing on comprehensive coverage; a compact collection can win on observation and reading pleasure. |
| *How to Speak Machine* | A book positioned around understanding computation and its implications. [Penguin Random House](https://www.penguinrandomhouse.com/books/539046/how-to-speak-machine-by-john-maeda/) | Nontechnical interest in computing is an existing positioning territory, not an untouched category. |
| Wizard Zines | An established collection of programming zines. [Creator's site](https://wizardzines.com/) | Short, visually explained computing already exists; your distinctive unit should be an original human scene with a software payoff. |

**My judgment on the gap:** there is a plausible, specific space worth testing at the intersection of adult everyday comedy, sequential storytelling, and software behavior. These comparisons support a differentiation hypothesis, not a claim that nobody has done it or that enough buyers exist. The opportunity is to execute that combination unusually well. Broader competitor research and reader tests could still change the positioning.

### Price the physical format before expanding the manuscript

Color and trim size materially affect printing cost. Using Amazon's currently published US paperback rates, an illustrative 144-page book costs approximately:

| Interior | Regular trim | Large trim |
| --- | ---: | ---: |
| Black ink | US$2.73 | US$3.45 |
| Standard color | US$4.67 | US$6.79 |
| Premium color | US$10.36 | US$12.52 |

These are printing costs, not retail prices or profit. Calculations use the listed fixed charge plus per-page rate. KDP classifies a trim as large when it exceeds 6.12 inches wide or 9 inches high; other marketplaces have different rates. Verify the chosen format in its calculator before setting a price. [Amazon KDP: paperback printing costs](https://kdp.amazon.com/en_US/help/topic/G201834340)

The editorial implication is to test standard color and a deliberately designed black-and-white treatment at the intended size. A limited palette still involves color printing. Do not shrink the book until it becomes unpleasant to read simply to reduce cost.

Paperback is a sensible first prototype for the gift hypothesis. Treat any Kindle edition as a separate reading experience to test, especially on small screens. No publication format has been selected or validated by this review.

The broader “___ in Disguise” brand can stay in a future-ideas note. Domain checks are a small administrative task; a convincing sample is the priority.

## 9. Test the book promise, not only the Shorts hooks

The episode ledger offers early clues about openings and pacing. It cannot yet establish book demand, and the small samples and changing formats do not isolate which creative choice caused a performance difference. A viewer leaving during a reveal is worth investigating; it does not prove that book readers dislike explanations.

Do not wait for ten polished entries before getting feedback. Make three rough but readable print entries:

1. **#1 stale cache:** tests the strongest everyday recognition and the story-to-software bridge.
2. **#18 barista prefetching:** tests warmth, a useful shortcut, and a genuine trade-off.
3. **#28 repeated flowers:** tests whether a less familiar word becomes understandable through the story.

Give them to 6–10 people, mostly intended nontechnical readers who do not follow the channel. Include a couple of potential gift buyers and ask them separately about the recipient. This is a small qualitative test, not a representative survey.

Useful prompts are:

- “What do you think this book is offering?” Show the cover concept before explaining it yourself.
- “Talk me through what happened here.” Listen for missing visual information.
- “How would you explain the software idea to someone else?” This tests transfer beyond remembering the scene.
- “Where did you stop reading or skim?” Observe whether the reveal earns its space.
- “Which entry would you show another person, and why?” This tests sharing appeal.
- “Would you choose another entry to read now?” Actual continuation is more informative than polite praise.
- “At this proposed price, would you consider it for yourself or for someone specific?” Test after format costs are known.

As a working editorial gate, revise any entry when several readers independently make the same wrong inference. Proceed to a larger sampler when most can explain the intended idea without your help and voluntarily want more. A sampler signup is interest; it is not a sale. Keep reader enjoyment, comprehension, and purchase intent as separate observations.

## 10. Recommended revision order

**Before producing more book art:** choose the primary reader and one-sentence promise; resolve #19 and #21; decide whether #39 deserves space; remove duplicate concepts from the initial shortlist.

**For the first prototype:** adapt the three suggested entries, compare two- and four-page treatments on one of them, and print at the intended size. Check the story without narration and the explanation without a developer present.

**After initial reader feedback:** settle the page system, build a 24–30-entry shortlist with deliberate tonal variety, and obtain a technical review of the actual scripts and diagrams. Keep each entry's main concept, source, analogy boundary, and reader-test notes together.

**Before committing to the full manuscript:** estimate the intended Amazon edition's costs, test a plausible price with readers and gift buyers, and decide whether the evidence justifies a larger sample or full production.

My strongest advice is to protect the quality of the recognition. The book earns its place when readers feel that it noticed something about their lives and gave them a useful new way to understand it. Every extra term, panel, and explanation should serve that experience.
