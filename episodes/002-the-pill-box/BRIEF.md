# Software in Disguise — Episode 02 (remake): the pill box

Book moment 9.5 (idempotency), rebuilt in the code-drawn format. Replaces the published old-format Episode 2 ("He
Tried Not to Overdo the Apology", the three bouquets; 21 views).

## What this episode tests (2026-09-29)

Swipe-away sat at 57–63% for Episodes 6, 7, 8 and the 3 remake, each with a different single hook fix. This episode
changes four things at once (Hussain's call), to find out whether the hook can move at all; if it does, remove them
one at a time later.

1. **Frame 1 is the danger itself:** the pill at Mom's lips, Mira's hand grabbing her wrist, "Mom! Stop!"
2. **Tight framing:** the first three shots are close-ups (a face is about 30% of the frame height), cutting every
   1.3–2.7 s.
3. **Voice at frame 0:** "Mom! Stop!" is the first sound; the music comes in under it after the line.
4. **No promise card** ("Programmers have a name for this." is gone).

Also tested, at Hussain's request: **the reveal says why it matters**, not only the definition: one extra sentence
("It's why tapping Pay twice doesn't charge you twice.") with a small PAY × 2 → charged once diagram. This runs past
the guide's 3–4 s reveal; watch the retention graph at the reveal.

The look stays the current kit: a comic-page version of the first 14 s was rendered and compared, and Hussain chose
the current look.

## Premise

- **Everyday situation:** Mom can't remember whether she took today's pill, and "one more, to be safe" is how she
  doubled up yesterday. A Monday-to-Sunday pill box fixes it: if today's slot is empty, she took it, and checking again
  changes nothing.
- **Software concept:** idempotency: doing an operation twice has the same effect as doing it once.
- **Why the analogy is accurate:** "take today's pill" from the box is keyed by the day, like a request carrying a
  unique ID; a repeat finds the slot empty and does nothing. The blister strip has no key, so every retry is a new
  dose.
- **Why it matters (shown, not told):** retries are normal (forgetting, a lost confirmation). Without idempotency a
  retry doubles the effect (two doses, two charges); with it, retrying is safe. The reveal names the software case.
- **The limit (final gag):** it only works if each dose goes with its own day. Mom takes Thursday's now "to save
  time"; the key is wrong, so the protection is gone.
- **What the viewer must not infer:** that the box prevents every mistake.

## Beats (34.0 s with Hussain's reveal)

| Time | Shot | Dialogue |
| --- | --- | --- |
| 0.0 | **S01** Tight on Mom, pill at her lips; Mira's hand grabs her wrist | MIRA: "Mom! Stop!" MOM: "What? It's my pill." |
| 2.7 | **S01b** Mira, close, pointing | MIRA: "You already took it!" |
| 4.05 | **S01c** Mom, close, pill lowered | MOM: "...Did I?" |
| 5.45 | **S02** Two-shot; the pill goes back up | MOM: "One more won't hurt. Just to be safe." MIRA: "That's what you said yesterday!" |
| 9.6 | **S03** Top-down: the strip, three gone | MIRA: "Three gone. It's only Tuesday." MOM: "The strip doesn't say which day!" |
| 13.8 | **S04** The pill box slams onto the counter | MIRA: "Then we use this." |
| 16.4 | **S05** Next morning: the wall calendar's TUE page rips off to WED; Mira flips Wednesday's lid: empty | MOM: "...Did I?" MIRA: "Wednesday's empty. You took it." |
| 19.65 | **S06** Mom flips the lid open and shut, again and again: empty every time | MOM: "And if I forget again?" MIRA: "Check ten times. Still one pill." |
| 23.6 | **R1** Freeze on S06, dimmed; IDEMPOTENCY stamped; PAY × 2 → charged once | HUSSAIN (recorded, 5.8 s) |
| 30.5 | **S07** Mom takes the pill out of Thursday's slot | MOM: "Then I'll take Thursday's now." |
| 32.6 | **S07b** Back to frame 1's close-up, pill to her lips → loops into "Mom! Stop!" | MOM: "Saves time." |

## Hussain's reveal recording

- **Line:** "Doing it twice should only count once. That's called idempotency. It's why tapping Pay twice doesn't
  charge you twice."
- **Delivery:** light and quick; stress **once**, **idempotency** and the second **twice**. Aim for about 5 seconds
  (the stand-in takes 8).
- **Workflow:** same as Episodes 7–8: send the voice note; it becomes `audio/source/reveal-hussain-raw.*`, then
  `prep_reveal.py` (copy from Episode 08 and update the phrase times).

## Packaging

- **YouTube title:** `Did I Take It? | Idempotency Explained`
- **Thumbnail:** "“DID I TAKE IT?”" over Mom's close-up with the pill at her lips.
- **Description:**
  > "Did I take my pill?" One more, to be safe... and that's how you take two.
  >
  > A Monday-to-Sunday pill box fixes it: if today's slot is empty, you took it, and checking again changes nothing.
  > Software needs the same thing. Networks drop replies, so apps retry. An idempotent operation has the same effect
  > whether it runs once or ten times, which is why tapping "Pay" twice shouldn't charge you twice. It only works if
  > each request carries the right label, just like each pill needs the right day.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Pinned comment:** `Ever been charged twice for one order? That's a missing idempotency key. 👇`

## Production

- [x] Look test (current vs comic page): current kept
- [x] Hook v2 (the four changes above)
- [x] Voices (Mira af_heart, Mom bf_isabella)
- [x] Full cut with stand-in narrator (35.7 s)
- [x] Days made visible: Mo–Su lids, tear-off wall calendar (TUE → WED)
- [x] Hussain's reveal (WhatsApp, 2026-09-29, one take), `prep_reveal.py`; re-rendered at 34.0 s, -14 LUFS
- [x] Hussain's review
- [x] Published on YouTube 2026-09-29 ~9:30 PM ET (https://youtube.com/shorts/uQi0gcv5R54): playlist, related video
      (Episode 3 remake), custom thumbnail (had to be re-uploaded on the edit page), comment pinned; old Episode 2 private
- [ ] Instagram: web composer refused the video again; Hussain posts from the app
- [x] Ledger updated

## Post-publication notes (fill in 48 h after publishing)

- **Swiped away (Episodes 6–8 and 3R: 57–63%; Episode 5 best: 41%):**
- **Retention at the reveal (longer than the guide's 3–4 s):**
- **Lesson for the next episode:**
