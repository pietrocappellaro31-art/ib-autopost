"""
17 Nov (YouTube #11): measure the held-life layer (sketch.held_life) on the same script, before and after.

    python3 build/held_life_check.py build/youtube_ep010.py 60 150 200 240

Builds the episode's page twice from the same voice and timings, once with ep["held_life"] = False (the drawings
freeze once drawn, as in #1 to #10) and once with it on, renders the same drawn spans (start and end seconds, in
pairs; filmed beats are dark placeholders on this page and are skipped), and measures each with
yt_preview.motion_stats (the film's own motion measure: share of static seconds, longest static run, mean motion).
Writes build/out/<slug>/held_life.json and a side-by-side strip held_life_strip.jpg (the same frames, off above,
on below) to look at.
"""

import importlib.util
import json
import math
import subprocess
import sys

import youtube as Y
from yt_preview import motion_stats

path, spans = sys.argv[1], [float(x) for x in sys.argv[2:]]
spans = list(zip(spans[::2], spans[1::2]))
spec = importlib.util.spec_from_file_location("ep", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ep = mod.EP
work = Y.OUT / ep["slug"]
work.mkdir(parents=True, exist_ok=True)
items = Y.synth(ep, Y.YOUTUBE_VOICE, work)
res = {}
for mode in (False, True):
    Y.PACING.clear(); Y.CINE.clear(); Y.BEATS.clear(); Y.CAM_USE.clear()
    sc, chapters, sounds, total = Y.scenes(dict(ep, held_life=mode), items)
    cine = [(c["t"], c["t"] + c["dur"]) for c in Y.CINE]
    html, total = Y.page(sc)
    src = work / f"held_{int(mode)}.html"
    src.write_text(html)
    clips = []
    with Y.sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": Y.W, "height": Y.Hh})
        pg.goto(src.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        pg.evaluate("fitSketches()")
        for k, (a, z) in enumerate(spans):
            assert not any(ca < z and cb > a for ca, cb in cine), f"span {a}-{z} touches a filmed beat"
            clip = work / f"held_{int(mode)}_{k}.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(Y.FPS), "-c:v", "mjpeg", "-i", "-",
                                   "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", str(clip)], stdin=subprocess.PIPE)
            for f in range(int(a * Y.FPS), int(z * Y.FPS)):
                pg.evaluate(f"seek({f / Y.FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
            ff.stdin.close(); ff.wait()
            clips.append(clip)
        b.close()
    per = [motion_stats(c) for c in clips]
    secs = sum(x["seconds"] for x in per)
    res["on" if mode else "off"] = dict(
        seconds=secs,
        static_share=round(sum(x["static_share"] * x["seconds"] for x in per) / secs, 3),
        longest_static_s=max(x["longest_static_s"] for x in per),
        mean_motion=round(sum(x["mean_motion"] * x["seconds"] for x in per) / secs, 2),
        spans=[{k: v for k, v in x.items() if k != "per_second"} for x in per])
    print(("ON " if mode else "OFF"), {k: v for k, v in res["on" if mode else "off"].items() if k != "spans"}, flush=True)
res["spans_s"] = spans
json.dump(res, open(work / "held_life.json", "w"), indent=1)
# a strip: 6 frames 1/6 s apart from the first span's last second, off on top, on below
a, z = spans[0]
tiles = []
for mode in (0, 1):
    for k in range(6):
        t = (z - a) - 1.2 + k / 6
        out = work / f"_h{mode}{k}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(work / f"held_{mode}_0.mp4"), "-frames:v", "1",
                        "-vf", "scale=480:-1", str(out)], check=True)
        tiles.append(out)
lay = "|".join(f"{'+'.join(['w0'] * c) or '0'}_{'h0' if r else '0'}" for r in (0, 1) for c in range(6))
subprocess.run(["ffmpeg", "-y", "-v", "error", *sum((["-i", str(p)] for p in tiles), []), "-filter_complex",
                "".join(f"[{i}:v]" for i in range(12)) + f"xstack=inputs=12:layout={lay}", str(work / "held_life_strip.jpg")], check=True)
for p in tiles:
    p.unlink()
print("strip:", work / "held_life_strip.jpg")
