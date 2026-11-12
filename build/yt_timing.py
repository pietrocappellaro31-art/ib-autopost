"""Timing check before a long render (11 Nov): synthesise (cached) and lay out the episode, print the
length, the chapters and any visual/sentence mismatch, without rendering a frame.

    python build/yt_timing.py build/youtube_ep004.py [--takes]   (12 Nov: --takes checks every line word for word)
"""
import importlib.util, sys
import youtube as Y

spec = importlib.util.spec_from_file_location("ep", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ep = m.EP
work = Y.OUT / ep["slug"]; work.mkdir(parents=True, exist_ok=True)
items = Y.synth(ep, Y.YOUTUBE_VOICE, work)
if "--takes" in sys.argv:
    Y.takes(ep, items, Y.YOUTUBE_VOICE, work)
sc, chapters, sounds, total = Y.scenes(ep, items)
html, total = Y.page(sc)
print(f"total {total / 60:.2f} min, {len(sc)} scenes")
for t, title in chapters:
    print(f"  {int(t // 60)}:{int(t % 60):02d} {title}")
