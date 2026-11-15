"""
Delivery check (15 Nov 2026): the other half of a natural narrator. The 14 Nov chain fix removed the processed sound;
this measures how the lines are said, so a Short's script can be compared with the one before it.

    python3 build/delivery_check.py build/shorts_first-cash-machine.py build/shorts_jackpot-two-billion.py

For each episode (story engine, build/story.py) it synthesises the narration exactly as the render does
(story.synth: one pass per beat, split=True beats sentence by sentence) and reports:
    words per second      speaking rate per sentence (words / sentence time), mean and spread (sd)
    sentence gaps         the pauses Kokoro leaves between sentences inside one pass (mean, sd, min, max)
    inner pauses          silences of 150 ms or more inside a sentence (a held breath or a stumble)
    words per sentence    mean and max (short sentences read as spoken)
    contractions          sentences with a contraction (it's, wasn't, that's ...)
    split beats           beats said sentence by sentence instead of in one pass
Nothing here is a listening verdict: it is supporting evidence for one. JSON lands in
build/out/delivery-check/<slug>.json.
"""

import importlib.util
import json
import pathlib
import re
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from voice import SR            # noqa: E402

OUT = pathlib.Path(__file__).parent / "out" / "delivery-check"
CONTRACTION = re.compile(r"\b\w+'(s|t|re|ve|ll|d|m)\b", re.I)


def load(path):
    spec = importlib.util.spec_from_file_location("ep_" + pathlib.Path(path).stem.replace("-", "_"), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.EP


def inner_pauses(a, floor_frac=.06, min_s=.15):
    hop = int(.01 * SR)
    rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, max(len(a) - hop, 1), hop)])
    if not len(rms):
        return []
    quiet = rms < max(.006, np.percentile(rms, 95) * floor_frac)
    out, run = [], 0
    for q in list(quiet[5:-5]) + [False]:
        if q:
            run += 1
        else:
            if run * .01 >= min_s:
                out.append(round(run * .01, 2))
            run = 0
    return out


def measure(path, voice_name="HEART"):
    import story
    ep = load(path)
    _, parts = story.synth(ep, voice_name)
    rows, gaps = [], []
    for k, (audio, segs) in parts.items():
        for j, (text, x, y) in enumerate(segs):
            seg = audio[int(x * SR):int(y * SR)]
            words = len(text.split())
            rows.append(dict(part=k, text=text, words=words, seconds=round(y - x, 2), wps=round(words / max(y - x, .01), 2),
                             inner=inner_pauses(seg), contraction=bool(CONTRACTION.search(text))))
            if j:
                gaps.append(round(x - segs[j - 1][2], 3))
    wps = [r["wps"] for r in rows]
    st = lambda v: dict(mean=round(float(np.mean(v)), 3), sd=round(float(np.std(v)), 3), min=round(float(min(v)), 3),
                        max=round(float(max(v)), 3)) if v else None
    s = dict(slug=ep["slug"], sentences=len(rows), words=sum(r["words"] for r in rows),
             speaking_s=round(sum(r["seconds"] for r in rows), 2), wps=st(wps), sentence_gaps=st(gaps),
             inner_pauses=sum(len(r["inner"]) for r in rows),
             words_per_sentence=dict(mean=round(float(np.mean([r["words"] for r in rows])), 2), max=max(r["words"] for r in rows)),
             contractions=sum(r["contraction"] for r in rows),
             split_beats=sum(1 for b in ep["beats"] if b.get("split")), rows=rows)
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(s, open(OUT / f"{ep['slug']}.json", "w"), indent=1)
    return s


def line(s):
    w, g = s["wps"], s["sentence_gaps"]
    return (f"{s['slug']}: {s['sentences']} sentences, {s['words']} words, {w['mean']} w/s (sd {w['sd']}, {w['min']} to {w['max']}); "
            f"sentence gaps {g['mean'] if g else '-'} s (sd {g['sd'] if g else '-'}, {g['min'] if g else '-'} to {g['max'] if g else '-'}); "
            f"{s['inner_pauses']} inner pauses; {s['words_per_sentence']['mean']} words a sentence (max {s['words_per_sentence']['max']}); "
            f"{s['contractions']} with a contraction; {s['split_beats']} split beats")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(line(measure(p)), flush=True)
