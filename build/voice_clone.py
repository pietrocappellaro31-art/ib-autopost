"""
A cloned voice with the same interface as voice.Voice (say, phonemes), so any
voiced Reel can be rendered in it: pass "clone:/path/to/reference.wav" as the
voice name.

Backed by Kyutai's Pocket TTS (weights CC BY 4.0, credit Kyutai), run locally
by sherpa-onnx's command-line synthesiser. Pocket TTS takes a short reference
recording and speaks new text in that voice.

Only ever clone a voice whose owner has explicitly agreed: Pietro's own, or
someone who said yes. Never a public figure (see docs/decisions-log.md).
Every Reel voiced this way still carries Instagram's AI label.

Files (not in the repo): $SHERPA_DIR is the sherpa-onnx release folder
(sherpa-onnx-v2.0.1-linux-x64-shared, from github.com/k2-fsa/sherpa-onnx
releases) and $POCKET_DIR the model folder sherpa-onnx-pocket-tts-int8-2026-01-26
(same releases page, tts-models).

A good reference: 20 to 30 seconds, one speaker, a quiet room, the phone a
hand's width from the mouth, no music, spoken the way the Reels should sound.
"""

import os
import pathlib
import subprocess
import tempfile
import wave

import numpy as np

from voice import SR, trim

SHERPA = os.environ.get("SHERPA_DIR", "")
POCKET = os.environ.get("POCKET_DIR", "")


class CloneVoice:
    def __init__(self, reference, steps=8, sherpa=SHERPA, model=POCKET):
        self.ref = str(pathlib.Path(reference).resolve())
        self.steps = steps
        self.bin = pathlib.Path(sherpa) / "bin" / "sherpa-onnx-offline-tts"
        self.lib = str(pathlib.Path(sherpa) / "lib")
        m = pathlib.Path(model)
        self.args = [f"--pocket-lm-flow={m / 'lm_flow.int8.onnx'}", f"--pocket-lm-main={m / 'lm_main.int8.onnx'}",
                     f"--pocket-encoder={m / 'encoder.onnx'}", f"--pocket-decoder={m / 'decoder.int8.onnx'}",
                     f"--pocket-text-conditioner={m / 'text_conditioner.onnx'}", f"--pocket-vocab-json={m / 'vocab.json'}",
                     f"--pocket-token-scores-json={m / 'token_scores.json'}"]

    def phonemes(self, text):
        """passage() only uses this for relative sentence lengths."""
        return text

    def say(self, text, speed=None):
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d) / "out.wav"
            subprocess.run([str(self.bin), *self.args, f"--reference-audio={self.ref}", f"--num-steps={self.steps}",
                            "--num-threads=4", f"--output-filename={out}", text],
                           env={**os.environ, "LD_LIBRARY_PATH": self.lib}, check=True, capture_output=True)
            if speed and abs(speed - 1) > .005:              # Pocket has no speed control: stretch, keeping pitch
                st = pathlib.Path(d) / "st.wav"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-af", f"atempo={speed}", "-ar", str(SR), str(st)],
                               check=True)
                out = st
            with wave.open(str(out)) as w:
                if w.getframerate() != SR:
                    raise ValueError(f"expected {SR} Hz from Pocket TTS, got {w.getframerate()}")
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return trim(a)


def make_voice(name):
    """'af_heart' (Kokoro) or 'clone:/path/to/reference.wav' (Pocket TTS)."""
    if name.startswith("clone:"):
        return CloneVoice(name.split(":", 1)[1])
    from voice import Voice
    return Voice(name)
