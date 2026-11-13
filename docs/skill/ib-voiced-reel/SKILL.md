---
name: "ib-voiced-reel"
description: "Make every Instagram Reel for @investmentbankinginterviews to the same cinematic standards as the YouTube films: the HEART narrator (Kokoro af_heart, 0.9), real animation and filmed segments, synchronised sound effects, a clean master plus an original-scored alternative when feasible, motion and quality gates, caption, comment question and the daily quality log. The Levels quiz is one format, not the only one."
---

# Voiced Reels for @investmentbankinginterviews

Version 2026-11-13 (cinematic upgrade). Authoritative copy: `docs/skill/ib-voiced-reel/SKILL.md` in the ib-autopost
repo; the installed plugin is built from it (`docs/production/skill-sync.md`).

**Standards (13 Nov 2026, Pietro: "Do the new standards apply to reels as well? They should."):** every Reel
follows `docs/production/cinematic-standard.md`, `audio-standard.md`, `quality-gates.md` (section 9 is the Reel
gate), the formats A to F of `short-form-standard.md` and `voice-decision.md`, exactly as Shorts and long videos do.
`docs/reel-style.md` stays the visual base (paper, kinetic type). The bar is the cinematic proof of concept
(`build/cine_poc_newton.py`; Pietro, 13 Nov: "exactly the quality we are looking for"). These win over this file
where they disagree, unless `docs/decisions-log.md` records a newer decision by Pietro. An older copy of this skill
that names the G2, BELLA, EMMA rotation, "no music in any file" or the Levels quiz as the only format is out of date.

## The voice rule (from 13 Nov)

**HEART: Kokoro af_heart, speed 0.9, en-us**, the same narrator as the YouTube channel (Pietro's cinematic-upgrade
directive, 13 Nov). `voice_clone.next_voice()` returns it (`REEL_PICK = "HEART"`); render with
`python3 build/reels_<slug>.py HEART`. A different voice only if Pietro names one for a Reel, recorded in
`build/voices/voice_log.json`.

History, kept: the 8 Nov one-month rotation G2, BELLA, EMMA and the older clones (P1, L2 to L4, F1 to F3) stay in
`voice_log.json`, `voices.json` and `docs/production/voice-decision.md`, for re-rendering old Reels only. Never clone
anyone. The narrator is synthetic, has no name, face, credentials or past, and never says "when I worked at...".

## Before making anything

Read `docs/brand-system.md`, `docs/decisions-log.md`, `docs/reel-style.md`,
`docs/daily/quality-log.md` (the last row's "next improvement" is today's
job) and `docs/daily/topics.md` in the ib-autopost repo.

## Setup, once per new session

From the repo root:
`bash build/setup_voice.sh && source ~/voice-tools/env.sh`
It downloads Kokoro, Pocket TTS, the speech recogniser, the speaker model and
the DNSMOS quality model (about 1 GB, a few minutes). No key is needed for
HEART or any stock Kokoro voice. Never print or commit a key if one is around.

## Make the Reel

1. **Format**: the Levels quiz is the main recurring series (`build/levels.py`; copy the latest
   `build/reels_levels<N>.py`), not the only format: an animated story, one concept, a calculation, a myth or a
   choice (formats B to F of `docs/production/short-form-standard.md`) when the topic is better told that way.
   Every segment carries real movement that explains the idea (`cinematic-standard.md` section 6); filmed scenes
   from `build/cine.py` can be used in 9:16 (the world reframes with `cine.stage()`). Pick a topic not in `docs/daily/topics.md`
   "Used" for Reels; IB interview technicals first.
2. **Write the episode file** `build/reels_<slug>.py`. Work every answer in
   its docstring. Never invent a number, statistic or credential. No em
   dashes. Spoken text uses words for numbers; on-screen text uses digits.
   Each hook is one sentence in one `say` entry, and it is the only entry:
   the question alone. Never "That's level 4. Keep score." (Pietro, 11 Nov).
3. **New words**: the voice stops on a word it cannot pronounce. Add it to
   `PHONEMES` in `build/voice.py` (plurals, -ed and -ing are worked out from
   the stem automatically).
4. **Render**: `python3 build/reels_<slug>.py HEART` (the name `next_voice()` returns). A few minutes.
5. **Layout problems** ("SAFE-AREA PROBLEMS"): smaller type (`qsize`,
   `bigsize`) or a shorter chip, then
   `make(EP, "<VOICE>", keep_voice=True)` so the voice stays the same. A
   wrong line: `make(EP, "<VOICE>", keep_voice=True, redo=["a2"])`.

## Checks before delivering (`quality-gates.md` section 9)

- Motion in motion: `python3 build/yt_preview.py --clip build/out/<slug>/<slug>.mp4` (static share, longest static
  run, logged) and a contact sheet of the hook, each level or beat, the transitions and the close. Cards with only a
  push-in fail.
- Facts and rights as for any film: every number worked in the docstring, reconstructions badged, props show only
  sourced figures.
- `build/out/<slug>/takes.json`: every line `"wer": 0` (heard word for word).
- Quality: `python3 -c "import quality; print(quality.score('build/out/<slug>/<slug>.mp4'))"`
  (DNSMOS overall; about 3.1 to 3.5 is studio-clean).
- Loudness about -16 LUFS, true peak no higher than -1.5 dB
  (`ffmpeg -i <mp4> -af ebur128=peak=true -f null -`).
- Look at frames: the cover, each level settled, the transitions.

## Sound

Sound effects on every Reel (`build/sfx.py`): ticks, pops, dings, thump, and for filmed scenes footsteps, paper,
coins, quill, a soft mallet on numbers (`audio-standard.md` 5). Each effect belongs to something on screen.
**Never a whoosh on the swipe between scenes.**

Masters (`audio-standard.md` 3): the **clean master** (voice and effects, no music, about -16 LUFS, true peak at or
under -1.5 dBTP) is the deliverable; Pietro adds music from Instagram's library in the app. An **original-scored
alternative** is made when feasible (the IG Reel task's 13 Nov override asks for it):
`python3 build/master.py scored build/out/<slug>/<slug>.mp4 -16 <mood> <mood>` writes `<slug>-scored.mp4` and
`<slug>-scored.json` (our own `build/score.py` score, class ORIGINAL_GENERATED, ducked under the voice, mastered to
-16 LUFS, word check against the clean file). Offer it as an alternative Pietro has not heard yet; the clean file
stays the default. Never a commercial or trending song in a file, and never a version carrying YouTube-library audio.

## Compliance

Run the content-compliance gate. Write `docs/rights/posts/<slug>.md`.

## Deliver

1. Send the MP4 and the cover with SendUserFile.
2. Caption: PASS on ig-human, one ask, up to 4 hashtags, no promise of returns or jobs, no invented experience,
   a title that matches the content, then just before the hashtags:
   `Narration: AI-generated voice; script is our original work.` (and, only for an old G2 re-render,
   `Voice model: Pocket TTS by Kyutai`).
3. Comment question: a bonus level.
4. Paste the description and the comment question in the reply, ready to
   copy.
5. Remind Pietro to turn on Instagram's AI label when he posts (realistic synthetic voiceover, Meta's rule), with
   the reason; judge any other disclosure on the finished Reel (`quality-gates.md` section 6).
6. Say which voice was used.
7. Add a row to `docs/daily/ig-reels.md`, the topic to `docs/daily/topics.md`
   and the measures plus one improvement to `docs/daily/quality-log.md`.
8. Commit the episode file, captions, logs and `build/voices/voice_log.json`,
   and push.

## Get better every day

Every run fixes the "next improvement" from yesterday's quality-log row
before anything else (a pacing issue, a clearer chip, a new sound cue, a
sharper hook), measures it, and names the next one. Pietro's notes on a Reel
outrank the metrics.

## Never

- Clone any real person. Use HEART unless Pietro names another voice.
- Put recordings, decrypted samples or keys in the repo.
- Add a whoosh, or any music we do not hold the rights to. A scored alternative uses only our own score.
- Post or schedule a Reel: Pietro posts by hand.
