"""
Pick the best reference for the cloned voice from Pietro's recordings.

Pocket TTS copies a voice from one short sample, and which sample matters:
on 6 Nov the best 15 to 20 second window of the new memos scored 0.79 for
likeness against 0.71 for the first memo, on the same test. This script
finds it:

  1. cuts every memo into 14 to 20 second windows at natural pauses,
     skipping any region listed as a stumble or a repeated take;
  2. clones the same test lines from each window, several takes each;
  3. scores every take for likeness (speaker embedding against real speech
     from the OTHER memos, so a window is never judged against itself) and
     for words (transcript against the script);
  4. writes the ranking and the winning reference.

    python build/voice_refsearch.py out_dir memo1.m4a memo2.m4a ... \
        [--avoid memo2:15-31] [--takes 2] [--top 5]

Needs $SHERPA_DIR, $POCKET_DIR, $PARAKEET_DIR and $SPEAKER_MODEL (see
voice_clone.py and voice_check.py). Pietro's recordings and the references
made from them stay out of this public repo.
"""

import argparse
import json
import pathlib
import subprocess
import wave

import numpy as np

from voice import SR, write_wav
from voice_check import embedding, transcribe, wer
from voice_clone import CloneVoice, prepare_reference

LINES = ["Equity value. Earnings belong to shareholders, so you match them with equity.",
         "A company has a hundred of equity value and fifty of net debt. The share price doubles. What's the new enterprise value?",
         "What's your score out of four? Comment it below.",
         "Accretive. It pays with expensive shares for cheaper earnings."]


def load(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def pauses(a, min_s=.25):
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    q = rms < rms.max() * .03
    out, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]:
                j += 1
            if j - i >= min_s * 100:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


def windows(a, avoid, lo=14, hi=20):
    ends = [(x + y) / 2 for x, y in pauses(a)] + [len(a) / SR]
    start, out = 0.0, []
    while len(a) / SR - start >= lo:
        opts = [e for e in ends if lo <= e - start <= hi]
        if not opts:
            later = [e for e in ends if e > start + .01]
            if not later:
                break
            start = later[0]
            continue
        end = opts[-1]
        if not any(s < end and start < e for s, e in avoid):
            out.append((start, end))
        start = end
    return out


def chunks(a, size=12):
    ends = [(x + y) / 2 for x, y in pauses(a)] + [len(a) / SR]
    cuts = [0.0]
    for e in ends:
        if e - cuts[-1] > size:
            cuts.append(e)
    return list(zip(cuts[:-1], cuts[1:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("memos", nargs="+")
    ap.add_argument("--avoid", action="append", default=[], help="memo_stem:start-end in seconds")
    ap.add_argument("--takes", type=int, default=2)
    ap.add_argument("--top", type=int, default=5, help="windows re-tested with every take")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    avoid = {}
    for x in a.avoid:
        stem, rng = x.split(":")
        s, e = rng.split("-")
        avoid.setdefault(stem, []).append((float(s), float(e)))

    audio, targets, cands = {}, {}, []
    for m in a.memos:
        stem = pathlib.Path(m).stem
        wav = out / f"{stem}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m, "-ac", "1", "-ar", str(SR), str(wav)], check=True)
        audio[stem] = x = load(wav)
        for k, (s, e) in enumerate(chunks(x)):                     # real speech to judge clones against
            if e - s > 9 and not any(s < ee and ss < e for ss, ee in avoid.get(stem, [])):
                p = out / f"{stem}_t{k}.wav"
                write_wav(p, x[int(s * SR):int(e * SR)])
                targets.setdefault(stem, []).append(embedding(p))
        for s, e in windows(x, avoid.get(stem, [])):
            raw = out / f"{stem}_w{int(s)}.wav"
            write_wav(raw, x[int(s * SR):int(e * SR)])
            ref = out / f"{stem}_w{int(s)}_ref.wav"
            prepare_reference(raw, ref, max_s=21, min_s=10)
            cands.append(dict(name=f"{stem}@{int(s)}s", memo=stem, ref=str(ref)))

    def score(c, takes):
        v = CloneVoice(c["ref"])
        others = [t for m, ts in targets.items() if m != c["memo"] for t in ts]
        sims, errs = [], []
        for line in LINES:
            for _ in range(takes):
                x = v._take(line)
                p = out / "take.wav"
                write_wav(p, x)
                sims.append(float(np.mean([embedding(p) @ t for t in others])))
                errs.append(float(wer(line, transcribe(p))))
        return dict(likeness=round(float(np.mean(sims)), 3), spread=round(float(np.std(sims)), 3),
                    word_errors=round(float(np.mean(errs)), 3), clean=int(sum(e == 0 for e in errs)), takes=len(errs))

    for c in cands:                                                  # first pass: one take per line
        c.update(score(c, 1))
        print(f"{c['name']:16} likeness {c['likeness']:.3f}  word errors {c['word_errors']:.0%}", flush=True)
    best = sorted(cands, key=lambda c: -c["likeness"])[:a.top]
    for c in best:                                                   # second pass on the leaders
        c.update(score(c, a.takes))
        print(f"  {c['name']:14} likeness {c['likeness']:.3f} +/- {c['spread']:.3f}  clean {c['clean']}/{c['takes']}", flush=True)
    # Likeness first, but a sample whose clones keep slipping words costs
    # retakes and risks a wrong word: 10 points of word errors cost 0.05.
    win = max(best, key=lambda c: c["likeness"] - .5 * c["word_errors"])
    (out / "best_ref.wav").write_bytes(pathlib.Path(win["ref"]).read_bytes())
    reals = [(m, t) for m, ts in targets.items() for t in ts]
    ceiling = [float(x @ y) for i, (mx, x) in enumerate(reals) for my, y in reals[i + 1:] if mx != my]
    json.dump(dict(winner=win["name"], real_vs_real=round(float(np.mean(ceiling)), 3) if ceiling else None,
                   candidates=cands), open(out / "ranking.json", "w"), indent=1)
    print(f"best: {win['name']} (real vs real across memos: {np.mean(ceiling):.3f})" if ceiling else f"best: {win['name']}")


if __name__ == "__main__":
    main()
