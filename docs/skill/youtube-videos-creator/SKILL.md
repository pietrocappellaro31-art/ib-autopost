---
name: "youtube-videos-creator"
description: "Daily YouTube run for the finance channel: research a topic that could travel, write and render one cinematic long-form 16:9 documentary (filmed scenes, one MP4 with an original score whose style changes every video) and one Short in the HEART narrator (natural, unprocessed), with thumbnails, titles, description, chapters and tags, checked against YouTube's AI, originality and monetisation rules. Posting stays manual."
---

# YouTube Videos Creator

Version 2026-11-16 (black background for Shorts; cinematic upgrade; Pietro's 14 Nov note: a natural, unprocessed narrator). The authoritative copy is `docs/skill/youtube-videos-creator/SKILL.md` in the
ib-autopost repo; the installed plugin is built from it (`docs/production/skill-sync.md`).

**17 Nov, Pietro: ONE file per YouTube video, the one with the music, and different music every time.** Long films
and Shorts deliver only the scored MP4 (our `score.py` score); the clean mix is never sent or offered. `score.pick()`
rotates the style (orchestral, noir_jazz, solo_piano, ambient, acoustic, mallets, harp) and the key so no video uses a
style or key of the last three; name the style in the delivery. Details: `docs/decisions-log.md` (17 Nov).

**From 19 Nov (Pietro, 18 Nov): Shorts are number puzzles cut from the films; films stay daily with the effort on
the opening minute and the thumbnail.** Each Short is the sharpest universal number puzzle of the newest long film
without a Short, asked in the title and on the first frame, set as the film's Related video in Studio. Each film opens
on its hook (puzzle or number on screen within 5 s, no chapter card first), says its question by 0:15, and carries the
same number in title and thumbnails (five words at most, checked at 168 x 94, both offered for Test & compare).
Details: `docs/decisions-log.md` (18 Nov), `short-form-standard.md`, `long-form-standard.md`.

**The standards live in the repo and win over this file where they disagree:** `docs/production/long-form-standard.md`,
`short-form-standard.md`, `cinematic-standard.md`, `audio-standard.md`, `quality-gates.md`, `scene-library.md`,
`animation-engine.md`, `voice-decision.md`. A newer decision by Pietro in `docs/decisions-log.md` wins over all of
them. Rules that are **no longer current** and must not come back from an older copy: GEORGE as the only YouTube
voice; a different trial voice every day; "no music in any long video"; one drawing card for every sentence; an
automatic AI-disclosure tick.

The channel is independent: the IB editorial identity only, nothing from any other channel, brand or project.
Runs every day as two scheduled tasks (long video and Short), or when Pietro asks. Everything is automated except
posting: Pietro uploads.

## FIRST: YouTube from 27 Nov (Pietro) wins over everything below

Pietro, 27 Nov: "For youtube please follow these guidelines moving forward: 1. Eliminate subtitles 2. 5 mins and not
any longer than that (current about 10 mins and too long) 3. Use voice from 'can share holders equity be negative?' ...
4. Thumbnail with yellow spark color 5. for the short youtube video make sure to use the same reels. Simply when you
produce the instagram reels, please provide the same description and tabs for youtube." And: "For youtube we will also
experiment with 'what if videos'" (his list below).

1. **No subtitles in the picture.** `youtube.SUBTITLES = False` removes the drawn beats' caption bar and the filmed
   beats' word-by-word captions. The big headline words of a drawn beat are design, not subtitles, and stay. The .srt is
   still written and delivered for YouTube's CC button (asked 27 Nov: "Keep the CC file").
2. **At most 5 minutes**, aim 4:00 to 4:50. `youtube.MAX_SECONDS = 300` stops the build above it: cut the script (about
   600 to 680 words at EMMA's pace), never speed up the voice. Story structure stays (hook in 5 s, mechanism, turn,
   payoff), compressed: 4 to 6 chapters.
3. **Voice EMMA** (Kokoro bf_emma, speed 0.97, the voice of the 12 Nov Reel "Can shareholders' equity be negative?"):
   long films and Shorts, 27 Nov to 4 Dec like the Reels (`voice_clone.NARRATOR_WINDOWS`), then Pietro decides again
   (asked 27 Nov: "Until 4 Dec, then decide").
4. **Thumbnails on a spark-yellow background only** (asked 27 Nov: "Only yellow background"): `youtube.thumb_looks()`
   returns spark-yellow (art right) and spark-yellow-left (art left), both a bright #FFD400 ground, black type, red
   highlight.
5. **Shorts are the Reels.** No separate Short is made (the "YouTube Short daily" task stays off). Each Reel run also
   runs `python3 build/yt_short_from_reel.py <slug> --mood <mood>`: the Reel's picture with a track from Pietro's
   library under the voice (item 7; the Instagram track is never on YouTube) and `youtube.txt` with the title (the hook), the Reel's
   description (follow line turned into a subscribe line, music credit, not-advice line, #Shorts) and tags. Pietro
   uploads by hand.
7. **Music on every YouTube video comes from Pietro's library** (27 Nov): load it with the ib-music-access skill (the
   private artifact "IB Music Library", slug 331a2c60-239a-4b00-acd3-dffde353a56a: read_file files.json and
   library.json, then only the tracks needed, .pNN parts joined in order, sha256 checked, into
   build/music_library/audio/, never committed). Shorts: `yt_short_from_reel.py <slug> --mood <mood>`. Long films:
   render as usual, then `yt_short_from_reel.py <slug> --film --mood <mood>` (a second track crossfades in if the first
   runs out) and deliver <slug>-music.mp4 as the one file. Only tracks where `music_library.mixable(t, "youtube")` is
   true (never Presentation 1 and 2). Credit in the description: "Music: <title> by <artist> (Pixabay)". Music clearly
   audible (Pietro, 27 Nov, at about 20 dB under: "Too quiet - almost inaudible"): then "Even louder": default level about 3 dB
   under the voice (library_alternative music_under_db -1, duck 4); the word check must stay at 0, voice at least 2 dB over. If a track gets a Content ID claim, tell Pietro and drop it from the
   library. Our original score (`--score`) only when the artifact cannot be read, and say so.
6. **"What if" films**, alternating with the finance documentaries (a what-if on 30 Nov, a documentary on 1 Dec, and so
   on). Pietro's list, take them in this order unless a newer idea of his comes first:
   What could you buy with $1 billion? (scenarios: how many Ferraris, an island, a sports team, a small city's budget) /
   What if you inherited $20 million tomorrow? / What if you invested $10 a day for 30 years? / What if there were a
   world with no taxes? / What if you could travel back in time with $20 million? / What if you dropped out of college?
   / Living on $1 a day / How much money does Harvard make?
   Every price, return and figure is sourced and dated (the price of a Ferrari model, Harvard's annual report, the
   World Bank poverty line); a return assumption is named as an assumption (for example "if it grew 7% a year, the
   S&P 500's long-run average after inflation is about that, not a promise") and shown with a plain range; no advice.
   Titles may be playful, never false; the thumbnail carries the title's number.

## Before making anything

1. In the ib-autopost repo read the production files above, `docs/brand-system.md`, `docs/decisions-log.md`,
   `docs/daily/README.md`, `docs/daily/quality-log.md` (the last row's "Next improvement" for your run is the first
   job), `docs/daily/topics.md`, and the last rows of `docs/daily/youtube-long.md` and `youtube-shorts.md`. Load the
   skills content-compliance, music-library and ig-human.
2. `bash build/setup_voice.sh && source ~/voice-tools/env.sh` (Kokoro, recogniser, DNSMOS, the SoundFont).
3. Inspect `git status` and keep any changes already there; `git pull --rebase` before committing (the long-video,
   Short and Reel runs write the same logs). Never force-push.

## Voice

**HEART: Kokoro v1.0 `af_heart`, speed 0.9, en-us** for long videos and Shorts (`voice_clone.YOUTUBE_PICK`).
`youtube.make` uses it by default; render a Short with `python3 build/shorts_<slug>.py HEART`. Synthetic, imitates
nobody. The narrator has no name, face, credentials or past: never "when I worked at a bank". Names and terms go
in `build/voice.py` `PHONEMES` (unknown words stop the render). Lines are cached (`synth.pkl`): editing one line
re-says only that line. The 11 to 13 Nov voice trial is closed; its log stays as history.

**A natural voice, not a processed one (Pietro, 14 Nov: "from tomorrow on voice should feel more natural"; least
natural was "robotic / processed sound").** `docs/production/audio-standard.md` 1b:
- The narrator chain `voice.MASTER` is a highpass and a 1.5 dB dip at 7.2 kHz, nothing more. Never add compression,
  echo or reverb, de-noise or an exciter to HEART; no limiter before the master (Shorts and Reels: `levels.two_stage`,
  one true-peak limiter). `voice.MASTER_8NOV` exists only to re-render an old video exactly.
- Every render prints `SIG drop voice to mix` (gate 0.15 or less) and clipped voice-stem samples (gate 0); fix a CHECK
  before delivery and log both in the quality-log row.
- Delivery: each beat or passage said in one pass (the story engine does); `split=True` (sentence by sentence) only
  when the recogniser hears a word wrong in context and rewording cannot fix it. Write lines to be said: contractions,
  short sentences, how a person explains it aloud, no read-out constructions.
- Nobody here can listen: when the voice changes, send Pietro a short A/B clip of the same lines.

## 1. Topic

A surprising, true central question that makes a good film or Short: finance history, bubbles, crises, behavioural
finance, banking and careers, PE and LBOs, modelling, corporate finance, scandals, money psychology. Search the web
for what people are asking now. Not in `topics.md` "Used" within 60 days; long video and Short on different topics.

## 2. Research and script

- Every material claim sourced in the episode docstring and linked in the description (`sources=[(label, url)]`,
  only URLs opened or returned by a search in the run; `source_note=` for our own illustration). **Never invent a
  number, date, quote, statistic, URL or credential.** Check every calculation with a short script.
- Keep apart: documented fact, uncertain anecdote ("is supposed to have said"), our interpretation, illustrative
  reconstruction. Historical quotes verified and attributed; legends told as legends.
- Original analysis with a point of view (what the common story gets wrong, why it matters): that is what keeps the
  channel monetisable. No em dashes. Spoken numbers in words; on-screen numbers in digits. Educational, not advice.

## 3. Long video (16:9, 8 to 12 minutes)

Follow `long-form-standard.md`: hook in 5 to 15 s, context, mechanism, escalation, turning point, analysis,
conclusion and one takeaway.

1. Visual plan `build/plans/ep<NNN>.md` **before** rendering: one row per beat (narration, objective, scene family A
   to L from `scene-library.md`, assets, motion, camera, data and source, effects, score mood, seconds).
2. Copy the latest `build/youtube_ep<NNN>.py`. Chapters of 3 to 6 beats. Mix scene families; **visual progression**,
   not a card per sentence: one evolving scene may carry several sentences.
   - **Filmed beats** where the story has people, places or a mechanism: `show=dict(kind="cine", shot=fn)` with
     `fn(w, h, dur, ctx)` returning `dict(shots=[...], foley=[...], amb=array)` from `build/cine.py` and
     `build/cine_lib.py` (worked examples: `build/cine_poc_newton.py`, `build/youtube_cine_test.py`). Aim for one
     filmed beat per two chapters and a filmed hook when it can be. Reconstructions carry the RECONSTRUCTION badge;
     props show only sourced figures.
   - Drawn beats: `build/sketch.py` scenes (`kind="sketch"` beside a line, `kind="scene"` alone) and the other kinds
     (icon, split, timeline, flow, verdict, quote, number, compare, list). At most one text-only beat per chapter;
     every chapter card has `art=`. Add a scene or a cine set when the story needs one: a good daily improvement.
   - `score="reflective" | "suspense" | "light"`: the scored mix (`build/score.py`, one mood per chapter); the style
     and key come from `score.pick` (17 Nov: never one of the last three videos'); `score_style=` overrides.
   - `thumb=dict(...)`: two looks from `youtube.THUMB_LOOKS`, never one used the day before.
3. `python3 build/yt_preview.py build/youtube_ep<NNN>.py` (variety test, must pass), then
   `python3 build/yt_timing.py build/youtube_ep<NNN>.py --takes` (length, every line heard word for word).
4. Render `python3 build/youtube_ep<NNN>.py`. Outputs in `build/out/<slug>/`: `<slug>.mp4` (the one deliverable, always
   scored; the gate lowers the music and remixes if it fails), `<slug>-clean.mp4` (the gate's reference, not delivered), `thumbnail_a.jpg`, `thumbnail_b.jpg`,
   `<slug>.srt`, `transcript.txt`, `description.txt`, `metadata.json`, `sound.json`, `music.json`. Filmed beats cost
   0.5 to 1.3 s of render a frame: budget for them.
5. `python3 build/yt_preview.py build/youtube_ep<NNN>.py --motion`: look at the motion sheets and `motion.json`, not
   only stills. Then every gate in `quality-gates.md`.

## 4. Short (9:16)

**Black background (Pietro, 16 Nov: "Set this as the rule from now on for both IG reels and YouTube shorts").** Every
Short renders on black: it is the default of `levels.py` and `story.py` (`theme="black"`). No colour ground per part
(`bg=` is ignored on black), light text on the ground, bright teal answers, white cards, every drawing on a paper
panel, films unchanged. Look at the frames on black: nothing ink-coloured may sit directly on the ground (floaters
and close art included: give them light fills or leave them out). Same format, quality bar and gates otherwise.

Follow `short-form-standard.md`. Formats: A the four-level quiz (the hook is the last question alone, never "That's
level 4. Keep score."), B story, C one surprising concept, D animated calculation, E myth, F choice or challenge.
Pick the best for the topic and vary the week. 35 to 55 s for most; under 60 for the quiz.

- Levels engine: copy the latest `build/shorts_<slug>.py` (the penny and Friday-13th Shorts are the floor): black
  ground (16 Nov; the colour grounds per part are retired), a drawing of the concept in each answer zone, floaters, an animated close; `clear.json` and `WRAP`
  at zero; two-stage master at -14 LUFS.
- A filmed segment (a story beat, a character reacting) can come from `cine.py`: the same world is reframed for 9:16
  (`cine_poc_newton.py --vertical` is the example).
- Music (17 Nov): deliver ONLY the scored Short (`python3 build/master.py scored ...`, style and key from
  `score.pick`, never the last three videos'); no clean file, no "add a sound" steps. Earlier rule, history only:
  the **clean master** was the one delivered (voice, effects, room tone; Pietro adds a sound in the YouTube
  app). A **scored alternative** is prepared when practical: `python3 build/master.py scored build/out/<slug>/<slug>.mp4
  <mood> <mood>` writes `<slug>-scored.mp4` and a report; offer it as unheard until Pietro approves a score.py cue.
  If the scheduled task's own prompt says "no scored master unless Pietro asks", Pietro's 17 Nov decision overrides it: make and deliver the scored Short only.
- Set `mood=` so the render writes `music_pick.json` for the music block (music-library skill).

## 5. Compliance, metadata and disclosure

Run the content-compliance gate. Then:

- **AI disclosure: a recommendation per finished video with its reason** (`quality-gates.md` section 6). Current
  reasoning: YouTube asks for disclosure of realistic altered or synthetic content and exempts animation; a synthetic
  narrator is not addressed and disclosure costs nothing in reach or earnings, so the recommendation is Yes, said
  with that reason. Re-check the help page monthly.
- "Made for kids": No, unless a video really is aimed at children.
- Long video: five title candidates and one recommended; description with real chapter times, "Sources and
  references" with links, the music line (scored: `Music: original score made for this video.`; clean with Pietro's
  track: `Music: [song title] by [artist], from the YouTube Audio Library`), `Narration: AI-generated voice; script
  and analysis are our original work.` and the not-financial-advice line (the engine writes them); 2 or 3 hashtags;
  Studio tags (500 characters at most, `tags_for_studio`); a pinned-comment question.
- Short: title under 70 characters plus two alternatives; `#Shorts` and one or two hashtags.
- Title and description PASS on ig-human. No third-party footage, logos or photos of real people; no bank logos or
  implied affiliation; no promised returns or job outcomes. Rights record `docs/rights/posts/<slug>.md`.

## 6. Deliver

Long video, with SendUserFile: `<slug>.mp4` only (the scored mix; 17 Nov: never the clean MP4 as well), both
thumbnails, the `.srt`, `description.txt`, the motion sheets and the rights record. Then one SendUserMessage: titles,
description, chapters, tags, hashtags, pinned comment, voice, the music (the style, key and tempo from `music.json`,
the gate result, the credit line `Music: original score made for this video.`), Studio settings with reasons,
sources, quality results, today's verified improvement, what needs his review.

Short: the scored MP4 only (17 Nov), the cover, the `.srt` if written, `qa.md`, then one message with the titles,
description, hashtags, tags, pinned comment, voice, the music (style, key, the credit line), disclosure and audience
with the reason, measures, sources and today's improvement. Upload steps: YouTube app, +, "Upload a video", pick the
file, "Next", no added sound (the score is already in the file), title and description, "No, it's not made for
kids", upload; then the AI setting in Studio on a computer (Content, Shorts, the Short, Show more, "Altered content"
or Attributes, "AI use") as recommended.

## 7. Log and improve

Rows in `docs/daily/youtube-long.md` or `youtube-shorts.md` (voice, format), the topic in `topics.md` "Used", and a
row in `quality-log.md`: voice and DNSMOS, exact lines, layout and pacing, drawing-beside-text share and filmed beats,
static share and longest static run, LUFS and true peak of each master, voice over music, the score gate, render
time, what improved (built, measured, shown in motion) and one concrete next improvement. A cosmetic change does
not count. Commit the episode, plan, engine changes, rights and logs (never MP4s, stems, recordings or keys).

## Never

- Clone or imitate a real person's voice or face; give a historical figure a voice or invented words.
- Put a commercial or trending song, or anything we have no rights to, in a file; edit audio to dodge Content ID.
- Claim a listening verdict nobody gave, or an improvement that was not rendered, watched in motion and measured.
- Post, schedule or change anything on YouTube: Pietro uploads.
