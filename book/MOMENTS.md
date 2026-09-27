# The moments, explained (draft 5)

What each entry in `IDEATION.md` is about. Each has three parts:

- **What happens:** the situation, not yet a story.
- **In software:** the behavior it matches, with a real example.
- **Don't let the reader infer:** where the analogy stops. The reveal page's boundary note comes from this.

**Quality gate before any entry is drawn:** write four sentences privately: what the person wants, what rule or
constraint drives the scene, which exact software behavior matches, and what the reader must not infer. If they don't
line up, fix the scene first. The story must also pass the rules in `IDEATION.md`: a real, relatable moment, and no
screens in the story.

## 1. "Is that still true?"

### 1.1 "I checked this morning." — stale cache
**What happens:** Dev looked at the fridge, the weather and Jo's door at 7 a.m. All day he answers from that one look:
there's milk, it's sunny, Jo's asleep. Reusing the answer is genuinely handy, until everything has changed.
**In software:** a cache keeps a copy of an answer so it doesn't have to be looked up again. If the original changes,
the copy is stale: a website still showing yesterday's price.
**Don't let the reader infer:** that an expiry time guarantees fresh answers. It only limits how old they can get.

### 1.2 "Wait, you didn't know?" — eventual consistency
**What happens:** Mira's sister got engaged. She told Mom on Friday; Mom told Dad; Dad meant to tell Grandpa. At
Sunday lunch, half the table knows and half doesn't, and an aunt congratulates the couple while Grandpa, fork in the
air, hears it for the first time. By dessert, everyone knows.
**In software:** big apps keep copies of the same data on many servers. A change reaches the copies one by one, so for
a while they disagree, and eventually they all match. Your new profile photo shows for some friends before others.
**Don't let the reader infer:** that the news got distorted (that's 2.3). Here it's the same news, just arriving at
different times. Two conflicting changes are a separate, harder problem.

## 2. "That's not what I meant!"

### 2.1 "We're both on the first floor." — off-by-one
**What happens:** Dev and Mira are both "on the first floor" of the same café. One counts the entrance level as the
ground floor, the other counts it as the first, so they're exactly one floor apart.
**In software:** code usually counts from zero and people from one. When the two conventions meet, results come out
exactly one off: a skipped first item, or a crash one past the end.
**Don't let the reader infer:** that every off-by-one error comes from counting conventions. This is one common route.

### 2.2 "Clean your room." — acceptance criteria
**What happens:** A parent says "Clean your room." Twenty minutes later: "Done!" The floor is clear because everything
is under the bed, the wardrobe is jammed shut and the dishes are on the windowsill. Next time, the parent says what
"clean" means: floor clear and nothing under the bed, clothes in the wardrobe, dishes in the kitchen, bed made. Each
one can be checked by both of them.
**In software:** before building something, teams write down concrete, checkable conditions for when it counts as
done ("the reset email arrives within a minute; the link stops working after 24 hours"). If every condition is met,
the work is accepted. It turns "make it nice" into a checklist, so nobody ends up saying "that's not what I meant."
**Don't let the reader infer:** that the kid was being sneaky. By their own definition the room *is* clean; the
problem is two different pictures of "done". And criteria can't capture everything.
**Side example:** "Just a little shorter" at the hairdresser. Next time, the customer brings a photo.

### 2.3 The message via your little brother, and the waiter's read-back — data corruption and checking
**What happens:** Mom tells the little brother: "Tell Dad to pick Grandma up from the station at 3." Dad hears:
"Grandma's coming, bring three things." Later, at a restaurant, the waiter does the opposite: "So that's one tea, no
sugar, and a samosa?" A mistake caught before it reaches the kitchen.
**In software:** data can change on its way from one place to another. Receivers check it. Instead of reading back the
whole message like the waiter, software sends a short fingerprint of the original (a checksum); if the fingerprint
doesn't match what arrived, the receiver asks for it again.
**Don't let the reader infer:** that checking repairs the message. It reveals that something changed, so it can be
sent again.
**Side example:** the photocopy of a photocopy of a photocopy.

## 3. "Why is nobody moving?"

### 3.1 The narrow lane — deadlock
**What happens:** A one-lane road between walls, or up a hill. Two cars meet head-on in the middle. Each driver holds
their half of the lane and waits for the other to reverse. Neither does. Engines idle, horns, folded arms.
**In software:** two programs each hold one resource and wait for the one the other holds. Neither can continue, and
the app freezes. The fixes mirror the road: a rule for who backs up, or a passing bay so the situation can't arise.
**Don't let the reader infer:** plain stubbornness. Each driver genuinely needs the space the other is holding.
**Sidebar:** "No job without experience, no experience without a job." The same loop shape, called a circular
dependency: A needs B to start, B needs A to start. People break it with a side door (an internship, volunteering);
software does too.

### 3.2 "After you." "No, after you." — livelock
**What happens:** Two people reach a door at the same moment. Each holds it for the other. "After you." "No, please,
after you." Both step back, both step forward, both step back. Nobody goes through.
**In software:** programs keep reacting to each other and changing what they do, but make no progress. Unlike deadlock,
everyone is busy. The fix is for one side to pause for a random moment.
**Don't let the reader infer:** that livelock and deadlock are the same. The chapter-end page contrasts them: frozen
versus busy.

### 3.3 "Where should we eat?" "Anywhere's fine." — consensus and choosing a leader
**What happens:** Five hungry friends. "Where should we eat?" "Anywhere's fine." "You pick." "I don't mind." Forty
minutes of polite indecision, until someone says "Riya, you choose," and they're eating in ten.
**In software:** when several computers must agree on one decision, agreement is surprisingly hard. Many systems solve
it by electing one leader who decides for the group, and electing a new one if the leader disappears.
**Don't let the reader infer:** that computers are indecisive. What makes their agreement hard is lost messages and
machines failing mid-conversation; the shared fix is to make one member the decider.

### 3.4 The jacket saving a seat — lock without a lease
**What happens:** Someone drapes a jacket over a library seat and leaves. Three hours later the jacket is still there,
the owner isn't, and nobody dares move it.
**In software:** a program claims something, then crashes or forgets it, and everyone else waits forever. The fix is a
lease: the claim expires unless its owner renews it.
**Don't let the reader infer:** that someone giving up is the same as the claim expiring. The fix is a rule on the
claim, not the patience of the people waiting.

### 3.5 The bus that never comes — timeout
**What happens:** Twenty-five minutes at the bus stop. "Ten more minutes, then I'm taking a rickshaw." Ten minutes
pass. You get in the rickshaw, and as it pulls away, the bus arrives.
**In software:** a program waiting for a reply sets a deadline. After it, it gives up and uses a fallback. Without one,
an app just hangs.
**Don't let the reader infer:** that the timeout was a mistake because the bus came. A timeout can't know what's
coming; it trades the risk of giving up too early for never waiting forever. Choosing the length is the hard part.
**Side example:** "I'm five minutes away." Twenty minutes later… This is why you set your own deadline instead of
trusting the estimate.

## 4. "When is it my turn?"

### 4.1 "I'll do it after these quick things." — starvation
**What happens:** Mira has one big job today: writing her best friend's wedding speech. She sits down at 9, and there's
"just one quick thing": the delivery at the door, then Mom calling, then Dev asking for help moving the sofa, then the
laundry. Each takes five minutes and each feels reasonable to do first. At midnight, the speech is a blank page.
**In software:** a scheduler that always runs short, quick jobs first can leave a big job waiting forever while small
ones keep arriving. The fixes match the ones people use: reserve time ("9 to 11 is speech time, no matter what"), or
aging, where the longer a job waits, the more it outranks the next quick one.
**Don't let the reader infer:** that the small tasks are the problem. Each is reasonable; the problem is the rule that
always lets them go first.
**Side examples:** the barber and the quick walk-ins (Episode 3); trying to get a word in at family dinner, fixed by
going round the table (round-robin, a real scheduling method).

### 4.2 ER triage — priority queue
**What happens:** You arrive at the ER at 8 with a sprained wrist. At 8:30, someone with chest pain walks in and goes
straight through. You're annoyed, and then you're not.
**In software:** a priority queue serves the most important job first, not the oldest. Your phone handles an incoming
call before a background download.
**Don't let the reader infer:** that priority alone is fair. Without care, low-priority jobs can wait forever (see 4.1
starvation). Good systems, like good ERs, let a long wait count for something.

### 4.3 "One 'are we there yet?' every 10 minutes" — rate limiting
**What happens:** A kid in the back seat asks every thirty seconds. The parent sets a rule: one question per ten
minutes. The parent's attention is what's being protected, since they're also driving.
**In software:** a service caps how many requests one caller can make in a time window, so one caller can't crowd out
everyone else. "Too many attempts, try again in 5 minutes."
**Don't let the reader infer:** that the limit is a punishment. It protects the shared resource.

## 5. "Why is this line so long?"

### 5.1 "This till's open!" — load balancing
**What happens:** One long checkout queue. A staff member opens a new till and waves the next shoppers over, and the
queues even out.
**In software:** a load balancer sends each incoming request to a server with room, so none is overwhelmed.
**Don't let the reader infer:** that shoppers choosing their own queue is load balancing. Show the person directing.

### 5.2 Four cooks, one oven — bottleneck
**What happens:** A big family dinner. Four people are chopping, mixing and ready to go, and every dish is waiting for
the one oven.
**In software:** one constrained stage (often a single database) limits the whole system. Adding more of everything
else doesn't make it faster.
**Don't let the reader infer:** that every slowdown is a bottleneck. Show the one stage everything queues for.

### 5.3 "Twenty-minute wait" (with empty tables) — backpressure
**What happens:** A busy Saturday. Half the tables are empty, and the host still says "twenty-minute wait". Why? The
kitchen is already behind; seating more people now would make everyone's food late.
**In software:** when a later stage is overloaded, it tells earlier stages to slow down rather than accept work it
can't finish. For example, an app telling you "busy, try again shortly" instead of timing out halfway.
**Don't let the reader infer:** that empty tables are wasted. The limit is the kitchen, not the room.

### 5.4 Sale-day rush — thundering herd
**What happens:** Doors open at 9 on sale day. Everyone who waited outside rushes in at the same second. Aisles jam,
staff are swamped, and nobody gets served well.
**In software:** many clients waiting for the same event all act at once and overwhelm the system: a website coming
back after an outage, with every app retrying in the same second, or tickets going on sale at exactly 10:00. The fix
is to stagger them: queue numbers, or letting people in in waves.
**Don't let the reader infer:** that it's just "busy". The damage comes from everyone starting at the same instant.

### 5.5 The government office — fail fast
**What happens:** Two hours in line. At the counter: "You're missing a photocopy of your ID. Come back tomorrow." Had
someone checked documents at the door, you'd have known in thirty seconds.
**In software:** check requirements at the start and fail immediately with a clear reason, instead of doing lots of
work and failing at the end. A form that flags a missing field right away, not after you've filled in ten pages.
**Don't let the reader infer:** that failing is the goal. The point is failing *early*, and saying why.

## 6. "How do we save time?"

### 6.1 "I need that shirt tomorrow." — batching
**What happens:** Mira waits for a full load before running the washing machine. Dev's one good shirt sits in the
basket, and he needs it tomorrow. Waiting uses fewer wash cycles, but the first item in waits for everyone else.
**In software:** grouping many small jobs into one saves overhead, at the cost of waiting while the batch fills. Real
systems send a batch when it's full or when a timer runs out, whichever comes first.
**Don't let the reader infer:** that every item waits longer. The last item in barely waits at all.

### 6.2 "Your usual?" — prefetching
**What happens:** A regular walks in, and the barista starts their oat latte before they reach the counter. Usually
that saves time. Today they wanted tea.
**In software:** loading data you'll probably need before it's asked for, like the next page of results. It's fast
when the guess is right and wasted work when it's wrong.
**Don't let the reader infer:** that software makes the drink. Tie the reveal to fetching data early.

### 6.3 "We'll buzz you when it's ready." — asynchronous work
**What happens:** At the food counter, you order, get a buzzer and sit down. You're not standing at the counter, and
the counter isn't held up by you. It buzzes when your food is ready.
**In software:** a request is accepted now and finished later, and the program is notified when it's done instead of
waiting. Standing at the counter is the "synchronous" alternative.
**Don't let the reader infer:** that the work happens faster. It takes just as long; nobody is stuck waiting on it.

### 6.4 Winter clothes into storage for the summer — hot and cold storage
**What happens:** Every spring, the winter coats, boots and sweaters go into bins in the basement, and the summer
clothes come up to the wardrobe. In autumn, the reverse. The wardrobe holds what you need now; the basement holds the
rest, cheaply and out of the way. (Hussain's example, from Canada.)
**In software:** data used often lives on fast, expensive storage ("hot"); data used rarely moves to cheap, slow
storage ("cold"), like old photos being archived. Moving between them takes effort, so it happens when needs change.
**Don't let the reader infer:** that cold storage holds copies. The items themselves move, unlike a cache (1.1), which
keeps a copy of the original.

### 6.5 The wardrobe sorted by type — indexing
**What happens:** When clothes go anywhere, finding the black shirt means searching everything. Sort them by type
(shirts here, trousers there) and you can go straight to it. The catch: every new shirt has to go in the right place.
**In software:** an index lets a database jump straight to what it needs instead of scanning everything. Adding data
gets a little slower, because the index has to be kept in order.
**Don't let the reader infer:** that indexing is free. Strictly, a database index is a separate list pointing to where
things are, like the index at the back of a book; the sorted wardrobe builds the same idea into the shelves.

## 7. "Who's allowed in?"

### 7.1 Passport and boarding pass — authentication vs. authorization
**What happens:** At the gate, the passport proves you are who you say you are. The boarding pass says which plane and
which seat. A real passport with the wrong boarding pass doesn't get you on; neither does a valid boarding pass with
someone else's passport.
**In software:** logging in proves who you are (authentication); permissions decide what you may do (authorization).
Mixing them up is a classic security hole.
**Don't let the reader infer:** that one check is enough. They're two different questions.

### 7.2 Childproofing — least privilege
**What happens:** A baby starts crawling, and the home changes. Medicines move to the top shelf, cabinet latches go on,
and snacks and toys stay low. The child can reach what they need and nothing else. (Every household does it
differently; the idea is the same.)
**In software:** give each person or program only the access its job needs, so a mistake or a stolen password can do
less damage.
**Don't let the reader infer:** that it's about distrust. It limits how much can go wrong.

### 7.3 The old flatmate still has a key — revoking access
**What happens:** The flatmate moved out a year ago. Everyone's friendly, and they still have a key that opens the front
door.
**In software:** access stays valid until someone removes it, as with old accounts or shared passwords. The safer
design is access that expires by itself.
**Don't let the reader infer:** that revoking (taking back now) and expiring (ending automatically) are the same.

## 8. "Can we change it without breaking it?"

### 8.1 "I'll just put it here for now." — technical debt
**What happens:** A shirt goes on the chair "for now". Then a bag, a charger, a jumper. Each time saves a minute. Weeks
later, finding one thing takes ten, and nobody can sit on the chair. Clearing it takes an afternoon and pays back every
day after.
**In software:** a shortcut that saves time once and costs a little extra on every later change, until someone pays it
down.
**Don't let the reader infer:** laziness. Debt often comes from reasonable choices made in a hurry.

### 8.2 Rewriting messy notes before the exam — refactoring
**What happens:** Term-time notes are scattered, out of order and full of arrows. The week before the exam, you
rewrite them: the same facts, nothing new, grouped by topic with clear headings. Every revision session after that is
faster.
**In software:** reorganizing code without changing what it does, so every future change is easier and safer.
**Don't let the reader infer:** that refactoring adds anything. "Nothing new" is the rule. (Pairs with 8.1: the messy
notes are the debt, and rewriting them pays it off.)

### 8.3 "I fixed the squeak." — regression
**What happens:** A cabinet door squeaks, so Dev adjusts the hinge. The squeak is gone, and now the door swings wide
enough to hit the fridge.
**In software:** a change that fixes one thing breaks something that used to work. It's why teams rerun old checks after
every change.
**Don't let the reader infer:** that every side effect is a regression. It's specifically something that used to work.

### 8.4 The dress rehearsal — staging environment
**What happens:** The day before the wedding, everyone walks through the ceremony in the real venue and finds the aisle
too narrow for the dress, while it's still easy to fix. On the day itself, it rains, which no rehearsal could test.
**In software:** changes are tried in a realistic copy of the live system before real users see them.
**Don't let the reader infer:** that a rehearsal catches everything. Show one thing it couldn't test.

## 9. "What if something goes wrong?"

### 9.1 "Mom, where's the…?" — single point of failure
**What happens:** Mom knows where everything is: the scissors, the spare key, the warranty card, the good tape. She goes
away for a week, and the house falls apart.
**In software:** one part (or one person) that everything depends on; when it's gone, everything stops. Teams call the
people version the "bus factor". The fix is spreading the knowledge.
**Don't let the reader infer:** that Mom is the problem. The problem is everyone depending on one place.

### 9.2 The power cut, dinner by candlelight — graceful degradation
**What happens:** The power goes. The fridge, the fan and the TV stop, but the gas stove works, so dinner still happens,
by candlelight. The house keeps its most important job going.
**In software:** when one part fails, a well-designed system keeps offering whatever doesn't depend on it. A shop still
takes orders while its recommendations are down.
**Don't let the reader infer:** that everything keeps working. What carries on must not need the broken part.
**Side examples:** the mic dies mid-speech and the speaker just talks louder; the substitute teacher's movie day; "No
naan today." "Roti then."

### 9.3 Grandma's recipe that only exists in her head — backup
**What happens:** Grandma's famous dish has no recipe; she cooks it "by feel". One holiday, a grandchild stands beside
her with a notebook, turning pinches into spoons. Years later, the family can still make it, apart from the change she
made the following year, which never got written down.
**In software:** a backup is a copy kept separately, so data can be restored after it's lost. It's a snapshot of a
point in time.
**Don't let the reader infer:** that a backup updates itself. Anything changed after the copy isn't in it. (Against
9.1: Mom is one *person* everyone depends on; the recipe is the one *copy* of something precious.)

### 9.4 The fire drill — failure drills (chaos engineering)
**What happens:** The alarm rings on a sunny Tuesday. Everyone files out, grumbling, and discovers the back exit is
locked, on a day when it didn't matter.
**In software:** companies deliberately cause failures to practise recovering. Netflix built a tool, Chaos Monkey, that
switches off its own servers during working hours so engineers find the weak spots first.
**Don't let the reader infer:** that drills prevent failures. They reveal weaknesses while it's still cheap to fix them.

### 9.5 The pill box — idempotency
**What happens:** Grandpa can't remember whether he took his morning tablet. Taking it twice is dangerous, and so is
skipping it. The family buys a Monday-to-Sunday pill box. Now "take today's tablet" is safe to do again: if today's
slot is empty, he already has.
**In software:** an idempotent operation has the same effect whether it's done once or many times, usually because each
request carries a unique label (like the day's slot) so a repeat is recognized. It's why tapping "Pay" twice shouldn't
charge you twice.
**Don't let the reader infer:** that the box prevents every mistake. It works because each dose has exactly one slot;
mix up the days and it fails.
