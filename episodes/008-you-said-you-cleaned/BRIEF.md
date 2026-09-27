# Software in Disguise — Episode 08: You Said You Cleaned

The book's "Clean your room" moment (`book/MOMENTS.md` 2.2), in the roommate version so it uses the existing cast
and apartment. Built on the Episode 7 first read: a close-up alone didn't fix the hook (57% swiped away). The two best
openers (Episodes 4 and 5) show **a visible problem plus an accusing line**, so frame 1 here is a bulging cupboard with a
sock sticking out and Mira saying "You said you cleaned!"

## Premise

- **Everyday situation:** Mira asked Dev to clean the living room before guests come. "Done!" The floor is spotless
  because everything is under the couch and jammed into the cupboard. By his own definition he cleaned. So Mira writes
  down what "clean" means: floor clear, nothing under the couch, cupboard shuts properly. Dev reads it: "Oh. *That*
  clean." Later, every item is ticked.
- **Software concept:** acceptance criteria.
- **Why the analogy is accurate:** before building something, software teams write down concrete, checkable conditions
  for when the work counts as done. "Clean the room" is a vague request that can be "done" in ways nobody wanted; the
  list turns it into conditions both people can check, and the work is accepted when every condition is met.
- **Boundary, shown by the final gag:** criteria can't capture everything. The stuff ends up somewhere the list never
  mentioned, which is exactly what real teams run into.
- **Human comic payoff:** Dev's honest "Oh. *That* clean." He isn't lazy; he had a different picture of "done".
- **Final gag (after the reveal):** Jo walks in with an armful of Dev's things. JO (deadpan): "Why is all your stuff on
  my bed?" DEV: "It wasn't on the list."
- **Reveal (Hussain, 3–4 s):** "Software teams write this list first. It's called acceptance criteria." The term on
  screen: **ACCEPTANCE CRITERIA**.

## Audience promise

- **Title:** `You Said You Cleaned | Acceptance Criteria Explained`
- **Cold-open frame:** Mira and Dev in front of the cupboard, the door bulging with a sock poking out, a pizza box edge
  under the couch. Faces big. The two-line promise card at the top.
- **First spoken line (0.1 s):** MIRA: "You said you cleaned!" DEV (proud): "I did!"
- **Loop:** Dev's "It wasn't on the list" cuts back to Mira's "You said you cleaned!"
- **Thumbnail:** `"I DID CLEAN."` over Dev's proud face and the bulging cupboard.
- **Non-technical viewer:** "That's me (or my kid, or my flatmate)."
- **Technical viewer:** acceptance criteria and their limits, in one familiar scene.

## Story beats (target about 25 s)

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.0–2.2 | **S01** Two-shot, faces big: Mira arms crossed, Dev proud, the bulging cupboard between them with a sock poking out. Promise card. | MIRA: "You said you cleaned!" DEV: "I did!" | Pluck; the cupboard creaks |
| 2.2–4.2 | **S02** Mira points down at the couch: shoes, a pizza box and a hoodie poking out from under it. | MIRA: "Everything's under the couch!" | |
| 4.2–5.8 | **S03** Dev close-up, smug. | DEV: "The floor is clean." | |
| 5.8–7.8 | **S04** The cupboard close-up: the door strains, a sock pops out. | MIRA: "And the cupboard?" DEV (off): "Closed." | Creak, a soft thump |
| 7.8–11.0 | **S05** Mira holds a handwritten list up to camera; the three lines are readable. | MIRA: "Clean means this." | Pen scribble |
| 11.0–12.8 | **S06** Dev reads it and deflates. | DEV: "Oh. *That* clean." | Sagging pluck |
| 12.8–15.2 | **S07** Hard cut: the room is actually tidy. Mira ticks the list: three ticks, three dings. | DEV: "Done!" | Three dings |
| 15.2–19.0 | **R1** Reveal inside the scene: freeze on Mira holding the ticked list, dimmed; **ACCEPTANCE CRITERIA** stamped. | HUSSAIN (recorded) | Soft pad |
| 19.0–24.5 | **S08** Jo walks in with an armful of Dev's things, deadpan. | JO: "Why is all your stuff on my bed?" DEV: "It wasn't on the list." | Pluck that leads into S01's opening pluck |

Speech runs through the first 10 seconds; no shot before 0:10 is silent.

## Hussain's reveal recording

- **Line:** "Software teams write this list first. It's called acceptance criteria."
- **Alternative:** "Software teams agree on 'done' before they start. Acceptance criteria."
- **Delivery:** amused, like you've been Dev before. Stress **first** and **acceptance criteria**. Aim for 3–4 seconds.
- **Workflow:** same as Episode 7 (send the voice note; it becomes `audio/source/reveal-hussain-raw.*`, then
  `prep_reveal.py`).

## Visual direction

- **Characters:** Dev, Mira, Jo (existing voices).
- **Setting:** the apartment living room (`kit/living_room.py`), daytime.
- **New kit pieces:** a cupboard with a bulge / straining door and a popping sock; clutter under the couch (shoes, a
  pizza box, a hoodie); a handwritten checklist prop that can show ticks; Jo carrying an armful of clothes; a creak
  sound.
- **Comic composition:** faces and the problem in the same frame from the first second.

## Production

- [x] Hussain approves the brief
- [x] Kit additions: cupboard with strain and a popping sock, clutter under the couch (`living_room.py`);
      crossed/hips/armful hands (`cast.py`); checklist overlay and stamp size (`overlays.py`); creak (`sound.py`)
- [x] Voices generated with the cast's established voices
- [x] Reveal recorded by Hussain (one take, 2026-09-27), cleaned with `prep_reveal.py`
- [x] Full cut rendered (23.1 s); Hussain's review fix: the cupboard contents and the under-couch clutter redrawn so
      every item is recognizable
- [ ] Retention checks: visible problem + accusing line in frame 1, speech through 0:10, reveal ≤ 4 s, final gag, loop
- [x] Thumbnail, subtitles
- [x] Published on YouTube and Instagram together, Sun 2026-09-27 (playlist Software in Disguise; related video:
      Episode 7, and Episode 7 now points forward to Episode 8; not made for kids; AI use: no; paid promotion: no;
      custom thumbnail and Instagram cover; original crop; AI label off; YouTube comment pinned; the Instagram comment
      is posted and needs pinning from the app)
- [x] Ledger updated

## Packaging

- **YouTube title:** `You Said You Cleaned | Acceptance Criteria Explained`
- **Description first line:** `Acceptance criteria explained through a flatmate who swears he cleaned.`
- **Description:**
  > "You said you cleaned!" "I did!" Everything's under the couch.
  >
  > Software teams hit the same problem: a vague request can be "done" in ways nobody wanted. So before building,
  > they write down checkable conditions for "done". Those are acceptance criteria.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Instagram caption hook (first line):** `"I did clean." Technically. 🧦`
- **Instagram hashtags:** `#SoftwareInDisguise #programming #computerscience #coding #roommates`
- **Pinned comment:** `What's the most creative "clean" you've ever seen? 👇`
- **YouTube URL:** https://youtube.com/shorts/h9lDr2ownpA
- **Instagram URL:** https://www.instagram.com/theunplannedstack/reel/DdyZGjpiGOf/

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:**
- **Viewed vs swiped away (Episodes 4–7: 52%, 59%, 42%, 43% stayed):**
- **Did the visible problem + accusing line in frame 1 beat Episode 7's opener?**
- **Average percentage viewed:**
- **Comments or confusion:**
- **Lesson for the next episode:**
