# Software in Disguise — Episode 01 (remake): Wait, you didn't know?

Book moment 1.2 (eventual consistency). Replaces the old Episode 1 ("Two People Bought the Same Concert Seat", 163
views), which goes private when this one is published.

## What this episode tests (2026-10-04)

The Episode 2 remake fixed the hook (40.2% swiped away, the best yet) but still stopped at ~1.3K views, with a 1.1%
like rate and two comments calling it AI-like and boring. Hussain also feels the jump from story to software is
forced. So this episode changes the format, not the hook:

1. **Hussain's voice the whole way through:** a third-person engineer narrating his family as if it were a
   distributed system, deadpan, like a nature documentary or an incident postmortem. No synthetic voices at all;
   characters speak only in short speech bubbles.
2. **The mapping is the joke, from frame 1:** every person wears a tag with their role and their copy of the data
   (`engaged = true` / `engaged = ???`). No hidden concept and no separate reveal section, so no reveal cliff.
3. **A new look:** style B (risograph zine) from `style_test.py`: wobbly hand-drawn lines, pink and yellow fills
   printed slightly off the lines, paper grain; lines redraw slightly every few frames so it reads hand-animated.
4. **Built for a reaction:** the pinned comment asks for one ("Who's the stale replica in your family?").

Keep from the Episode 2 remake: conflict in frame 1, voice at frame 0, tight shots, no promise card.

**Success:** more than ~1.5K views, or a like rate near 3% (now ~1%), or comments that answer the question.

## Premise

- **Everyday situation:** big family news spreads relative by relative. At Sunday lunch an aunt congratulates
  the couple while Grandpa, fork in the air, hears it for the first time. By dessert, everyone knows.
- **Software concept:** eventual consistency: copies of the same data on many servers are updated one by one, so
  for a while they disagree, and eventually they all match.
- **Why the analogy is accurate:** each relative holds their own copy of "the news"; the update reaches them at
  different times through different links; reading from a copy that hasn't caught up is a stale read; nothing is
  lost, it only arrives late.
- **The limit (final beat):** consistency is never "done": a new update starts the lag all over again.
- **What the viewer must not infer:** that the news got distorted along the way. Same news, different arrival times.

## Tags (the data each person holds)

| Person | Tag |
| --- | --- |
| Priya (Mira's sister, from the Episode 3 remake) | `PRIMARY · engaged = true` |
| Mom | `replica · engaged = true` |
| Dad | `replica · engaged = true` (turns true on Saturday) |
| The aunt | `replica · engaged = true` |
| Grandpa | `replica · engaged = ???` · `last sync: Thursday`, then a STALE READ stamp |

## Beats (target ~24 s)

| Time | Shot | On screen | Hussain (voice-over) |
| --- | --- | --- | --- |
| 0.0 | **S01** Sunday lunch, tight on the aunt and Grandpa | Aunt: "Congratulations!!" Grandpa, fork in the air: "…On what?" STALE READ stamp lands on "stale" | "This is a stale read." |
| 1.6 | Rewind: the frame scrubs backwards, ◄◄ FRIDAY | Tape-rewind sound | |
| 2.6 | **S02** Friday: Priya shows the ring | Her tag writes `engaged = true` | "Friday. Priya gets engaged. That's the write." |
| 5.2 | **S03** Mom on the phone with Priya | Mom: "AAAH!" Her tag flips to `true` | "It replicates. Mom syncs in seconds." |
| 7.6 | **S04** Saturday: Mom tells Dad on the couch | Dad, not looking up: "Nice." Tag flips to `true` | "Dad syncs on Saturday. Low bandwidth." |
| 10.0 | **S05** The aunt, already on the phone to three people | Tag `true`, a little antenna on her head | "The aunt is subscribed to everything." |
| 12.2 | **S06** Grandpa asleep in his armchair, TV on | Tag `engaged = ???` · `last sync: Thursday` | "Grandpa was offline. Napping. Nobody retried." |
| 14.8 | **S07** Back to Sunday lunch, wide: every tag visible | Grandpa's red `???` among the `true`s | "So on Sunday, two copies disagree." |
| 17.0 | **S08** Mom leans over and tells Grandpa | Grandpa: "OH!" His tag flips; all tags turn green: CONSISTENT | "Mom syncs him. By dessert, everyone agrees. That's eventual consistency." |
| 21.2 | **S09** Priya, clinking her glass | Priya: "Also, we moved the wedding to June." Every tag except hers flips to `???` | "…and here comes the next write." |
| ~24 | Cut on the clink, which loops into frame 1 | | |

Bubbles stay at three words or fewer and pop in the gaps between voice-over lines, so the viewer never has to read
and listen at the same time.

## Hussain's voice-over

- **Delivery:** calm, dry and a little amused, like an engineer explaining an incident that's mildly embarrassing for
  everyone. No big energy; the deadpan is the joke. Small pause after each sentence.
- **How to record:** one WhatsApp voice note, all nine lines in order, with a two-second gap between lines. A second
  take of any line is welcome; I'll pick.
- **Lines:**
  1. This is a stale read.
  2. Friday. Priya gets engaged. That's the write.
  3. It replicates. Mom syncs in seconds.
  4. Dad syncs on Saturday. Low bandwidth.
  5. The aunt is subscribed to everything.
  6. Grandpa was offline. Napping. Nobody retried.
  7. So on Sunday, two copies disagree.
  8. Mom syncs him. By dessert, everyone agrees. That's eventual consistency.
  9. …and here comes the next write.

## Packaging

- **YouTube title:** `Wait, You Didn't Know? | Eventual Consistency Explained`
- **Thumbnail:** Grandpa, fork in the air, "…On what?", with the STALE READ stamp.
- **Description:**
  > Big news reaches the family one person at a time. Mom knows in seconds, Dad by Saturday, Grandpa… at Sunday lunch.
  >
  > Big apps work the same way. They keep copies of your data on many servers, and an update reaches them one by
  > one, so for a moment they disagree, and eventually they all match. That's eventual consistency. It's why a
  > friend can see your new profile photo before someone else does.
  >
  > Software in Disguise: everyday life, narrated by an engineer.
  >
  > #programming #softwareengineering #SoftwareInDisguise
- **Pinned comment:** `Who's the stale replica in your family? 👇`

## Production

- [x] Style test (A notebook, B risograph, C chalk): Hussain liked B
- [ ] Hussain approves the script
- [ ] Hussain records the voice-over
- [ ] Riso style in the kit (wobbly strokes, off-register fills, grain, line boil), reusable by later episodes
- [ ] Sets: Sunday lunch table, Friday (Priya), Mom on the phone, the couch, the aunt, Grandpa's armchair
- [ ] Sound: rewind, tag flips, glass clink, room tone, light music under the voice
- [ ] Full cut, Hussain's review
- [ ] Publish on YouTube; set the old Episode 1 to private; Instagram from the app
