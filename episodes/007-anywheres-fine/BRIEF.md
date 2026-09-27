# Software in Disguise — Episode 07: Anywhere's Fine

The first episode built on the Episode 4–6 analytics (`EPISODES.md`, retention baseline): a close-up first frame,
speech and faces through the first 10 seconds, a 3–4 second reveal inside the scene, and a final gag after the reveal.
The moment comes from the book's moment lists (round 2, #45), ticked by Hussain.

## Premise

- **Everyday situation:** Dev, Mira and Jo are starving on the couch. "Where should we eat?" "Anywhere's fine." "You
  pick." "I don't mind." Everyone defers, nobody decides, and forty minutes pass. It ends when Mira makes one person
  the decider: "Jo. You choose. Nobody's allowed to argue." "Thai." They're out of the door in seconds.
- **Software concept:** leader election, the usual fix for the consensus problem.
- **Why the analogy is accurate:** big apps run on several computers that must make some decisions once and the same
  way everywhere. If every computer waits for all the others to agree, things can stall; the standard fix is for the
  group to elect one leader that decides while the others follow (and to elect a new one if it fails). The friends
  show the stall (consensus failing) and the fix (a leader). Only "leader election" is named in the Short.
- **Boundary (for the book, not the Short):** computers don't stall from politeness; lost messages and crashes are
  what make agreement hard. And even choosing the leader needs a little agreement (everyone has to accept Jo).
- **Human comic payoff:** the instant change once Jo decides: three people who couldn't move for forty minutes are
  standing with shoes on before Jo finishes the word "Thai".
- **Final gag (after the reveal):** at the restaurant, menus open. Mira: "So… what should we order?" Dev and Mira turn
  slowly to Jo. Jo, deadpan: "I'm not doing this every time."
- **Reveal (Hussain, 3–4 s):** "Computers get stuck like this too. So they elect a leader." The term on screen:
  **LEADER ELECTION**.

## Audience promise

- **Title:** `Anywhere's Fine`. Alternates: `Where Should We Eat?`, `Nobody Would Pick`.
- **Cold-open frame:** a tight three-shot on the couch, faces filling the frame, all three slumped and hungry. A
  stomach growl on the first frame. The two-line promise card at the top.
- **First spoken line (0.1 s):** MIRA: "Where should we eat?"
- **Loop:** Jo's "I'm not doing this every time" cuts straight back to the couch and "Where should we eat?". The replay
  reads as the next night.
- **Thumbnail:** `ANYWHERE'S FINE.` over the three hungry faces.
- **What a non-technical viewer gets:** "That's my friend group." Plus the idea that every group needs a decider.
- **What a technical viewer gets:** the consensus problem and leader election, in one familiar scene.

## Story beats (target about 25 s)

| Time | Shot | Dialogue | Sound |
| --- | --- | --- | --- |
| 0.0–1.6 | **S01** Tight three-shot on the couch, slumped. Promise card on top. Slow push-in. | MIRA: "Where should we eat?" | Stomach growl, then a pluck |
| 1.6–2.9 | **S02** Punch-in on Dev. | DEV: "Anywhere's fine." | |
| 2.9–4.0 | **S03** Punch-in on Jo. | JO: "You pick." | |
| 4.0–5.2 | **S04** Punch-in on Mira. | MIRA: "I don't mind." | |
| 5.2–8.4 | **S05** Three-shot. The wall clock behind them jumps from 7:00 to 7:40 (time passes inside the scene, no card). They've slid lower on the couch. | DEV (weak): "Whatever you guys want." MIRA: "I'm easy." JO: "Same." | Clock ticks under the dialogue; a bigger growl |
| 8.4–11.8 | **S06** Dev perks up, then deflates. | DEV: "What about Thai?" MIRA: "Sure, if you want." DEV: "Only if *you* want." | Hopeful pluck, then a sagging one |
| 11.8–14.6 | **S07** Mira sits up and points at Jo. Push-in on Jo. | MIRA: "Jo. You choose. Nobody's allowed to argue." | Pluck on the point |
| 14.6–16.4 | **S08** Jo, deadpan. Hard cut to all three standing at the door with shoes and jackets on. | JO: "Thai." | Whoosh on the cut; a single comic sting |
| 16.4–17.2 | Beat of silence on the doorway shot. | — | Silence |
| 17.2–21.0 | **R1** Reveal, inside the scene (below). | HUSSAIN (recorded) | Soft pad |
| 21.0–25.0 | **S09** The café set as the Thai place. Menus open. Mira looks up; Dev and Mira turn slowly to Jo. | MIRA: "So… what should we order?" JO: "I'm not doing this every time." | Pluck that leads into S01's opening pluck |

All dialogue beats keep faces on screen; no silent shot lasts longer than about 1 second before 0:10.

### Reveal (R1), inside the scene

The doorway shot freezes and dims slightly. A small mustard crown or "LEADER" tag pops above Jo, with two dotted
arrows from Dev and Mira to Jo. **LEADER ELECTION** is stamped across the lower third (inside the safe zone). No
separate explainer card, no list, no second diagram. The `SOFTWARE IN DISGUISE · 07` mark stays small in a corner.

## Hussain's reveal recording

- **Line:** "Computers get stuck like this too. So they elect a leader."
- **Alternative, if the first sounds flat:** "Computers have this problem too. Their fix? Elect a leader."
- **Delivery:** warm and a little amused, like letting a friend in on a secret. Stress **stuck** and **leader**. Aim for
  3–4 seconds.
- **Workflow:** same as Episode 6. Save the voice note as `audio/source/reveal-hussain-raw.m4a`, then `prep_reveal.py`
  (two phrases this time).

## Visual direction

- **Characters:** Dev, Mira, Jo (existing voices: am_puck, af_heart, af_nicole).
- **Settings:** the apartment living room (`kit/living_room.py`) at dusk turning to evening; the café set
  (`kit/cafe.py`) as the Thai restaurant, with a sign change.
- **New kit pieces:** a wall clock with settable hands (living room), a slumped seated pose, menus as a prop, a crown
  or "LEADER" tag overlay for the in-scene reveal, a stomach-growl sound.
- **Comic composition:** tight faces throughout; the one wide shot is the doorway (the payoff), where the contrast
  between forty minutes of slumping and instant readiness is the joke.

## Production

- [ ] Hussain approves the brief
- [ ] Kit additions: wall clock, slumped pose, menus, leader tag overlay, stomach growl
- [ ] Voices generated with the cast's established voices
- [ ] Reveal recorded by Hussain, cleaned with `prep_reveal.py`
- [ ] Full cut rendered; contact sheet reviewed at phone size
- [ ] Retention checks: close-up conflict in frame 1, speech by 0.3 s, speech and faces through 0:10, reveal ≤ 4 s,
      final gag after the reveal, runtime ≤ 30 s, loop works
- [ ] Thumbnail, subtitles
- [ ] YouTube and Instagram scheduled at the same date and time
- [ ] Ledger updated

## Packaging

- **YouTube title:** `Anywhere's Fine`
- **Description first line:** `Leader election explained through three friends who can't decide where to eat.`
- **Description:**
  > "Where should we eat?" "Anywhere's fine." Forty minutes later…
  >
  > Computers have the same problem: when several of them must agree, they can stall. The usual fix is to elect a
  > leader, one computer that decides while the others follow.
  >
  > Software in Disguise: everyday stories, software revealed.
  >
  > #programming #computerscience #SoftwareInDisguise
- **Instagram caption hook (first line):** `Every group needs one person who just decides. 🍜`
- **Instagram hashtags:** `#SoftwareInDisguise #programming #computerscience #coding #friends`
- **Pinned comment:** `Who's the one friend in your group who just decides? Tag them 👇`

## Post-publication notes (fill in 48 h after publishing)

- **Views after 48 hours:**
- **Viewed vs swiped away (Episodes 4–6: 52%, 59%, 42% stayed):**
- **Average percentage viewed:**
- **Did the short in-scene reveal hold viewers better than Episodes 4–6?**
- **Comments or confusion:**
- **Lesson for the next episode:**
