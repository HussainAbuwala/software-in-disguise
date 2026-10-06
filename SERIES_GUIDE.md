# Series guide (October 2026: Hussain on camera)

## Core promise

> *You use it every day. Here's what's happening behind it.*

The friendly app screen is the disguise. Each Short starts from something a viewer has done or seen in an app (a
glitch, a delay or a feature they never thought about), then Hussain takes the costume off and shows the software
underneath. Recognition comes first, as before. What changed is who explains it and where the story comes from.

- **It doesn't have to be a problem.** Three kinds of moment work:
  - **Glitch:** "Why did the like count go *down*?" (eventual consistency)
  - **Hidden feature:** "Undo Send never unsent anything." (a delay queue)
  - **Everyday magic:** "How does Netflix start blurry and then get sharp?" (adaptive bitrate)
- **The viewer must have lived it.** If someone who doesn't program wouldn't recognize the moment on their own phone,
  pick another one.
- **The mapping must be true.** Say only what the system actually does. When a popular explanation is a myth (for
  example, "airlines raise prices because you looked twice"), the Short can be about the myth, but never repeat it as
  fact.

## Reference format: candlesan

[candlesan](https://www.youtube.com/@candlesan/shorts) (119K subscribers; game designer of WoW and Diablo bosses)
explains game design in Shorts that get 0.1–2.8M views. His most relevant one, *The Simple Math Hiding in Your Favorite
Games* (1.3M), is our premise applied to games. What his Shorts do, as seen in their frames:

| What he does | Where it shows |
| --- | --- |
| **The same set every time:** orange wall, two game posters, same framing, same caption style. You know it's him before he speaks. | Every Short |
| **The frame-1 title card** sits on his chest: a dark rounded box holding the hook as a question, with one word in yellow (*Hiding*), plus a teaser line under it (`Dmg Mit % = X / (…?`). | Simple Math, Gruul, Tissue Test |
| **About half the runtime is full-screen diagrams:** a cream or dark-navy background, flat simple characters (a goblin, two playtesters), health bars, and tables or charts that build one row at a time. | Simple Math, Gruul |
| **Split screen:** a diagram on one half and his face on the other, or a checklist card filling the lower half while he talks. | Tissue Test (warm-up script) |
| **Proof it's everywhere:** a band of logos across the frame (League, Dota, Diablo) while he lists them. | Simple Math |
| **Real footage as receipts:** an actual game clip showing the mechanic. | Gruul (WoW raid footage) |
| **A real prop in hand:** he holds a tissue for "the tissue test". | Tissue Test |
| **Small pops:** emoji reactions and mini avatars appear next to his head. | Tissue Test, Simple Math |
| **Authority in the first person:** "I designed…", "When we started work on Diablo 3…" | Most titles |
| **Bold 2–3-word captions** in the middle of the frame, always on. | Every Short |
| **Length: 2½–3 minutes.** Depth, not speed. | Every Short |

## Visual toolkit

These are the ideas to pick from. The ones marked ★ are the signature moves that would make the series recognizable.

1. ★ **Phone up to the lens (the cold open).** Frame 1 is Hussain holding his phone toward the camera, with the real
   screen recording composited large beside him or over the phone: the "Seen" tick, the Undo Send toast, the price that
   changed. The viewer recognizes their own phone before a word is said.
2. ★ **The unmasking wipe (the "disguise" moment).** Hussain swipes his hand across the frame, and the app screen peels
   away to reveal the diagram of what's underneath. The UI and the machinery share the same layout, so the button
   becomes a box that sends a request. Doing this the same way every episode makes it the series' signature.
3. **One small icon vocabulary.** A phone, a server, a database, a queue, a clock, and a person, drawn the same way
   every time on one background color (candlesan uses cream). Requests travel between them as dots, and the viewer
   learns the visual language over the episodes.
4. **Physical props for the system.** Sticky notes as a cache ("I wrote it down this morning"), a stack of plates as a
   stack, numbered tickets as a queue, two phones tapping Buy at the same moment for a race condition. Film the props
   for real; they're cheap, human, and nobody mistakes them for AI.
5. **Two-phone split screen.** For sync and consistency topics, film two real devices side by side, with one showing
   "Delivered" and the other not. It shows the problem without any drawing.
6. **Slow motion with a millisecond ruler.** Freeze the real screen recording and run a timeline under it that reads
   "0 ms tap, 40 ms request leaves, 180 ms server answers…". It's candlesan's "slow motion examination", applied to an
   app.
7. **Receipts for the technical viewer.** One second of the real network tab, the HTTP response, or the actual
   header, captioned "this is the real request". It rewards developers without slowing everyone else down.
8. **Logo band: "it's not just WhatsApp."** A row of the apps that do the same thing (Gmail, Slack, iMessage),
   which shows the concept is everywhere. These are logos used to identify the products: keep them small, plain and
   factual, and never imply that a company endorses the video.
9. **The concept tag.** At the moment of the reveal, a mustard label carrying the concept's name slaps onto the app
   screenshot, like a price tag on the disguise. (The mustard carries over from the story-era promise card.)
10. **Talking with the hands.** Count steps on the fingers, and use two hands for two servers. Hands give the edit
    motion between cutaways without any extra graphics.

## Set and on-camera identity

Choose one setup and keep it for every Short:

- one wall and one dominant background color
- one or two objects that say "software person" to a non-programmer (an old phone, a server blade, sticky notes)
- the same framing (chest up, eyes on the upper-third line) and a recurring shirt color
- the same caption font and color, with one highlight color for the key word in each line

## Carry over from the story era (our own analytics)

The cartoon Shorts were tested on about 1.1–1.3K feed viewers each and stalled there. One stranger's comment
summed up the look: *"It's weird. Like if AI was given video creation software."* A real face is the change none of
those tests tried. The retention lessons below still apply:

- **The first second decides.** Frame 1 shows the moment the viewer recognizes, and speech starts immediately.
- **Don't name the concept in frame 1.** Episode 3's remake did, and 63% swiped away, the worst result. Hook with the
  experience and name the concept later.
- **Silent cutaways early cost viewers.** In the first 10 s, every graphic needs Hussain's voice over it.
- **The old reveal was the exit.** In the story Shorts, the explanation was an add-on and viewers left when it came.
  In this format the explanation *is* the content, but still name the concept within the first third, so viewers know
  where it's going.
- **Likes and follows are the weak numbers** (about 0.7–1.6% likes, 0–3 subscribers per episode). A face, a
  first-person voice, and an ending question ("What app does this to you?") are the levers to test.
- **Length: no target. The topic decides.** Take as long as a good explanation needs, up to the platform limit
  (3 min for YouTube Shorts; Instagram recommends Reels of up to 3 min to non-followers). Every line must earn its
  place: cut anything that doesn't help the explanation. The retention graph judges each one. A steady slide means
  it dragged; a sharp drop points to the exact line that lost people.

## Workflow

1. Pick the moment (`EPISODES.md` lists what's done and the ideas to try).
2. Fill in [`templates/episode-brief.md`](templates/episode-brief.md): the hook, the script, and the visual beat for
   each line.
3. Record the A-roll (Hussain to camera) and capture the B-roll (screen recordings, prop shots, diagrams).
4. Edit, then caption and check the Shorts safe area: keep important text out of the bottom 20% and the right 15%.
5. Record the episode and, after about 2 days, its analytics in `EPISODES.md`.
