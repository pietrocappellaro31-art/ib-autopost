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
    def __init__(self, reference, steps=8, sherpa=SHERPA, model=POCKET, min_pitch=None, tempo=None):
        self.ref = str(pathlib.Path(reference).resolve())
        self.tempo = tempo                              # < 1 slows every take (rubberband, pitch and tone kept)
        self.min_pitch = min_pitch                      # Hz; a take below it is retaken (feminised voices)
        self.tries = 6                                  # takes per line before keeping the closest
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

    def say(self, text, speed=None, tries=None):
        """Pocket TTS samples, so each take differs and a take can drop, add
        or swap a word. Every take is transcribed (voice_check) and compared
        with the script; the first exact take wins, else the closest one."""
        import voice_check
        if not (voice_check.MOON or voice_check.PARAKEET):
            return self._take(text, speed)
        best = None
        for k in range(tries or self.tries):
            a = self._take(text, speed)
            with tempfile.TemporaryDirectory() as d:
                w = pathlib.Path(d) / "t.wav"
                write_wav(w, a)
                heard, ws = voice_check.transcribe(w, with_words=True)
            e = voice_check.wer(text, heard)
            if self.min_pitch and voice_check.pitch(a) < self.min_pitch:
                e += 1                                   # drifted towards a male pitch: never the take to keep
            if best is None or e < best[0]:
                best = (e, a, heard, ws)
            if e == 0:
                break
        self.log.append(dict(text=text, wer=round(best[0], 3), heard=best[2], takes=k + 1))
        self._words = best[3]
        return best[1]

    def align(self, sents, audio):
        """Sentence timings for voice.passage, from the recogniser's word
        times on the chosen take (a real voice's pauses are too irregular for
        the pause matching that works on Kokoro). None falls back to it."""
        import voice_check
        return voice_check.sentence_times(sents, getattr(self, "_words", []), len(audio) / SR)

    LEAD = "Okay."

    def _take(self, text, speed=None):
        """One take. The model tends to swallow the first word of a line
        ("Can", "What's"), so every line is spoken after a throwaway "Okay."
        that is cut off at the first pause (tested 6 Nov on Pietro's voice)."""
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d) / "out.wav"
            subprocess.run([str(self.bin), *self.args, f"--reference-audio={self.ref}", f"--num-steps={self.steps}",
                            "--num-threads=4", f"--output-filename={out}", f"{self.LEAD} {text}"],
                           env={**os.environ, "LD_LIBRARY_PATH": self.lib}, check=True, capture_output=True)
            rate = (speed or 1) * (self.tempo or 1)
            if abs(rate - 1) > .005:                         # Pocket has no speed control: stretch, keeping pitch
                st = pathlib.Path(d) / "st.wav"
                af = (f"rubberband=tempo={rate:.4f}:pitchq=quality:transients=crisp:formant=preserved" if self.tempo
                      else f"atempo={rate}")
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-af", af, "-ar", str(SR), str(st)], check=True)
                out = st
            with wave.open(str(out)) as w:
                if w.getframerate() != SR:
                    raise ValueError(f"expected {SR} Hz from Pocket TTS, got {w.getframerate()}")
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return trim(cut_lead(a))


def cut_lead(a):
    """Drop everything up to the first pause of 100 ms or more after the
    first 0.2 s (the lead-in word); if there is none, keep the take whole and
    let the transcript check decide."""
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    if not len(rms):
        return a
    quiet = rms < max(.006, np.percentile(rms, 95) * .06)
    i = 20
    while i < min(len(quiet), 150):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if j - i >= 10:
                return a[(j - 3) * hop:]
            i = j
        else:
            i += 1
    return a


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


# ------------------------------------------------- Pietro's two voices ----
# Two cloned voices, both approved by Pietro on 7 Nov: L2 (the voice of
# Levels #2) and L3 (the voice of Levels #3). Reels alternate between them
# unless Pietro names one. Their samples are encrypted in voices/ (the key is
# in the claude.ai Project, never in this public repo); setup_voice.sh
# decrypts them into $VOICE_DIR. Each voice has an EQ curve that matches its
# tone to Pietro's real recordings (measured 7 Nov: the clones were duller,
# with less presence above 4 kHz and more mud at 150 to 500 Hz).

import json

VOICES = pathlib.Path(__file__).parent / "voices"
VOICE_DIR = os.environ.get("VOICE_DIR", "")


def voices():
    return json.load(open(VOICES / "voices.json"))


def sample(name):
    """'L2' -> the decrypted sample in $VOICE_DIR; a path is returned as is."""
    if name in voices() and voices()[name].get("plain"):     # a synthetic sample, kept in the repo as is
        return str(VOICES / voices()[name]["sample"].split("/")[-1])
    if name in voices():
        p = pathlib.Path(VOICE_DIR) / f"{name}.wav"
        if not p.exists():
            raise FileNotFoundError(f"{p} missing: run build/setup_voice.sh first (see the ib-voiced-reel skill)")
        return str(p)
    return name


def master_chain(voice_name):
    """The ffmpeg chain for a named clone: rumble cut, the voice's EQ curve,
    a light de-esser and gentle compression. None for anything else."""
    ref = voice_name.split(":", 1)[1] if voice_name.startswith("clone:") else None
    v = voices().get(ref)
    if not v:
        return None
    entries = ";".join(f"entry({b},{g})" for b, g in v["eq"])
    return (f"highpass=f=75,firequalizer=gain_entry='{entries}',deesser=i=0.3,"
            "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=140:makeup=1.5")


def next_voice():
    """The voice for the next Reel: whichever of L2 and L3 was not used last."""
    rot = [k for k, v in voices().items() if v.get("rotation")]      # L2 and L3; test voices are never logged
    log = [x for x in json.load(open(VOICES / "voice_log.json")) if x["voice"] in rot]
    last = log[-1]["voice"] if log else rot[-1]
    return rot[(rot.index(last) + 1) % len(rot)]


def log_voice(reel, voice, date=None):
    """Record which voice a Reel used (one entry per Reel; a re-render updates it)."""
    import datetime
    path = VOICES / "voice_log.json"
    log = [x for x in json.load(open(path)) if x["reel"] != reel]
    log.append(dict(reel=reel, voice=voice, date=date or datetime.date.today().isoformat()))
    json.dump(log, open(path, "w"), indent=1)


def make_voice(name):
    """'af_heart' (Kokoro), 'clone:L2' / 'clone:L3' (Pietro's two voices) or
    'clone:/path/to/reference.wav' (Pocket TTS on any consenting sample)."""
    if name.startswith("clone:"):
        ref = name.split(":", 1)[1]
        v = voices().get(ref, {})
        return CloneVoice(sample(ref), steps=v.get("steps", 8), min_pitch=v.get("min_pitch"), tempo=v.get("tempo"))
    from voice import Voice
    return Voice(name)
