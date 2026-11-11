# Reel style

The standard for every Reel from 3 November 2026. It comes from a reference
Reel Pietro chose ("Familiarity doesn't create excitement", a kinetic
typography piece by another creator), studied frame by frame, then mapped onto
this page's brand. The first Reel built to it is `w1-r04-dinged` in
`build/reels_motion.py`; copy its patterns.

## What the reference does

- **Kinetic typography carries the whole idea.** One argument told as a chain
  of short phrases, a new beat every 1.3 to 3 seconds, about 27 seconds long.
- **Lockups, not sentences.** Each beat stacks three sizes: a small sans
  connector ("But the"), one huge accent word ("Moment"), and an italic serif
  tail ("you change"). The eye lands on the big word first.
- **Letters arrive out of a blur**, one at a time, rising slightly.
- **Nothing is ever still.** A slow camera push-in under every scene; scenes
  whip across with motion blur or zoom through the camera into the next.
- **Highlighter swipes** behind key phrases; hand-drawn strokes (dashed curves,
  swooshes) draw themselves; small ornaments (sparkles, rings) move.
- **Light ground, soft deep shadows**, so cards and objects read as physical.
- **One dominant accent colour** used generously.
- Ends on the brand mark.

## How we apply it

| Reference | Ours |
|---|---|
| White ground | Paper `#F7F5F2` (`page(theme="paper")`) |
| Mustard accent | Red `#D93A12` for the mistake, teal `#0F766E` for the fix |
| Condensed sans + italic serif | Source Serif 4 700 for the huge word, Source Serif 4 italic for the tail, IBM Plex Sans for connectors |
| Photos and 3D renders | No stock imagery. Objects are built in HTML: quote cards, scorecards, charts, counters, all with soft shadows |
| Voiceover | Since 6 Nov: the Kokoro voice `af_heart` (or Pietro's cloned voice once recorded), captions burned in word by word, and sound effects; Pietro adds a trending track under it. The text must still carry the idea muted |

## The toolkit (`build/motion.py`)

- `ch(text, at, size)` reveals letters out of a blur; long lines speed up so
  they finish in about a second. Plain text only, real quotes and apostrophes.
- Scene keys: `enter` right, whip or zoomin; `exit` left, whip or zoom;
  `push` (about .03 to .04) for the slow camera push-in.
- Effects: `wipe` (highlighter), `draw` (strokes and swooshes), `stamp`,
  `count`, `ripple` (rings), `spin`, `flipin`/`flipout`, `roll` (slot word),
  `float`, `press`.
- `build(..., theme="paper", cover_at=seconds)`: the Reel can open on motion
  because the cover is taken from a fully composed moment.

## Rules

1. **Hook in the first second**, and it must work as the cover at `cover_at`.
2. **A beat every 2 to 3 seconds**; no scene sits still. Content starts
   building during the transition into its scene, never after it lands.
3. **One big word per beat.** If two words compete, split the beat.
4. **Under 35 seconds** unless the idea genuinely needs more.
5. **Every number worked through**; never invent a figure, statistic,
   credential or outcome. No em dashes.
6. **Safe area**: y 230 to 1440, left 84, right 244 clear. The renderer
   checks every scene and reports anything outside it. The check measures
   the layout without the push-in, which is a camera move of a few percent.
7. **Watch it in motion before shipping**: contact sheets at transitions, not
   just settled frames. Most problems only show mid-move.
8. **Sound effects on every Reel** (6 Nov, Pietro: "that's the standard we're
   going to use every time from now on"). Every beat with a physical feel gets
   a sound from `build/sfx.py`: ticks on a timer or a spinning number, a soft
   ding on a reveal, a thump when time is up, a pop when something lands
   (a level number, a chip, a score). More is better (Pietro, 6 Nov), with one
   exception: **no whoosh on the swipe between scenes**, which he found
   annoying.
   Quiet and short, under the voice and under the music added in the app.
   A Reel without voice still ships with its effects track (`sfx.mux`, -24
   LUFS) instead of silent.
9. Every Reel ships with: the MP4, the cover JPG, the caption (PASS on
   ig-human, one ask, up to 4 hashtags) and the comment question.
   The description (caption with hashtags) and the comment question are
   always pasted in the reply too, ready to copy, not only sent as files.

## Second format: the story Reel (4 Nov reference)

Modelled on a cinematic ad Pietro chose: a man so absorbed in a newspaper that
he walks through the whole city reading it, arrives at the place it was about,
and the paper flies off and loops back to the first shot. We cannot make
photoreal footage, so ours is illustrated (`build/reels_story.py`):

- **One object carries the story.** Our newspaper, *The IB. Daily*, is the
  page itself; the reveal at the end is that it was this page.
- **A character whose face is always hidden** by the paper: comic, and it
  keeps the account faceless. Built in SVG, walking with swinging limbs.
- **Escalating obliviousness** (taxi, building site, fountain) with a clock
  counting down, so there is tension every few seconds.
- **The payoff is the question the paper asked**, answered correctly on screen.
- **It loops**: the last shot is the first shot, so a second play feels free.
- One ask at the end, tied to what the page actually posts.

## Third format: the suspense Reel (4 Nov reference)

Modelled on a macro shot of a balloon and a needle: a camera HUD, "FRAMES TO
IMPACT" counting down, then the fourth wall ("you just watched a balloon for
7 seconds... still here, waiting for it to pop"), a pivot, and the pop held
back until the end. `build/reels_pop.py`, dark ground. The pivot must teach
something true: ours makes the balloon a DCF and the needle WACC, with a
worked perpetuity example. Key words over a red object go in ink, never red.

## Fourth format: the voiced game Reel (6 Nov)

`build/reels_find.py`. The viewer plays: "One number on this screen is wrong.
You have ten seconds." A countdown ring with real ticks, a spotlight that
searches the statement, then the voice walks the answer row by row, the wrong
cell is circled, struck and replaced, and the close is kind ("If you didn't,
that's okay. Now you are."). Voice, captions, ticks and visuals are all
generated from one timeline, so they cannot drift. Needs the Kokoro model
files in `$KOKORO_DIR` (see `build/voice.py`). AI label on when posting.

### The format is now an engine: `build/findgame.py` (6 Nov)

Each episode is a small config (`build/reels_find2.py` is #2, the LBO IRR).
Voice delivery upgraded for naturalness: whole passages per call so intonation
flows across sentences (sentence timings recovered from the audio's own
pauses, and checked against voice onsets), a slightly unhurried pace with
small variation, a recording chain (warmth, de-harsh, gentle compression, a
small room), a faint room tone, captions chunked to 7 words with no overlap.
Keep episodes at or under about 45 seconds.

## Fifth format: the levels Reel (6 Nov)

`build/levels.py`, episodes like `build/reels_levels1.py`. Interview questions
that get harder, read by the voice; the viewer keeps score and comments it.

- **The hook asks the last question first** ("Can enterprise value be
  negative?") and the final level answers it, so the Reel opens a loop only
  the end closes. **The hook is the question alone** (11 Nov, Pietro): no
  "That's level 4. Keep score." spoken or on screen, on every Reel from now on. The hook question is fully readable at
  frame 0 and is the cover.
- **Each level is one card**: lockup (big red numeral, LEVEL, italic tail
  from "easy." to "final boss."), the question lit word by word as it is read,
  a think bar with ticks that gets longer as the levels get harder, then the
  answer. The verdict ("Nothing.", "Yes.") is said on its own, a beat, then
  the reason, and a worked chip pops in. Answer words stay hidden until said.
- **Levels whip** left to right with motion blur (silent: no whoosh); the level meter at the top
  stays and fills, red for the current level, ink for the ones done.
- **Callbacks pay off**: level 3 teaches the formula level 4 needs, and the
  voice says so ("Remember level three").
- Close: "What's your score out of four?", a spinning score, "Comment it
  below", follow, brand. Comment question: a bonus level.
- Four levels keeps it near 52 seconds; five ran past a minute.
- Voice: Pietro's clone, alternating `clone:L2` and `clone:L3` (7 Nov; see
  the `ib-voiced-reel` skill). The engine can also take Pietro himself
  (`real:` memo of the script) if he asks for it.
