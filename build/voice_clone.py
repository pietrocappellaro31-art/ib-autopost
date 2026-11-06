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
Run prepare_reference() on it first. With $MOONSHINE_DIR set, every line is
transcribed and retaken until the words match the script (voice_check.py).
"""

import os
import pathlib
import subprocess
import tempfile
import wave

import numpy as np

from voice import SR, trim, write_wav

SHERPA = os.environ.get("SHERPA_DIR", "")
POCKET = os.environ.get("POCKET_DIR", "")


class CloneVoice:
    def __init__(self, reference, steps=8, sherpa=SHERPA, model=POCKET):
        self.ref = str(pathlib.Path(reference).resolve())
        self.steps = steps
        self.log = []                                   # one entry per line: takes used, how it was heard
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

    def say(self, text, speed=None, tries=6):
        """Pocket TTS samples, so each take differs and a take can drop, add
        or swap a word. Every take is transcribed (voice_check) and compared
        with the script; the first exact take wins, else the closest one."""
        import voice_check
        if not voice_check.MOON:
            return self._take(text, speed)
        best = None
        for k in range(tries):
            a = self._take(text, speed)
            with tempfile.TemporaryDirectory() as d:
                w = pathlib.Path(d) / "t.wav"
                write_wav(w, a)
                heard = voice_check.transcribe(w)
            e = voice_check.wer(text, heard)
            if best is None or e < best[0]:
                best = (e, a, heard, k + 1)
            if e == 0:
                break
        self.log.append(dict(text=text, wer=round(best[0], 3), heard=best[2], takes=k + 1))
        return best[1]

    def _take(self, text, speed=None):
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


def prepare_reference(src, out, max_s=25.0, min_s=12.0):
    """Turn a phone recording into a clean Pocket TTS reference: mono 24 kHz,
    loudness evened out, cut at the longest pause before max_s and ended on a
    little silence. A reference that stops mid-word makes the model 'finish'
    that word at the start of every line it speaks (tested 6 Nov)."""
    with tempfile.TemporaryDirectory() as d:
        mid = pathlib.Path(d) / "m.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ac", "1", "-ar", str(SR),
                        "-af", "highpass=f=70,loudnorm=I=-20:TP=-2", str(mid)], check=True)
        with wave.open(str(mid)) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    idx = np.where(np.abs(a) > .01)[0]
    a = a[max(idx[0] - int(.1 * SR), 0):]                      # drop the silence before the first word
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    quiet = rms < rms.max() * .03
    lo, hi = int(min_s * 100), min(int(max_s * 100), len(quiet))
    best, i = None, lo
    while i < hi:
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if best is None or j - i > best[1] - best[0]:
                best = (i, j)
            i = j
        else:
            i += 1
    cut = len(a) if len(a) <= max_s * SR else ((best[0] + best[1]) // 2 * hop if best else int(max_s * SR))
    ref = np.concatenate([a[:cut], np.zeros(int(.3 * SR), np.float32)])
    write_wav(out, ref)
    return len(ref) / SR


def make_voice(name):
    """'af_heart' (Kokoro) or 'clone:/path/to/reference.wav' (Pocket TTS)."""
    if name.startswith("clone:"):
        return CloneVoice(name.split(":", 1)[1])
    from voice import Voice
    return Voice(name)
