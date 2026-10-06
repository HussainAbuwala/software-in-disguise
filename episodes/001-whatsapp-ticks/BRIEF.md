# Software in Disguise — Episode 001: WhatsApp ticks

## The moment

- **What the viewer has seen on their phone:** a message stuck on one grey tick; two grey ticks that never turn
  blue; someone with blue ticks off.
- **Kind:** hidden feature
- **What's actually happening behind it:** each tick is a receipt, a small message sent back to your phone saying how
  far your message got. One tick: WhatsApp's server has it. Two: the other person's phone has it. Blue: their phone
  says they opened the chat.
- **The twist:** one tick doesn't mean your friend has it. The message is sitting on a server, waiting for their phone
  to come online. And blue ticks aren't WhatsApp watching your friend. Their own phone reports it, so with read
  receipts off, it simply doesn't send that last receipt.
- **Concept:** acknowledgements ("acks"), with store-and-forward (the server holds the message until the phone is
  reachable)
- **Where I've met this myself (first-person authority):** *Hussain to fill in: a system at work that waits for
  acknowledgements or retries until it gets one.*

### Accuracy notes (check against the WhatsApp Help Center before recording)

- The tick meanings (clock / one grey / two grey / two blue) follow WhatsApp's own help article on check marks.
- **The clock** means the message hasn't left your phone yet (usually no connection).
- **Group chats:** two ticks only when *everyone* has received it, blue only when everyone has read it. Leave this out
  of the video, and put it in the pinned comment if people ask.
- **Read receipts off works both ways:** turning yours off also hides other people's. Group chats still show read
  receipts.
- **One tick for days** fits several causes (their phone is off, they haven't opened WhatsApp, or they blocked you).
  WhatsApp lists one tick as a possible sign of a block, but it's never proof. The ending joke must stay a joke.
- **Undelivered messages** are kept on WhatsApp's servers for a limited time (30 days per WhatsApp's privacy policy).
  Check the current number before saying it on camera, or leave it out.
- **The internet line** ("the internet confirms data the same way") is true of TCP, which acknowledges data as it
  arrives. Keep the wording general. Don't say "every packet gets its own receipt" (TCP acknowledgements are
  cumulative).
- Don't get into encryption. It's true and interesting, but it's a separate episode.

## Hook

- **Frame 1:** Hussain holds his phone up to the lens. The screen recording beside him shows a chat with one grey tick.
- **Title card (no concept name):** `Where is your message *right now*?` (yellow: *right now*)
- **First spoken line:** "This message has one grey tick. So where is it right now?"
- **Working title:** `Where Your WhatsApp Message Waits | Acknowledgements Explained`
- **Alternative:** `What One Grey Tick Really Means | Acknowledgements Explained`

## Script and visuals

Length is whatever the explanation needs; this draft reads at about 60–70 s.

| # | Line (spoken) | On screen |
| --- | --- | --- |
| 1 | "This message has one grey tick. So where is it right now?" | Phone up to the lens; real chat with one tick beside him; title card |
| 2 | "Not on my friend's phone. It's sitting on a WhatsApp server, waiting." | Hussain to camera, a small server icon pops beside his head |
| 3 | "Every tick is a receipt: a tiny message coming *back* to my phone, telling it how far mine got." | **Unmasking wipe:** the chat screen peels away into the diagram: my phone → server → friend's phone |
| 4 | "Clock? It hasn't even left my phone." | Real screen recording: airplane mode on, send, clock icon |
| 5 | "One tick: the server got it, and sent a receipt back." | Diagram: a dot travels phone → server, a small receipt returns |
| 6 | "My friend's phone is off. So the server holds onto it." | Diagram: friend's phone dark, message parked inside the server box |
| 7 | "Their phone comes back online, the server hands it over, and *their* phone sends a receipt: delivered. Two ticks." | **Two-phone split screen (real phones):** right phone leaves airplane mode → left phone flips to two ticks |
| 8 | "And blue? WhatsApp isn't watching them. When they open the chat, their phone sends one more receipt: read." | Split screen: right phone opens the chat → left phone turns blue |
| 9 | "Programmers call these acknowledgements. Acks." | **Concept tag** (`ACKNOWLEDGEMENTS`) slaps onto the chat screenshot |
| 10 | "The internet itself works like this. Data gets sent, and the other side confirms it arrived." | Diagram: many small dots and receipts flowing between the icons |
| 11 | "Which is why turning read receipts off is so simple: your phone just… doesn't send that last one." | Screen recording: Settings → Privacy → Read receipts toggle |
| 12 | "So next time it's stuck on one tick, their phone's off. Probably." *(beat, look at camera)* | Back on Hussain; one grey tick on screen; hold the beat |
| 13 | "What's the longest you've waited on one grey tick?" | Hussain to camera; question as a caption |

**Pinned comment:** group chat rules, read receipts off works both ways, and one tick is never proof of a block.

## Capture list

- [ ] **A-roll:** Hussain to camera, chest up, on the series set (still to be chosen; see "Set and on-camera
      identity" in `SERIES_GUIDE.md`)
- [ ] **Two phones with WhatsApp** in one test chat (Hussain's + a second phone or a friend's). Use a test contact
      name, and blur or crop phone numbers and profile photos.
- [ ] **Screen recordings:** clock (airplane mode on) → one tick → two ticks → blue; the Message Info screen
      (long-press → Info, showing delivered and read times) as an optional receipt; the read receipts toggle
- [ ] **Two-phone split shot** filmed for real (both phones on a table, one camera), not only screen recordings
- [ ] **Diagrams:** phone, server and friend's phone icons; a message dot; a receipt shape; the message parked in the
      server. These are the first pieces of the shared icon set.
- [ ] **Unmasking wipe:** a hand swipe in the A-roll, timed for line 3

## After publishing

- **Published / links:**
- **Analytics after ~2 days (views, swiped away, average view duration, likes, comments, subscribers, where viewers
  leave):**
