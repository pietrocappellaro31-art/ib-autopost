# Cinematic standard: animation and scene variety

Pietro, 13 Nov 2026, for long-form YouTube. Read with `long-form-standard.md`.

## What a film should look like

A fully produced animated documentary in the IB editorial identity: paper, ink, red for the mistake or the
warning, teal for the right answer, Source Serif 4 and IBM Plex Sans, hand-drawn marker scenes. Motion serves the
explanation. No clutter and no motion for its own sake.

Where the engine supports them, a film uses:

- historical figures as **clearly stylised reconstructions**: drawn, never a portrait or likeness, and never
  given a synthetic voice of their own (see `quality-gates.md`, AI disclosure)
- animated environments: a bank hall, a counting house, a trading floor, an exchange, a desk
- objects that move with purpose: coins falling, documents placed, stamps, ledgers filling in
- charts that build and move with the story, at honest scales
- document interactions: a page turned, a line underlined, a figure circled
- light and depth: a lamp, a window, foreground and background layers in parallax
- camera moves that lead the eye (push in on the detail, pan along a timeline, rack between layers)
- characters that react (turn, point, slump, cheer) with articulated limbs
- transitions driven by objects (a coin rolls into the next scene, a page turns into it)

Not allowed: stick figures sliding as one frozen image where articulated motion would teach better; zoom and pan
as the main animation; one template repeated for the whole film.

## Scene families

Mix several in every film, as the story needs:

historical reconstruction, mechanism animation, chart explanation, timeline, financial calculation, transaction
flow, character interaction, document analysis, comparison, consequence scene, cinematic conclusion.

**Variety test.** Before the render, count the beats by family and by visual kind. A film fails if:

- one visual kind carries more than 40% of the beats, or
- three beats in a row share a kind and a layout, or
- it has fewer than 6 families, or
- a chapter has more than one text-only beat.

"30 nearly identical cards" fails, and so does swapping one repeated template for another.

## What the engine does today (13 Nov), honestly

`build/youtube.py` with `build/sketch.py` (about 100 drawn scenes) and `build/motion.py`:

- **Can:** marker strokes that draw themselves on, pops, stamps, slides, swings, floats, keyframed paths (`kf`),
  counters, charts that draw point by point, flows, timelines, icon rows, quotes, verdict stamps, splits, number
  reveals; a drawing for every sentence; drawings fitted to their boxes; chapter cards with art; layout and
  pacing checks; two thumbnail looks a day.
- **Cannot yet:** articulated characters (figures are fixed strokes; a figure moves only as a whole), environments
  with depth and parallax layers, a camera (each scene has one slow push, nothing else), lighting, object-driven
  transitions between scenes, sound tied to on-screen actions (the effects are a pop per beat and per visual and a
  ding per chapter card, see `audio-standard.md`).

## Build order (one per run as the "Next improvement", unless the film needs another first)

1. **Camera**: per-scene keyframed camera (push, pan, tilt, rack between two layers) on the scene container, set in
   the episode (`cam=`), with the layout check run at the camera's extreme positions.
2. **Articulated figure rig** in `sketch.py`: head, torso, upper and lower arms and legs as joints, poses (stand,
   walk cycle, point, slump, cheer, write, hand over) keyframed in time; a stylised period costume layer (hat, coat,
   wig) so historical figures read as reconstructions.
3. **Environments with depth**: 3 layers (back wall and windows, mid furniture, foreground desk or rail) with
   parallax under the camera; first sets: a bank hall, a counting house, a trading floor, a modern office.
4. **Sound on actions**: scenes report their actions (coin lands, stamp hits, page turns, door opens) with times,
   and the sound track plays matching effects from them instead of a pop per beat.
5. **Object-driven transitions**: an element that carries over from one scene into the next (a coin, a page, a
   line on a chart).
6. **Light**: a warm lamp or window light and soft shadow per environment, as a layer, not a filter on everything.

Each step is measured (what share of beats uses it, and a motion preview that shows it working) before it counts.
