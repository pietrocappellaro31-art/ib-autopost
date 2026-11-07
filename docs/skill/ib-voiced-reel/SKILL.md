---
name: ib-voiced-reel
description: Make every Reel for @investmentbankinginterviews voiced in Pietro's cloned voice, alternating the L2 and L3 voices, with sound effects, voice checks, caption and comment question.
---

# Voiced Reels for @investmentbankinginterviews

Every Reel is voiced in Pietro's cloned voice. There are exactly two approved
voices:

- **L2**: the voice of Levels #2.
- **L3**: the voice of Levels #3.

## The voice rule

1. **Alternate L2 and L3.** One Reel L2, the next L3, and so on. To see which
   is next, run from `build/`:
   `python3 -c "import voice_clone; print(voice_clone.next_voice())"`.
   The record is `build/voices/voice_log.json`; it updates itself when a
   Reel renders.
2. **If Pietro names a voice** ("use L2", "use the level 3 voice"), use that
   one instead.
3. **Only these two voices.** Not the stock voice, not anyone else's voice.
4. Why: an A/B test of which voice goes more viral. Keep the log accurate
   and say in every delivery which voice the Reel used.

## Before making anything

Read `docs/brand-system.md`, `docs/decisions-log.md` and `docs/reel-style.md`.

## Setup, once per new session

1. Read the Project doc `claude/voice-samples-key.md` (Projects tool,
   `project_read`) to get the key.
2. From the repo root run
   `VOICE_KEY=<key> bash build/setup_voice.sh && source ~/voice-tools/env.sh`.
   It downloads the voice model and the speech recogniser (about 0.7 GB) and
   decrypts the two voice samples. Never print, paste or commit the key.

## Make the Reel

1. **Format**: the Levels quiz by default (`build/levels.py`; copy
   `build/reels_levels2.py` or `build/reels_levels3.py`). Other formats take
   the same voice names.
2. **Write the episode file** `build/reels_<slug>.py`. Work every answer in
   its docstring. Never invent a number, statistic or credential. No em
   dashes. Spoken text uses words for numbers ("twenty five percent"); the
   on-screen text uses digits ("25%").
3. **Render**: `python3 build/reels_<slug>.py clone:L2` (or `clone:L3`). About
   10 to 12 minutes.
4. **Layout problems** ("SAFE-AREA PROBLEMS" in the output): make the type
   smaller (`qsize`, `bigsize`) or shorten the chip, then re-render only the
   visuals with `make(EP, "clone:L2", keep_voice=True)`, so the voice takes
   stay the same.

## Make sure the voice is clear

Check all of these before delivering:

- `build/out/<slug>/takes.json`: every line has `"wer": 0`, meaning the
  speech recogniser heard exactly the script. If a line is not 0, render
  again (each take is different) or reword that line.
- Loudness about -16 LUFS and true peak no higher than -1.5 dB:
  `ffmpeg -i build/out/<slug>/<slug>.mp4 -af ebur128=peak=true -f null -`.
- The voice's EQ (in `build/voices/voices.json`) is applied automatically. It
  makes the clone as bright and clear as Pietro's real recordings. Do not
  remove it.
- Look at frames: the cover, each level settled, and the transitions.

## Sound

Sound effects on every Reel (`build/sfx.py`): ticks, pops, dings, thump. The
more the better. **Never a whoosh on the swipe between scenes**: Pietro finds
it annoying.

## Deliver

1. Send the MP4 and the cover with SendUserFile.
2. Caption: PASS on ig-human, one ask, up to 4 hashtags, and this line just
   before the hashtags: `Voice model: Pocket TTS by Kyutai` (the voice
   model's licence requires the credit).
3. Comment question: a bonus level.
4. Paste the description and the comment question in the reply, ready to
   copy.
5. Remind Pietro to turn on Instagram's AI label when he posts.
6. Say which voice (L2 or L3) the Reel used.
7. Commit the episode file, the captions and `build/voices/voice_log.json`,
   and push.

## Never

- Clone anyone but Pietro (a public figure's voice is ruled out).
- Put Pietro's recordings, the decrypted samples or the key in the repo.
