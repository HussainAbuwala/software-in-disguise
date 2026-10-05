# Software in Disguise — Episode 01 (remake): Wait, you didn't know?

Book moment 1.2 (eventual consistency). Replaces the old Episode 1 ("Two People Bought the Same Concert Seat", 163
views), which goes private when this one is published.

## What this episode tests (2026-10-04)

The Episode 2 remake fixed the hook (40.2% swiped away, the best yet) but still stopped at ~1.3K views, with a 1.1%
like rate and two stranger comments calling it AI-like and boring. So this episode changes how it looks and sounds,
and keeps the story:

1. **A new look:** risograph-zine drawing (style B, `style_test_v2.py`): curves instead of circles, pink halftone
   shading, overprinted inks, paper grain, a lived-in set; lines redraw slightly every few frames so it reads
   hand-animated.
2. **New voices:** characters voiced with Dia, a dialogue model with natural turn-taking, gasps and pauses (Hussain
   picked it over Kokoro, our old engine, and Qwen3-TTS by ear). Each scene is generated as a whole exchange.
3. **Hussain narrates** the links between scenes in plain words, like a dry sitcom narrator (no jargon). The software
   name arrives only at the end, from the same voice, so it doesn't feel like a switch to a lecture.
4. **The disguise comes off:** at the end the scene freezes and every person gets a tag (their copy of the news).
5. **Built for a reaction:** the pinned comment asks "Who finds out last in your family?"

Rejected along the way (2026-10-04): Hussain on camera, his hands on camera (he's not comfortable with either); the
tags-from-frame-1 engineer-commentary version (Hussain prefers the story).

Keep from the Episode 2 remake: conflict in frame 1, a voice at frame 0, tight shots, no promise card, a reveal of
3–4 s.

**Success:** more than ~1.5K views, or a like rate near 3% (now ~1%), or comments that answer the question.

## Premise

- **Everyday situation:** big family news spreads relative by relative. At Sunday lunch the aunt congratulates the
  couple while Grandpa, fork in the air, hears it for the first time.
- **Software concept:** eventual consistency: copies of the same data on many servers are updated one by one, so for
  a while they disagree, and eventually they all match.
- **Why the analogy is accurate:** each relative holds their own copy of the news; it reaches them at different times
  by different routes; nothing is lost, it only arrives late.
- **The limit (final beat):** it's never "done": the next update starts the lag again.
- **What the viewer must not infer:** that the news got distorted. Same news, different arrival times.

## Beats (target ~28 s)

| Time | Shot | Voices |
| --- | --- | --- |
| 0.0 | **S01** Sunday lunch. Close on Grandpa, fork in the air; the aunt's line comes from off screen | AUNT: "Congratulations!! Oh, I'm so happy for you!" GRANDPA: "…On what?" |
| 3.8 | The frame scrubs backwards: ◄◄ FRIDAY | HUSSAIN: "This is how Grandpa found out Priya got engaged." |
| 6.5 | **S02** Friday. Split screen: Priya on her phone / Mom in the kitchen | PRIYA: "Mom… guess what? I'm engaged!" MOM: (gasps) "Oh my God! Oh my God!" |
| 10.5 | **S03** Saturday. Mom bursts in; Dad on the couch behind his newspaper | MOM: "Priya's engaged! Can you believe it?" DAD (not looking up): "Mm. Nice." |
| 13.5 | **S04** The aunt, phone at her ear, already dialling the next person | HUSSAIN: "The aunt found out the way the aunt finds out everything." |
| 16.5 | **S05** Grandpa asleep in his armchair, the TV on | HUSSAIN: "Grandpa was napping. Nobody called him back." |
| 19.0 | **S06** Back at lunch, wide: Mom leans over to him | MOM: "Dad… Priya's engaged!" GRANDPA: "Oh!" |
| 21.0 | **S07** Freeze. Tags snap on: Priya `the original`, everyone `copy · updated`, Grandpa `copy · updated just now` | HUSSAIN: "Engineers call this eventual consistency. Everyone gets the news, just not at the same time." |
| 25.5 | **S08** Priya clinks her glass; every tag flips to `out of date` | PRIYA: "Also… we moved the wedding to June." MOM: (gasps) HUSSAIN: "…Here we go again." |
| ~28.5 | Cut on the gasp; it loops into frame 1 | |

## Voices

- **Characters (Dia, via mlx-audio on the Mac):** cast by scene in `dia_casting.py`: seeded takes, filtered by
  speech-to-text, length and pitch; Hussain picks one take per scene. The picked takes become the voice references
  for S06 and S08, so every character keeps one voice.
- **Hussain's narration:** dry, warm, a little amused; plain words. One WhatsApp voice note, lines in order, two
  seconds between them:
  1. This is how Grandpa found out Priya got engaged.
  2. The aunt found out the way the aunt finds out everything.
  3. Grandpa was napping. Nobody called him back.
  4. Engineers call this eventual consistency. Everyone gets the news, just not at the same time.
  5. …Here we go again.
- **Making it sound real:** room tone and cutlery under the lunch, a phone filter on Priya's side of the call, a
  newspaper rustle on Dad's "Nice", the aunt's line overlapping Grandpa's reaction, breaths left in.

## Packaging

- **YouTube title:** `Wait, You Didn't Know? | Eventual Consistency Explained`
- **Thumbnail:** the S01 close-up: Grandpa, fork in the air, "…On what?"
- **Description:**
  > Big news reaches the family one person at a time. Mom knows in seconds, Dad by Saturday, Grandpa… at Sunday lunch.
  >
  > Big apps work the same way. They keep copies of your data on many servers, and an update reaches them one by
  > one, so for a moment they disagree, and eventually they all match. That's eventual consistency. It's why a
  > friend can see your new profile photo before someone else does.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Pinned comment:** `Who finds out last in your family? 👇`

## Production

- [x] Style test (A notebook, B risograph, C chalk): B
- [x] Finished-quality frame (`style_test_v2.py`, Grandpa close-up)
- [x] Voice bake-off (Kokoro, Qwen3-TTS, Dia): Dia
- [ ] Dia casting by scene; Hussain picks takes
- [ ] S06 and S08 lines with the locked voices
- [ ] Hussain records the narration
- [ ] Riso kit (`kit/riso.py`): primitives, halftone, line boil, the five characters, the sets
- [ ] Full cut, Hussain's review
- [ ] Publish on YouTube; set the old Episode 1 to private; Instagram from the app
