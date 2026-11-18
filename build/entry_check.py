"""
Beat entry check (18 Nov, the 17 Nov Short's next improvement): does each beat's drawing have its set on the panel
when the beat arrives, or does it open on an empty paper panel and draw itself from nothing?

For every story beat (and the close) of a rendered Short it reads the final MP4 at the beat's end (the reference:
the finished drawing) and in the first 0.3 s after the beat has swiped in (s0 + 0.34 to s0 + 0.64; the hook from
frame 0). The paper panel is found in the reference frame (the rows and columns where most pixels are panel paper,
#F7F5F2); ink is the share of the panel's pixels that are not paper. A beat-entry frame is "empty" when its ink is
under 20% of the reference ink. The aim is 0 empty entry frames.

    python3 build/entry_check.py shorts-raise-tax-bracket [shorts-coin-toss-150-100 ...]

Writes build/out/<slug>/entry.json and prints one line per beat.
"""

import json
import pathlib
import subprocess
import sys

import numpy as np

OUT = pathlib.Path(__file__).resolve().parent / "out"
PAPER = np.array([247, 245, 242], np.float32)
T_SW = .34


def frame(mp4, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(mp4), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).astype(np.float32)


def paper_mask(img):
    return np.abs(img - PAPER).max(axis=2) < 14


def panel_box(img):
    """The drawing's paper panel: the panel's columns (where paper fills over 20% of the frame height), then the
    longest run of rows where the strip just inside its left and right edges is paper (drawings are fitted to 0.93
    of the box, so those strips stay clear of ink)."""
    m = paper_mask(img)
    cols = np.where(m.mean(axis=0) > .2)[0]
    if len(cols) < 40:
        return None
    x0, x1 = int(cols[0]), int(cols[-1])
    edge = (m[:, x0 + 3:x0 + 10].mean(axis=1) > .9) & (m[:, x1 - 9:x1 - 2].mean(axis=1) > .9)
    rows = np.where(edge)[0]
    if len(rows) < 40:
        return None
    runs, start = [], rows[0]
    for a, b in zip(rows, rows[1:]):
        if b != a + 1:
            runs.append((start, a))
            start = b
    runs.append((start, rows[-1]))
    y0, y1 = max(runs, key=lambda r: r[1] - r[0])
    return int(y0), int(y1), x0, x1


def ink(img, box):
    y0, y1, x0, x1 = box
    reg = img[y0 + 6:y1 - 6, x0 + 6:x1 - 6]
    # ink: anything clearly off-paper (strokes, fills, labels); the black page outside the panel's rounded corners
    # is a few hundred pixels at most and is the same in every frame
    return float(1 - paper_mask(reg).mean())


def check(slug):
    work = OUT / slug
    t = json.load(open(work / "timeline.json"))
    mp4 = work / f"{slug}.mp4"
    spans = [tuple(s) for s in t["spans"]]
    close_end = t["at"]["close"] + t["segments"]["close"][-1][2]
    beats = [(f"b{i}", (0.0 if i == 0 else s0 + T_SW), s1) for i, (s0, s1) in enumerate(spans)]
    beats.append(("close", t["at"]["close"] - .35 + T_SW + .1, close_end))
    rows, empty, n = [], 0, 0
    for k, e0, s1 in beats:
        ref = frame(mp4, s1 - .25)
        box = panel_box(ref)
        if box is None:
            rows.append(dict(beat=k, panel=None))
            print(f"  {slug} {k:6s} no panel found")
            continue
        full = ink(ref, box)
        ent = [ink(frame(mp4, e0 + d), box) for d in (0, .1, .2, .3)]
        share = [round(x / full, 3) if full > 0 else None for x in ent]
        bad = sum(1 for s in share if s is not None and s < .2)
        empty += bad
        n += len(share)
        rows.append(dict(beat=k, panel=box, ref_ink=round(full, 4), entry_ink=[round(x, 4) for x in ent], share=share, empty=bad))
        print(f"  {slug} {k:6s} panel y{box[0]}-{box[1]}  ink at end {full:.3f}  entry {min(share):.2f}-{max(share):.2f} of it"
              + (f"  CHECK {bad} empty" if bad else ""))
    res = dict(slug=slug, frames=n, empty=empty, empty_share=round(empty / max(n, 1), 3), beats=rows)
    json.dump(res, open(work / "entry.json", "w"), indent=1)
    print(f"  {slug}: {empty}/{n} beat-entry frames with the panel under 20% of its final ink")
    return res


if __name__ == "__main__":
    for s in sys.argv[1:]:
        check(s)
