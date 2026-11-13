"""
Integration test for the cinematic upgrade (13 Nov 2026), not an episode for release: one short long-form film made
by the normal long-video engine (build/youtube.py) with a FILMED beat (kind="cine", the Exchange Alley street from
build/cine_poc_newton.py) between drawn beats, and score="reflective" (build/score.py). It proves, on a real render,
that the daily long-video run can splice filmed scenes into a film, carry their foley and ambience in both mixes,
write the score with score.py and gate it.

    python3 build/youtube_cine_test.py          about 6 minutes on 2 CPUs (the filmed beat is most of it)

Facts (as YouTube #6, build/youtube_ep006.py): Exchange Alley's coffee houses were where shares were traded in 1720;
Newton sold his South Sea shares on 19 and 23 April 1720 and bought back in June (Odlyzko, Notes and Records 2019).
The street and its people are our illustration, badged RECONSTRUCTION.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from youtube import make  # noqa: E402

SOLD, BOUGHT = (2, "SOLD", "#0F766E"), (4, "BOUGHT", "#D93A12")          # as build/youtube_ep006.py
S = lambda art, txt="", lab="", hl=(), size=96, flip=False, **opts: dict(kind="sketch", art=art, opts=opts, label=lab, text=txt,
                                                                       hl=list(hl), size=size, flip=flip)


def street(w, h, dur, ctx):
    """The filmed beat: the PoC's street shot, timed to this beat, with its footsteps and street ambience."""
    import cine as C
    import cine_poc_newton as P
    import sfx
    shot, ex = P.shot_street(w, h, dur)
    near = sorted(set(sum((C.footsteps(a, dur) for a in [ex["passer"]] + ex["main"][:1]), [])))
    foley = [("step", t, .45, (-.3, .3)[i % 2]) for i, t in enumerate(near) if t < dur - .3]
    foley += [("paper", 1.0, .45, .3)]                         # the hawker lifts the price list
    amb = sfx.street_ambience(dur + .5, seed=3)
    fade = np.clip((dur + .3 - np.arange(len(amb)) / sfx.FSR) / .6, 0, 1)
    return dict(shots=[shot], foley=foley, amb=amb * fade[:, None] * .6)


EP = dict(
    slug="test-cine-integration",
    title="Integration test: a filmed beat in a long video",
    thumb=dict(art=("price_path", dict(marks=[SOLD, BOUGHT], note="SOUTH SEA STOCK, 1720", counter=False)),
               big_a="Test", size_a=92, art_b=("crowd_rush", dict(n=6, target="SOUTH SEA")),
               big="Test", size=100, small="Integration test", ghost="1720"),
    score="reflective",
    chapters=[
        dict(title="Exchange Alley", art=("crowd_rush", dict(n=5, target="SOUTH SEA")), beats=[
            dict(say="June, seventeen twenty. In Exchange Alley, it seemed everyone was getting rich.",
                 show=dict(kind="cine", shot=street)),
            dict(say="Newton had sold his South Sea shares in April. In June, he bought back in.",
                 shows=[S("price_path", "Out in April, back in June.", "Our chart of 1720", ["June"], 92, marks=[SOLD, BOUGHT])]),
        ]),
        dict(title="What it means", art=("bulb", dict()), beats=[
            dict(say="Selling early is only half of a decision. The other half is staying out.",
                 shows=[S("bulb", "Selling is half the decision.", "", ["half"], 110, text="?")]),
        ]),
    ],
    description="Integration test for the cinematic engine. Not for upload.",
    sources=[("Odlyzko, Newton's financial misadventures in the South Sea Bubble (Notes and Records, 2019)",
              "https://royalsocietypublishing.org/doi/10.1098/rsnr.2018.0018")],
    hashtags=["Test"],
    tags=["test"],
)

if __name__ == "__main__":
    make(EP)
