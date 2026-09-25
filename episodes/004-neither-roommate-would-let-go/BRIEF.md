# Software in Disguise — Episode 04: Neither Roommate Would Let Go

First episode made under the September 2026 retention and human-signal rules in [`SERIES_GUIDE.md`](../../SERIES_GUIDE.md). It also introduces the recurring cast.

## Premise

- **Everyday situation:** Dev holds the TV remote. Mira holds the only two AA batteries in the apartment. Each wants both, so each can pick the show. Neither will hand theirs over first.
- **Software concept:** Deadlock.
- **Why the analogy is accurate:** All four conditions for a deadlock are present:
  - *Mutual exclusion:* there is one remote and one pair of batteries.
  - *Hold and wait:* each keeps what they have while waiting for the other's.
  - *No preemption:* neither grabs the other's item.
  - *Circular wait:* Dev waits on Mira, and Mira waits on Dev.

  Neither can make progress, so both wait forever. This is not livelock: in livelock both would keep actively changing state, and here nobody moves.
- **Human comic payoff:** The next morning, their third roommate Jo walks past and turns the TV on with the button on the TV itself: "It has a button."
- **One-sentence software reveal:** "That's a deadlock. Each one holds what the other needs, so both wait forever. It's one reason apps freeze."

Jo's button does not solve the deadlock. It is the joke: the resource was never necessary for turning the TV on. The reveal does not claim otherwise, and the loop shows the deadlock is still in place because the channel still can't be changed.

## Audience promise

- **Search-friendly working title:** `Neither Roommate Would Let Go`
- **Cold-open frame:** two-shot on the couch. Dev and Mira each grip their item and glare at each other. The remote's empty battery compartment is visible.
- **First spoken line (starts by 0:00.3):** DEV: "Batteries. Now."
- **Payoff promise overlay (0:00–0:03, top safe zone):** `Programmers have a name for this.`
- **Loop:** the TV comes on showing golf, which nobody wants, so they need the remote again. Both tighten their grip, then a hard cut back to "Batteries. Now."
- **Thumbnail hook:** `NOBODY LETS GO.` over a tight two-shot of both gripping their items.
- **What a nontechnical viewer expects:** a petty roommate standoff and who blinks first.
- **What a technical viewer learns:** a clean picture of circular wait, the one deadlock condition people usually forget.

## Story beats (as rendered: 29.5 s final)

Times after S03 shifted by about +0.25 s when Mira's S04 line changed; `render_episode.py` prints the exact
timeline on every render.

Shot lengths follow the actual dialogue durations; `render_episode.py` prints the timeline on every render.

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.00–1.80 | **S01** Two-shot, day. Dev raises the empty remote, Mira clutches the batteries. Promise overlay at top. | DEV: "Batteries. Now." | Duel-style bass plucks |
| 1.80–3.30 | **S02** Punch-in on Mira. | MIRA: "Remote first." | Pluck on the cut |
| 3.30–5.43 | **S03** Insert: Dev's hand shaking the remote, empty slots and springs visible. | DEV: "It doesn't even work without them!" | Plastic click, plucks |
| 5.43–7.34 | **S04** Close-up, Mira smug. | MIRA: "Then why are you holding it?" | Pluck |
| 7.34–8.09 | Card `3 HOURS LATER` snaps in over the night two-shot. | — | Clock ticks ×3 |
| 8.09–9.91 | **S05a** Night, pizza box, both baggy-eyed; slow push-in. | DEV: "You could just let go." | Fridge hum |
| 9.91–11.44 | **S05b** Mira close-up, tired. | MIRA: "You first." | |
| 11.44–12.09 | Card `NEXT MORNING` | — | Birdsong |
| 12.09–14.09 | **S06** Asleep upright, heads tilted together, still gripping; floating Z's. | — | Snore duet |
| 14.09–16.29 | **S07** Wide. Jo walks in with a mug and presses the TV's own power button; golf comes on. | TV (quiet): "Lovely conditions out here this morning." | Footsteps, click, TV power-on |
| 16.29–17.09 | **S08a** Both jolt awake, staring at Jo. | — | Surprise stab |
| 17.09–18.94 | **S08b** Jo close-up, golf on the TV behind. | JO: "It has a button." | |
| 18.94–20.04 | **S08c** Dev and Mira stare blankly, then blink in sync. | — | Silence, then slide whistle |
| 20.29–27.88 | **R1** Reveal graphic. | HUSSAIN (recorded): the reveal line | Soft pad; pluck on the loop highlight |
| 27.96–29.56 | **S10** Golf on TV. They look at it, then back at each other, determined; push-in toward S01's framing. | TV (quiet): "He'll want to take his time with this one." | Pluck that leads into S01's opening pluck |

The longest hold without dialogue is S06 at 2.0 s, carried by the snoring and animated Z's.

### Reveal graphic (R1)

Built and rendered by `reveal.py`, which writes `deliverables/reveal-graphic.mp4` (7.5 s, silent) and `build/reveal-contact-sheet.png`. The graphic is animated only to show the cycle. Times below are relative to the start of the reveal:

1. **0.15 s, on "deadlock":** `DEADLOCK` pops in large, in the top safe zone.
2. **0.8–3.5 s:** four nodes (Dev, batteries, Mira, remote). Arrows grow one by one, tracing `Dev → wants → batteries → held by → Mira → wants → remote → held by → Dev`.
3. **3.9–5.3 s, on "wait forever":** a red highlight travels around the loop twice.
4. **5.3 s, on "apps freeze":** labels and icons crossfade. Dev becomes `TASK A` (a frozen app window), Mira becomes `TASK B`, the remote becomes `FILE 1`, and the batteries become `FILE 2`. The cycle stays identical, which is the point.

Optional face cameo: replace step 1's first 1.5 seconds with Hussain to camera saying "That's a deadlock." Then cut to the graphic for the rest of the voice-over.

## Hussain's reveal recording

- **Line:** "That's a deadlock. Each one holds what the other needs, so both wait forever. It's one reason apps freeze."
- **Length:** aim for 6.5–7.5 seconds. Keep the pace brisk, like explaining to a friend, not a lecture.
- **Setup:** use a phone voice memo in a small room with soft furnishings (a closet works). Hold the phone 15–20 cm from your mouth, slightly off-axis.
- **Takes:** record three: one straight, one amused, one a bit faster. The amused take usually wins.
- **Delivery:** stress **"deadlock"** and **"forever"**. Keep a small smile in the voice on "apps freeze."
- **File:** save as `audio/reveal-hussain.wav` (or `.m4a`; the renderer converts to 48 kHz).

## Visual direction

Everything is drawn in code by the shared kit in [`kit/`](../../kit); there is no image generation anywhere in the pipeline.

- **Characters:** the recurring cast, defined in `kit/cast.py`. Expressions available: neutral, angry, determined, smug, unimpressed, tired, tired_angry, asleep, shock, deadpan. Mouths move with the dialogue audio, eyes blink on a schedule, and bodies breathe.
  - **Dev** (late 20s): dark, slightly messy hair and a mustard hoodie. Expressive eyebrows; the stubborn one.
  - **Mira** (late 20s): high ponytail, round glasses, teal oversized t-shirt. A smug half-smile; the calm, immovable one.
  - **Jo** (roommate, 30ish): buzz cut, grey pajamas, big mug. Permanently unbothered. A recurring deadpan fixer.
- **Setting:** `kit/living_room.py`, a small living room with day, night and morning variants. Couch facing the camera, TV on the left edge with a visible physical power button, and a window behind the couch that shows time of day.
- **Important objects:** the remote with its battery cover off, clearly empty; two AA batteries, oversized for readability; the pizza box; Jo's mug.
- **Comic composition:** the same two-shot angle for S01, S05, S06, and S10, so the only changes are time, fatigue, and props. The repetition is the joke. Punch-ins for S02, S03, and S04.
- **Palette/style:** flat graphic comic with bold uniform ink lines and flat fills. Mustard, teal, and warm grey on an off-white wall. No bokeh, gloss, or rim light.
- **Continuity:** guaranteed by construction. The same drawing code renders every shot, and shots differ only by camera (zoom and focus), time of day, props and pose.

## Production

- [x] Premise, analogy, and script (this brief)
- [x] Character kit and set built (`kit/`)
- [x] Cast voices chosen and generated (`voices.py`, `audio/casting.md`)
- [x] Reveal graphic animated (`reveal.py`), timed to the voice-over
- [x] Full cut rendered with sound design (`render_episode.py`)
- [x] Retention checks: conflict in frame 1, speech at 0.12 s, no silent hold over 2.0 s, runtime 29.6 s, loop pluck leads back into the opening
- [x] 1080×1920 H.264 30 fps, AAC 48 kHz stereo, −15 LUFS, −1.5 dBTP
- [x] Thumbnail, subtitles, title, description, hashtags
- [ ] Hussain listens to the cut and confirms the cast voices (they become permanent)
- [x] Reveal recorded by Hussain (one take), denoised, trimmed, and caption-timed; re-rendered at 29.5 s
- [x] Mira's S04 line changed to "Then why are you holding it?" (clearer than "Then you won't miss it.", and it previews hold-and-wait)
- [ ] Published; ledger updated

## Packaging

- **Final title:** `Neither Roommate Would Let Go`. Alternates: `The Remote Had No Batteries`, `Remote vs. Batteries. Nobody Blinked.`
- **Description first line:** `Deadlock explained through two roommates, one remote, and the only batteries in the apartment.`
- **Description:**
  > Dev has the remote. Mira has the batteries. Neither will go first.
  >
  > In software this is a deadlock: two tasks each hold something the other needs, so both wait forever. It's one reason apps freeze.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #deadlock #programming #SoftwareInDisguise
- **Pinned comment (drives replies):** `What's the pettiest standoff you've had with a roommate? 👇`
- **Published URL:**
- **Published date:**

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:**
- **Viewed vs swiped away (compare to Ep 01–03):**
- **Average percentage viewed (above 100% = loop working):**
- **Retention drop points:**
- **Comments or confusion:**
- **Lesson for the next episode:**
