"""Reference voices for the Episode 1 remake, designed with Qwen3-TTS VoiceDesign.

Dia delivers lines naturally but can't be told who is speaking (age, gender). Qwen3-TTS VoiceDesign can: it builds a
voice from a written description. So each character gets a few seeded reference clips here; the chosen clip is
then Dia's audio prompt for that character in every scene (`dia_scenes.py`).

Run: ../../.venv-mlx/bin/python voice_refs.py [CHARACTER ...]
Output: audio/refs/<character>/take-N.wav (+ .txt transcript), audio/refs/<character>/reel.m4a
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf

OUT = Path(__file__).parent / "audio" / "refs"
TAKES = 3

REFS = {
    "GRANDPA": ("A man in his eighties with a slightly hoarse, slow, gentle voice, a little hard of hearing, warm "
                "and a bit grumpy.",
                "Eh? What's all the fuss about? Nobody tells me anything in this house."),
    "AUNT": ("A woman in her late fifties with a big, warm, theatrical voice, gushing and quick.",
             "Oh, I knew it! I always said those two would get married, didn't I say it?"),
    "MOM": ("A woman in her mid fifties with a warm, expressive voice, emotional and loving.",
            "Oh my goodness, I can't believe it. My little girl is getting married!"),
    "DAD": ("A man around sixty with a low, calm, dry voice, unbothered and a little distracted.",
            "Mm. Yes, yes, I heard you. I'm just finishing the paper."),
    "PRIYA": ("A woman in her late twenties with a bright, warm, slightly nervous voice.",
              "Mom, can you sit down for a second? I have something to tell you."),
}


def main(names):
    from mlx_audio.tts.utils import load_model

    model = load_model("mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16")
    for name in names:
        desc, text = REFS[name]
        d = OUT / name.lower()
        d.mkdir(parents=True, exist_ok=True)
        parts = []
        for k in range(1, TAKES + 1):
            mx.random.seed(100 + k)
            res = list(model.generate_voice_design(text=text, language="English", instruct=desc))
            a = np.concatenate([np.asarray(r.audio, dtype=np.float32).reshape(-1) for r in res])
            a = a / (np.abs(a).max() or 1) * 0.89
            sf.write(d / f"take-{k}.wav", a, model.sample_rate)
            (d / f"take-{k}.txt").write_text(text)
            parts += [a, np.zeros(int(model.sample_rate * 0.9), np.float32)]
            print(f"{name} take {k}: {len(a) / model.sample_rate:.1f}s", flush=True)
        sf.write(d / "reel.wav", np.concatenate(parts), model.sample_rate)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(d / "reel.wav"), "-c:a", "aac", "-b:a", "160k",
                        str(d / "reel.m4a")], check=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(REFS))
