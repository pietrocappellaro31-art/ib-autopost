"""
Pietro's real voice: build a Reel on his own recording of its script, so the
voice is him, not a model of him (offered 6 Nov, when he asked for "no
difference between the way I talk and the way the Reels sound").

He reads the Reel's script in one memo, pauses and all. The memo is
transcribed with word timings (voice_check, Parakeet), the script is aligned
to what he said (edit distance over words, so a misheard word does not
break it), and each passage of the Reel (hook, each question and answer,
close) is cut out with its sentence timings. The Reel engine then places the
passages on its own timeline, with its own think time, exactly as it does
with a generated voice.

A real recording needs no AI label. Pietro's recordings stay out of the
public repo.

    parts = parts_from_recording([("hook", [sentences]), ("q0", [...]), ...], "memo.wav")
"""

import pathlib
import subprocess
import tempfile
import wave

import numpy as np

from voice import SR, write_wav
from voice_check import transcribe, words


def load(path):
    with tempfile.TemporaryDirectory() as d:
        w = pathlib.Path(d) / "a.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), str(w)], check=True)
        with wave.open(str(w)) as f:
            return np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768


def heard_words(a, size=13):
    """Word timings over a whole memo: transcribed in chunks cut at pauses
    (the recogniser is happiest under about 15 seconds), then offset."""
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    quiet = rms < rms.max() * .03
    cuts, run = [0.0], 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run == 20 and i / 100 - cuts[-1] > size:           # cut in the middle of a 0.2 s pause
            cuts.append(i / 100 - .1)
    cuts.append(len(a) / SR)
    out = []
    with tempfile.TemporaryDirectory() as d:
        for s, e in zip(cuts[:-1], cuts[1:]):
            p = pathlib.Path(d) / "c.wav"
            write_wav(p, a[int(s * SR):int(e * SR)])
            _, ws = transcribe(p, with_words=True)
            out += [(w, s + x, s + y) for w, x, y in ws]
    return out


def align(order, heard):
    """Script sentences (in reading order) against heard words: for every
    (part, sentence) the time of its first and last word."""
    ref = [(t, k, j) for k, (_, ss) in enumerate(order) for j, s in enumerate(ss) for t in words(s)]
    hyp = [(t, a, b) for w, a, b in heard for t in words(w)]
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        r = ref[i - 1][0]
        for j in range(1, m + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r != hyp[j - 1][0]))
    i, j, link = n, m, {}
    while i > 0 and j > 0:
        if d[i, j] == d[i - 1, j - 1] + (ref[i - 1][0] != hyp[j - 1][0]):
            link[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif d[i, j] == d[i - 1, j] + 1:
            i -= 1
        else:
            j -= 1
    spans = {}
    for i, (_, k, jj) in enumerate(ref):
        if i in link:
            a, b = hyp[link[i]][1], hyp[link[i]][2]
            s = spans.setdefault((k, jj), [a, b])
            s[0], s[1] = min(s[0], a), max(s[1], b)
    missing = [order[k][1][jj] for k, (_, ss) in enumerate(order) for jj in range(len(ss)) if (k, jj) not in spans]
    if missing:
        raise ValueError(f"not found in the recording: {missing}")
    return spans, d[n, m] / max(n, 1)


def parts_from_recording(order, memo, lead=.12, tail=.16):
    a = load(memo)
    heard = heard_words(a)
    spans, err = align(order, heard)
    starts = [spans[(k, 0)][0] for k in range(len(order))]
    ends = [spans[(k, len(ss) - 1)][1] for k, (_, ss) in enumerate(order)]
    parts = {}
    for k, (key, ss) in enumerate(order):
        s0 = max(starts[k] - lead, ends[k - 1] + .02 if k else 0)
        e0 = min(ends[k] + tail, starts[k + 1] - .03 if k + 1 < len(order) else len(a) / SR)
        clip = a[int(s0 * SR):int(e0 * SR)].copy()
        f = int(.01 * SR)                                            # 10 ms fades: no clicks at the cuts
        clip[:f] *= np.linspace(0, 1, f)
        clip[-f:] *= np.linspace(1, 0, f)
        segs = [[s, spans[(k, j)][0] - s0, spans[(k, j)][1] - s0] for j, s in enumerate(ss)]
        segs[0][1] = max(segs[0][1] - .03, 0.0)              # captions start with the first word, not the cut
        for j in range(len(segs) - 1):
            segs[j][2] = min(segs[j][2] + .06, segs[j + 1][1])
        segs[-1][2] = len(clip) / SR
        clip, segs = tighten(clip, segs)
        parts[key] = (clip, [(s, round(x, 3), round(y, 3)) for s, x, y in segs])
    return parts, err


def tighten(clip, segs, longest=.45, keep=.3):
    """Shorten long silences inside a passage to a natural beat, the way an
    editor would: a pause of more than `longest` seconds becomes `keep`
    seconds. Short pauses, breaths and the rhythm of the voice are untouched.
    Sentence timings move with the audio."""
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(clip[i:i + hop] ** 2)) for i in range(0, len(clip) - hop, hop)])
    if not len(rms):
        return clip, segs
    quiet = rms < rms.max() * .03
    cuts, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) / 100 > longest and i > 0 and j < len(quiet):     # inside the passage, not at its edges
                mid = (i + j) / 200
                cuts.append((mid - ((j - i) / 100 - keep) / 2, mid + ((j - i) / 100 - keep) / 2))
            i = j
        else:
            i += 1
    if not cuts:
        return clip, segs
    keep_parts, t0 = [], 0.0
    for a, b in cuts:
        keep_parts.append(clip[int(t0 * SR):int(a * SR)])
        t0 = b
    keep_parts.append(clip[int(t0 * SR):])
    f = int(.008 * SR)
    for k in range(len(keep_parts)):                                   # tiny fades at every join
        x = keep_parts[k].copy()
        if len(x) > 2 * f:
            if k:
                x[:f] *= np.linspace(0, 1, f)
            if k < len(keep_parts) - 1:
                x[-f:] *= np.linspace(1, 0, f)
        keep_parts[k] = x
    shift = lambda t: t - sum(min(max(t - a, 0), b - a) for a, b in cuts)
    return np.concatenate(keep_parts), [[s, shift(x), shift(y)] for s, x, y in segs]
