# Cinematic standard (long videos, Shorts, Reels)

Pietro, 13 Nov 2026: first his long-form documentary instructions (morning), then the cinematic-upgrade directive
(the same day), merged here. The permanent visual and storytelling standard for the
finance channel and @investmentbankinginterviews. Format-specific rules: `long-form-standard.md`,
`short-form-standard.md`. Sound: `audio-standard.md`. Checks: `quality-gates.md`. Engine: `animation-engine.md`.
Where an older rule disagrees, this folder wins unless `docs/decisions-log.md` records a newer decision by Pietro.

This is the IB finance brand only. Another channel was named as a reference for production *quality* (cinematic 2D
animation, polished narration, original score, ambience, fluid transitions). Nothing of it is used here: no brand,
characters, story, palette, logos, music, files or schedules.

Applies to Reels too (Pietro, 13 Nov evening: "They should."); the Reel gates are `quality-gates.md` section 9.

## 1. The goal

A viewer should feel they are watching an animated financial documentary or short film, not a narrated
presentation. The picture teaches through movement: people do things, objects are handled, numbers come from
somewhere and go somewhere, the camera looks at what matters.

Measured baseline (13 Nov, `yt_preview.py`): in the last three long videos 66 to 77% of visuals were "a drawing
beside a line of text". That share has to come down, with filmed scenes (`kind="cine"`) replacing it where the story
has people, places or a mechanism to show.

## 2. Keep the brand

Keep: the IB mark, Source Serif 4 and IBM Plex Sans, cream and paper grounds, red `#D93A12` as the accent, teal
`#0F766E`, mustard `#F2C35B`, ink `#0A0A0A`, ink-outlined flat illustration, explanatory charts, the four-level quiz,
the research and sourcing rules, the daily logs.

Add: illustrated environments in depth, people with joints, camera movement, light (time of day, windows, lamps,
shafts with dust), subtle texture (grain, vignette), depth of field, transitions motivated by objects.

Red stays an accent: in a crowd, one or two red coats, not ten.

Where the engine supports them, a film uses (long-form standard, 13 Nov morning):

- historical figures as **clearly stylised reconstructions**: drawn, never a portrait or likeness, and never given
  a synthetic voice of their own (`quality-gates.md`, AI disclosure)
- animated environments: a bank hall, a counting house, a trading floor, an exchange, a desk
- objects that move with purpose: coins falling, documents placed, stamps, ledgers filling in
- charts that build and move with the story, at honest scales
- document interactions: a page turned, a line underlined, a figure circled
- light and depth: a lamp, a window, foreground and background layers in parallax
- camera moves that lead the eye (push in on the detail, pan along a timeline, rack between layers)
- characters that react (turn, point, slump, cheer) with articulated limbs
- transitions driven by objects (a coin rolls into the next scene, a page turns into it)

Not allowed: stick figures sliding as one frozen image where articulated motion would teach better; zoom and pan as
the main animation; one template repeated for the whole film. No clutter and no motion for its own sake.

## 3. Show the event, do not caption it

Instead of a card saying "Newton bought back into the South Sea Company", film it: the street where shares were
traded, the price list in a hawker's hand, the camera pushing into the paper, the same paper in Newton's study, the
two prices lifting off the page, his hand writing the order, the coins moving from one jar to the other, the price
path with the moment marked. (Proof of concept: `build/cine_poc_newton.py`.)

## 4. Honesty in reconstruction

- A reconstructed scene carries the on-screen badge **RECONSTRUCTION** (and, for a real person, "our illustration").
- Never invented dialogue, quotes, expressions or events presented as evidence. A figure may react (brows up, lowers
  the paper) to something the records say happened; it may not say anything the records do not.
- A document on screen paraphrases what the sources say was done ("Sell the bonds. Buy South Sea.") and is badged.
- Charts use sourced data only, with units and sources on screen; approximate values are labelled approximate; a
  month with no sourced value gets no point (the 1720 chart skips July and draws the gap dashed).
- No bank logos, no real-institution branding, no likeness of a living person.

## 5. Scene families (use the topic to choose; do not force one template)

A historical reconstruction, B financial mechanism, C data reveal, D decision point, E comparison, F calculation,
G visual metaphor, H character action, I document explanation, J chapter transition, K quiz interaction,
L cinematic conclusion. What each is and which components build it: `scene-library.md`.

**Variety test** (`python3 build/yt_preview.py build/youtube_ep<NNN>.py`, before the render; a failure stops the run):
one visual on more than 40% of the visuals, three beats in a row opening on the same visual, or a chapter with more
than one text-only beat. Checked by eye, not yet in code: at least 6 of the families above in a long film. "30 nearly
identical cards" fails, and so does swapping one repeated template for another.

## 6. Motion rules

- Every meaningful scene has a reason to move. A line reveals with the sentence that names it; a figure reacts when
  the news arrives; a balance sheet rearranges as the financing changes; a crowd moves as individuals.
- Stillness is allowed when it serves the story. A film that reads as a slideshow is not.
- Fake animation (only pans, zooms and floating particles over a still) does not count as animation.
- Several sentences may share one evolving scene (visual progression), instead of one card per sentence.
- Check motion in motion: motion sheets and the static-share measure (`yt_preview.py --motion`), never stills alone.

## 7. Formats and frame rates

- Long-form 1920 x 1080. The existing engine renders at 24 fps; filmed beats are rendered at the episode's frame
  rate so they splice cleanly. A whole new filmed episode may use 30 fps (cine.render(fps=30)).
- Shorts and Reels 1080 x 1920 at 30 fps. The same world is reframed by `cine.stage()`: one scene serves both.
- Old videos are never converted to another frame rate.

## 8. Build order (each daily run takes the next unfinished step after its own "next improvement")

1. **Camera** (done 13 Nov): keyed camera with parallax per depth layer, depth of field with an in-focus band,
   handheld drift, push-ins that land on measured targets.
2. **People** (done 13 Nov, first version): articulated figures, gait from distance walked, poses, faces, held
   props. Next: hand poses, a sitting-down and standing-up transition helper, a 3/4 view.
3. **Sets** (started): London 1720 street and study. Next: a modern trading floor, a bank office, a city street
   today, a boardroom, a kitchen table (household finance).
4. **Data in the world** (started): price paths that draw with flags; numbers that lift off documents. Next:
   balance sheet that rearranges, cash-flow waterfall, LBO structure, debt schedule (see `scene-library.md`).
5. **Transitions** (started): push into an object and match on it, cut on action, dissolve. Next: object wipes
   (a page turn, a door), light transitions.
6. **Speed**: the render is CPU-bound in a headless browser (0.6 to 1.3 s a frame per core). Next: bake blurred
   static layers to images; cache static SVG.
7. **Shorts**: a filmed segment inside the Levels engine (Formats B to F of `short-form-standard.md`).

## 9. What the engine cannot do yet (13 Nov, after the prototype)

Hands are mitts (no finger poses); figures are side or front views (no 3/4 turn); only two sets exist (London 1720
street and study); a modern trading floor, bank office, boardroom and household set are not built; the balance
sheet, waterfall, LBO and debt-schedule scenes in `scene-library.md` are specified, not built; a filmed second costs
0.5 to 1.3 s of render per frame, so a fully filmed 10-minute film is 2 to 3 hours on 2 CPUs. Long films are hybrid
until that changes.

## 10. What cannot be claimed

A thumbnail or a still is not proof of animation quality. No run reports an improvement it did not render, watch
in motion and measure.
