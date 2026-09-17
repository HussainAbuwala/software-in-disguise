# Episode 03 production review

## Result

The revised review cut runs 50.8 seconds at 1080×1920, 30 fps. It uses H.264 video and stereo AAC audio at 48 kHz. The human story remains static; only the closing job cards animate. It is unpublished.

The story remains understandable without the software explanation: the empty chair establishes a credible promise, three small requests cumulatively displace the groom, the waiting car raises the cost, and “What if you just cut the front? That's quick” explicitly converts his haircut into the sort of small request the barber keeps prioritizing.

All essential text is kept inside a conservative shared Shorts/Reels area: x=70–930 and y=260–1320 in the 1080×1920 frame. Captions end at y=1240, leaving 680 pixels below them; the right 150 pixels remain free for platform action buttons. `deliverables/safe-zone-preview.png` visualizes the boundary. YouTube's own editor displays guides for UI collision, Google advises keeping essential elements within its vertical-video safe area because overlays vary, and Meta provides a Reels safe-zone checker. Final upload preview remains the last platform-specific check.

Platform references checked on 2026-09-17:

- YouTube Help — editor safe-area guides: https://support.google.com/youtube/answer/16215842
- Google Ads Help — vertical-video safe zones: https://support.google.com/google-ads/answer/9128498
- Meta for Business — Reels safe-zone checker and guidance: https://www.facebook.com/business/ads/facebook-instagram-reels-ads

## Implemented

- Eight original static story illustrations plus a character/environment reference sheet.
- Thirteen fixed story states plus a restrained code-drawn printer-queue animation, including deterministic captions, clock labels, phone UI, cover hook, and reveal typography.
- Fourteen neutral-ID character voice candidates, four role comparison reels, two groom/barber chemistry scenes, and a 73.8-second combined comparison reel.
- Eleven provisional final dialogue lines with stable line and speaker IDs.
- Original synthesized shop ambience, bell, clippers, phone vibration, and sparse tonal music.
- Burned-in captions, separate SRT subtitles, thumbnail, publishing draft, source prompts, license records, and reproduction scripts.

## Verification

- Full video decoded successfully with FFmpeg.
- Verified H.264/AAC, 1080×1920, 30 fps, 50.8 seconds, stereo audio at 48 kHz.
- Measured final encoded audio at -15.9 LUFS integrated, 8.9 LU loudness range, and -1.1 dBTP true peak.
- Inspected a contact sheet covering the complete cut and full-resolution opening and reveal frames. Captions and overlays remain in safe areas; the suit bag, empty-chair promise, customer changes, payoff, and reveal are legible.
- Audition files and dialogue files were probed successfully; source IDs, durations, rates, peaks, and RMS values are stored in manifests.

## Review limits

No human real-time listening review or publication is implied. Final casting, synthetic-speech naturalness, pronunciation, and comic timing require listening to the comparison reel and full cut. The provisional cast was chosen for age/profile contrast, line timing, and role separation, then carried into the review render.

Visual continuity is intentionally anchored by the groom, cream shirt, dark trousers, charcoal suit bag, barber's teal overshirt, warm shop palette, left entrance, waiting bench, central chair, mirror, and wall clock. Small incidental background details vary between generated stills. Those changes are acceptable only if they do not distract in playback; the final creative review should watch specifically for them.
