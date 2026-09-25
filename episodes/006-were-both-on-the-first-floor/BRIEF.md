# Software in Disguise — Episode 06: We're Both on the First Floor

The first episode built on the retention baseline (see `EPISODES.md`): a three-chunk reveal of about 6 s, a larger
two-line promise card, and motion from the first frame (a slow push-in while both characters are already talking).

## Premise

- **Everyday situation:** Dev and Mira agree to meet at a two-floor café. They're on the phone, each at an identical
  window table, exactly one floor apart, and each certain they're on the first floor. The building's sign says the
  upstairs is "1" and the entrance level is "G"; Mira counts the entrance level as the first floor.
- **Software concept:** Off-by-one error. The specific cause is counting from zero versus counting from one.
- **Why the analogy is accurate:** Code usually numbers from 0 (the first item in a list is `[0]`), while people
  number from 1. When two parties use different starting points for the same sequence, they end up exactly one apart,
  and both are right by their own count. That's the most common source of off-by-one bugs.
- **Human comic payoff:** Each finally works out the other's counting ("Oh! Upstairs!" / "Oh! The entrance!"),
  and both politely say "Stay there, I'm coming!" at the same moment. Dev takes the stairs down while Mira takes the
  glass elevator up. They pass each other at the same height in slow motion, eyes on their phones, and each arrives
  where the other just was. "Okay. I'm here." "…Where?"
- **Why the floor tags:** not every viewer knows floor numbering differs by country, and without that one of them
  just looks wrong. The tags appear when the characters realize it, so they explain without spoiling the early beats.
- **Why both move:** it doesn't need to be strictly realistic, only to follow its own logic. Two people both saying
  "stay there, I'll come to you" is a familiar real-life moment. The realization lines make the cause clear, and the
  slowed-down pass makes the near-miss read as intended, not as a plot hole.
- **Reveal (about 7 s):** "That's an off-by-one error. Computers count from zero, people from one. One slip means a
  skipped item, or a crash." The last sentence is the "why it matters", kept concrete; it is the first thing to cut
  if retention data shows viewers leaving during reveals.
- **Series variety:** not a concurrency concept.

## Audience promise

- **Title:** `We're Both on the First Floor`. Alternates: `Meet Me on the First Floor`, `One Floor Apart`.
- **Cold-open frame:** the café in cross-section, Dev upstairs, Mira directly below, both on the phone. The
  two-line promise card sits at the top.
- **First spoken line (0.1 s):** MIRA: "I'm here. First floor."
- **Loop:** after the reveal, they set off again ("Coming up!" "Coming down!"), which puts them back in the opening
  positions.
- **Thumbnail:** `WE'RE BOTH ON THE 1ST FLOOR.` over the split café.

## Story beats (final: 30.7 s with Hussain's reveal; times below are from the stand-in render, R1 is now 0.2 s shorter)

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.00–1.82 | **S01** Split café, slow push-in. Dev upstairs, Mira downstairs, both on the phone, looking around. | MIRA: "I'm here. First floor." | Plucks, café murmur |
| 1.82–3.50 | **S02** Dev close-up. | DEV: "Me too. Window table." | |
| 3.50–5.24 | **S03** Mira close-up, ENTRANCE sign behind her. | MIRA: "I'm AT the window table." | |
| 5.24–7.58 | **S04** Split. Both stand and wave, exactly above and below each other. | DEV: "I'm waving!" MIRA: "So am I!" | |
| 7.58–9.08 | **S05** Dev points at the "1" sign. | DEV: "The sign says one!" | |
| 9.08–11.01 | **S06** Mira points at the entrance, under the "G". | MIRA: "The front door is right here!" | |
| 11.01–14.84 | **S07** Split. Each realizes, then both say the same polite thing at once. Floor tags pop in as each realizes: upstairs "1st floor in the UK & India", ground "1st floor in the US & Canada" (they stay up through S09). | MIRA: "Oh! Upstairs!" DEV: "Oh! The entrance!" BOTH: "Stay there, I'm coming!" | Two lightbulb dings |
| 14.84–18.14 | **S08** The swap: Dev down the stairs, Mira up the glass elevator. The pass at the same height plays in slow motion, eyes on phones. | — | Crossing slide whistles, whoosh on the pass, arrival ding |
| 18.14–21.37 | **S09** Split, swapped, looking around. | BOTH: "Okay. I'm here." MIRA: "Where?" | Womp-womp plucks |
| 21.37–29.12 | **R1** Reveal (below). | HUSSAIN (recorded) | Pad, ding |
| 29.34–30.87 | **S10** They set off again. | DEV: "Coming up!" MIRA: "Coming down!" | Footsteps; pluck leads into the opening |

### Reveal graphic (R1), `reveal.py`

1. **"That's an off-by-one error."** The title appears over a simplified two-floor building, with Dev upstairs, Mira
   downstairs and a "1 apart" bracket.
2. **"Computers count from zero, people from one."** A CODE column labels the floors 0 / 1, then a PEOPLE column labels
   them 1st / 2nd. Both "first floors" are circled: *both "first floor"*.
3. **"One slip means a skipped item, or a crash."** A list in code (`milk [0]`, `eggs [1]`, `bread [2]`): counting
   from 1 crosses out milk (*skipped!*), and one step past the end, an empty `[3]`, is marked *crash!*

## Hussain's reveal recording

- **Line:** "That's an off-by-one error. Computers count from zero, people from one. One slip means a skipped item,
  or a crash."
- **Delivery:** brisk and amused, stressing **zero**, **one** and **crash**. Aim for about 6.5 s.
- **Workflow:** save the voice note as `audio/source/reveal-hussain-raw.m4a`, copy `prep_reveal.py` from Episode 05,
  update `NOISE`, `TRIM` and the three `PHRASES` (one per sentence) from the new take, run it, then run `render_episode.py`. The
  framework reads three captions because `reveal_chunks` has three entries.

## Production

- [x] Premise, analogy check, script
- [x] Kit: two-floor café set (`kit/cafe.py`), glass elevator, stairs; phone-at-ear, wave-on-phone and
      point-on-phone poses; two-line promise card; pluggable sets in `kit.episode.scene`; a newer line from the same
      speaker replaces their previous bubble
- [x] Voices (`voices.py`), reveal graphic (`reveal.py`), full cut (`render_episode.py`): 30.9 s with the stand-in,
      1080×1920 30 fps, −14.3 LUFS
- [x] Review fixes: realization lines so the swap follows from the counting mix-up; "Stay there, I'm coming!" said by
      both at once; slow-motion near-miss (the elevator and stairs now cross at exactly the same height); a concrete
      "why it matters" line in the reveal; simultaneous lines share one subtitle
- [x] Thumbnail, subtitles
- [ ] Hussain listens and approves
- [x] Floor tags added at the realization ("1st floor in the UK & India" / "1st floor in the US & Canada")
- [x] Reveal recorded by Hussain (one take, 2026-09-25), cleaned and trimmed by `prep_reveal.py`, re-rendered: 30.7 s,
      −14.4 LUFS
- [x] YouTube: scheduled Fri 2026-09-25, 8:00 PM ET (playlist Software in Disguise; related video: Episode 05;
      not made for kids; AI use: no; paid promotion: no; custom thumbnail)
- [x] Instagram: scheduled Fri 2026-09-25, 8:00 PM ET (original crop, thumbnail as cover, AI label off)
- [ ] Ledger updated

## Packaging

- **YouTube title:** `We're Both on the First Floor`
- **Description first line:** `Off-by-one error explained through two friends who are both "on the first floor" of the same café, one floor apart.`
- **Description:**
  > "I'm here. First floor." "Me too." One of them is upstairs.
  >
  > In software this is an off-by-one error: computers count from zero, people from one. One slip means a skipped
  > item, or a crash.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Instagram caption hook (first line):** `Both on the first floor. One floor apart. 🏢`
- **Instagram hashtags:** `#SoftwareInDisguise #programming #computerscience #coding #offbyone`
- **Pinned comment:** `Where you're from, is the ground floor "1" or "0"? 👇`
- **YouTube URL:** https://youtube.com/shorts/EVcvuKnatMA
- **Instagram URL:** (appears once it goes live)

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:**
- **Viewed vs swiped away:**
- **Average percentage viewed:**
- **Retention drop points (especially: did the shorter reveal hold viewers?):**
- **Comments or confusion:**
- **Lesson for the next episode:**
