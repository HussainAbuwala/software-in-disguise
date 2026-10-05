# Software in Disguise — Episode 01 (remake): The Last Room

Race condition. Replaces the old Episode 1 ("Two People Bought the Same Concert Seat", 163 views), which goes private
when this one is published. First episode of the new format (2026-10-05): real people hit a real glitch in a real
(unbranded) app; the software is visible from frame 1, and the *cause* is revealed by tilting a phone into X-ray view.

## What this episode tests

The Episode 2 remake fixed the hook (40.2% swiped) but stopped at ~1.3K views with a ~1% like rate and two comments
calling the look AI-like. This one changes the format and the look together (Hussain's call):

1. **Glitch-in-a-real-app format:** two identical "Booking confirmed · Room 204" screens in frame 1.
2. **"Inside the app" as a scene:** Priya X-rays the phone; the characters watch the real requests, database row and
   bookings, and react. No narrator and no cut to a lecture, so no reveal cliff.
3. **Big-head cartoon characters** (kit/bighead.py), chosen over code-drawn realistic faces, riso/comic/clean looks,
   Open Peeps and a cat family. Crisp app screens on top (kit/phone.py).
4. **Natural voices:** Dia exchanges in voices designed with Qwen3-TTS; single lines cloned with Qwen3 where Dia
   swapped voices or dropped one-word lines (kit/voices.py).
5. **Series hook:** Priya's wedding is the arc; Priya is the recurring explainer.

**Success:** more than ~1.5K views, a like rate near 3%, or comments about the booking IDs / "this happened to me".

## Beats (26.1 s, first cut)

| Shot | What happens |
| --- | --- |
| standoff | Meena (pointing) vs Lata (arms crossed); two confirmations on screen; "That's MY room!" "Excuse me, I booked it first!" |
| one_room | Lata: "Tell her!" The clerk holds up the one key: "Ma'am… we have one room." |
| flashback | 3 weeks ago, 9:41:07: both tap "Book now" at the same second; "Got it!" "Got it!" |
| priya | Priya slides in: "Wait. Show me your phones." Meena: "Look! It says confirmed!" |
| xray | Inside the app: two requests 4 ms apart, both check Room 204 = FREE, both book: 2 bookings, 1 room. Lata: "So it sold it twice?!" Priya: "Engineers call that a race condition" (stamp). The fix replayed: check + lock, Lata's request waits, then SOLD OUT. Meena: "Hmph." |
| key | "So… who gets the key?" Both: "MINE!" Both hands land on the key at once; RACE CONDITION stamp |

## Packaging (draft)

- **Title:** `We Both Booked the Last Room | Race Condition Explained`
- **Thumbnail:** frame 1 (two aunts, two identical confirmations)
- **Pinned comment:** `Spot the clue on the two phones 👀 (hint: look at the booking IDs)`

## Production

- [x] Characters, voices, renderer, first full cut (`deliverables/the-last-room.mp4`, -15.5 LUFS)
- [ ] Hussain's review (takes, timing, jokes)
- [ ] Publish; set the old Episode 1 to private; Instagram from the app
