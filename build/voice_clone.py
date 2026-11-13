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
            if getattr(self, "anchor", None) is not None:
                # Coherence (8 Nov): of the exact takes, keep the one that sounds most
                # like the sample, so every line sounds like the same speaker.
                if isinstance(self.anchor, bool):
                    self.anchor = voice_check.embedding(self.ref)
                with tempfile.TemporaryDirectory() as d2:
                    w2 = pathlib.Path(d2) / "t.wav"
                    write_wav(w2, a)
                    e = e - .001 * float(voice_check.embedding(w2) @ self.anchor)
            if best is None or e < best[0]:
                best = (e, a, heard, ws)
            if e == 0 and getattr(self, "anchor", None) is None:
                break
        self.log.append(dict(text=text, wer=round(max(best[0], 0), 3), heard=best[2], takes=k + 1))
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


BRIGHT = ("highpass=f=110,equalizer=f=150:t=q:w=1:g=-3,equalizer=f=300:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=3,"
          "equalizer=f=7000:t=q:w=1:g=1.5,deesser=i=0.3,acompressor=threshold=-20dB:ratio=2:attack=12:release=140:makeup=1.5")


def key(voice_name):
    """'clone:G2' or 'G2' -> 'G2' (the voices.json key), or None."""
    k = voice_name.split(":", 1)[1] if voice_name.startswith("clone:") else voice_name
    return k if k in voices() else None


def master_chain(voice_name):
    """The ffmpeg chain for a named voice: its own chain if it has one
    ("bright" = the 8 Nov audition chain, "kokoro" = voice.MASTER), else the
    clone chain built from its EQ curve. None for unnamed voices."""
    v = voices().get(key(voice_name) or "")
    if not v:
        return None
    if v.get("denoise"):
        # 13 Nov (Levels #12, G2): a non-local-means de-noise AFTER the voice's own chain. On the G2 stem
        # DNSMOS voice 3.29 -> 3.35 (SIG 3.53 -> 3.57, BAK 4.09 -> 4.14), same 17/20 sentences heard
        # exactly cut by cut; strength 2e-4 to 8e-4 scored the same, placed before the chain it did nothing;
        # afftdn (nr 6 or 10) and a stronger de-ess scored lower.
        return master_chain_plain(v) + "," + v["denoise"]
    return master_chain_plain(v)


def master_chain_plain(v):
    if v.get("chain") == "bright":
        return BRIGHT
    if v.get("chain") == "kokoro" or v.get("engine") == "kokoro":
        from voice import MASTER
        return MASTER
    entries = ";".join(f"entry({b},{g})" for b, g in v["eq"])
    return (f"highpass=f=75,firequalizer=gain_entry='{entries}',deesser=i=0.3,"
            "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=140:makeup=1.5")


# Since 8 Nov (Pietro): Reels rotate G2, BELLA, EMMA, one each time, for a month
# (to about 8 Dec), then he decides. YouTube was always GEORGE until 10 Nov.
# From 11 Nov (Pietro: "experiment with different voices. A different one each day, until
# we find the perfect one"): a different voice every day, the same one for that day's long
# video and Short, in the order of "youtube_trial" in voices.json (Reel voices excluded so the
# channels stay distinct). When the list runs out it starts again; when Pietro picks one, set
# YOUTUBE_PICK to it and the trial ends.
# 13 Nov (Pietro, the Shorts production standard, docs/production/short-form-standard.md): the narrator is
# Kokoro af_heart, en-us, speed 0.9, for long videos and Shorts. The trial ends; its log stays as history.
# 13 Nov, cinematic-upgrade directive: the same narrator for finance Reels too (REEL_PICK), ending the G2, BELLA,
# EMMA rotation; build/voices/voice_log.json and docs/production/voice-decision.md keep the history. To reopen a
# trial set the pick back to None.
YOUTUBE_PICK = "HEART"
REEL_PICK = "HEART"
TRIAL_START = "2026-11-11"


def youtube_trial():
    return sorted((v["youtube_trial"], k) for k, v in voices().items() if v.get("youtube_trial"))


def youtube_voice(date=None):
    """The voice for a YouTube video made on this date (default today, New York)."""
    import datetime
    if YOUTUBE_PICK:
        return YOUTUBE_PICK
    if date is None:
        try:
            from zoneinfo import ZoneInfo
            date = datetime.datetime.now(ZoneInfo("America/New_York")).date()
        except Exception:
            date = datetime.date.today()
    elif isinstance(date, str):
        date = datetime.date.fromisoformat(date)
    day = (date - datetime.date.fromisoformat(TRIAL_START)).days
    if day < 0:
        return "GEORGE"
    trial = [k for _, k in youtube_trial()]
    return trial[day % len(trial)]


YOUTUBE_VOICE = youtube_voice()


def rotation():
    return [k for k, v in voices().items() if v.get("rotation")]


def next_voice():
    """The voice for the next Reel: REEL_PICK (the channel narrator since 13 Nov), else the rotation voice
    after the last one logged (the 8 Nov G2, BELLA, EMMA test, kept for the record)."""
    if REEL_PICK:
        return REEL_PICK
    rot = rotation()
    log = [x for x in json.load(open(VOICES / "voice_log.json")) if x["voice"] in rot]
    if not log:
        return rot[0]
    return rot[(rot.index(log[-1]["voice"]) + 1) % len(rot)]


def log_voice(reel, voice, date=None):
    """Record which voice a Reel used (one entry per Reel; a re-render updates it)."""
    import datetime
    path = VOICES / "voice_log.json"
    log = [x for x in json.load(open(path)) if x["reel"] != reel]
    log.append(dict(reel=reel, voice=voice, date=date or datetime.date.today().isoformat()))
    json.dump(log, open(path, "w"), indent=1)


def make_voice(name):
    """A voices.json name ('G2', 'BELLA', 'EMMA', 'GEORGE', also 'clone:G2'),
    a Kokoro voice ('af_heart'), or 'clone:/path/to/reference.wav'."""
    k = key(name)
    v = voices().get(k, {}) if k else {}
    if v.get("engine") == "kokoro":                       # stock Kokoro voice, said directly
        from voice import Voice
        voice = Voice(v["kokoro_voice"], speed=v.get("speed", 1.0))
        voice.pace_scale = v.get("speed", 1.0)
        return voice
    if k or name.startswith("clone:"):
        ref = k or name.split(":", 1)[1]
        cv = CloneVoice(sample(ref), steps=v.get("steps", 8), min_pitch=v.get("min_pitch"), tempo=v.get("tempo"))
        if v.get("coherent"):                             # pick, of every line's takes, the one closest to the sample
            cv.anchor = True
            cv.tries = v.get("takes", 8)
        return cv
    from voice import Voice
    return Voice(name)
