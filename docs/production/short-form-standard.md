# YouTube Shorts: production standard

Pietro, 13 Nov 2026. This is the permanent standard for every YouTube Short. Each daily Shorts run
reads it first, along with `docs/skill/youtube-videos-creator/SKILL.md`. Where an older rule
disagrees, this file wins, unless Pietro has since recorded a newer decision in
`docs/decisions-log.md`.

The Shorts are for the finance channel's IB identity. They are separate from any other project:
no other channel's characters, branding or data. Posting stays manual: Pietro uploads.

## What is settled here (13 Nov)

- **Narrator:** Kokoro af_heart (HEART), en-us, speed 0.9, for Shorts and long videos alike.
  `voice_clone.YOUTUBE_PICK = "HEART"`; `voices.json` HEART speed 0.9. The daily voice trial is over,
  and `docs/daily/youtube-voice-trial.md` stays as history. Render with
  `python3 build/shorts_<slug>.py HEART`.
- **Music:** the clean master (narration, sound effects and room tone, no music) is the one delivered; Pietro adds a
  sound in the YouTube app. Later the same day the cinematic-upgrade directive asked for a scored alternative "when
  practical": `python3 build/master.py scored build/out/<slug>/<slug>.mp4 <mood> <mood>` adds an original `score.py`
  cue to the finished clean file (`<slug>-scored.mp4`, measured), offered as unheard until Pietro approves a cue.
  If the day's task prompt says "no scored master unless Pietro asks", the prompt wins. No commercial song is ever
  in a file.
- **Formats:** the four-level quiz stays. Five more formats are allowed (below). Pick the one that
  suits the topic best; vary it across the week.

## 1. Each run starts with

1. Read this file, `docs/brand-system.md`, `docs/decisions-log.md`, `docs/reel-style.md`,
   `docs/daily/README.md`, `docs/daily/quality-log.md`, `docs/daily/topics.md`,
   `docs/daily/youtube-shorts.md`, `docs/daily/youtube-long.md`, `docs/daily/ig-reels.md`, and the
   skills youtube-videos-creator, ib-voiced-reel (how the Levels engine renders and is checked),
   content-compliance, music-library and ig-human.
2. The last YouTube Short row in `quality-log.md`: its "Next improvement" is the first job. Do it
   when feasible, measure it, and record what changed. No change only for novelty.
3. Inspect the working tree and keep any changes already there (`git pull --rebase` before
   committing: the long-video run writes the same logs).

## 2. Topic

A topic for a broad finance audience, researched on the web: finance history, banking careers, IB
interviews, money psychology, financial myths, corporate finance, modelling, famous market events,
personal finance concepts, behavioural economics, simple maths challenges, surprising facts. Not in
`topics.md` "Used" within 60 days, and different from the day's long video and Reel when possible.
Never invent or stretch a claim to make it more sensational.

## 3. Formats

- **A. Four levels.** Four questions, easy to hard, the hardest asked first as the hook (the
  question alone: never "That's level 4. Keep score."). Clear level meter, animated reveals,
  worked answers, a final comment invitation. The penny Short and the Friday the 13th Short
  (`build/shorts_friday-13th-stocks.py`) are the baseline; each new one must beat them in
  animation and presentation.
- **B. Financial story.** One story told in animated scenes: beginning, conflict, turning point,
  conclusion.
- **C. One surprising concept.** One counterintuitive idea, shown in a focused animated
  demonstration.
- **D. Animated calculation.** One meaningful calculation built up on screen, every step correct
  (compound interest, contribution margin, break-even, enterprise value, leverage, multiples,
  returns).
- **E. Financial myth.** The misconception, the evidence, the correct reading.
- **F. Choice or challenge.** A scenario the viewer reasons through. No misleading promises.

Formats B to F are new on 13 Nov and have no engine of their own yet. Build them with the existing
tools (`build/levels.py` and `build/motion.py` scenes, `build/sketch.py` drawings) and log what
was built, so the first run of each format becomes the template for the next.

## 4. Length and the first seconds

About 35 to 55 seconds for most Shorts; always under 60 for the quiz. No padding, no rushed
narration: it must be clear at normal speed. Open at once on a question, an unusual visual, a
sourced surprising claim, a historical moment, a number puzzle or a strong story beat. No branded
intro.

## 5. Animation

Every major segment carries real movement that explains the idea: coins stacking, a chart drawing
on, a figure walking into a bank, a document being signed, a balance sheet changing, a clock
counting down, a payment timeline unfolding, a debt pile shrinking, a comparison counting. A
moving background behind a still card does not count. Never so busy that the text is hard to read.

Quiz standard: a colour ground per part, a drawing of the concept being tested (not decoration) in
each level's answer zone, a readable timer, an animated reveal, a short worked explanation, a
consistent level meter, faint floaters at the edges, an animated close.

Figures: use our own stick figures (`sketch.figure`, `figures`) when a person helps explain the
idea (walking, pointing, thinking, paying, reacting, deciding), the same figure throughout one
Short. Original only.

Engine: `levels.py`, `motion.py` and `sketch.py` for the quiz and most formats. Since 13 Nov (cinematic upgrade)
`build/cine.py` can film a segment (a story beat, a figure reacting, a historical moment) in 9:16 from the same
world as a long video: `python3 build/cine_poc_newton.py --vertical` is the worked example. A filmed segment costs
about 1 s of render per frame, so use it where it teaches, not as decoration. No Remotion (`animation-engine.md`).

## 6. Voice

HEART at 0.9 (above). Natural, expressive delivery; numbers, financial terms and company names
said right (add words to `PHONEMES` in `build/voice.py`). Every line is checked (`takes.json`,
WER 0). When the recogniser reports a miss, listen to the actual line: it may be a real slip
(reword it) or a false miss (teach the word check). The narrator has no credentials and no life
story.

## 7. Sound

Effects tied to what happens on screen: coins, calculator keys, a page turning, a ticking clock, a
soft register or payment chime, a chart accent, footsteps. Never overused, never a whoosh on every
swipe. Master at about -14 LUFS integrated, true peak no higher than -1.5 dBTP (two-stage master,
`levels.two_stage`), narration clearly on top, no clipping or over-compression.

## 8. Text and safe area

Readable on a phone. Nothing essential under YouTube's controls, channel name, description overlay
or bottom bar. The render checks the current safe box (nothing above y=230 or below y=1440, the
right 230 px clear) plus overlaps (`clear.json`) and one-word lines (`WRAP`). If YouTube's
interface changes, update the box.

## 9. Accuracy

Every answer correct: maths worked in the docstring, sources opened in the run, dates checked,
questions unambiguous, estimates called estimates, illustrations marked as not data. No invented
figures, no income claims, no personal investment advice.

## 10. Checks before delivery

Full render; contact sheet of frames and a few moving stretches watched; safe area, overlap and
wrap flags at zero; every expected line in `takes.json` at WER 0; DNSMOS on voice and mix; loudness
and true peak; effects in sync with their actions; originality, rights and monetisation review
(content-compliance gate). Nothing ignored silently.

## 11. Cover and metadata

- A cover that shows the actual Short: the IB brand, readable type, one strong focal point.
- One recommended title under 70 characters and two alternatives.
- Description: what the Short covers, sources with links (only URLs opened in the run), the
  not-financial-advice line, then hashtags (#Shorts plus one or two), then last:
  `Narration: AI-generated voice; script is our original work.`
- Studio tags (one comma-separated line, under 500 characters) and a pinned-comment question.
- Title and description PASS on ig-human. No em dashes.

## 12. Disclosure and audience

Judge the AI setting on the actual video and YouTube's current rules: say what the content is and
why the setting is Yes or No. A clearly animated drawing is not by itself a realistic altered scene.
A realistic-sounding synthetic narrator can be taken for a real person, so the current
recommendation stays "Altered or synthetic content: Yes" (no effect on earnings) unless YouTube's
rules change; the description always names the AI narration. Audience: our finance Shorts are made
for adults and teens, not for kids: "No, it's not made for kids", unless a video really is.

## 13. Music for the clean master

Only sounds verified in the run: Pietro's music library pick (`music_pick.json`) first, then one or
two sounds shown by a current source to be trending on Shorts that week. If trending sounds cannot
be verified, say so and suggest the library pick and a mood only. Then the steps from section 7
of the youtube-videos-creator skill (open the app, upload, "Add sound", the start point, volume
about 15 to 25 under "Original sound" at 100, check the voice is easy to follow in the first 10
seconds, finish the upload, the AI setting in Studio on a computer).

## 14. Deliverables

With SendUserFile: the clean MP4, the cover, the subtitle file when one is written, and a QA report
(`build/out/<slug>/qa.md`: measures, checks, sources, rights). Then one message with the title and
two alternatives, the description, hashtags, Studio tags, pinned comment, the voice, the music
options and upload steps, the disclosure and audience settings, the measured results, a source
summary and the day's improvement.

## 15. Logs and git

Update `docs/daily/youtube-shorts.md`, `docs/daily/topics.md`, `docs/daily/quality-log.md` (run
"YouTube Short": topic, voice, runtime, measures, the improvement and the next improvement), and
`docs/rights/posts/<slug>.md`. The voice-trial log is closed; the voice and DNSMOS now go in the
quality-log row. Commit the episode source, engine changes, captions, rights and logs; never MP4s,
recordings or credentials. `git pull --rebase` first, never force-push.
