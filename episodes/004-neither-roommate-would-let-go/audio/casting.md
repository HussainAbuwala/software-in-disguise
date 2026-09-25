# Casting: recurring cast voices

Engine: Kokoro-82M via kokoro-onnx, run locally (model Apache-2.0, kokoro-onnx MIT; same licenses as Episode 01).
These voices are now **permanent** for the recurring cast. Keep them in every future episode so the characters are
recognizable by voice.

| Role | Voice | Speed | Why |
| --- | --- | --- | --- |
| Dev | `am_puck` | 0.92–1.05 | One of Kokoro's three highest-graded American male voices. Brighter and younger than `am_michael`, so the stubborn roommate reads as energetic rather than authoritative. |
| Mira | `af_heart` | 0.9–0.95 | Kokoro's highest-graded voice overall. Slowed slightly so the smug lines ("Then why are you holding it?") land calmly. |
| Jo | `af_nicole` | 0.9 | A soft, breathy voice. Its flat delivery is the deadpan joke: Jo is unbothered by everything. Clearly distinct from Mira despite both being female voices. |
| TV golf commentator | `bm_george` | 0.88 | British, measured. Played quietly through a band-pass filter so it sounds like a small TV speaker. |
| Reveal | Hussain (recorded) | — | Real voice, per the human-signal rule. `am_michael` remains in `voices.py` as a stand-in used only when no recording exists. |

Voices were chosen from Kokoro's published quality grades plus separation between speakers. They have not yet been
compared by ear against alternatives. If a voice sounds wrong in review, swap it in `voices.py` (`CAST`) now, before
Episode 05 makes it permanent. All lines are loudness-matched in the render, so a quieter voice such as Nicole stays
as present as the others.
