"""
Beat entry check (18 Nov, the 17 Nov Short's next improvement): does each beat's drawing have its set on the panel
when the beat arrives, or does it open on an empty paper panel and draw itself from nothing?

For every story beat (and the close) of a rendered Short it reads the final MP4 at the beat's end (the reference:
the finished drawing) and in the first 0.3 s after the beat has swiped in (s0 + 0.34 to s0 + 0.64; the hook from
frame 0). The paper panel is found in the reference frame (the rows and columns where most pixels are panel paper,
#F7F5F2); ink is the share of the panel's pixels that are not paper. A beat-entry frame is "empty" when its ink is
under 20% of the reference ink. The aim is 0 empty entry frames.

    python3 build/entry_check.py shorts-raise-tax-bracket [shorts-coin-toss-150-100 ...]

19 Nov (the 18 Nov Short's next improvement): the same report also measures the quietest stretches, so a beat that
lands in its first second and then holds still through a long sentence is gated with the empty entries. The motion
measure is the films' own (yt_preview.motion_stats: 6 frames a second at 160 x 90 grey, the mean change per second),
over a sliding 6 s window; the aim is no window under 1.0 (QUIET_6S). Each quiet window is named by the beat and
sentence it starts in, so the fix (a second action in that sentence) is easy to place.

20 Nov (the 19 Nov Short's next improvement): the panel-only motion. The frame figure above counts the film grain,
the captions lighting and the floaters, so a still drawing under a lit caption still reads near 0.7 to 1.0. The
panel measure reads only the drawing: each second is cropped to the paper panel of the beat it falls in (found as
above), at 6 frames a second on a 270 x 480 grey copy, and only pixel changes over 10 grey levels count (the grain's
jitter stays under that), so a drawing that does not move reads 0. Reported beside the frame figure: the lowest 6 s
panel window, where it starts, and the per-beat panel means; the aim for a puzzle hook is no panel second at 0 while
the question is spoken (PANEL_STILL).

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
QUIET_6S = 1.0
SAFE_BOTTOM = 1440


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


def ink_bottom(img, box):
    """19 Nov: the lowest row of the drawing that carries ink (a row with over 1% of the panel's width off-paper).
    The paper panel is 'nochk' for the render's safe-area check, so a drawing's labels could sit under YouTube's
    bottom bar unseen; this gates them (nothing below y=1440)."""
    y0, y1, x0, x1 = box
    reg = img[y0 + 6:y1 - 6, x0 + 30:x1 - 30]
    rows = np.where((~paper_mask(reg)).mean(axis=1) > .01)[0]
    return int(y0 + 6 + rows[-1]) if len(rows) else int(y0)


def check(slug):
    work = OUT / slug
    t = json.load(open(work / "timeline.json"))
    mp4 = work / f"{slug}.mp4"
    spans = [tuple(s) for s in t["spans"]]
    close_end = t["at"]["close"] + t["segments"]["close"][-1][2]
    beats = [(f"b{i}", (0.0 if i == 0 else s0 + T_SW), s1) for i, (s0, s1) in enumerate(spans)]
    beats.append(("close", t["at"]["close"] - .35 + T_SW + .1, close_end))
    rows, empty, n, unsafe = [], 0, 0, 0
    for k, e0, s1 in beats:
        ref = frame(mp4, s1 - .25)
        box = panel_box(ref)
        if box is None:
            rows.append(dict(beat=k, panel=None))
            print(f"  {slug} {k:6s} no panel found")
            continue
        full = ink(ref, box)
        low = ink_bottom(ref, box)
        under = low > SAFE_BOTTOM
        unsafe += under
        ent = [ink(frame(mp4, e0 + d), box) for d in (0, .1, .2, .3)]
        share = [round(x / full, 3) if full > 0 else None for x in ent]
        bad = sum(1 for s in share if s is not None and s < .2)
        empty += bad
        n += len(share)
        rows.append(dict(beat=k, panel=box, ink_bottom=low, under_1440=bool(under), ref_ink=round(full, 4), entry_ink=[round(x, 4) for x in ent], share=share, empty=bad))
        print(f"  {slug} {k:6s} panel y{box[0]}-{box[1]}  ink at end {full:.3f}  entry {min(share):.2f}-{max(share):.2f} of it"
              + (f"  CHECK {bad} empty" if bad else "") + f"  lowest ink y{low}" + ("  CHECK under the 1440 line" if under else ""))
    print(f"  {slug}: {unsafe} drawings with ink under the 1440 line")
    res = dict(slug=slug, frames=n, empty=empty, ink_under_1440=unsafe, empty_share=round(empty / max(n, 1), 3), beats=rows)
    res.update(quiet(t, mp4))
    res.update(panel_motion(t, mp4, beats, rows))
    json.dump(res, open(work / "entry.json", "w"), indent=1)
    print(f"  {slug}: {empty}/{n} beat-entry frames with the panel under 20% of its final ink")
    return res


def where(t, sec):
    """The beat and sentence a second of the Short falls in (b2 s1, close s0)."""
    for k, at in sorted(t["at"].items(), key=lambda kv: kv[1], reverse=True):
        if sec >= at - .35:
            j = max([i for i, (_, a, b) in enumerate(t["segments"][k]) if at + a <= sec + .5] or [0])
            return f"{k} s{j}"
    return "b0 s0"


def quiet(t, mp4):
    """The sliding 6 s motion windows (19 Nov): the lowest, and every window under QUIET_6S with where it starts."""
    from yt_preview import motion_stats
    per = motion_stats(mp4)["per_second"]
    win = [(round(float(np.mean(per[i:i + 6])), 2), i) for i in range(max(len(per) - 5, 0))]
    low = min(win) if win else (None, None)
    under = [dict(at=i, mean=v, where=where(t, i)) for v, i in win if v < QUIET_6S]
    print(f"  6 s windows: lowest {low[0]} at {low[1]} s ({where(t, low[1] or 0)}); {len(under)} under {QUIET_6S}"
          + (f"  CHECK quiet from {', '.join(sorted({u['where'] for u in under}))}" if under else "")
          + f"; under 1.2: {sum(1 for v, _ in win if v < 1.2)}")
    return dict(lowest_6s=low[0], lowest_6s_at=low[1], windows_6s=len(win), quiet_6s=under, quiet_limit=QUIET_6S,
                windows_6s_under_1_2=sum(1 for v, _ in win if v < 1.2), mean_motion=round(float(np.mean(per)), 2) if per else None)


PANEL_STILL = .05          # a panel second whose motion is under this is a still drawing


def panel_motion(t, mp4, beats, rows, fps=6, w=270, h=480, thr=10):
    """20 Nov: motion inside the drawing's panel only (see the docstring). beats are (key, entry, end), rows the
    per-beat results with each panel box in 1080 x 1920 pixels."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    f = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
    d = np.abs(np.diff(f, axis=0))
    d[d < thr] = 0
    sx, sy = w / 1080, h / 1920
    boxes = []
    for (k, e0, s1), row in zip(beats, rows):
        b = row.get("panel")
        if b:
            boxes.append((e0 - T_SW if k != "b0" else 0, s1, [int(b[0] * sy) + 2, int(b[1] * sy) - 2, int(b[2] * sx) + 2, int(b[3] * sx) - 2], k))
    per, owner = [], []
    for i in range(0, len(d) - fps + 1, fps):
        sec = i / fps
        box = next((bx for a, z, bx, k in boxes if a <= sec + .5 < z), None)
        key = next((k for a, z, bx, k in boxes if a <= sec + .5 < z), None)
        if box is None:
            per.append(None)
            owner.append(None)
            continue
        y0, y1, x0, x1 = box
        per.append(float(d[i:i + fps, y0:y1, x0:x1].mean()))
        owner.append(key)
    vals = [(v, i) for i, v in enumerate(per) if v is not None]
    win = []
    for i in range(len(per) - 5):
        chunk = [v for v in per[i:i + 6] if v is not None]
        if len(chunk) == 6:
            win.append((round(float(np.mean(chunk)), 2), i))
    low = min(win) if win else (None, None)
    still = [i for v, i in vals if v < PANEL_STILL]
    by_beat = {}
    for v, k in zip(per, owner):
        if k:
            by_beat.setdefault(k, []).append(v)
    means = {k: round(float(np.mean(v)), 2) for k, v in by_beat.items()}
    hook = by_beat.get("b0", [])
    print(f"  panel-only motion: lowest 6 s window {low[0]} at {low[1]} s ({where(t, low[1] or 0)}); still panel seconds "
          f"{len(still)}{' at ' + ', '.join(map(str, still)) if still else ''}; hook min {min(hook):.2f} mean {np.mean(hook):.2f}" if hook else "")
    print("  panel means by beat: " + ", ".join(f"{k} {v}" for k, v in means.items()))
    return dict(panel_per_second=[None if v is None else round(v, 2) for v in per], panel_lowest_6s=low[0], panel_lowest_6s_at=low[1],
                panel_still_seconds=still, panel_means=means, panel_hook_min=round(min(hook), 2) if hook else None)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        check(s)
