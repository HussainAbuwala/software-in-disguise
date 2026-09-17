# Series guide

## Core promise

The viewer sees a short comic about ordinary life, laughs at the situation, and then learns that the situation has a software name.

The series is intentionally broader than software bugs. Episodes may cover algorithms, data structures, networking, databases, security, permissions, caching, queues, distributed systems, architecture, tradeoffs, testing, reliability, or good design.

## Creative rules

- Lead with a human situation. The title and most of the episode should make sense to someone outside software.
- Keep the technical term hidden until the final reveal unless testing shows that the term improves discovery enough to justify revealing it.
- Make the comedy stand on its own. The technical explanation is the satisfying second payoff.
- Use one concept per episode and explain it in one plain sentence.
- Treat 25–35 seconds as a common outcome, not a limit. Let the story determine the runtime, preserve reaction beats, and remove only time that adds no new information.
- Prefer fully static illustrated states, character voices, and situation-specific sound. Tell a sequential story through deliberate compositions, close-ups, reactions, and hard cuts. A restrained conceptual animation is appropriate when motion itself explains the mechanism; animate the data or state change rather than decorating the scene.
- Put dialogue bubbles close to the artwork, give them clear speaker tails, and keep faces and story objects unobscured.
- Use short synthetic dialogue. Hussain's own voice remains reserved for long-form videos.
- Audition voices with neutral role IDs, compare candidates on identical lines, and test the leading cast together in a complete scene. Record the selected source voices, speeds, licenses, and rationale.
- Music must follow the scene: tension, celebration, uncertainty, silence, comic sting, and resolution as appropriate. Do not add a constant background bed merely to fill silence.
- Favor original art, voices, music, and sound effects. Use film, television, meme, or creator footage only when its license or permission clearly allows the intended use.

## Repeatable episode structure

1. **Cover hook (about 1–2 seconds):** `SOFTWARE IN DISGUISE`, episode number, and a concrete nontechnical story hook.
2. **Setup:** establish the ordinary situation immediately.
3. **Escalation:** make the problem or pattern visible through actions and reactions.
4. **Comic payoff:** land the human joke before teaching.
5. **Software reveal:** name the concept and map the story to it in one sentence.
6. **Series signature:** `SOFTWARE IN DISGUISE` and the episode number.

The reveal may add one familiar computer example and one sentence about why the concept matters. Keep both concrete and brief; their purpose is to make the term useful to a nontechnical viewer.

## Model responsibilities

Use the more capable model where judgment has the highest value, then hand a stable specification to the execution model.

### GPT-6 Astra — creative direction

- Research and select promising everyday premises.
- Choose the software concept and verify that the analogy is accurate.
- Develop the joke, characters, narrative beats, and final reveal.
- Direct the comic composition, thumbnail promise, title options, and music arc.
- Review the finished cut for clarity, originality, pace, and audience appeal.

### GPT-5.6 Sol — implementation

- Generate local voice files from the approved dialogue.
- Assemble panels, bubbles, timing, music, and sound effects from the approved brief.
- Make requested production revisions without reopening settled ideation.
- Render the video and perform routine format, duration, audio, and clipping checks.
- Keep status reports concise to conserve tokens.

The model split is a production preference, not a reason to skip creative review. Astra should still inspect the finished result before publication.

## Tools used and available

- **Built-in image generation:** create original comic pages, character-consistent panels, and thumbnails. Keep all final assets inside the episode folder.
- **Kokoro-82M with kokoro-onnx:** free local synthetic speech. Episode 1 used `af_bella`, `am_michael`, and `bf_emma`. Keep license notes with every generated voice set.
- **FFmpeg and ffprobe:** crop panels, assemble the vertical cut, mix dialogue/music/effects, encode H.264/AAC, and verify media metadata.
- **Python, Pillow, NumPy, and SoundFile:** compose frames and speech bubbles and synthesize simple original situational music and sound effects.
- **YouTube and web research:** validate search wording, competing titles, and current creator patterns. Treat autocomplete as directional evidence; exact YouTube search volume is not public. YouTube Studio's Research tab is the best account-specific source when available.

Avoid committing downloaded voice-model weights. Store them in the repository-level ignored `models/` directory and document how to obtain them from the official sources.

## Discovery and packaging

- Write a human title around the episode's situation. Put the strongest relevant phrase near the beginning.
- Keep the series name and episode number on the opening cover instead of spending title space on them.
- Put the technical concept in the first description line so search can still understand the topic.
- Use a small number of focused hashtags in the description. Keep hashtags out of the title.
- Check audience retention after publishing, especially the first two seconds, the first conflict, and the final reveal.
- Reserve the maximum caption footprint before placing story or explanation graphics. Review every animated state, not only the opening and final frames, and use a contact sheet when several objects accumulate or cross paths.

## Definition of done

- Story is understandable without the final explanation.
- Technical mapping is accurate and visible before it is named.
- Cover is legible on a phone and does not reveal the concept.
- Voices are clear, dialogue is captioned, and speakers are visually identifiable.
- Music changes with the situation and stays below dialogue.
- Video is vertical 1080×1920, H.264, 30 fps, with AAC audio at 48 kHz.
- Final video, thumbnail, sources, dialogue metadata, licenses, and episode notes are saved together.
- The final upload file has an unambiguous name and is not confused with intermediate review cuts.
- Episode ledger is updated after each production or publication milestone with the actual status.
