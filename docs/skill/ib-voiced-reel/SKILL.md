---
name: "ib-voiced-reel"
description: "Make every Instagram Reel for @investmentbankinginterviews voiced: the voice rotates G2, BELLA, EMMA (one per Reel, a one-month test from 8 Nov), with sound effects, voice and quality checks, caption, comment question and the daily quality log. YouTube videos run their own daily voice trial (see youtube-videos-creator)."
---

# Voiced Reels for @investmentbankinginterviews

## The voice rule (from 8 Nov, a one-month test)

Reels rotate three voices, one per Reel, in this order. After a month Pietro
picks the winner from the results, so the rotation must stay strict:

| Name | What it is | Engine |
|---|---|---|
| **G2** | "E, slower": Kokoro bm_george read slowly, re-spoken by Pocket TTS, 8 exact takes per line, the most consistent kept | Pocket TTS (CC BY 4.0) |
| **BELLA** | Kokoro af_bella, bright and warm, US | Kokoro (Apache 2.0) |
| **EMMA** | Kokoro bf_emma, British, calm | Kokoro (Apache 2.0) |

1. `voice_clone.next_voice()` returns the next one in the rotation (it reads
   `build/voices/voice_log.json`). Use it. Do not pick by taste.
2. If Pietro names a voice for a Reel, use that one; it still counts in the
   log.
3. **YouTube (long-form and Shorts) runs its own trial from 11 Nov**: a different
   Kokoro voice each day (`voice_clone.youtube_voice()`), never the Reel voices.
   Never in the Reel rotation.
4. All four are synthetic voices, not a real person. Never clone anyone.
   Older voices (P1, L2 to L4, F1 to F3) are kept only to re-render old Reels.
5. Say in every delivery which voice was used.

## Before making anything

Read `docs/brand-system.md`, `docs/decisions-log.md`, `docs/reel-style.md`,
`docs/daily/quality-log.md` (the last row's "next improvement" is today's
job) and `docs/daily/topics.md` in the ib-autopost repo.

## Setup, once per new session

From the repo root:
`bash build/setup_voice.sh && source ~/voice-tools/env.sh`
It downloads Kokoro, Pocket TTS, the speech recogniser, the speaker model and
the DNSMOS quality model (about 1 GB, a few minutes). No key is needed for
G2, BELLA, EMMA or GEORGE. Never print or commit a key if one is around.

## Make the Reel

1. **Format**: the Levels quiz by default (`build/levels.py`; copy the latest
   `build/reels_levels<N>.py`). Pick a topic not in `docs/daily/topics.md`
   "Used" for Reels; IB interview technicals first.
2. **Write the episode file** `build/reels_<slug>.py`. Work every answer in
   its docstring. Never invent a number, statistic or credential. No em
   dashes. Spoken text uses words for numbers; on-screen text uses digits.
   Each hook is one sentence in one `say` entry.
3. **New words**: the voice stops on a word it cannot pronounce. Add it to
   `PHONEMES` in `build/voice.py` (plurals, -ed and -ing are worked out from
   the stem automatically).
4. **Render**: `python3 build/reels_<slug>.py <VOICE>` with the name from
   `next_voice()`. Kokoro voices take a few minutes, G2 about 30 to 45.
5. **Layout problems** ("SAFE-AREA PROBLEMS"): smaller type (`qsize`,
   `bigsize`) or a shorter chip, then
   `make(EP, "<VOICE>", keep_voice=True)` so the voice stays the same. A
   wrong line: `make(EP, "<VOICE>", keep_voice=True, redo=["a2"])`.

## Checks before delivering

- `build/out/<slug>/takes.json`: every line `"wer": 0` (heard word for word).
- Quality: `python3 -c "import quality; print(quality.score('build/out/<slug>/<slug>.mp4'))"`
  (DNSMOS overall; about 3.1 to 3.5 is studio-clean).
- Loudness about -16 LUFS, true peak no higher than -1.5 dB
  (`ffmpeg -i <mp4> -af ebur128=peak=true -f null -`).
- Look at frames: the cover, each level settled, the transitions.

## Sound

Sound effects on every Reel (`build/sfx.py`): ticks, pops, dings, thump. The
more the better. **Never a whoosh on the swipe between scenes.** No music:
Pietro adds it in the app.

## Compliance

Run the content-compliance gate. Write `docs/rights/posts/<slug>.md`.

## Deliver

1. Send the MP4 and the cover with SendUserFile.
2. Caption: PASS on ig-human, one ask, up to 4 hashtags, then just before the
   hashtags: `Narration: AI-generated voice; script is our original work.`
   and, for G2 only, `Voice model: Pocket TTS by Kyutai`.
3. Comment question: a bonus level.
4. Paste the description and the comment question in the reply, ready to
   copy.
5. Remind Pietro to turn on Instagram's AI label when he posts.
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

- Clone any real person. Use only the four voices above.
- Put recordings, decrypted samples or keys in the repo.
- Add a whoosh, or music.
