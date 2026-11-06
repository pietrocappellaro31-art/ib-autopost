"""
Voiceover for Reels: Kokoro-82M (Apache 2.0) run locally with onnxruntime.

Kokoro was trained on phonemes from the misaki G2P, so words are looked up in
misaki's own US dictionaries (gold, then silver). Words not in either must be
given phonemes explicitly in PHONEMES below, never guessed: an unknown word
raises, so a mispronounced word cannot slip into a Reel unnoticed.

Each phrase is synthesised on its own, which gives exact phrase timings for
syncing captions and visuals.

Model files (not in the repo, ~350MB): put kokoro-v1.0.onnx and voices-v1.0.bin
in $KOKORO_DIR. Dictionaries: misaki's us_gold.json and us_silver.json in the
same folder. Sources: github.com/thewh1teagle/kokoro-onnx releases
(model-files-v1.0) and github.com/hexgrad/misaki (misaki/data).
"""

import json
import os
import re
import wave

import numpy as np
import onnxruntime as ort

SR = 24000
DIR = os.environ.get("KOKORO_DIR", "")

# Words outside misaki's dictionaries, with their phonemes written by hand.
PHONEMES = {
    "ebitda": "ˈibɪtdˌɑ",
    "ebit": "ˈibɪt",
    "wacc": "wˈæk",
    "dcf": "dˌisˌiˈɛf",
    "that's": "ðæts",
    "questions": "kwˈɛsʧᵊnz",
    "a": "ɐ",          # the article is reduced; the dictionary gives the letter name
}


class Voice:
    def __init__(self, voice="af_heart", speed=1.0, kdir=DIR):
        self.sess = ort.InferenceSession(os.path.join(kdir, "kokoro-v1.0.onnx"),
                                         providers=["CPUExecutionProvider"])
        self.voices = np.load(os.path.join(kdir, "voices-v1.0.bin"))
        self.style = self._style(voice)
        self.speed = speed
        cfg = os.path.join(kdir, "config.json")
        self.vocab = json.load(open(cfg))["vocab"]
        self.dict = {}
        for name in ("us_silver.json", "us_gold.json"):   # gold overrides silver
            for k, v in json.load(open(os.path.join(kdir, name))).items():
                self.dict[k.lower()] = v if isinstance(v, str) else (v.get("DEFAULT") or next(iter(v.values())))

    def _style(self, voice):
        """A voice name, or a blend like 'af_heart:0.7,af_bella:0.3'."""
        if ":" not in voice:
            return self.voices[voice]
        mix = None
        for part in voice.split(","):
            name, w = part.split(":")
            arr = self.voices[name] * float(w)
            mix = arr if mix is None else mix + arr
        return mix

    def phonemes(self, text):
        out = []
        for tok in re.findall(r"[A-Za-z']+|[.,!?;:]", text):
            if tok in ".,!?;:":
                out.append(tok)
                continue
            w = tok.lower()
            p = PHONEMES.get(w) or self.dict.get(w) or self.dict.get(w.strip("'"))
            if not p:
                raise KeyError(f"No pronunciation for {tok!r}; add it to PHONEMES")
            out.append(p)
        s = " ".join(out)
        return re.sub(r" ([.,!?;:])", r"\1", s)

    def say(self, text):
        ps = self.phonemes(text)
        ids = [self.vocab[c] for c in ps if c in self.vocab]
        missing = {c for c in ps if c not in self.vocab}
        if missing:
            raise ValueError(f"Phonemes outside the model vocabulary: {missing}")
        style = self.style[min(len(ids), len(self.style)) - 1]
        audio = self.sess.run(None, {"tokens": np.array([[0, *ids, 0]], dtype=np.int64),
                                     "style": np.asarray(style, dtype=np.float32),
                                     "speed": np.array([self.speed], dtype=np.float32)})[0]
        return trim(np.asarray(audio, dtype=np.float32).ravel())


def trim(a, thresh=0.004):
    """Cut leading and trailing near-silence, keeping a few ms of breath."""
    idx = np.where(np.abs(a) > thresh)[0]
    if not len(idx):
        return a
    pad = int(0.03 * SR)
    return a[max(idx[0] - pad, 0): idx[-1] + pad]


def write_wav(path, audio, sr=SR):
    a = np.clip(audio, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((a * 32767).astype(np.int16).tobytes())
