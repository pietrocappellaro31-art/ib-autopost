"""Motion preview and variety test for a long video (13 Nov, docs/production/quality-gates.md).

    python build/yt_preview.py build/youtube_ep007.py            # variety test only (before the render)
    python build/yt_preview.py build/youtube_ep007.py --motion   # plus motion sheets from the rendered MP4

Variety: every visual is keyed by what it shows (the drawing's name for sketch/scene, else its kind). The test
fails if one key carries more than 40% of the visuals, if three beats in a row open on the same key, or if a
chapter has more than one text-only beat. Motion: three stretches (the hook, a mechanism scene about a third in,
a later chapter), 12 s each, one frame every 0.25 s, tiled 8 x 6 into out/<slug>/motion_<n>.jpg.
"""
import collections
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

TEXT_ONLY = {"statement", "quote", "verdict", "number", "term", "compare", "list"}


def key(show):
    k = show.get("kind", "statement")
    return f"{k}:{show['art']}" if k in ("sketch", "scene") else k


def variety(ep):
    keys, firsts, fails = [], [], []
    for ch in ep["chapters"]:
        text_only = 0
        for b in ch["beats"]:
            shows = b.get("shows") or [b.get("show", dict(kind="statement"))]
            keys += [key(s) for s in shows]
            firsts.append(key(shows[0]))
            text_only += all(s.get("kind", "statement") in TEXT_ONLY for s in shows)
        if text_only > 1:
            fails.append(f"chapter '{ch['title']}' has {text_only} text-only beats")
    c = collections.Counter(keys)
    top, n = c.most_common(1)[0]
    if n / len(keys) > .4:
        fails.append(f"'{top}' carries {n / len(keys):.0%} of the visuals")
    for i in range(len(firsts) - 2):
        if firsts[i] == firsts[i + 1] == firsts[i + 2]:
            fails.append(f"beats {i + 1} to {i + 3} all open on '{firsts[i]}'")
    kinds = collections.Counter(k.split(":")[0] for k in keys)
    return dict(visuals=len(keys), distinct=len(c), top=c.most_common(6), kinds=dict(kinds), fails=fails)


def motion(ep, work):
    tm = json.load(open(work / "timing.json"))
    ch = tm["chapters"]
    starts = [0.0, ch[min(2, len(ch) - 1)] + 4, ch[-2] + 4 if len(ch) > 2 else tm["total"] * .7]
    out = []
    for i, t0 in enumerate(starts, 1):
        dst = work / f"motion_{i}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.2f}", "-t", "12", "-i", str(work / f"{ep['slug']}.mp4"),
                        "-vf", "fps=4,scale=320:-1,tile=8x6", "-frames:v", "1", "-q:v", "4", str(dst)], check=True)
        out.append((round(t0, 1), dst.name))
    return out


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    spec = importlib.util.spec_from_file_location("ep", sys.argv[1])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ep = m.EP
    v = variety(ep)
    print(f"variety: {v['visuals']} visuals, {v['distinct']} distinct, top {v['top']}")
    print("  " + ("PASS" if not v["fails"] else "FAIL: " + "; ".join(v["fails"])))
    if "--motion" in sys.argv:
        import youtube
        for t0, name in motion(ep, youtube.OUT / ep["slug"]):
            print(f"  motion sheet from {t0} s: {name}")
