"""Voice bake-off for the Episode 1 remake: the same character lines through several TTS engines.

Kokoro is what Episodes 2–8 used (two viewers called the result AI-like). The others are newer open models that run
locally on Apple Silicon through mlx-audio:
- Qwen3-TTS VoiceDesign: builds a voice from a written description (age, tone, emotion) per character
- Dia: generates a whole exchange at once, with turn-taking and non-verbal sounds like (gasps) and (laughs)

Run (two venvs: Kokoro lives in the old one):
    KOKORO_MODEL_DIR=... ../../.venv/bin/python voice_bakeoff.py kokoro
    ../../.venv-mlx/bin/python voice_bakeoff.py qwen
    ../../.venv-mlx/bin/python voice_bakeoff.py dia
Output: audio/bakeoff/<engine>/<line>.wav
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

OUT = Path(__file__).parent / "audio" / "bakeoff"

# Who each character is, written the way the VoiceDesign model reads it.
CHARACTERS = {
    "PRIYA": "A woman in her late twenties, bright and warm, a little breathless.",
    "MOM": "A woman in her mid fifties, warm, expressive and loud when excited.",
    "DAD": "A man around sixty, low and flat, distracted, barely paying attention.",
    "AUNT": "A woman in her late fifties, big theatrical voice, gushing and overjoyed.",
    "GRANDPA": "A man in his eighties, slightly hoarse and slow, a little hard of hearing.",
}

# (key, speaker, text, emotion for this line)
LINES = [
    ("01-aunt-congrats", "AUNT", "Congratulations!!", "Bursting with joy, almost singing it."),
    ("02-grandpa-on-what", "GRANDPA", "...On what?", "Genuinely confused, mouth half full, slow."),
    ("03-priya-engaged", "PRIYA", "Mom... I'm engaged!", "Nervous pause, then thrilled."),
    ("04-mom-scream", "MOM", "Oh my God! Aaaah!", "Shrieking with happiness."),
    ("05-mom-tells-dad", "MOM", "Priya's engaged!", "Excited, telling her husband the big news."),
    ("06-dad-nice", "DAD", "Nice.", "Completely flat, not looking up from his newspaper."),
    ("07-grandpa-oh", "GRANDPA", "Oh!", "Sudden realisation, delighted."),
    ("08-priya-june", "PRIYA", "Also, we moved the wedding to June.", "Casual and cheerful, as if it's nothing."),
]

KOKORO_CAST = {"PRIYA": ("af_heart", 1.0), "MOM": ("bf_isabella", 0.95), "DAD": ("am_michael", 0.9),
               "AUNT": ("af_bella", 1.0), "GRANDPA": ("bm_george", 0.85)}


def save(engine: str, key: str, audio, sr: int):
    d = OUT / engine
    d.mkdir(parents=True, exist_ok=True)
    a = np.asarray(audio, dtype=np.float32).reshape(-1)
    peak = np.abs(a).max() or 1
    sf.write(d / f"{key}.wav", a / peak * 0.89, sr)
    print(f"{engine}/{key}.wav  {len(a) / sr:.2f}s")


def run_kokoro():
    from kokoro_onnx import Kokoro

    md = Path(os.environ["KOKORO_MODEL_DIR"])
    k = Kokoro(str(md / "kokoro.onnx"), str(md / "voices.bin"))
    for key, who, text, _ in LINES:
        voice, speed = KOKORO_CAST[who]
        audio, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
        save("kokoro", key, audio, sr)


def run_qwen():
    from mlx_audio.tts.utils import load_model

    model = load_model("mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16")
    for key, who, text, emotion in LINES:
        res = list(model.generate_voice_design(text=text, language="English",
                                               instruct=f"{CHARACTERS[who]} {emotion}"))
        audio = np.concatenate([np.asarray(r.audio) for r in res])
        save("qwen3-voicedesign", key, audio, model.sample_rate)


def run_dia():
    from mlx_audio.tts.utils import load_model

    model = load_model("mlx-community/Dia-1.6B-fp16")
    scenes = {
        "dia-lunch": "[S1] Congratulations!! (laughs) [S2] ...On what?",
        "dia-phone": "[S1] Mom... I'm engaged! [S2] (gasps) Oh my God! (screams)",
        "dia-couch": "[S1] Priya's engaged! [S2] Nice.",
    }
    for key, text in scenes.items():
        res = list(model.generate(text=text))
        audio = np.concatenate([np.asarray(r.audio) for r in res])
        save("dia", key, audio, model.sample_rate)


if __name__ == "__main__":
    {"kokoro": run_kokoro, "qwen": run_qwen, "dia": run_dia}[sys.argv[1]]()
