"""
Is the sound of the drawn beats tied to what moves? (16 Nov 2026, YouTube #10; audio-standard.md 5.)

    python3 build/sfx_sync.py build/youtube_ep010.py              both sound modes on the same script, no voice needed
    python3 build/sfx_sync.py build/youtube_ep009.py --json out.json

Builds the film's scenes on estimated timings (2.6 words a second; the real voice moves every time a little, which
does not change the comparison) twice: with the 15 Nov sound (fx="pops": one pop per visual change, a ding per card)
and with the action-timed sound (fx="action", the default from 16 Nov). For the drawn beats and cards only (filmed
beats carry their own foley), it reads the page itself and reports:

  key actions   things on screen that land and should be heard: a stamp landing, a coin landing, a bar finishing,
                a number finishing its count, a card or box popping in (read off the HTML, data-fx and timing)
  coverage      share of key actions with an effect starting within 0.15 s of the landing
  on action     share of effects that start within 0.15 s of any animated element starting or landing in its scene
  distinct      how many different sounds the drawn beats use
"""

import json
import re
import sys

import numpy as np

sys.path.insert(0, "build")
import yt_preview          # noqa: E402
import youtube as Y        # noqa: E402
import sketch              # noqa: E402
from voice import split_sentences, SR     # noqa: E402

ACT = re.compile(r'class="a[^"]*" data-fx="([a-zA-Z]+)" data-at="([0-9.\-]+)" data-d="([0-9.]+)"')
COIN = sketch._COIN
WIN = .15


def fake_items(ep):
    items = []
    for c, ch in enumerate(ep["chapters"]):
        n = len(ch["title"].split())
        items.append(("title", c, None, np.zeros(int(max(n / 2.6, .9) * SR), np.float32), [(ch["title"], 0, n / 2.6)]))
        for b, beat in enumerate(ch["beats"]):
            segs, t = [], 0.0
            for s in split_sentences(beat["say"]):
                d = len(s.split()) / 2.6
                segs.append((s, t, t + d))
                t += d + .35
            items.append(("beat", c, b, np.zeros(int(t * SR), np.float32), segs))
    return items


def key_actions(html):
    keys, anyt = [], []
    marks = list(ACT.finditer(html))
    for i, m in enumerate(marks):
        fx, at, d = m.group(1), float(m.group(2)), float(m.group(3))
        body = html[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(html)]
        anyt += [at, at + d / 2, at + d]                               # start, impact, landing
        if fx in ("stamp", "coinflip", "growY", "growYdown", "scaleY", "count") or (fx in ("pop", "scale", "slide") and COIN.search(body)):
            keys.append(at + d * (.85 if fx == "stamp" else 1))
        elif fx == "pop" and m.group(0).startswith('class="a"') and "<div" in body[:400]:
            keys.append(at + d * .5)                                   # an HTML card or box popping in
    return keys, anyt


def measure(ep, mode):
    e = dict(ep, fx=mode)
    for reg in (Y.PACING, Y.CINE, Y.BEATS, sketch.SOUND_LOG):
        reg.clear()
    Y.CAM_USE.clear()
    sc, chapters, sounds, total = Y.scenes(e, fake_items(e))
    t, keys, anyt, spans = 0.0, [], [], []
    for s in sc:
        if s["html"]:                                                  # filmed beats leave an empty placeholder
            k, a = key_actions(s["html"])
            keys += [t + x for x in k]
            anyt += [t + x for x in a]
            spans.append((t, t + s["dur"]))
        t += s["dur"]
    inside = lambda x: any(a <= x < b for a, b in spans)
    fx = [ev for ev in sounds if inside(ev[1])]
    on = np.array(sorted(fx[i][1] for i in range(len(fx))))
    near = lambda x, arr: len(arr) and np.min(np.abs(np.asarray(arr) - x)) <= WIN
    cov = sum(1 for k in keys if near(k, on)) / max(len(keys), 1)
    onact = sum(1 for ev in fx if near(ev[1], anyt)) / max(len(fx), 1)
    kinds = sorted({ev[0] for ev in fx})
    drawn = len(spans)
    return dict(mode=mode, drawn_scenes=drawn, key_actions=len(keys), effects=len(fx), coverage=round(cov, 3),
                on_action=round(onact, 3), distinct=len(kinds), kinds=kinds, effects_per_scene=round(len(fx) / max(drawn, 1), 2))


if __name__ == "__main__":
    ep = yt_preview.load_ep(sys.argv[1])
    res = [measure(ep, "pops"), measure(ep, "action")]
    for r in res:
        print(f"  {r['mode']:>6}: {r['drawn_scenes']} drawn scenes and cards, {r['key_actions']} key actions, {r['effects']} effects "
              f"({r['effects_per_scene']} a scene), coverage {r['coverage']:.0%}, on an action {r['on_action']:.0%}, "
              f"{r['distinct']} sounds: {', '.join(r['kinds'])}")
    if "--json" in sys.argv:
        json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
