# Audio source and license notes — Episode 03

The generated dialogue in this directory was synthesized locally with these sources:

- **Kokoro-82M model** — Apache License 2.0. Official model page: https://huggingface.co/hexgrad/Kokoro-82M
  License copy: [`licenses/Kokoro-82M-Apache-2.0.txt`](licenses/Kokoro-82M-Apache-2.0.txt)
- **kokoro-onnx runtime** — MIT License. Official repository: https://github.com/thewh1teagle/kokoro-onnx
  License copy: [`licenses/kokoro-onnx-MIT.txt`](licenses/kokoro-onnx-MIT.txt)

The Apache text is the canonical Apache 2.0 license from https://www.apache.org/licenses/LICENSE-2.0.txt, matching the license declared by the official model page.

All dialogue and audition WAVs were synthesized locally from the text recorded in `dialogue.json` and `auditions/manifest.json`. The generated files do not imitate a named real person.

The room tone, door bell, clipper buzz, phone vibration, and sparse musical tones were synthesized from noise and sine waves by `render_episode.py`; no third-party recordings or musical compositions are included.
