# Episode 02 — Production review

Full cut: 35.4 seconds, 1080×1920, H.264, 30 fps, stereo AAC at 48 kHz. Storyboard approved; video produced for review, not published.

## Implemented

- Eight locally synthesized dialogue lines with four voice identities: af_bella, am_michael, am_adam and bf_emma.
- Audio-driven open/closed mouth drawings on the sender, recipient and courier, plus blink drawings and facial reactions.
- A lowering-book pose change, a moving delivery arm, continuous apartment geography and a reverse angle that reveals the second extra bouquet.
- One-, two- and three-bouquet florist states that make the duplicate orders visible.
- A readable phone order, missing confirmation and two retry attempts.
- Burned-in dialogue captions, a separate SRT, original situational music and foley, and a closing idempotency diagram.
- A cover, publishing copy, artwork, exact generation prompts, voice metadata, source licenses and reproduction scripts.

## Checks performed

- Reviewed exported frames from every shot for composition, caption readability, visible bouquet counts, face-patch placement and the technical diagram.
- Decoded the full export successfully; verified H.264/AAC, dimensions, frame rate, duration and sample rate.
- Checked every voice line fits inside the cut and prevented source PCM clipping before export.
- Measured final encoded loudness at approximately -16.26 LUFS integrated and -1.48 dBTP true peak.

## Practical limits

This is illustrated limited animation. Mouth changes follow speech energy and cadence using two drawn poses; they are not phoneme-level lip sync. Most body poses remain held between actions. The reaction is restrained rather than broad comedy. The first line is spoken off screen while we watch the sender's response.

Frame inspection and technical audio measurements do not replace a human real-time playback and listening review for delivery, comic timing and pronunciation. No audience testing or publication is implied.
