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
    "experian": "ɛkspˈɪɹiən",
    "affirm": "əfˈɜɹm",
    "ebitda": "ˈibɪtdˌɑ",
    "ebit": "ˈibɪt",
    "wacc": "wˈæk",
    "dcf": "dˌisˌiˈɛf",
    "that's": "ðæts",
    "questions": "kwˈɛsʧᵊnz",
    "moic": "mˈYk",
    "irr": "ˌIˌɑɹˈɑɹ",
    "you've": "juv",
    "here's": "hˈɪɹz",
    "what's": "wˈʌts",
    "borrows": "bˈɑɹOz",
    "compound": "kəmpˈWnd",   # the verb; the dictionary has the noun
    "a": "ɐ",          # the article is reduced; the dictionary gives the letter name
    "mackay": "məkˈI",
    "goldgar": "ɡˈOldɡɑɹ",
    "garber": "ɡˈɑɹbəɹ",
    "schabowski": "ʃəbˈɔfski",
    "poehl": "pˈOl",
    "bundesbank": "bˈʊndəsbˌæŋk",
    "treuhand": "tɹˈYhˌɑnt",
    "alexanderplatz": "ˌælɪɡzˈændəɹplˌɑts",
    "gdr": "ʤˌidˌiˈɑɹ",
    "akerlof": "ˈAkəɹlˌɔf",
    "yellen": "jˈɛlən",
    "reint": "ɹˈInt",
    "gropp": "ɡɹˈɑp",
    "schroeder": "ʃɹˈOdəɹ",
    "tietmeyer": "tˈitmˌIəɹ",
    "lothar": "lˈOtɑɹ",
    "maiziere": "mɛzjˈɛɹ",
    "trabi": "tɹˈæbi",
    "de": "də",
    "guenter": "ɡˈʊntəɹ",
    "hans": "hˈɑns",
    "karl": "kˈɑɹl",
    "janet": "ʤˈænɪt",
    "unlevered": "ʌnlˈɛvəɹd",
}

VOICELESS = set("ptkfθsʃʧ")
SIBILANT = ("s", "z", "ʃ", "ʒ", "ʧ", "ʤ")


def inflect(w, look):
    """Plurals, -ed and -ing from the stem, for words the dictionary only has in
    their base form (it has 'tulip', not 'tulips'). Same rules a speaker uses:
    s/z/iz after the stem's last sound, t/d/id for the past."""
    def end(p):
        return p.rstrip("ˈˌ")[-1:]
    for suf, stems in (("ies", ("y",)), ("es", ("",)), ("s", ("",)), ("'s", ("",))):
        if w.endswith(suf) and len(w) > len(suf) + 2:
            for st in stems:
                p = look(w[: -len(suf)] + st)
                if p:
                    e = end(p)
                    return p + ("ɪz" if p.endswith(SIBILANT) else "s" if e in VOICELESS else "z")
    if w.endswith("ed") and len(w) > 4:
        for stem in (w[:-2], w[:-1], w[:-3] if w[-3] == w[-4] else None):
            p = stem and look(stem)
            if p:
                e = end(p)
                return p + ("ɪd" if e in "td" else "t" if e in VOICELESS else "d")
    if w.endswith("ing") and len(w) > 5:
        for stem in (w[:-3], w[:-3] + "e", w[:-4] if w[-4] == w[-5] else None):
            p = stem and look(stem)
            if p:
                return p + "ɪŋ"
    return None


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
            look = lambda x: PHONEMES.get(x) or self.dict.get(x)
            p = look(w) or self.dict.get(w.strip("'")) or inflect(w, look)
            if not p:
                raise KeyError(f"No pronunciation for {tok!r}; add it to PHONEMES")
            out.append(p)
        s = " ".join(out)
        return re.sub(r" ([.,!?;:])", r"\1", s)

    def say(self, text, speed=None):
        ps = self.phonemes(text)
        ids = [self.vocab[c] for c in ps if c in self.vocab]
        missing = {c for c in ps if c not in self.vocab}
        if missing:
            raise ValueError(f"Phonemes outside the model vocabulary: {missing}")
        style = self.style[min(len(ids), len(self.style)) - 1]
        audio = self.sess.run(None, {"tokens": np.array([[0, *ids, 0]], dtype=np.int64),
                                     "style": np.asarray(style, dtype=np.float32),
                                     "speed": np.array([speed or self.speed], dtype=np.float32)})[0]
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


def split_sentences(text):
    import re as _re
    return [x.strip() for x in _re.split(r"(?<=[.!?])\s+", text.strip()) if x.strip()]


def passage(voice, text, speed=None):
    """Synthesise several sentences in one pass, for natural intonation across
    them, then find where each sentence starts and ends.

    Kokoro leaves a pause at every sentence end. Each expected boundary (from
    the sentences' share of the phonemes) is matched to the nearest real pause,
    so the timings come from the audio itself. Returns (audio, [(sentence,
    start, end), ...]) in seconds.
    """
    sents = split_sentences(text)
    audio = voice.say(" ".join(sents), speed=speed)
    if hasattr(voice, "align"):                       # a cloned voice: timings from the transcript check
        segs = voice.align(sents, audio)
        if segs:
            return audio, segs
    if len(sents) == 1:
        return audio, [(sents[0], 0.0, len(audio) / SR)]
    hop = int(.01 * SR)
    rms = np.array([np.sqrt(np.mean(audio[i:i + hop] ** 2)) for i in range(0, len(audio) - hop, hop)])
    quiet = rms < max(.006, np.percentile(rms, 95) * .06)
    allruns, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            allruns.append((i * .01, j * .01, j - i))
            i = j
        else:
            i += 1
    # Pauses of 90 ms or more; if a sentence end was spoken faster than that,
    # accept shorter ones (down to 40 ms) rather than fail.
    for min_len in (9, 6, 4):
        runs = [(a, b) for a, b, n in allruns if n >= min_len]
        if len(runs) >= len(sents) - 1:
            break
    lens = [len(voice.phonemes(x)) for x in sents]
    total = len(audio) / SR
    bounds, used = [], -1
    for k in range(1, len(sents)):
        expect = total * sum(lens[:k]) / sum(lens)
        cands = [(abs((a + b) / 2 - expect) - (b - a) * .5, n) for n, (a, b) in enumerate(runs) if n > used]
        if not cands:
            raise ValueError(f"Could not find the pause before: {sents[k]!r}")
        _, n = min(cands)
        used = n
        bounds.append(runs[n])
    out, start = [], 0.0
    for k, x in enumerate(sents):
        end = bounds[k][0] if k < len(bounds) else total
        out.append((x, round(start, 3), round(end, 3)))
        if k < len(bounds):
            start = max(bounds[k][1] - .03, 0)
    return audio, out


# A voice-recording chain for ffmpeg: rumble cut, a little warmth, the
# synthetic fizz around 7 kHz taken down, gentle compression and a very small
# room, so the voice sounds recorded rather than generated.
MASTER = ("highpass=f=75,equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=7200:t=q:w=1.3:g=-2.5,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=140:makeup=1.5,"
          "aecho=0.9:0.85:19|31:0.09|0.05")
