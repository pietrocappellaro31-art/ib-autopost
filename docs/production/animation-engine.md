# Animation engine

13 Nov 2026, cinematic upgrade. How the picture is made, what was decided and why, and the component API.

## Architecture decision: extend the browser engine, no Remotion

The existing engine (`motion.py`, `levels.py`, `youtube.py`, `sketch.py`) already renders like Remotion does: an
HTML/SVG page with one deterministic `seek(t)`, a headless Chromium screenshot per frame, frames piped to FFmpeg.
Remotion (React, TypeScript) would add a second toolchain, a rewrite of about 2,000 lines of drawings and every
episode script, and a licence question (Remotion's company licence applies to for-profit companies above a size
threshold; we would have to check and track it). It would not give better pictures: the quality comes from the
drawings, the rig and the direction, not the framework. So the cinematic layer is `build/cine.py` on the same
machinery, and every `motion.py` effect still works inside a filmed shot.

| | Existing engine | + cine.py |
|---|---|---|
| Picture | text and a drawing per sentence, drawings draw themselves | depth layers, camera, people, light, props, transitions |
| Speed (2 CPUs) | about 0.15 s a frame | 0.5 to 1.3 s a frame per browser; 0.52 s a frame with 2 workers on the 20 s proof |
| Use | most beats, charts, lists, Levels quizzes | hooks, history, mechanisms with people, conclusions |

A fully filmed 10-minute video would take about 2 to 3 hours to render on this machine: long videos are hybrid
(filmed beats spliced into the existing engine) until rendering is faster (`cinematic-standard.md` 8, step 6).

## Files

- `build/cine.py` runtime: camera, layers, depth of field, rig, poses, walk, faces, held props, procedural life
  (swing, drift, flicker, dust motes, steam), keyed attributes, transitions, captions, render, stills, footsteps.
- `build/cine_lib.py` sets and props: `street_1720`, `foreground_1720`, `crowd`, `study_1720`, `parchment`;
  `newspaper`, `letter`, `quill`, `coin`, `coin_stack`, `jar`, `certificate`, `candle`, `cup`, `ledger_book`,
  `phone`, `card`, `terminal`; `price_line` (chart that draws on, flags, riding counter, sourced x positions).
- `build/cine_poc_newton.py` the proof of concept and the worked example of a director's script.
- `build/master.py` dual masters; `build/score.py` score; `build/sfx.py` foley and ambience.
- `build/youtube.py` `kind="cine"` beats (`scenes()` leaves a placeholder; `cine_splice()` renders each filmed beat at the
  film's size and frame rate, overlays it on the silent film and adds its foley and ambience to `sfx.wav`); `score=`
  writes the scored mix with `score.py`; `sound_report()` runs the score gate. Tested end to end on
  `build/youtube_cine_test.py` (13 Nov).
- `build/master.py scored <clean.mp4>` a scored alternative for a finished Levels Short or Reel.
- `build/yt_preview.py` variety test, motion sheets, motion measures.

## Shot API

```python
shot = dict(dur=6.0,
            layers=[cine.layer(z, svg, x=..., y=..., w=..., h=..., noblur=False), ...],   # z: 0 far ... 1 focus ... >1 near
            actors=[cine.actor(...), ...],
            cam=[[t, cx, cy, zoom(, roll)(, ease)], ...],     # world px on the depth-1 plane
            focus=[[t, z], ...], dof=7, band=.28,             # blur grows outside the in-focus band
            over=[html, ...], grade="warm"|"cool"|"dusk"|"none", vig=1, shake=.5,
            tin=("cut"|"dissolve"|"flash"|"iris", seconds))
html, total = cine.film_html([shot, ...], w, h, caps=cine.captions(lines, w, h))
mp4, secs = cine.render(html, total, work, name, w, h, fps=30, workers=2)
```

A layer at depth z pans z times as far as the depth-1 plane and magnifies `1 + (zoom - 1) * z`. To aim the camera at
a point (px, py) on layer z: `cx = 960 + (px - 960) / z`, `cy = 540 + (py - 540) / z`. Measure the point with the
browser rather than by hand (`cine_poc_newton.py` notes the measured centres; the probe sets an identity camera so
screen equals world).

Animated attributes on any SVG element: `cine.kv(translate=[[t, x, y(, rot)(, scale)(, ease)], ...],
opacity=[[t, v], ...], dash=[[t, 0..1], ...], count=[[t, value], ...], clip=[[t, top, right, bottom, left], ...])`.
Ambient life: `data-swing`, `data-drift`, `data-flick`, `data-motes`, `data-steam` (see `cine.RUNTIME`).

## Rig API

```python
a = cine.actor("id", "gent_teal", pos=[[0, x, ground_y], [4, x2, ground_y, "lin"]],
               pose_keys=[[0, cine.pose("sit_read")], [2.1, cine.pose("sit_read", brow=1, mouth=2)]],
               turn=[[1.0, 1], [1.3, -1]], scale=.8, seed=3, holdF=svg, upright=True)
```

Looks (`cine.LOOKS`): 1700s gentlemen (long coat, wig, tricorn), a working man with a cap, women in long dresses with
bonnets, modern suits. Poses (`cine.POSES`): stand, relaxed, read, seated, sit_read, sit_write, point, reach,
hold_up, shrug, cheer, concern, talk_a, talk_b; any field can be overridden (lean, head, shF, elF, shB, elB, hipF,
knF, hipB, knB, ftF, ftB, rootY, brow -1..1, mouth -1 frown 0 neutral 1 smile 2 open, eyeY). Between position keys
the figure walks: phase from distance, so feet do not skate; `cine.footsteps(actor, dur)` returns the landing times
for the sound. Breathing, head drift, sway and blinks never stop. `upright=True` keeps a held paper level and
readable whatever the arm and the facing do.

## Performance notes (measured 13 Nov, 1920 x 1080, 2 CPUs, software GPU)

Blur dominated: a frame of the street shot took 1.59 s with depth of field on every layer, 0.61 s with none.
Skipping blur under 1 px, on gradients (`noblur`) and inside a focus band brought it to 0.95 s; two browsers on a
queue of short frame chunks give 0.52 s a frame overall. Canvas size made no measurable difference.
