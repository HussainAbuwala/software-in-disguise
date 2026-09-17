# Episode 03 — Just One Quick Trim

Astra creative plan · 17 September 2026

## Handoff and decision record

Hussain selected the barbershop story (the “beard story”) from the episode 3 pitches. This document supplies the creative direction for GPT-5.6 Sol to implement. The story, dialogue, staging, sound arc, and voice experiment below are specified by Astra; Sol owns production implementation and technical verification. The finished performances have not yet been auditioned, and no media production or audience testing is implied by this plan.

User decisions that override older guidance in SERIES_GUIDE.md and the episode template:

- Use static images, character voices, and background/situation-specific sound. Do not animate characters, mouths, eyes, props, or cameras.
- Thirty seconds is not a requirement. Let the story breathe, then remove unnecessary time. Do not speed up speech to meet a duration target.
- The human story must work before the technical reveal. The software connection should emerge from its events.
- Experiment with voices to find a fit for each character; do not automatically reuse episode 1 or 2 casting.
- Astra owns creative planning. Sol implements this plan, documents production choices, and surfaces creative issues rather than silently rewriting the story.

The output is an unpublished episode for review. Do not upload or publish. Do not alter previous episodes. Use `episodes/003-just-one-quick-trim/` for episode assets.

## Creative thesis

A groom needs a haircut before his wedding. A friendly barber keeps fitting in apparently tiny jobs before starting his. Each exception seems reasonable; together they leave the groom permanently next. Finally he offers to turn his own haircut into a tiny job.

The emotional movement is confidence → politeness → recognition → weary ingenuity. The comedy comes from a familiar social trap: being accommodating once becomes being accommodating forever. Nobody explains a scheduling policy in dialogue.

Working title: **Just One Quick Trim**. Opening hook: **YOU'RE NEXT.** Small series label: **SOFTWARE IN DISGUISE · 03**.

Human payoff: **“What if you just cut the front? That's quick.”** He explicitly turns his full haircut into the kind of small request the barber keeps prioritizing.

Technical concept: **starvation** in scheduling. Repeatedly prioritizing short jobs can keep a longer job waiting. This is not deadlock: the barber remains busy and other customers get served. A finite story illustrates the mechanism and risk, not mathematical proof of infinite waiting.

Closing voiceover, exactly:

> “That's starvation. Imagine your report never printing because every new one-page job jumps ahead. Good software makes sure waiting work gets a turn.”

On-screen label: **STARVATION**. Supporting text: **When one job never gets its turn.** Cut from the barber's reaction to a clean printer queue. A 20-page report remains waiting while three one-page jobs slide ahead and print first. A fair-rule state then gives the report its turn. Animate only job-card order; keep the printer and background fixed. Frame the example as imaginary so the episode does not claim that ordinary printers always prioritize one-page jobs.

Technical reference: https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/6_CPU_Scheduling.html — priority scheduling and shortest-job scheduling discussion.

## Characters and performance

### Groom — audience point of view

An adult man in his early thirties, recognizably in need of a tidy-up rather than a drastic makeover. Smart casual clothes, white shirt visible inside a dark suit bag beside him. His wedding matters; he is trying to remain pleasant in a situation where complaining feels disproportionate.

Voice: clear, conversational, medium register, warm, slightly breathy if natural. Initial confidence gives way to careful restraint. The final line is a practical question delivered with tired sincerity. No shouting, exaggerated stammering, cartoon panic, or winking delivery.

### Barber — well-meaning source of the problem

An experienced adult, roughly forties or fifties. Competent and locally familiar. He believes each exception really will be quick and does not notice the cumulative effect. A slightly embarrassed glance later should preserve his humanity.

Voice: relaxed, reassuring, grounded, medium to lower register, a little warmth or texture. “You're next” is a sincere promise every time. Do not make him sneering, dishonest, or a broad accent caricature.

### Three walk-ins — short requests

1. Bearded customer: an adult man, familiar with the shop, easygoing.
2. Neckline customer: adult, a brief cleanup request; mostly seen from behind or in profile.
3. Moustache customer: older adult man, neat clothes, entirely sincere about the smallness of his request.

Give them distinguishable silhouettes and natural voices, but not subplots. Their requests are normal; the barber chooses to prioritize them. Avoid making the joke about ethnicity, age, appearance, or entitled caricatures.

### Reveal narrator

Calm, brief, observant. A separate vocal identity helps mark the closing explanation without making the barber lecture the customer. The narrator appears only after the joke has landed.

## Locked dialogue and still-image storyboard

Durations are initial editing estimates, not limits. Expect roughly 50–65 seconds including reaction space and the reveal. Adjust holds to the actual performances. Each numbered shot is an entirely static composition; changing expression requires a cut to a separate finished illustration.

| Shot | Approximate hold | Finished image and narrative information | Dialogue and sound |
| --- | --- | --- | --- |
| 1 | 4–5 s | Vertical shop establishing view. Groom at entrance with suit bag; barber by empty chair. Small series label and YOU'RE NEXT integrated in free wall space, not a separate opening bumper. Wall clock around 12:50. | Groom: “I'm getting married at two. Time for a haircut?” Door bell, subdued shop room tone. |
| 2 | 3–4 s | Medium barber, open welcoming stance toward the chair. Groom remains standing at edge of frame. | Barber: “Plenty of time. You're next.” Very short reassuring musical phrase, then it ends. |
| 3 | 4–5 s | Cut back to groom about to take the offered place, then a static entrance composition with the bearded regular. Keep eyelines and chair geography consistent. Two stills may be used within this beat. | Entrance bell leads the cut. Customer 1: “Just a quick beard trim?” Barber, off screen: “Two minutes.” |
| 4 | 4–5 s | Groom now in waiting chair, suit bag beside him. Beard customer already in barber chair in the background. Do not depict the sitting-down action. | Clippers begin before the cut and continue naturally. Groom gives a small, accepting “Sure.” Let the audience read his patience. |
| 5 | 4–5 s | Same waiting-chair composition later, clock around 1:10. A new customer is at the entrance; beard customer has gone. Groom looks up expecting his turn. | Clippers stop, entrance bell. Customer 2: “Just the neckline.” Barber: “Then you're up.” |
| 6 | 3–4 s | Groom remains waiting; neckline customer now occupies the barber chair. Same physical environment, changed occupancy and time. | Clippers resume. Brief groom exhale. Do not synthesize a fake sigh if it sounds unnatural; room tone is sufficient. |
| 7 | 4–5 s | Clock around 1:30. Close view of groom listening; next cut reveals moustache customer near the barber. Groom recognizes the pattern before responding. | Customer 3, initially off screen: “Only the moustache.” Short silence. Barber: “Won't take a minute.” |
| 8 | 3–4 s | Tight static composition: groom's phone displays “Wedding car: Outside.” Suit bag remains recognizably beside him. Avoid a messaging brand or excess UI. | One ordinary message vibration. Cut to groom looking toward the occupied barber chair; no dialogue. |
| 9 | 4–5 s | Medium groom leaning slightly forward in the waiting chair, composed rather than furious. The pose is already present when this still appears. | Groom: “What if you just cut the front? That's quick.” Deliver it as a sincere workaround, not a wink at the audience. No music under the line. |
| 10 | 2–3 s | Held reaction: barber finally understands; moustache customer remains in his chair. Mild embarrassment, no enormous eyes or slapstick face. | Clippers stop. Leave approximately 0.8–1.3 seconds of room tone after the thought lands. An optional tiny musical resolution comes afterward, not as a laugh cue. |
| 11 | 12 s | Clean printer-queue illustration. Three “1 PAGE” cards successively slide past “YOUR REPORT — 20 pages — WAITING.” Then a fair-rule label appears, the report moves to “YOUR TURN,” and the next small job waits behind it. | Narrator: “That's starvation. Imagine your report never printing because every new one-page job jumps ahead. Good software makes sure waiting work gets a turn.” Three quiet paper cues, then a resolving tone. |

The empty chair at the start establishes genuine expectation of service. The later clock changes communicate elapsed time; do not draw a moving clock. The groom never receives a partial haircut. “Just the front” is his proposed way to get started, not a reference to work already done.

If total runtime grows, first shorten redundant entrances or silent holds that convey nothing new. Preserve the first promise, all three increasingly revealing exceptions, the car message, the punchline, and the reaction before the explanation. Do not add extra jokes or explain the problem before the payoff.

## Visual direction

Use original adult editorial-comic illustration: controlled ink contours, subtle paper texture, warm cream and muted teal shop palette, natural skin tones, dark suit bag as a recurring visual anchor. Favor readable facial acting over ornamental detail. Keep a consistent illustration style across all shots; do not imitate a named living artist.

One location. Establish a simple floor plan before generating assets: entrance on screen left, waiting bench in lower left/foreground, barber chair center-right, mirror behind it, clock on the rear wall. Preserve this layout and eyelines. Do not accidentally create confusing mirror duplicates.

Create a reference sheet for groom and barber, and a single shop reference image. Lock clothing, hair, beard, accessories, lighting, bag placement, and chair design. Supporting customers need only the views used in the cut. Approve internally for continuity before making all compositions.

Aim for 9–12 finished compositions, reusing the waiting-chair environment with discrete state changes. This is an estimate, not an asset cap. The waiting-room repetition is intentional: other people make progress while his frame barely changes.

No lip sync, blinking, parallax, puppet movement, animated transitions, moving crops, pans, or zooms. Use hard cuts between completely held images. A cut to a closer fixed crop is allowed when it reveals a meaningful detail. No need to simulate smooth movement between poses.

Render text, captions, clock numerals, and phone content as clean overlays rather than relying on generated lettering. Full-screen portrait 1080×1920. Reserve caption space without covering expressions, hands, clock, or phone. Use one caption system rather than duplicating every line in both subtitles and speech bubbles. Show a speaker cue on ambiguous off-screen lines. Caption meaningful sounds when useful for accessibility.

## Voice experiments — required, before locking final dialogue

The audition is part of production, not a promise that a particular engine can deliver every performance direction. Start by checking locally available licensed voice models and the existing episode tooling. Kokoro is a baseline because it is already in this project; voice IDs from earlier episodes are examples of available prior casting, not selections for these characters. Verify the actual installed voice inventory. Do not claim controls such as emotion tags exist unless the engine supports them.

### Audition batch A: character fit

- Groom: three genuinely distinct candidate voices, each reading the opening and punchline.
- Barber: three candidates, each reading “Plenty of time. You're next” and “Won't take a minute.”
- Narrator: two candidates reading the complete reveal.
- Supporting customers: two candidate voices per role reading that role's short line. Keep this lightweight.

Use the same text and comparable perceived loudness across candidates. Label previews with neutral candidate IDs so the engine name does not bias the comparison. Save the underlying voice IDs and settings in a manifest. First compare default natural delivery; do not pitch-shift one voice into several supposed characters.

### Audition batch B: performance and chemistry

For the best two groom/barber pairings, assemble a short audio scene containing the initial promise, a walk-in request, and the final question. Compare a more restrained delivery with a slightly more anxious groom only where the engine can produce a credible difference. Keep words identical. Use natural pauses and small supported rate changes; never stretch speech merely to match a predetermined cut length.

Judge each candidate by character fit, conversational naturalness, intelligibility, distinction from other speakers, and whether the final line works without exaggerated emphasis. Character fit and naturalness take priority over novelty. Listen to complete exchanges as well as isolated lines. Check “moustache” and “starvation” pronunciation. If none is convincing, report the limitation and propose a better available voice source rather than disguising it with effects. Do not purchase services or imitate a real person's voice.

Deliver labelled audition WAVs and one comparison reel, plus a brief written casting recommendation with reasons and any audible limitations. Sol may carry the strongest provisional cast into the review cut so the whole production can be assessed. Mark it provisional; audition clips let Hussain/Astra make the final creative casting choice. Do not describe a casting choice as listened to or approved unless that actually happened.

## Sound and edit direction

Sound tells us that time and activity continue between the stills. Keep a quiet, continuous shop ambience through cuts. Use the same entrance bell signature, with ordinary acoustic variation if needed. Clippers are the central motif: they repeatedly serve someone else. Their stop creates hope; their restart defeats it.

Use sound lead-ins sparingly: the third request is heard while we are still on the groom, allowing anticipation before the new face appears. Sound changes must correspond to story events. Do not run a loud ticking clock throughout or use a stock comedy bed.

Music: brief reassurance near the opening, optional restrained transition phrase during waiting, silence under the punchline, small resolution after the reaction and beneath the reveal. Silence means room tone remains, not a digital void. Keep all effects subordinate to dialogue.

Prefer original or properly licensed audio; record provenance. Avoid reusing recognizable copyrighted film or meme audio. Retain clean dialogue stems, separate ambience/effects/music stems, and a final mix. Inspect the result on headphones and ordinary small-speaker playback where available. Target approximately -16 LUFS integrated with true peak at or below -1 dBTP as a working mix target; perceptual clarity governs the final decision.

## Sol implementation sequence and deliverables

1. Read this document and the existing series context. These newer user decisions take precedence over the old duration and animation instructions.
2. Set up the episode folder and record dialogue with stable speaker and line IDs. Inspect available voice tools and licenses.
3. Produce auditions and the provisional casting recommendation. In parallel with audio preparation, establish character and shop references; no delegated agents are required.
4. Build a full-length scratch cut from static storyboard placeholders and the provisional voices. Test whether the story is understandable with the technical reveal removed. Check that the groom appears patient, the barber sincere, and the interruptions cumulative.
5. Generate consistent final artwork using the available image-generation workflow and its required skill instructions. Implement still layouts, captions, sound, and final timing. Preserve provenance and editable sources.
6. Review the full video in real time where playback tools permit. Inspect individual frames for continuity and text, but do not represent frame inspection as a performance/listening review. Correct observable issues and document anything requiring human playback.
7. Export and verify 1080×1920, H.264, 30 fps, AAC at 48 kHz; check full decode, caption alignment, clipping, pronunciation where audible, and final metadata. The file's frame rate does not imply animated content.
8. Prepare thumbnail and packaging; keep all assets unpublished and mark the episode produced for review. Update the ledger only with the actual production status; never claim publication.

Suggested output structure:

- `README.md` — premise, status, preview links, reproduction steps.
- `audio/auditions/` — labelled candidate clips and comparison reel.
- `audio/casting.md` — choices, rationale, alternatives, provisional/approved status.
- `audio/dialogue.json` — exact text, speaker IDs, source voice IDs and settings.
- `audio/SOURCE-LICENSES.md` — voice, effects, and music provenance.
- `art/` — references and final stills; save exact generation prompts.
- `storyboard.md` — actual shot list and timing after dialogue generation.
- `deliverables/storyboard-preview.mp4` — initial scratch cut.
- `deliverables/short.mp4` — finished review cut; filename does not constrain duration.
- `deliverables/subtitles.srt`, `deliverables/thumbnail.png`.
- `REVIEW.md` — technical checks, creative observations, unresolved issues.
- Reproduction scripts plus editable caption and shot data.

Thumbnail: groom beside suit bag in the waiting chair, barber serving the bearded customer in the background. Strong visual hierarchy and one phrase, “YOU'RE NEXT.” Do not reveal STARVATION in the thumbnail. Title: “Just One Quick Trim”. Description first line: “A barbershop queue explains starvation: shorter jobs keep jumping ahead while one customer keeps waiting.” Packaging remains a draft until the final cut is assessed.

## Creative acceptance criteria

- The story makes sense and has a payoff with the closing explanation removed.
- Every interruption plausibly seems smaller than a full haircut; none feels inserted just to teach terminology.
- The repeated waiting image has changing context, rather than functioning as filler.
- Voices sound like these characters in conversation; candidates were actually generated and compared, not merely listed.
- No animated mouths, eyes, bodies, cameras, or decorative motion appear. The ending intentionally animates only the order of simple queue cards to explain starvation.
- Sound supports causality and timing; dialogue is intelligible and captioned.
- The final question receives a genuine reaction beat before the narrator starts.
- The technical reveal describes starvation accurately and introduces no competing concept.
- Runtime serves the story. No arbitrary 30-second trim or artificially fast speech.
- Review status and limitations are honest. Final creative approval remains with Hussain/Astra; production completion is not publication approval.

## Research basis

These informed Astra's approach; they are not templates to reproduce or claims about Shorts retention:

- Chris Marker's La Jetée: narrative built almost entirely from still photographs, with a brief moving-image exception. Borrow information sequencing and the changing meaning of a held image. https://player.bfi.org.uk/subscription/film/watch-la-jetee-1962-online
- City of Gold, Colin Low and Wolf Koenig: photographic history and narration, alongside contemporary footage. Borrow specific human details and a coherent environment. https://www.nfb.ca/film/city_of_gold/
- Ken Burns interview, Library of Congress: photographs and sound as storytelling material. Borrow environmental sound and attention to details; do not import camera motion into this deliberately static episode. https://lcweb2.loc.gov/static/programs/national-film-preservation-board/documents/Interview_Ken-Burns.pdf
- UIC operating-systems course notes: scheduling and starvation. https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/6_CPU_Scheduling.html

The directorial choices above are creative interpretations of the research. No audience-retention evidence has been collected for this episode.
