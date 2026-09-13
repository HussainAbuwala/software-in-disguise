# Episode 02 — One apology. Three deliveries.

Status: full 35.4-second voiced cut produced for review. Storyboard approved by Hussain. Not published.

## Watch and review

- [Full episode](deliverables/short.mp4)
- [Cover](deliverables/thumbnail.png)
- [Dialogue subtitles](deliverables/subtitles.srt)
- [Production review](REVIEW.md)
- [Title and description](PACKAGING.md)

The cut uses illustrated limited animation: audio-driven mouth poses, blinks, a lowering-book gesture, an approaching delivery arm, and reaction keyframes. It does not use continuous full-body animation or phoneme-level lip sync.

## What changes from Episode 1

Episode 1's documented story gives two strangers a shared problem, explains it in flashback, and supplies an usher's stool joke. This is a script-level assessment, not an audience-retention finding. No analytics are available in the repository.

This episode gives the protagonist an intention that the outcome contradicts. A restrained apology becomes an excessive gesture. The recipient's initial warmth matters: the gesture was working before the duplicates arrived. The joke is the reversal of that small success, rather than a separate witty remark.

Visually, test full-bleed connected staging, warmer dimensional lighting, readable eye lines, moving foreground props, and held reactions. Preserve the adult illustrated identity. The look test is limited animation, not evidence of finished character animation or lip sync.

## Premise

After being told he turns every disagreement into a grand gesture, a man orders one modest bouquet with the note: “I'm learning not to overdo it.” The order confirmation never arrives. He retries twice. The florist processes all three attempts. His partner appreciates the first bouquet—until the next two appear.

The sender means well. The recipient is initially receptive. Neither should be played as foolish or cruel. His discomfort with uncertainty drives the choice that defeats his intention.

- Working title: **He Tried Not to Overdo the Apology**
- Cover hook: **ONE APOLOGY. THREE DELIVERIES.**
- Concept: idempotency, introduced as the missing protection against duplicate effects when retrying an order.
- Reveal: “Idempotency means retrying the same order doesn't create another bouquet.”
- Mapping: one intended purchase, a missing response, repeated attempts, multiple fulfilled orders.
- Accuracy: a missing confirmation does not establish that the order failed. Identical contents alone do not prove two purchases are the same intent. A real implementation needs a stable request identifier and correct handling of duplicates. Do not label the flawed florist behavior itself “idempotent.”
- Technical reference: [AWS Builders' Library — Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).

## Approved storyboard — produced as a 35.4-second cut

| Time | Action and performance | Dialogue / text | Sound |
| --- | --- | --- | --- |
| 0–3 | She gently pushes an absurdly elaborate apology scrapbook back toward him. He stops halfway through unveiling a matching banner. The series label is small over the action. | Her: “You don't have to make everything a grand gesture.” | Paper movement; he stops mid-flourish. |
| 3–6 | Alone later, he removes the extravagant upgrade from a flower order and chooses one small bouquet. A deliberate, hopeful decision. | Him: “Okay. One little bouquet.” | One restrained musical phrase. |
| 6–9 | Close on the note he types. Match cut to the florist printing that same note and preparing the order. | Note: “I'm learning not to overdo it.” | Typing; paper printer. |
| 9–14 | His screen says “Confirmation unavailable.” He waits, checks the time, then taps “Retry.” Cut to a second florist order. Another pause and another tap create a third. The audience sees the mistake before he does. | Him, quietly: “Did it go through?” | Music becomes uncertain; two taps and two printer cues. |
| 14–17 | At her apartment, she receives the first bouquet, reads the note, and softens. Do not rush this moment. | Her: “That's actually sweet.” | Warm room tone; paper rustle. |
| 17–23 | A second bouquet enters from the doorway. Her eyes move from the bouquet to the courier; her smile fades. A cut reveals a third bouquet waiting beside the courier. | Courier: “And these two.” | Paper movement, then an awkward silence. |
| 23–26 | Close on the identical notes. Back to her, surrounded by flowers, reading the promise again. | Her, dry: “Not to overdo it.” | No comic music until after the look. |
| 26–33 | Keep the flowers on screen. Label the missing safeguard, then visually group the three attempts beneath ONE order identifier and one bouquet. End with the series signature. | “The missing safeguard? Idempotency. Retrying the same order shouldn't create another bouquet.” | Quiet resolving phrase. |

## Earlier eight-second sample scope

An excerpt centered on the second delivery, with a silent visual performance and timed captions. The first warm reaction turns into a deadpan stare as an animated courier arm offers another identical bouquet. A brief crop closer to her expression tests emotional readability. Paper foley and a door knock give objects weight. The sample does not attempt a full handoff: the courier continues to hold the bouquet. No unsourced voices or temporary dialogue presented as final performances.

The third bouquet remains a full-episode beat; the sample isolates one exchange so its acting can be evaluated clearly.

## Production decisions and review gates

- Consistent light direction and apartment geography; doorway stays screen right.
- Animate anticipation, approach, overshoot, and settle on the offering arm. Avoid a constant zoom standing in for acting.
- Change her expression in response to the object arriving, not before.
- Keep her first bouquet physically anchored in both hands.
- Leave room for the audience to read the response before the next line.
- Captions stay in the bottom safe area and do not cover the hands or face.
- Before full production, assess whether the expression transition feels like acting. If it reads as two drawings dissolving, commission/generate additional breakdown poses or move to a proper character-animation pipeline.
- The full cut adds dialogue performances and audio-driven mouth animation. The delivery arm offers the flowers; the sequence cuts before a full handoff. Kokoro weights were located in the earlier Episode 1 workspace and used locally without committing model files.
- Keep the episode marked produced for review until publication.

## Assets and reproduction

Artwork generated with the built-in image generation tool. Sample prompts are in `prompts.json` and `blink-prompt.txt`; full-production prompts are in `production-prompts.json`.

Requirements: Python with Pillow, NumPy, SoundFile and kokoro-onnx; FFmpeg and ffprobe. Set `KOKORO_MODEL_DIR` to a folder containing `kokoro.onnx` and `voices.bin`, or place them in the repository-level ignored `models/` folder.

1. Run `voices.py` to regenerate dialogue when needed.
2. Run `render_episode.py` to assemble the full cut, mix sound, export subtitles and run metadata checks.
3. Run `package_episode.py` to generate the cover.

`render_sample.py` preserves reproduction of the original silent look test. All generated-art compositing uses FFmpeg. Python creates original typography, phone-screen graphics and sound. Build intermediates are ignored.

## Opening revision

A 1.4-second Episode 1-style title card now precedes the complete 34-second story. The main render script adds it automatically through `add_intro.py`. `deliverables/opening.png` is the opening frame; `story-cut.mp4` preserves the story without the card. Subtitles are shifted by 1.4 seconds.
