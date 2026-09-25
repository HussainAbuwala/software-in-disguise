# Software in Disguise — Episode 05: He Checked This Morning

## Premise

- **Everyday situation:** Mira holds up an empty milk carton. Dev, on his phone, insists there is milk because he checked, at 7:02. Every answer he gives comes from what he saw that morning, and every one is wrong.
- **Software concept:** Stale cache.
- **Why the analogy is accurate:**
  - Dev's memory is a **cache**: a saved copy of answers, so he never has to go and look again.
  - The fridge, Jo's room and the sky are the **source of truth**.
  - Jo changes the source at 8:15 by finishing the milk. Dev's copy is never refreshed, so he keeps serving an answer that was right when it was saved.
  - The fix named in the reveal, expiring cached answers, is how real caches handle this (a time-to-live, or TTL).
- **Human comic payoff:** Thunder cracks right after Dev says "Sunny." Without looking up, he says: "It was sunny at seven."
- **One-sentence software reveal:** "That's a stale cache. An answer saved once, and never checked again. It's why a site can show you yesterday's price. Good caches expire."
- **Series variety:** Episodes 1–4 were all about concurrency. This one deliberately isn't.

## Audience promise

- **Working title:** `He Checked This Morning`. Alternates: `My Roommate Answers Everything From Memory`, `He Never Checks Twice`.
- **Cold-open frame:** Mira shaking an upside-down, empty milk carton, with one last drop falling; Dev on the couch absorbed in his phone. Rain in the window.
- **First spoken line (0.12 s):** MIRA: "You said there was milk."
- **Payoff promise overlay (0–3 s):** `Programmers have a name for this.`
- **Loop:** Mira holds up an empty mug: "Is there coffee?" Dev: "Yep. Checked." His note says COFFEE ✓ 7:02 AM. It cuts back to the empty milk carton, implying the next conversation.
- **Thumbnail:** `HE CHECKED. AT 7:02.` over Mira with the carton, Dev on his phone, and the MILK ✓ note.
- **Recurring visual device:** Dev's **memory note**, a thought bubble holding a sticky note with his answer and the time he last checked. Each wrong answer pops one up. In the reveal, the note becomes the cache.

## Story beats (final: 30.8 s with Hussain's reveal)

Times from the stand-in render; the reveal is now 0.7 s shorter. `render_episode.py` prints the exact timeline.

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.00–1.84 | **S01** Low two-shot. Mira shakes the empty carton; a drop falls. Dev on his phone. | MIRA: "You said there was milk." | Two plucks, drip; rain throughout the present |
| 1.84–3.75 | **S02** Dev close-up, eyes on phone. Note pops: MILK ✓ 7:02 AM. | DEV: "There is. I checked." | Ding, pencil scribble |
| 3.75–4.30 | Card `7:02 AM` | — | Ticks |
| 4.30–5.60 | **S03a** Fridge's-eye view: Dev looks at the full carton and nods. Note written. | — | Fridge door, hum, scribble |
| 5.60–6.15 | Card `8:15 AM` | — | Ticks |
| 6.15–8.10 | **S03b** Fridge's-eye view: Jo reaches in, drinks straight from the tilted carton (eyes closed), puts it back; the empty carton rocks; Jo smiles. | — | Gulps, hollow tonk, door |
| 8.10–9.88 | **S04** Mira close-up. | MIRA: "Is Jo still asleep?" | |
| 9.88–12.58 | **S05** Low two-shot. Note: JO: zzz ✓ 7:02. Jo walks in behind the couch and stops in the middle, waving with a mug, right beside Dev's note; Mira's eyes follow Jo. | DEV: "Fast asleep." JO: "Morning!" | Footsteps |
| 12.58–14.21 | **S06** Mira close-up, rain in the window behind. | MIRA: "Is it still raining?" | |
| 14.21–16.15 | **S07** Dev with the rainy window behind. Note: SUNNY ✓ 7:02. Lightning flash and thunder right after "Sunny." | DEV: "Nope. Sunny." | Thunder |
| 16.15–17.88 | **S08** Dev close-up, unmoved. | DEV: "It was sunny at seven." | |
| 17.88–18.93 | **S08b** Mira's blank stare and slow blink. | — | Sad trombone |
| 18.93–28.13 | **R1** Reveal graphic (below). | HUSSAIN (recorded) | Pad, dings, crumple |
| 28.85–31.54 | **S10** Low two-shot. Mira holds up an empty mug. Note: COFFEE ✓ 7:02. | MIRA: "Is there coffee?" DEV: "Yep. Checked." | Ding; pluck leads into S01's opening pluck |

Runtime is just over the 20–30 s target and under the 35 s ceiling. If retention data shows a drop in the middle, cut S06–S07 (the weather exchange) first. The milk and Jo beats carry the idea on their own.

### Reveal graphic (R1), `reveal.py`

Beats are keyed to the four spoken chunks:

1. **"That's a stale cache."** The title pops in.
2. **"An answer saved once, and never checked again."**
   - Mira asks "milk?" and Dev answers "yes!" from his note (MILK ✓ 7:02 AM).
   - The fridge's "RIGHT NOW" box says *no milk*.
   - A dashed grey arrow from Dev to the fridge is labelled *never checks*.
3. **"It's why a site can show you yesterday's price."**
   - Labels crossfade: Mira → YOU, Dev → CACHE, fridge → DATABASE.
   - The fridge's value becomes $12, and the note flips to $10 · yesterday.
4. **"Good caches expire."**
   - The note is stamped EXPIRED (with a crumple sound).
   - The arrow turns solid teal: *checks again*.
   - The note refreshes to $12 · just now, and the answer becomes $12.

## Hussain's reveal recording

- **Line:** "That's a stale cache. An answer saved once, and never checked again. It's why a site can show you yesterday's price. Good caches expire."
- **Delivery:** light and amused. Stress **stale**, **never**, and **expire**. Aim for 8–9 s.
- **Recorded:** one take, a WhatsApp voice note on 2026-09-24, kept in `audio/source/reveal-hussain-raw.m4a`.
  `prep_reveal.py` cleans it with `kit/clean_voice.py` (background noise −45 to −48 dB → −59 to −65 dB in the pauses),
  trims it to the words (1.68–10.28 s) and records measured phrase times for the captions.

## Production

- [x] Premise, analogy check, script
- [x] Kit extended: phone and milk carton props; phone, carton, wave and mug poses; confident, phone, annoyed and cheerful expressions; eyes that look down; rain in the window; memory-note overlay; Episode 05 sound effects
- [x] Voices generated with the permanent cast (`voices.py`)
- [x] Reveal graphic (`reveal.py`)
- [x] Full cut rendered (`render_episode.py`): 1080×1920 30 fps H.264, AAC 48 kHz, −14.4 LUFS
- [x] Retention checks: conflict in frame 1, speech at 0.12 s, no silent hold over 2 s, loop back into the opening
- [x] Thumbnail, subtitles
- [x] Review fixes:
  - Jo now visibly drinks from the carton (it used to fly off-screen and back).
  - "Out cold" → "Fast asleep" (the idiom was unclear, and could be misheard in a rainy scene).
  - Jo stops mid-frame with the "Morning!" bubble directly overhead, clear of Dev's bubble and note.
- [x] Reveal recorded by Hussain, prepared, re-rendered (30.8 s, −14.3 LUFS)
- [x] Uploaded and scheduled for 2026-09-25 9:00 AM EDT; ledger updated

## Packaging

- **Final title:** `He Checked This Morning`
- **Description first line:** `Stale cache explained through a roommate who answers everything from what he saw at 7:02 AM.`
- **Description:**
  > "There is milk. I checked." At 7:02.
  >
  > In software this is a stale cache: an answer saved once and served without checking again. It's why a website can show you yesterday's price. Good caches expire.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #caching #programming #SoftwareInDisguise
- **Pinned comment:** `What's the most confidently wrong thing a roommate has told you? 👇`
- **Published URL:** https://youtube.com/shorts/oroEZpeOLDs
- **Published date:** scheduled for 2026-09-25 9:00 AM EDT (uploaded 2026-09-24 with custom thumbnail; not made for kids; AI-use disclosure: No, since it's a cartoon with no real people or realistic scenes; no paid promotion)

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:**
- **Viewed vs swiped away:**
- **Average percentage viewed:**
- **Retention drop points:**
- **Comments or confusion:**
- **Lesson for the next episode:**
