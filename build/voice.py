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
    # 20 Nov (YouTube Short, the short-interest puzzle): the illustration's three owners
    "ann": "ˈæn",
    "ann's": "ˈænz",
    "cal": "kˈæl",
    # misaki reads SEC as the word "sec" (sˈɛk; heard "sex" in the first cut): the letters (the recogniser then wrote
    # "SESC" / "SESE", so the 20 Nov Short says "the market regulator" instead; kept for the next script)
    "sec": "ˌɛsˌiˈsi",
    "sec's": "ˌɛsˌiˈsiz",
    # 19 Nov (YouTube #13, GameStop 2021)
    "gamestop": "ɡˈAmstˌɑp",
    "reddit": "ɹˈɛdɪt",
    "gensler": "ɡˈɛnzləɹ",
    "nscc": "ˌɛnˌɛsˌsisˈi",
    "tenev": "tˈɛnəv",
    "robinhood": "ɹˈɑbɪnhˌʊd",
    "robinhood's": "ɹˈɑbɪnhˌʊdz",
    "wallstreetbets": "wˈɔlstɹˌitbˌɛts",
    "vlad": "vlˈæd",
    "melvin": "mˈɛlvɪn",
    # 18 Nov, Reel A (accretion / dilution): "dilutive" was heard "deludive" with the default reading
    "dilutive": "daɪlˈutɪv",
    # 18 Nov, YouTube #12 (Long-Term Capital Management, 1998)
    "merton": "mˈɜɹtᵊn",
    "scholes": "skˈOlz",
    "myron": "mˈIɹən",
    "meriwether": "mˈɛɹiwˌɛðəɹ",
    "merrill": "mˈɛɹəl",
    "donald": "dˈɑnᵊld",
    "ubs": "jˌubˌiˈɛs",
    "ltcm": "ˌɛltˌisˌiˈɛm",
    # 20 Nov (YouTube #14, Silicon Valley Bank 2023)
    "svb": "ˈɛs vˈi bˈi",
    "svb's": "ˈɛs vˈi bˈiz",
    "fdic": "ˈɛf dˈi ˈI sˈi",
    "barr": "bˈɑɹ",
    "debtholders": "dˈɛthˌOldəɹz",
    "wachovia": "wˌɑʧəvˈiə",
    "salomon": "sˈæləmən",
    "mackenzie": "məkˈɛnzi",
    "mcdonough": "məkdˈʌnə",
    # 22 Nov (YouTube #15, Barings 1995)
    "leeson": "lˈisən",
    "mia": "mˈiə",                 # 23 Nov (Reel B): the print shop owner in our story
    "leeson's": "lˈisənz",
    "barings'": "bˈɛɹɪŋz",
    "nikkei": "nˈɪkA",
    "simex": "sˈImɛks",
    "kuala": "kwˈɑlə",
    "lumpur": "lˈʊmpʊɹ",
    "ing": "ˈI ˈɛn ʤˈi",
    "mcdonough's": "məkdˈʌnəz",
    "counterparty": "kˈWntəɹpˌɑɹɾi",
    "counterparties": "kˈWntəɹpˌɑɹɾiz",
    # 17 Nov, the coin toss Short (Paul Samuelson, 1963)
    "samuelson": "sˈæmjuəlsən",
    # 17 Nov, YouTube #11 (Herstatt, 1974)
    "herstatt": "hˈɛɹʃtˌɑt",
    "herstatt's": "hˈɛɹʃtˌɑts",
    "bankhaus": "bˈæŋkhˌWs",
    "deutsche": "dˈYʧə",
    "bis": "bˌiˌIˈɛs",
    "cls": "sˌiˌɛlˈɛs",
    "cls's": "sˌiˌɛlˈɛsɪz",
    "fx": "ˌɛfˈɛks",
    "withdrew": "wɪðdɹˈu",
    "sizeable": "sˈIzəbᵊl",
    # 15 Nov, YouTube #9 (Charles Ponzi and the reply coupon)
    "ponzi": "pˈɑnzi",
    "pulitzer": "pˈʊlɪtsəɹ",
    "ponzi's": "pˈɑnziz",
    "centavos": "sɛntˈɑvOz",
    "peseta": "pəsˈAtə",
    "madoff": "mˈAdɔf",
    "madoff's": "mˈAdɔfs",
    # 13 Nov, cinematic upgrade: finance terms the narrator must never guess (narrator_check.py)
    "barron": "bˈæɹən",                   # 14 Nov, the first cash machine Short (John Shepherd-Barron)
    "barclays": "bˈɑɹkliz",
    "enfield": "ˈɛnfˌild",
    "lbo": "ˌɛlbˌiˈO",
    "lbos": "ˌɛlbˌiˈOz",
    "ipo": "ˌIpˌiˈO",
    "ipos": "ˌIpˌiˈOz",
    "ev": "ˌiˈvi",
    "fcf": "ˌɛfsˌiˈɛf",
    "ltv": "ˌɛltˌiˈvi",
    "jpmorgan": "ʤˈApˈi mˈɔɹɡən",
    "goldman": "ɡˈOldmən",
    "sachs": "sˈæks",
    "threadneedle": "θɹˈɛdnˌidᵊl",
    "garraway's": "ɡˈæɹəwˌAz",
    "tulips": "tˈuləps",
    "aislabie": "ˈAzləbi",                # 13 Nov, YouTube #6 (John Aislabie, 1720)
    "odlyzko": "Odlˈɪʒkˌo",
    "southwark": "sˈʌðəɹk",
    "heinze": "hˈInts",                   # 13 Nov, YouTube #7 (the Panic of 1907)
    "tino": "tˈinO",                      # 16 Nov, YouTube #10 (the salad oil swindle, 1963)
    "angelis": "ænʤˈɛlɪs",                # De Angelis
    "haupt": "hˈWpt",                     # Ira Haupt & Co.
    "ira": "ˈIɹə",
    "beane": "bˈin",                      # J. R. Williston & Beane
    "buffett": "bˈʌfᵻt",
    "multi": "mˈʌlti",
    "cortelyou": "kˈɔɹtəljˌu",
    "aldrich": "ˈɔldɹɪʧ",
    "bretton": "bɹˈɛtᵊn",                 # 14 Nov, YouTube #8 (the gold window, 1971)
    "triffin": "tɹˈɪfɪn",
    "connally": "kˈɑnəli",
    "kissinger": "kˈɪsɪnʤəɹ",
    "smithsonian": "smɪθsˈOniən",
    "paul": "pˈɔl",
    "volcker": "vˈOlkəɹ",
    "imf": "ˌIˌɛmˈɛf",
    "knox": "nˈɑks",
    "bordo": "bˈɔɹdO",
    "pierpont": "pˈɪɹpɑnt",
    "rockefeller": "ɹˈɑkəfˌɛləɹ",
    "shareholders'": "ʃˈɛɹhˌOldəɹz",       # 12 Nov, Levels #11
    "uk": "jˌukˈA",                        # 13 Nov, Friday the 13th Short
    "shareholders": "ʃˈɛɹhˌOldəɹz",
    "multiplied": "mˈʌltəplˌId",          # 12 Nov, YouTube #5
    "goldsmiths'": "ɡˈOldsmˌɪθs",
    "alibaba": "ˌælɪbˈɑbə",
    "experian": "ɛkspˈɪɹiən",
    "affirm": "əfˈɜɹm",
    "ebitda": "ˈibɪtdˌɑ",
    "ebit": "ˈibɪt",
    "wacc": "wˈæk",
    "dcf": "dˌisˌiˈɛf",
    "that's": "ðæts",
    "questions": "kwˈɛsʧᵊnz",
    "moic": "mˈYɪk",                     # 14 Nov, Levels #13: MOY-ick, two syllables (as one syllable the recogniser heard "Mike" once)
    "irr": "ˌIˌɑɹˈɑɹ",
    "you've": "juv",
    "here's": "hˈɪɹz",
    "what's": "wˈʌts",
    "borrows": "bˈɑɹOz",
    "compound": "kəmpˈWnd",   # the verb; the dictionary has the noun
    "a": "ɐ",          # the article is reduced; the dictionary gives the letter name
    "mackay": "məkˈI",
    "mcnealy": "məknˈili",          # 10 Nov, YouTube #3
    "greenspan": "ɡɹˈinspæn",
    "microsystems": "mˈIkɹOsˌɪstəmz",
    "businessweek": "bˈɪznəswˌik",
    "keynes": "kˈAnz",              # 11 Nov, YouTube #4
    "nairn": "nˈɛɹn",
    "consols": "kˈɑnsɑlz",
    "consol": "kˈɑnsɑl",
    "versailles": "vəɹsˈI",
    "dawes": "dˈɔz",
    "chamberlain": "ʧˈAmbəɹlɪn",
    "maynard": "mˈAnəɹd",
    "hitler": "hˈɪtləɹ",
    "winston": "wˈɪnstən",
    "gordon": "ɡˈɔɹdən",
    "harvey": "hˈɑɹvi",
    "buyback": "bˈIbˌæk",
    "buybacks": "bˈIbˌæks",
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


# The narrator chain (14 Nov, Pietro: the voice should feel more natural; asked what was least natural, he picked
# "robotic / processed sound"). The 8 Nov chain below added a 19/31 ms "small room" echo (a comb filter on a dry
# voice), 2.5:1 compression and a warmth boost, and the masters then ran it into a limiter at 0.4 that was cutting
# 16% of the speech by up to 2 dB. Measured on the cash machine Short's narration, voice alone at -14 LUFS:
# old chain DNSMOS 3.29 (SIG 3.55), no echo 3.32, no echo and no pre-limiter 3.31, this chain 3.40 (SIG 3.62), the
# untouched Kokoro output 3.40; the short-term loudness spread went from 9.8 dB (squashed) back to 12.4 dB (the raw
# voice's 12.5). So the narrator is now left almost as Kokoro says it: rumble cut and a light 1.5 dB dip of the
# synthetic fizz at 7 kHz. No compressor, no echo, no limiter before the master's single true-peak limiter.
MASTER = "highpass=f=70,equalizer=f=7200:t=q:w=1.3:g=-1.5"
MASTER_8NOV = ("highpass=f=75,equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=7200:t=q:w=1.3:g=-2.5,"
               "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=140:makeup=1.5,"
               "aecho=0.9:0.85:19|31:0.09|0.05")      # until 13 Nov; kept to re-render an old video exactly
