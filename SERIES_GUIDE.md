# Series guide

## Core promise

> *You've already lived it. Programmers just have a name for it.*

Everyday situations often behave the way software does. The viewer recognizes a moment from their own life ("that's
happened to me"), then learns that it has a software name. Recognition comes first and the lesson rides along with it:
nobody should feel taught.

- **Recognition is the test.** Before anything else, ask whether a viewer who doesn't program has lived this, or could
  easily picture it. Start from real, lived situations and find the software behavior they match, not the other way
  round. Stories invented to fit a concept tend to feel like textbook examples.
- **Humor is a strong bonus, not the requirement.** In Shorts, a laugh keeps people watching and makes the series fun,
  so aim for one wherever the situation allows. It never replaces recognition.
- **The mapping must be true.** Getting it right is what makes the series teach something; a mapping that's only cute
  just decorates. See the accuracy rule under Creative rules.

The series is intentionally broader than software bugs. Episodes may cover algorithms, data structures, networking, databases, security, permissions, caching, queues, distributed systems, architecture, tradeoffs, testing, reliability, or good design.

Not every story has to be a disaster. A Short needs **a question in frame 1**, and several kinds of story create one:

| Mode | The question | Example |
| --- | --- | --- |
| Mishap | Why is this going wrong? | Both "on the first floor", one floor apart (off-by-one) |
| Clever trick | How do they pull that off? | A coat check never mixes up 300 coats (key → value) |
| Trade-off | Which way is right? | One trip with a full tray, or one glass at a time (batching vs. latency) |
| Curiosity | How does that even work? | Finding your row in a dark cinema by asking the person in front (recursion) |

Mishaps are the most reliable hook so far (Episodes 1 and 4–6), and their retention data is the baseline. Test the
other modes against it before relying on them.

## Retention rules (September 2026 revision)

Episodes 1–3 averaged 72 views. Episode 1, the only one whose first frame showed the conflict, received about six times the views of the other two. Most Shorts views come from the swipe feed, so the first second decides whether anything else is seen.

- **The first frame is the conflict, in close-up.** No title card, series card, or episode number at 0:00. Open on the moment the problem is already visible: two people holding one ticket, two hands gripping one object, a person staring at three bouquets. Faces must be big enough to read on a phone: Episode 6's wide cross-section with two small figures had the most swipe-aways of Episodes 4–6 (58%), although its story held viewers best.
- **Speech starts within 0.3 seconds.** The first line is mid-argument, not setup. "Excuse me, that is my seat" works; "You don't have to make everything a grand gesture" does not.
- **Promise the payoff on screen from 0:00 to about 0:03 without naming it.** From Episode 6 this is a large two-line mustard card, `Programmers have / a name for this.` (`promise_size = 64`); Episodes 4–5 used a small one-line pill. The term itself stays hidden until the reveal. The line gives nontechnical viewers a reason to stay and tells technical viewers there is a payoff.
- **Speech and faces through the first 10 seconds.** No silent inserts, time cards or flashbacks before about 0:10: Episode 4's wordless close-up of the remote (0:03) and Episode 5's time cards and silent flashback (0:04–0:08) are where those episodes lost their early viewers. Show time passing inside the scene (a wall clock, lower light) while people keep talking.
- **Change the picture at least every 2 seconds.** Hard cut, punch-in on a face or object, a new time card, or a new arrival. A still that holds longer than about 2.5 seconds must be carrying a dialogue beat.
- **Target 20–30 seconds; 35 seconds is the ceiling.** If the story needs more, cut an escalation step rather than slowing the pace. Three interruptions can become two. Episode 3's 50.8 seconds is not a precedent.
- **Reveal in 3–4 seconds, inside the scene.** One or two sentences: name the concept and give one fact. The characters stay on screen (freeze frame, term stamped over them, a tiny diagram at most) instead of cutting to a separate explainer card. The reveal was the biggest exit point in Episodes 1 and 4–6: Episode 6 held about 83% through its story and lost about half of them in a ~7.5 s card reveal; Episode 5's four-sentence reveal ended at about 16%. The "why it matters" line goes in the description or pinned comment.
- **Reward staying past the reveal.** A final gag comes after the reveal, then the loop, so viewers learn that the end is worth reaching.
- **End on a loop.** The final beat either cuts straight back to the opening conflict or restarts a new version of it, so the replay feels intentional. No end card longer than 1 second.
- **Mobile-safe captions.** Keep all text inside the Shorts safe zone. Leave the bottom 20% and the right 15% clear of important text.

## Human signal (not AI slop)

AI illustration combined with synthetic voices is the pattern viewers swipe past fastest. Every episode must carry obvious signs of a human author.

- **Hussain's real voice delivers the reveal.** The story characters may stay synthetic. The reveal ("That's a deadlock...") is recorded by Hussain, so the teaching moment has a person behind it and connects the Shorts to the long-form channel.
- **Optional face cameo, recommended once the format stabilizes.** A 1–2 second clip of Hussain to camera delivering the concept name, with the illustrated scene continuing behind or after it. The real face is the strongest trust signal the series has.
- **Recurring cast.** From Episode 4, stories take place in one world centered on Dev, Mira and Jo. A recurring cast reads as intentional authorship. It lets returning viewers recognize the series before any text appears, and each new episode reuses the same character kit. **The situation decides the cast and the setting, never the other way round.** The world grows to fit the moment: family (parents, a grandparent, a younger sibling), coworkers, neighbors, strangers, and any place the story needs, whether an office, a wedding, a car or an airport. The core trio appears when they fit, not in every episode. A new character or set is added to `kit/` once and reused from then on.
- **Code-drawn art, no image generation.** From Episode 4, every frame is drawn by the shared kit in `kit/`: bold uniform ink lines, flat color fills, a limited palette, simple backgrounds, and exaggerated but consistent expressions. This rules out generative tells (wrong fingers, melted objects, squiggle text, characters that change between panels), and characters stay identical across episodes by construction. Fewer details, more personality.
- **Small signs of life.** Mouths move with the dialogue audio, eyes blink, bodies breathe, and cameras push in. A still frame with a blinking, breathing character reads as animated and intentional.
- **Deliberate comic timing through sound.** A well-timed silence, a clock tick, or a single comic sting reads as human judgment. A constant music bed reads as automation.
- **Write the jokes, don't generate them.** Every line of dialogue should sound like something a specific person would say. Read it aloud; cut any line that sounds like a caption.

## Creative rules

- Lead with a human situation. The title and most of the episode should make sense to someone outside software.
- **Moments first.** Pick moments people have really lived (the book's moment lists in `book/UNSURE.md` are the source), then map a concept onto them. Stories invented to fit a concept feel forced.
- **No screens in the story.** If the moment happens in an app, a website, an online order or a digital list, the software is showing and the disguise fails. Phones can be props; the behavior must happen offline.
- Keep the technical term hidden until the final reveal. Promise that a term is coming (see Retention rules), but do not name it.
- Make the story stand on its own for someone who doesn't program: recognizable first, funny wherever possible. The technical explanation is the satisfying second payoff.
- Use one concept per episode and explain it in one plain sentence.
- Verify that the analogy is technically accurate before writing jokes. If the story matches a neighboring concept better (for example, polite doorway dancing is livelock, not deadlock), change either the story or the concept.
- Prefer fully static illustrated states, character voices, and situation-specific sound. Tell a sequential story through deliberate compositions, close-ups, reactions, and hard cuts. A restrained conceptual animation is appropriate when motion itself explains the mechanism; animate the data or state change rather than decorating the scene.
- Put dialogue bubbles close to the artwork, give them clear speaker tails, and keep faces and story objects unobscured.
- Use short synthetic dialogue for story characters. Hussain records the reveal (see Human signal).
- Once the recurring cast has voices, keep them. Audition only for new characters: use neutral role IDs, compare candidates on identical lines, and test them in a scene with the existing cast. Record the selected source voices, speeds, licenses, and rationale.
- Music must follow the scene: tension, celebration, uncertainty, silence, comic sting, and resolution as appropriate. Do not add a constant background bed merely to fill silence.
- Favor original art, voices, music, and sound effects. Use film, television, meme, or creator footage only when its license or permission clearly allows the intended use.

## Repeatable episode structure

1. **Cold open (0:00–0:02):** the conflict is already on screen and someone is already speaking. The payoff promise line is overlaid at the top.
2. **Escalation (to about 0:15):** make the problem or pattern visible through actions, reactions, and time jumps. Two escalation steps are usually enough.
3. **Comic payoff (about 0:15–0:19):** land the human joke before teaching. Give it a beat of silence.
4. **Software reveal (3–4 seconds, inside the scene):** Hussain's voice names the concept and gives one fact over a freeze frame of the story.
5. **Final gag and loop tail (about 3–5 seconds):** one more human beat that rewards staying, leading straight back into the opening conflict. The `SOFTWARE IN DISGUISE` wordmark sits small in a corner during the reveal instead of on a separate end card.

The series name and episode number belong on the thumbnail and in a small corner mark, never on a full-screen card at the start.

## Production economy

The series needs 2–3 episodes per week for about four weeks before the format can be judged. Cadence matters more than polish.

- Reuse the kit. `kit/episode.py` handles the timeline, lip-sync, dialogue levelling and mixing, rendering, subtitles and the contact sheet. An episode's `render_episode.py` subclasses `Episode` and contains only the story: shot functions, `build_shots()`, `sound_design()`, `thumbnail()` and `reveal_frame()`. Start from the previous episode's files.
- When a story needs something the kit lacks (a new prop, pose, set, or character), add it to `kit/` so later episodes get it too.
- If a premise is not working after one draft, move it to the idea bank and pick another. Do not build three versions of one episode.

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

- **Character kit (`kit/`):** Python/Pillow drawing code for the cast, sets, props, camera, and expressions. It replaced image generation from Episode 4. Episodes 1–3 used built-in image generation.
- **Kokoro-82M with kokoro-onnx:** free local synthetic speech. Episode 1 used `af_bella`, `am_michael`, and `bf_emma`. Keep license notes with every generated voice set.
- **FFmpeg and ffprobe:** crop panels, assemble the vertical cut, mix dialogue/music/effects, encode H.264/AAC, and verify media metadata.
- **Python, Pillow, NumPy, and SoundFile:** compose frames and speech bubbles and synthesize simple original situational music and sound effects.
- **YouTube and web research:** validate search wording, competing titles, and current creator patterns. Treat autocomplete as directional evidence; exact YouTube search volume is not public. YouTube Studio's Research tab is the best account-specific source when available.

Avoid committing downloaded voice-model weights. Store them in the repository-level ignored `models/` directory and document how to obtain them from the official sources.

## Discovery and packaging

- Write a human title around the episode's situation. Put the strongest relevant phrase near the beginning. The title should describe a conflict ("Neither Roommate Would Let Go") rather than a character's intention ("He Tried Not to Overdo the Apology").
- Keep the series name and episode number on the thumbnail instead of spending title space or the first second of video on them.
- Put the technical concept in the first description line so search can still understand the topic.
- Use a small number of focused hashtags in the description. Keep hashtags out of the title.
- Reserve the maximum caption footprint before placing story or explanation graphics. Review every animated state, not only the opening and final frames, and use a contact sheet when several objects accumulate or cross paths.

## Publishing schedule

Consistency matters more than the exact slot. A new episode is never held back to protect a previous one that's still
climbing: each Short is tested on its own.

- **Same date and time on both platforms.** Each new episode goes live on YouTube Shorts and Instagram Reels at the
  same moment, three episodes a week (Monday, Wednesday, Friday; the slot can be morning or evening, as long as both
  platforms match). Schedule both a day or more ahead.
- **YouTube:** check that Studio is on The Unplanned Stack channel (it can open on the personal channel).
- **Instagram:** account `theunplannedstack`. The web composer supports **Schedule content** (a toggle on the caption
  step), so Reels can be scheduled ahead like YouTube. The composer defaults to a square crop: pick **Original** in
  "Select crop" before continuing.
- **Which episodes go to Instagram:** Episode 4 onward, the code-drawn format with Hussain's voice. Episodes 1–3 stay
  YouTube-only: they use the old AI-illustrated look and slow openings, and would introduce the series to a new
  audience with its weakest episodes.

### YouTube upload checklist

- Title (no hashtags), the description from the brief, and 2–3 **unambiguous** hashtags. Avoid tags that collide with
  other topics: `#deadlock` pulls in Valve's game, so prefer `#computerscience` or `#concurrency`.
- The custom thumbnail from `deliverables/thumbnail.png`.
- Audience: not made for kids. Paid promotion: no. AI use: no (cartoon, fictional characters, Hussain's real voice).
  Revisit this if an episode ever depicts a real person or a realistic scene.
- Playlist: **Software in Disguise**. Related video: the previous episode. Once the new one is public, update the
  previous episode's related video to point forward to it.
- After it goes public: pin the comment from the brief.

### Instagram upload checklist

- Upload the same final MP4 (never a re-download from YouTube, which carries compression and possibly a watermark).
- Caption: the brief's description, with the first line rewritten as the hook (Instagram shows about one line before
  "more"). 3–5 hashtags: `#SoftwareInDisguise #programming #computerscience` plus the concept.
- Cover: `deliverables/thumbnail.png`. Keep "Also share to feed" on.
- Safe zones: Instagram's caption and buttons cover roughly the bottom 20% and the right edge, the same reserve the
  series already keeps clear.
- After it goes up: pin the same comment question.

## Measuring retention

Record these in each episode's brief 48 hours after publishing (YouTube Studio; for Instagram, the Reel's
insights: plays, average watch time, and skip rate if shown):

- **Viewed vs. swiped away** (YouTube Studio → the Short → Engagement). This is the main measure of the hook. It says whether the first second worked.
- **Average percentage viewed.** Above 100% means viewers are replaying, which means the loop worked.
- **The retention graph at the first conflict and at the reveal.** A drop just before the reveal means the escalation ran too long.

Judge the format after 8–10 episodes made under these rules, not after one.

## Definition of done

- The first frame shows the conflict, and speech begins within 0.3 seconds.
- The payoff promise line is visible in the opening seconds and does not name the concept.
- No still holds longer than about 2.5 seconds without a dialogue beat.
- Runtime is 35 seconds or less.
- Story is understandable without the final explanation.
- Technical mapping is accurate and visible before it is named.
- The reveal is in Hussain's recorded voice.
- No still contains a generative-art tell (hands, text squiggles, continuity breaks).
- The ending loops back into the opening.
- Thumbnail is legible on a phone and does not reveal the concept.
- Voices are clear, dialogue is captioned, and speakers are visually identifiable.
- Music changes with the situation and stays below dialogue.
- Video is vertical 1080×1920, H.264, 30 fps, with AAC audio at 48 kHz.
- Final video, thumbnail, sources, dialogue metadata, licenses, and episode notes are saved together.
- The final upload file has an unambiguous name and is not confused with intermediate review cuts.
- Episode ledger is updated after each production or publication milestone with the actual status.
