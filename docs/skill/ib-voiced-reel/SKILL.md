---
name: "ib-voiced-reel"
description: "Make and queue ONE fully animated Instagram Reel a day for @investmentbankinginterviews (from 27 Nov 2026): the whole frame is a filmed world made with build/reel_film.py (no card, no picture in a picture, no blur), story first, the HEART narrator (Kokoro af_heart, 0.9), action-timed effects, a trending licensed track attached by Instagram at posting through the Audio API, some Reels as Trial Reels, posted automatically at 18:00 ET with the AI label, caption, comment question and the daily quality log."
---

# Voiced Reels for @investmentbankinginterviews

## FIRST: the 27 Nov standard (Pietro, 26 Nov) wins over everything below

Read `docs/production/reel-film-standard.md` and follow it. In short: ONE Reel a day at 18:00 ET (slot B); the whole
frame is the animated world (`build/reel_film.py`, copy `build/reelf_depreciation.py`); no card, panel, black ground or
blur; a person with something at stake, the wrong answer struck out, the mechanism shown as it is said, the payoff in one
number, the question back; voice and effects only in the MP4 (one clean master, no score); the music is a trending
licensed track Instagram attaches at posting (`publish.py --audio` through the workflow's audio mode, then
`reel_queue.py ... --audio-id <id> --audio-title "<title - artist>"`); about two Trial Reels a week (`--trial`, never two
days running); Pietro hides the like and share counts in the app, so the delivery message names the posting time. Where a
section below says two or three Reels a day, slots A or C, Formats A to F on cards, the black ground, the scored master
or `entry_check.py`, it is history.

Version 2026-11-16 (black background from 17 Nov; cinematic upgrade; Pietro's 14 Nov notes: more animated, drawn scenes everywhere, a more natural voice, unprocessed). Authoritative copy: `docs/skill/ib-voiced-reel/SKILL.md` in the ib-autopost
repo; the installed plugin is built from it (`docs/production/skill-sync.md`).

**Standards (13 Nov 2026, Pietro: "Do the new standards apply to reels as well? They should."):** every Reel
follows `docs/production/cinematic-standard.md`, `audio-standard.md`, `quality-gates.md` (section 9 is the Reel
gate), the formats A to F of `short-form-standard.md` and `voice-decision.md`, exactly as Shorts and long videos do.
`docs/reel-style.md` stays the visual base (paper, kinetic type). The bar is the cinematic proof of concept
(`build/cine_poc_newton.py`; Pietro, 13 Nov: "exactly the quality we are looking for"). These win over this file
where they disagree, unless `docs/decisions-log.md` records a newer decision by Pietro. An older copy of this skill
that names the G2, BELLA, EMMA rotation, "no music in any file" or the Levels quiz as the only format is out of date.

## Pietro, 23 Nov: a call to follow on every Reel, and stronger hooks

"Make sure all the reels created from today on have a call to follow action. We want to improve conversion rate.
Also, we want stronger hooks. We want to go viral!" (`docs/decisions-log.md` 23 Nov).

**Follow ask, every Reel, three places.** (1) Spoken: the close's last line asks for it, e.g. "Answer in the
comments, and follow for tomorrow's." (`story.make` prints a CHECK otherwise). (2) On screen: the follow end card,
automatic on every -16 LUFS story-engine Reel (`story.FOLLOW_LINE`, `FOLLOW_HOLD`; `follow=False` only for a
re-render of an older Reel). The Levels engine has no card yet: use the story engine, or add the card to
`levels.py` first. (3) Caption: after the comment ask, "Follow @investmentbankinginterviews for a new IB interview
question, worked out, every day." (`reel_queue.py` refuses a caption without "Follow @investmentbankinginterviews").
Never "follow for more" (reflex bait in ig-human): say what a follower gets.

**Hooks, from 24 Nov.** The performance reading so far: short clash openings (two facts that seem to conflict,
question last) reach 1,100+; long set-ups stay under 1,000. Every hook now:
- shows the clash on screen from frame 0 (both numbers drawn and moving before the first word), so a scroller sees
  the conflict before the voice starts;
- puts a number in its first three words and stays at 13 words or fewer on screen, the question last and alone;
- is chosen from five candidates written from different formulas (the ig-reel skill's hook list: the clash, the
  wrong-answer reveal "It's not 10x", the you-stake "You have $100...", the trap "Most people divide by the wrong
  number" only if it is true by arithmetic, the challenge "Answer before the bar lands"); score each on clash, number
  early, second person, length and "would someone send this to a friend preparing for interviews", keep the
  candidates and scores in the episode docstring, and log the chosen type in the ig-reels row;
- never leans on an invented claim ("90% get this wrong", "asked at every bank") unless it is sourced.
Topics: pick for shareability (questions people get wrong with a surprising answer), near the families that did
best (equity and EV, cash, buyouts, bonds). Each run reads reach, shares and saves by hook type in
`docs/daily/performance.md` and keeps the types that win over at least three Reels.

## Pietro, 16 Nov: black background

"From tomorrow on - same exact format and quality but black background please." Then, the same evening: "Set this as
the rule from now on for both IG reels and YouTube shorts." Black is the default of `build/levels.py` and
`build/story.py` (THEMES; `theme="paper"` only re-renders older work); per-part colour grounds are ignored on black: black ground, light text on the ground, answers in bright
teal, white question cards unchanged, each level drawing on a paper panel, films unchanged. Same format, same quality
bar and gates. Check the frames on black: nothing ink-coloured may sit directly on the ground (an ink label outside a
panel or a card disappears). Older Reels keep the paper look; do not re-render them.

## Pietro, 14 Nov: more animated, drawn scenes everywhere, a more natural voice

From 15 Nov (`docs/decisions-log.md`): every beat carries a large drawn scene or a filmed `cine.py` shot through the question, the think time and the answer (never text alone, drawings at 85%+ of their box, at least two filmed beats); the drawings act the idea out; HEART stays, with a more natural delivery (whole passages synthesised together, natural pauses and emphasis, spoken-style script). Our own drawings only: no stock, licensed or AI images.

**Not processed (Pietro, 14 Nov evening: "robotic / processed sound" was what felt least natural):** the narrator chain
`voice.MASTER` is now a highpass and a 1.5 dB dip at 7.2 kHz only (no compressor, no echo, no pre-limiter); the
Reel master runs `levels.two_stage` at -16 LUFS with one true-peak limiter; stems are written with headroom. Every
render prints the SIG drop from voice to mix (gate 0.15 or less) and clipped voice samples (gate 0): a CHECK on
either is fixed before delivery. Do not add compression, reverb, echo, de-noise or an exciter to HEART.
`docs/production/audio-standard.md` 1b.

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
   from `build/cine.py` can be used in 9:16 (the world reframes with `cine.stage()`). **Pictures in every beat
   (Pietro, 14 Nov):** each level or beat has a large drawn scene (`art=`, `art_after=`) or a filmed window (`film=`,
   see `levels.film_window`) through the question, the think time and the answer; at least two filmed beats; the
   drawing acts the idea out (builds, moves, splits, counts) and fills 85% or more of its box. Our own drawings only. Pick a topic not in `docs/daily/topics.md`
   "Used" for Reels; IB interview technicals first.
2. **Write the episode file** `build/reels_<slug>.py`. Work every answer in
   its docstring. Never invent a number, statistic or credential. No em
   dashes. Spoken text uses words for numbers; on-screen text uses digits. Write it to be said: contractions, short
   sentences, how a person explains it out loud (Pietro, 14 Nov: "the voice should feel more natural").
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
  run, mean motion, logged; mean motion above the last Reel's, 1.62 on Levels #13) and a contact sheet of the hook, each level or beat, the transitions and the close. Cards with only a
  push-in fail.
- Facts and rights as for any film: every number worked in the docstring, reconstructions badged, props show only
  sourced figures.
- `build/out/<slug>/takes.json`: every line `"wer": 0` (heard word for word).
- Quality: `python3 -c "import quality; print(quality.score('build/out/<slug>/<slug>.mp4'))"`
  (DNSMOS overall; about 3.1 to 3.5 is studio-clean).
- Loudness about -16 LUFS, true peak no higher than -1.5 dB
  (`ffmpeg -i <mp4> -af ebur128=peak=true -f null -`).
- Look at frames: the cover, each level settled, the transitions. No frame of a level is text alone; the fit step
  reports every drawing at 85% or more of its box.
- Voice: listen-proxy checks for a natural read: whole passages synthesised together where the timings allow, pauses
  between sentences that vary, no line that sounds read out.

## Sound

Sound effects on every Reel (`build/sfx.py`): ticks, pops, dings, thump, and for filmed scenes footsteps, paper,
coins, quill, a soft mallet on numbers (`audio-standard.md` 5). Each effect belongs to something on screen.
**Never a whoosh on the swipe between scenes.**

Masters (`audio-standard.md` 3): every Reel gets the **clean master** (voice and effects, no music, about -16 LUFS,
true peak at or under -1.5 dBTP) and the **scored master**
(`python3 build/master.py scored build/out/<slug>/<slug>.mp4 -16 <mood> <mood>`: our own `build/score.py` score,
class ORIGINAL_GENERATED, ducked under the voice, word check against the clean file). Since 16 Nov Reels post
automatically with no in-app music, so the scored master is the one queued when it passes its checks; the clean one
is the fallback. Never a commercial or trending song in a file, and never a version carrying YouTube-library audio.

## Compliance

Run the content-compliance gate. Write `docs/rights/posts/<slug>.md`.

## Two Reels a day, posted automatically (Pietro, 16 Nov 2026)

**22 Nov (Pietro): three Reels a day for the week of 22 to 29 Nov** ("for this week we are going for three reels a
day, one carousel a day and one story a day"). Each daily run makes A, B and C on three different topics and queues
them at slots A 12:30, B 18:00 and C 21:00 ET (`reel_queue.py --slot C`). Everything below applies to each of the
three. If time or usage runs short, queue what passed and say what did not, rather than ship a weak Reel.

Pietro: "We will post two each day. You won't need my approval. You will use your own intelligence to analyze the
top performing reels and make improvements if necessary. You will decide at what time to post each day."

- **Each daily run makes two Reels**, A and B, on two different topics (and, across the week, different formats),
  each to the full standard. Make A first and queue it, then B. Never let the second be a weaker copy of the first:
  if time runs short, queue A and deliver B's state honestly rather than ship a rushed Reel.
- **Read the performance first**: `docs/daily/performance.md` (written by the publisher from Instagram's insights:
  reach, views, shares, saves, likes, comments, follows, watch time per Reel, and when followers are online). Name
  the best and worst Reels of the last two weeks, what differs (hook, format, topic, length, slot), and turn it into
  today's choices. Write the reasoning in the quality-log row. Do not chase one outlier: a pattern needs at least
  three Reels.
- **Posting times**: the slots are `reel_slots_et` in `posts.json` (from 16 Nov: A 12:30, B 18:00 ET, chosen because
  the 12:33 and 18:03 ET dispatches fire reliably while GitHub's own cron does not). Move a slot only on evidence
  from `performance.md` (online followers, reach by slot over at least 10 Reels), only to a time a reliable dispatch
  covers, and record the change and the reason in `docs/decisions-log.md`.
- **Music**: nobody adds Instagram music any more, so the posted file is the scored master
  (`python3 build/master.py scored build/out/<slug>/<slug>.mp4 -16 <mood> <mood>`), our own score, rights class
  ORIGINAL_GENERATED. If the scored master fails its checks, the clean master is posted.
- **Queue**: `python3 build/reel_queue.py <slug> --slot A|B --caption <caption file> --comment "<question>"` checks
  the file (H.264/AAC, 1080 x 1920, 3 to 90 s), makes the grid-safe cover (`build/reel_cover.py`, from the hook
  question; look at `cover_grid_preview.jpg`, the exact profile tile, before committing), the caption (at most 2,200 characters, at most 5 hashtags, the
  AI-narration line, no em dash), pushes the video and cover to a temporary branch `reel/<slug>` and adds the entry
  to `posts.json`. Commit `posts.json` and push (`git pull --rebase` first). The publisher posts at the slot, sets
  Instagram's AI label at creation (`is_ai_generated`), posts the comment question as the first comment, then deletes
  the branch.
- **No approval step** (Pietro's decision): the content-compliance gate is the gate. Any STOP item, a failed fact
  check, a word missed by the recogniser or a failed quality gate means the Reel is not queued; say why.
- **If the API is blocked** (`posts.json` has `api_block`, or the last publisher run says API BLOCKED): do not queue.
  Deliver both Reels to Pietro to post by hand as before (files, caption, comment question, the AI-label reminder),
  and say the block is still on.

## Deliver (one message after both Reels)

1. Caption for each: PASS on ig-human, the comment ask plus the follow line (23 Nov), up to 4 hashtags, no promise of returns or jobs, no invented
   experience, a title that matches the content, then just before the hashtags:
   `Narration: AI-generated voice; script is our original work.`
2. Comment question for each: a bonus level or a follow-up question.
3. Send both MP4s and covers with SendUserFile, for the record, then one SendUserMessage: for each Reel the topic,
   format, slot and posting time, which master was queued, the caption and comment, the measures (motion, DNSMOS,
   loudness, words heard), and what the performance data changed today. If a Reel was not queued, why.
4. Add rows to `docs/daily/ig-reels.md` (one per Reel: voice, format, slot), the topics to `docs/daily/topics.md`,
   and one row to `docs/daily/quality-log.md` with the measures, the performance reading, what improved and the next
   improvement.
5. Commit the episode files, captions, rights records, logs, `posts.json` and `build/voices/voice_log.json`, and push.

## Get better every day

Every run fixes the "next improvement" from yesterday's quality-log row
before anything else (a pacing issue, a clearer chip, a new sound cue, a
sharper hook), measures it, and names the next one. Pietro's notes on a Reel
outrank the metrics.

## Never

- Clone any real person. Use HEART unless Pietro names another voice.
- Put recordings, decrypted samples or keys in the repo.
- Add a whoosh, or any music we do not hold the rights to. A scored alternative uses only our own score.
- Queue a Reel that failed a gate, or queue anything while the API is blocked.
- Put an MP4 on main: Reel media goes only on its temporary `reel/<slug>` branch.
