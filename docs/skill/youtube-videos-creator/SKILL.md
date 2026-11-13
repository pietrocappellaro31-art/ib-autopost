---
name: "youtube-videos-creator"
description: "Daily YouTube run for the finance channel: research a topic that could travel, write and render one cinematic long-form 16:9 documentary (filmed scenes, original score, clean and scored masters) and one Short in the HEART narrator, with thumbnails, titles, description, chapters and tags, checked against YouTube's AI, originality and monetisation rules. Posting stays manual."
---

# YouTube Videos Creator

Version 2026-11-13 (cinematic upgrade). The authoritative copy is `docs/skill/youtube-videos-creator/SKILL.md` in the
ib-autopost repo; the installed plugin is built from it (`docs/production/skill-sync.md`).

**The standards live in the repo and win over this file where they disagree:** `docs/production/long-form-standard.md`,
`short-form-standard.md`, `cinematic-standard.md`, `audio-standard.md`, `quality-gates.md`, `scene-library.md`,
`animation-engine.md`, `voice-decision.md`. A newer decision by Pietro in `docs/decisions-log.md` wins over all of
them. Rules that are **no longer current** and must not come back from an older copy: GEORGE as the only YouTube
voice; a different trial voice every day; "no music in any long video"; one drawing card for every sentence; an
automatic AI-disclosure tick.

The channel is independent: the IB editorial identity only, nothing from any other channel, brand or project.
Runs every day as two scheduled tasks (long video and Short), or when Pietro asks. Everything is automated except
posting: Pietro uploads.

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
   - `score="reflective" | "suspense" | "light"`: the scored mix (`build/score.py`, one mood per chapter).
   - `thumb=dict(...)`: two looks from `youtube.THUMB_LOOKS`, never one used the day before.
3. `python3 build/yt_preview.py build/youtube_ep<NNN>.py` (variety test, must pass), then
   `python3 build/yt_timing.py build/youtube_ep<NNN>.py --takes` (length, every line heard word for word).
4. Render `python3 build/youtube_ep<NNN>.py`. Outputs in `build/out/<slug>/`: `<slug>-clean.mp4`,
   `<slug>-scored.mp4`, `<slug>.mp4` (the recommended one after the score gate), `thumbnail_a.jpg`, `thumbnail_b.jpg`,
   `<slug>.srt`, `transcript.txt`, `description.txt`, `metadata.json`, `sound.json`, `music.json`. Filmed beats cost
   0.5 to 1.3 s of render a frame: budget for them.
5. `python3 build/yt_preview.py build/youtube_ep<NNN>.py --motion`: look at the motion sheets and `motion.json`, not
   only stills. Then every gate in `quality-gates.md`.

## 4. Short (9:16)

Follow `short-form-standard.md`. Formats: A the four-level quiz (the hook is the last question alone, never "That's
level 4. Keep score."), B story, C one surprising concept, D animated calculation, E myth, F choice or challenge.
Pick the best for the topic and vary the week. 35 to 55 s for most; under 60 for the quiz.

- Levels engine: copy the latest `build/shorts_<slug>.py` (the penny and Friday-13th Shorts are the floor): a colour
  ground per part, a drawing of the concept in each answer zone, floaters, an animated close; `clear.json` and `WRAP`
  at zero; two-stage master at -14 LUFS.
- A filmed segment (a story beat, a character reacting) can come from `cine.py`: the same world is reframed for 9:16
  (`cine_poc_newton.py --vertical` is the example).
- Music: the **clean master** is the one delivered (voice, effects, room tone; Pietro adds a sound in the YouTube
  app). A **scored alternative** is prepared when practical: `python3 build/master.py scored build/out/<slug>/<slug>.mp4
  <mood> <mood>` writes `<slug>-scored.mp4` and a report; offer it as unheard until Pietro approves a score.py cue.
  If the scheduled task's own prompt says "no scored master unless Pietro asks", follow the prompt.
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

Long video, with SendUserFile: the recommended MP4, the clean MP4 (and the scored one if it is not the
recommendation), both thumbnails, the `.srt`, `description.txt`, the motion sheets and the rights record. Then one
SendUserMessage: titles, description, chapters, tags, hashtags, pinned comment, voice, music (which master and why,
the gate result; for clean, the credit line and the Studio steps: Content, the video, Editor, Audio, pick an Audio
Library track, keep it low under the voice, Save), Studio settings with reasons, sources, quality results, today's
verified improvement, what needs his review.

Short: the clean MP4, the scored alternative if made, the cover, the `.srt` if written, `qa.md`, then one message with
the titles, description, hashtags, tags, pinned comment, voice, the music block below, disclosure and audience with
the reason, measures, sources and today's improvement.

```
Music for this Short (add it in the YouTube app on your phone)
Suggested sounds:
  1. <library pick: song - artist> (from your music library): <why it fits, one line>; start at <calm_start>
  2. <song - artist> (verified trending on Shorts this week): <...>   (or: none verified this week)
Steps:
  1. Open the YouTube app, tap +, then "Upload a video", and pick <slug>.mp4.
  2. On the trim screen tap "Next" (not "Add details"); in the editor tap "Add sound" and search the first song.
     If it is not there, try the next; if none is, pick any song the app offers that fits <mood>.
  3. Start it on <calm_start or a calm, instrumental stretch>, not on a vocal chorus.
  4. "Volume": original sound 100, the added track about 15 to 25; play the first 10 seconds; the voice must be easy
     to follow. Library songs may be cut to a short clip (YouTube Help: 15 s on uploaded videos): place it on the hook.
  5. Next, paste the title and description, "No, it's not made for kids", upload.
  6. AI setting (the phone may not show it): studio.youtube.com, Content, Shorts, the Short, Show more, "Altered
     content" (newer Studio: Attributes, "AI use"): answer as recommended. Save.
If you upload the scored alternative instead, skip steps 2 to 4: it already has our original score.
```

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
