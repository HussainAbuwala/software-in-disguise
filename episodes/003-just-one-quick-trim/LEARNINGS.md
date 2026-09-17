# Episode 03 production learnings

## Story and teaching

- Start with human stakes. The groom missing his wedding appointment carries the plot without requiring the viewer to know the software concept.
- Let the story set the runtime. This episode needs 50.8 seconds for three interruptions, the groom's payoff, and a readable explanation; compressing it to 30 seconds would remove causality or reaction time.
- The reveal works best as three short steps: name the concept, show a familiar consequence, then state why good software prevents it.
- A concrete printer queue is easier to grasp than a generic definition or a background phone task. “My report never prints” makes the cost of starvation immediate.

## Visual direction

- Static illustrations, hard cuts, voices, and situation-specific sound are enough for the human story. Each new still must add information through composition, expression, time, or a new arrival.
- Use motion only when it explains a changing relationship. The closing animation moves queue cards to show jobs overtaking one another; the characters, printer, and camera remain still.
- Treat the largest caption panel as occupied space before positioning any graphic. The first queue layout placed the completed jobs underneath the four-line caption. Moving the full “Printed first” strip above the panel fixed the collision.
- Inspect representative states across the whole animation with a contact sheet. Checking only the opening and final frames can miss collisions during accumulation or transition states.

## Voice and sound

- Audition voices by role with neutral IDs, then test the leading choices in the same multi-character scene. A voice that works alone may not remain distinct in dialogue.
- Choose for character fit, natural delivery, intelligibility, and separation from the other speakers. Keep the source voice, speed, licenses, and rationale recorded so the cast can be reproduced.
- Sound can imply activity that is absent from a still: the bell introduces an arrival, clippers sustain the haircut, a phone vibration changes the stakes, and paper cues make queue movement legible.

## Production workflow

- Generate lettering, captions, clocks, phone content, and explanatory graphics deterministically. Image generation should supply the illustration, not critical text.
- Keep one clearly named upload file alongside the thumbnail, subtitles, metadata, prompts, licenses, and renderer. Intermediate review cuts should not be mistaken for the upload master.
- Verify the final encode by decoding it, checking stream metadata, measuring loudness, and visually reviewing text-safe areas and every animated state.
