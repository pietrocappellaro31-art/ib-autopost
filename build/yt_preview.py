"""
Previews for a long video (13 Nov 2026, cinematic upgrade).

    python3 build/yt_preview.py build/youtube_ep007.py            variety test on the script, before any render
    python3 build/yt_preview.py build/youtube_ep007.py --motion   motion sheets and motion measures of the render
    python3 build/yt_preview.py --clip path/to/video.mp4          motion measures of any video file

Variety test (fails with a non-zero exit, so a run cannot skip it):
  - no chapter with more than one text-only beat (statement, quote, verdict, number with no drawing);
  - no one visual (a drawing counts by its name) on more than 40% of all visuals;
  - no three beats in a row opening on the same visual;
  - measured, not failed: the share of "drawing beside a line of text" beats (the presentation look the cinematic
    upgrade replaces) and the number of filmed beats;
  - every chapter card has a drawing (art=);
  - at least one filmed beat (kind="cine") or one beat with a figure in action, per two chapters (warning).

Motion measures (a picture can be beautiful and still be a slideshow, so stills are not proof):
  frames are sampled at 6 per second, shrunk to 160 x 90 grey, and compared with the frame before. A second in
  which nothing moved by more than 0.5 grey levels on average is "static". Reported: the share of static seconds,
  the longest static run, and the mean motion per second; written to <out>/motion.json. A filmed scene that should
  move but does not shows up here. Thresholds for pass or fail are not set yet: they need a few days of measures
  and Pietro's view (docs/production/quality-gates.md).

Motion sheets: for every chapter, 8 frames 0.25 s apart from the middle of its second beat (or its first),
saved as motion-<chapter>.jpg in the episode folder, to look at movement and transitions, not only at stills.
"""

import importlib.util
import json
import pathlib
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).parent
TEXT_ONLY = {"statement", "quote", "verdict", "number", "term", "list"}


def load_ep(path):
    spec = importlib.util.spec_from_file_location("ep", path)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(HERE))
    spec.loader.exec_module(m)
    return m.EP


def variety(ep):
    kinds, problems, warn, firsts = {}, [], [], []
    filmed = beside = 0
    for c, ch in enumerate(ep["chapters"]):
        if not ch.get("art"):
            problems.append(f"chapter {c + 1} '{ch['title']}': no art= on the chapter card")
        text_only = 0
        for b in ch["beats"]:
            shows = b.get("shows") or [b.get("show", dict(kind="statement"))]
            k0 = shows[0].get("kind", "statement")
            firsts.append(f"{k0}:{shows[0].get('art')}" if k0 in ("sketch", "scene") else k0)
            if all(s.get("kind", "statement") in TEXT_ONLY for s in shows):
                text_only += 1
            for s in shows:
                k = s.get("kind", "statement")
                beside += k == "sketch"
                if k in ("sketch", "scene"):                       # a drawing is its own kind: 84 different drawings are variety
                    k = f"{k}:{s.get('art')}"
                kinds[k] = kinds.get(k, 0) + 1
                filmed += k == "cine" or (k.split(":")[-1] in ("figures", "crowd_rush", "queue"))
        if text_only > 1:
            problems.append(f"chapter {c + 1} '{ch['title']}': {text_only} text-only beats (at most 1)")
    total = sum(kinds.values())
    top = max(kinds.items(), key=lambda kv: kv[1])
    if top[1] / total > .4:
        problems.append(f"'{top[0]}' is {top[1]} of {total} visuals ({top[1] / total:.0%}, at most 40%)")
    for i in range(len(firsts) - 2):                             # merged 13 Nov from the long-form standard's preview
        if firsts[i] == firsts[i + 1] == firsts[i + 2]:
            problems.append(f"beats {i + 1} to {i + 3} all open on '{firsts[i]}'")
    if filmed < len(ep["chapters"]) / 2:
        warn.append(f"{filmed} filmed or figure beats for {len(ep['chapters'])} chapters: aim for one per two chapters")
    # measured, not yet a pass mark: how much of the film is "a drawing beside a line of text" (the presentation look)
    return dict(kinds=dict(sorted(kinds.items(), key=lambda kv: -kv[1])[:12]), visuals=total, distinct=len(kinds),
                beside_text_share=round(beside / total, 2), filmed_beats=filmed, problems=problems, warnings=warn)


def frames_gray(mp4, fps=6, w=160, h=90):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)


def motion_stats(mp4, fps=6, still=.5):
    f = frames_gray(mp4, fps)
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))           # mean grey-level change per frame step
    per_s = [d[i:i + fps].mean() for i in range(0, len(d) - fps + 1, fps)]
    static = [x < still for x in per_s]
    run = best = 0
    for s in static:
        run = run + 1 if s else 0
        best = max(best, run)
    cuts = int((d > 25).sum())                                 # a frame-to-frame change that big is a cut or a flash
    return dict(seconds=len(per_s), static_share=round(float(np.mean(static)), 3) if per_s else None, longest_static_s=best,
                mean_motion=round(float(np.mean(per_s)), 2) if per_s else None, hard_changes=cuts,
                per_second=[round(float(x), 2) for x in per_s])


def motion_sheets(ep, work, mp4):
    tm = json.load(open(work / "timing.json"))
    starts = tm["chapters"] + [tm["total"]]
    out = []
    for c in range(len(tm["chapters"])):
        a, b = starts[c], starts[c + 1]
        mid = a + (b - a) * .35
        frames = []
        for k in range(8):
            t = mid + k * .25
            p = work / f"_m{k}.jpg"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=480:-1", str(p)], check=True)
            frames.append(p)
        sheet = work / f"motion-{c + 1:02d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *sum((["-i", str(p)] for p in frames), []), "-filter_complex",
                        "".join(f"[{i}:v]" for i in range(8)) + "xstack=inputs=8:layout=0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0",
                        str(sheet)], check=True)
        for p in frames:
            p.unlink()
        out.append(sheet)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--clip":
        print(json.dumps({k: v for k, v in motion_stats(sys.argv[2]).items() if k != "per_second"}, indent=1))
        sys.exit(0)
    ep = load_ep(sys.argv[1])
    v = variety(ep)
    print(f"variety: {v['visuals']} visuals, {v['distinct']} distinct, drawing-beside-text share {v['beside_text_share']:.0%}, "
          f"filmed beats {v['filmed_beats']}\n  most used: {v['kinds']}")
    for w in v["warnings"]:
        print("  warning:", w)
    for p in v["problems"]:
        print("  PROBLEM:", p)
    if "--motion" in sys.argv:
        work = HERE / "out" / ep["slug"]
        mp4 = work / f"{ep['slug']}.mp4"
        stats = motion_stats(mp4)
        json.dump(stats, open(work / "motion.json", "w"), indent=1)
        print("motion:", {k: v for k, v in stats.items() if k != "per_second"})
        for s in motion_sheets(ep, work, mp4):
            print("  sheet:", s)
    sys.exit(1 if v["problems"] else 0)
