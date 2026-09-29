# Software in Disguise — Episode 03 (remake): Just One Quick Thing

The book's "I'll do it after these quick things" moment (`book/MOMENTS.md` 4.1), rebuilt in the code-drawn format. It
replaces the published Episode 3 ("Just One Quick Trim", the barber), which gets set to private when this one goes
live. The old folder was deleted from the repo on 2026-09-27 (it is still in git history).

Two tests, one per metric, so they don't confound each other:

1. **Hook (swipe rate): name the concept in frame 1.** Hussain's experiment (2026-09-27): does showing the term
   up front, while saying it will be explained through an everyday situation, create curiosity ("how is a blank wedding speech
   *starvation*?")? The promise card changes from "Programmers have a name for this." to three lines:
   **"Software concept: / STARVATION / explained with everyday life."** This deliberately breaks the
   guide's "keep the term hidden until the reveal" rule, as a one-episode test; the guide changes only if it wins.
   Frame 1 is also a close-up (one face + one prop showing the problem: Mira over a blank WEDDING SPEECH notepad),
   but that composition is the same as Episodes 4–5's (41–48% swiped on YouTube, 18.6–21.2% skipped on Instagram),
   so a result clearly outside that range points at the label.
2. **Follows (end):** a one-line reason to follow over the last beat. Baseline: about 0.5 follows per 1,000
   Instagram views (8 follows on roughly 17.6K views, Episodes 4–8).

The series label stays on the thumbnail only, as before; removing it is a later test because it also changes frame 1.

## Premise

- **Everyday situation:** Mira has one big job: her best friend's wedding speech, due tomorrow. All evening, "just
  one quick thing" keeps arriving: Dev needs help with the sofa, Mom calls, the laundry beeps. Each takes a few
  minutes and each is reasonable to do first. At 11:58 PM the page is still blank.
- **Software concept:** starvation (scheduling).
- **Why the analogy is accurate:** Mira is a single worker (one CPU). Her rule is "quick things first", which is
  shortest-job-first scheduling. The speech is ready to run the whole time, but short jobs keep arriving and the rule
  always picks them, so the long job waits indefinitely. That is starvation. The standard fixes match what people do:
  reserve a time slot for the big job, or let a job gain priority the longer it waits (aging).
- **What the viewer must not infer:** that the small tasks are the problem. Each one is reasonable; the rule that
  always lets them go first is the problem. Jo's line says exactly this.
- **Boundary, shown by the final gag:** a reserved slot only works if something enforces it. Dev reads the sign and
  asks anyway.
- **Human comic payoff:** Mira at 11:58, flat: "The wedding is tomorrow." A beat of silence.
- **Final gag (after the reveal):** Mira tapes "9–11 SPEECH ONLY" to the wall. Next morning at 9:00, Mira writes
  "Dear—", Dev leans in, reads the sign, and says "Just one quick thing—", which cuts back to frame 1.
- **Reveal (Hussain, 3–4 s):** "If quick jobs always go first, the big one never runs. That's called starvation."
  The term on screen: **STARVATION**. Since the term is already named in frame 1, the reveal now *explains* it rather
  than introducing it; the line works for both.

## Audience promise

- **Title:** `Just One Quick Thing | Starvation Explained`
- **Cold-open frame:** close two-shot. Mira on the couch, the notepad on her knee facing camera (WEDDING SPEECH,
  blank), Dev leaning in from the side. Wall clock at 6:00. Faces big. The card at the top names the concept
  and ties it to everyday life: "Software concept: / STARVATION / explained with everyday life." (the
  experiment; held about 3.4 s so the three lines can be read).
- **First spoken line (0.1 s):** DEV: "Just one quick thing—" MIRA: "It's been quick things all day!"
- **Loop:** Dev's "Just one quick thing—" at 9:00 AM cuts to the same line at 6:00 PM in S01.
- **Follow line (change 3):** over the last ~1.2 s, a small text overlay, no voice, so the loop stays clean:
  `Your life is full of software. Follow for the next one.`
- **Thumbnail:** `"ONE QUICK THING."` over Mira's frustrated face, the blank WEDDING SPEECH notepad and Dev leaning in.
- **Non-technical viewer:** "That was my whole Sunday."
- **Technical viewer:** shortest-job-first starving a long job, and why reservations and aging exist.

## Story beats (about 30 s with Hussain's reveal)

Revised 2026-09-27 after Hussain's review of the first draft: every quick thing is now **shown being done**, the
wedding speech is set up in frame 1 (the invitation on the desk plus Mira's line), Mom is on screen (split screen),
the notepad lies flat on a desk, and the page is shown top-down. "Hi, Mom" became "Yes, Mom?" (it sounded like "Thai
Mom"), and Mom's "Beta" became "Sweetie" so the line isn't tied to one culture; all changed lines were checked
with a speech recognizer. Mom's quick thing is "did you eat?", the call that's never quick.

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.0–3.5 | **S01** Mira writing at her desk, a PRIYA & SAM invitation standing on it; Dev leans in from the door. Card: "Software concept: / STARVATION / explained with everyday life." | DEV: "Just one quick thing—" MIRA: "I'm writing Priya's wedding speech!" | Pluck, pen scribble |
| 3.5–5.4 | **S02** Quick thing 1: Mira and Dev carrying the sofa (6:40 on the living-room clock). | DEV: "Just two minutes!" | Scrape |
| 5.4–10.6 | **S03** Quick thing 2: split screen, Mom in her kitchen on top, Mira at the desk below. After the question, the clock spins 8:15 → 9:20 while Mom keeps talking ("…and another thing…") and Mira droops. | MIRA: "Yes, Mom?" MOM: "Sweetie, one quick thing… did you eat?" | Phone buzz; phone chatter and fast ticks under the time jump |
| 8.8–11.1 | **S04** Quick thing 3: the washing machine says END; Mira with an armful of laundry. | MIRA: "Laundry. Two minutes." | Beeps |
| 11.1–13.3 | **S05** Top-down: the page, still blank under its title. | MIRA (off): "The wedding is tomorrow." | Clock ticks |
| 13.3–14.3 | **S06** Mira at the desk, 11:58 on the clock. A beat of silence. | | Ticks, a low pluck |
| 14.3–19.0 | **S07** Jo in the doorway, deadpan. | JO: "Every one of those was quick." "So they always went first." | |
| 19.0–~24 | **R1** Freeze on S06 (Mira, 11:58), dimmed; **STARVATION** stamped. | HUSSAIN (recorded) | Soft pad |
| | **S08** The fix: Mira presses "9–11 SPEECH ONLY" onto the wall herself (moved from Jo after review: his reach read as a hand on his chin, and the sign was already up before you noticed it). | MIRA: "Tomorrow. Nine sharp." | Tape rip |
| | **S09** Top-down, 9 AM: "Dear Priya," being written. | | Scribble |
| | **S10** Dev walks in, reads the sign, and asks anyway. Follow line overlaid. | DEV: "Just one quick thing—" | Pluck into S01 |

## Hussain's reveal recording

- **Line:** "If quick jobs always go first, the big one never runs. That's called starvation."
- **Alternative:** "Quick jobs kept cutting in line. In computers, that's called starvation."
- **Delivery:** sympathetic, like you've had that day. Stress **always** and **starvation**. Aim for 3–4 seconds.
- **Workflow:** same as Episodes 7–8 (send the voice note; it becomes `audio/source/reveal-hussain-raw.*`, then
  `prep_reveal.py`).

## Visual direction

- **Characters:** Mira, Dev, Jo (existing voices). **New: Mom** (`cast.MOM`: greying bun, plum kurta; voice
  `bf_isabella`, picked by Hussain from a 5-voice audition).
- **Settings:** Mira's desk corner (new `kit/study.py`), the living room (sofa lifted), Mom's kitchen (new
  `kit/kitchen.py`), a laundry corner (new `kit/laundry.py`), and a top-down page (`overlays.page_closeup`).
  Evening → night → next morning, shown in the window and on the wall clock.
- **New kit pieces:** the desk corner with a wedding invitation and a wall sign spot (`study.py`); Mom, a bun
  hairstyle, `write` and `carry` poses and seated legs (`cast.py`); a carried sofa (`living_room.sofa_lifted`); the
  kitchen and laundry sets; the top-down page with stroke-by-stroke writing (`overlays.page_closeup`); beep, buzz,
  scrape and tape-rip sounds. (`cast.notepad_on_lap` from the first draft stays in the kit but isn't used here.)
- **Comic composition:** faces, the desk and the invitation in the same frame from the first second.

## Production

- [ ] Hussain approves the brief
- [x] Mom voice audition; Hussain picked mom-E (`bf_isabella`)
- [x] Kit additions: notepad on a lap (`cast.notepad_on_lap`), pleading/frazzled faces (`cast.py`); movable clock and
      door sign (`living_room.py`); beep, buzz, scrape, tape rip (`sound.py`); custom promise-card text
      (`overlays.py`); device voices, subtitled off-screen speakers, aimed bubble tails and a `props` layer
      (`episode.py`)
- [x] Voices generated with the cast's established voices (Mom: `bf_isabella`, phone-filtered)
- [x] Reveal recorded by Hussain (one take, 2026-09-27, 4.45 s after trimming), cleaned with `prep_reveal.py`
- [x] Full cut rendered: 32.3 s with Hussain's reveal (draft 4, after three review rounds)
- [ ] Retention checks: face + prop problem and the named concept in frame 1, speech through 0:10, reveal ≤ 4 s, final gag, loop, follow
      line inside the safe zone
- [ ] Thumbnail, subtitles
- [x] Published on YouTube Sun 2026-09-27 ~7:45 PM ET (playlist Software in Disguise; related video: Episode 8, and
      Episode 8 now points forward to this one; not made for kids; AI use: no; paid promotion: no; custom thumbnail;
      comment pinned). Old Episode 3 set to private at the same time.
- [x] Instagram: posted by Hussain from the app (the web composer refused video uploads that evening)
- [x] Ledger updated (analytics 2026-09-29)

## Packaging

- **YouTube title:** `Just One Quick Thing | Starvation Explained`
- **Description first line:** `Starvation explained through a wedding speech that never gets written.`
- **Description:**
  > "Just one quick thing." The sofa, Mom, the laundry. At midnight the wedding speech is still blank.
  >
  > Computers hit the same problem: if a scheduler always runs the quick jobs first, a big job can wait forever
  > while new small ones keep arriving. That's starvation. The fixes look familiar: reserve time for the big job, or
  > let a job gain priority the longer it waits.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Instagram caption hook (first line):** `"Just one quick thing." Said everyone, all day. 📝`
- **Instagram hashtags:** `#SoftwareInDisguise #programming #computerscience #coding #procrastination`
- **Pinned comment:** `What's the "quick thing" that always eats your day? 👇`
- **YouTube URL:** https://youtube.com/shorts/o2DTWqOxXnY

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:** 1,238 on YouTube (read 2026-09-29, ~2 days); 94.6% from the Shorts feed
- **YouTube swiped away (Episode 5 best: 41%) / Instagram skip rate (Episode 5 best: 18.6%):** 62.7% swiped (worst of
  the code-drawn episodes) / Instagram not read yet
- **Did naming the concept in frame 1 help or hurt the hook?** Hurt. Same close-up composition as Episodes 4–5
  (41–48% swiped), 62.7% here. The biggest drop is at 0:03–0:05, exactly when the card leaves.
- **Follows per 1,000 views (baseline ~0.5 on Instagram):** YouTube 0 subscribers from 1,238 views; Instagram not read
- **Average percentage viewed:** ~60% (0:20 of 0:33); stayed to watch 36.7%
- **Comments or confusion:** none yet
- **Lesson for the next episode:** keep the term hidden until the reveal (the guide rule stands). The reveal was not a
  cliff this time, so the in-scene reveal works; the problem is the first 5 seconds.
