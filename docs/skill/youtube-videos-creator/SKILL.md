---
name: "youtube-videos-creator"
description: "Daily YouTube run for the finance channel: research a topic that could travel, write and render one long-form 16:9 video and one Short voiced by GEORGE, with thumbnail, title, description, chapters and tags, checked against YouTube's AI and monetisation rules. Posting stays manual."
---

# YouTube Videos Creator

Runs every day at 7am New York as two scheduled tasks (long-form and Shorts),
or when Pietro asks for a YouTube video. Everything is automated except
posting: Pietro uploads.

## Before making anything

In the ib-autopost repo read `docs/brand-system.md`, `docs/decisions-log.md`,
`docs/daily/quality-log.md` (yesterday's "next improvement" is today's first
job), `docs/daily/topics.md` and the last rows of `docs/daily/youtube-long.md`
or `docs/daily/youtube-shorts.md`.

Setup: `bash build/setup_voice.sh && source ~/voice-tools/env.sh` from the
repo root.

## Voice

Always **GEORGE** (Kokoro bm_george, British, measured; Apache 2.0). It is a
synthetic voice, not a person. The narrator has no name, face or invented
life story: never "when I worked at a bank".

## 1. Pick the topic

Vary across: history of finance, politics and finance, how money is made,
challenges and stories (living a day on one euro), technical explainers
(DCF, LBO, IPO pricing), banking careers, and anything else in finance that
people share. Look for what is getting attention now: search the web for
recent news, anniversaries and questions people are asking, and prefer a
surprising angle ("the famous bubble that mostly never happened") over a
textbook title. Not in `topics.md` "Used" within 60 days. Long-form and
Short on different topics the same day.

## 2. Research and write

- Every fact has a source, listed in the episode docstring and in the
  description. **Never invent a number, statistic, quote or credential.** If
  a number cannot be sourced, say it without the number.
- Write the script as original analysis with a point of view: what the
  common story gets wrong, why it matters, what to take from it. That is
  what keeps the channel monetisable (YouTube's inauthentic-content policy
  excludes mass-produced, template-identical videos).
- No em dashes. Spoken numbers in words; on-screen numbers in digits.
- Educational, not financial advice. No "buy this".

## 3. Long-form (16:9)

Copy `build/youtube_ep001.py` to `build/youtube_ep<NNN>.py`. Chapters of
3 to 6 beats; each beat is one or two spoken sentences and one visual:
`statement`, `number`, `list`, `compare` or `term`. Aim for 8 to 12 minutes
once the format is proven; vary the visual kinds so no two videos look
alike. Render: `python3 build/youtube_ep<NNN>.py`. Outputs in
`build/out/<slug>/`: the MP4 (-14 LUFS, sound effects, no music),
`thumbnail.jpg` (1280x720), `metadata.json`, `description.txt` with chapter
times.

## 4. Short (9:16)

A four-level quiz with the Levels engine (`build/levels.py`, copy the latest
`build/reels_levels<N>.py` to `build/shorts_<slug>.py`), rendered with
`GEORGE`, under 60 seconds, on a finance topic for a general audience. Or a
single sharp idea from the long-form, said in its own words (not a cut of the
same file). Title under 70 characters with #Shorts in the description.

## 5. Checks

- Every line the recogniser checks is word for word (`takes.json` where
  written), DNSMOS via `build/quality.py`, loudness, and frames looked at:
  the thumbnail, every chapter card, two beats per chapter.
- No layout overflow, no text off the frame.

## 6. YouTube AI and monetisation compliance

Run the content-compliance gate, then:
- **Altered or synthetic content**: tick "Yes" in YouTube Studio for every
  video with the AI voice (no effect on earnings; removes any doubt).
  `metadata.json` carries the reminder.
- Description ends with `Narration: AI-generated voice; script and analysis
  are our original work.` and the not-financial-advice line (added by the
  engine).
- No music in the master. No third-party footage, logos or photos of real
  people. Fonts, sounds and visuals are ours (see `docs/rights/ledger.md`).
- Not "made for kids".
- Rights block in `docs/rights/posts/<slug>.md`.

## 7. Deliver

Send with SendUserFile: the MP4, the thumbnail and `description.txt`. In the
reply paste the title, the description (with chapters), the tags, and the
pinned-comment question, plus the Studio settings to tick. Add a row to the
log, the topic to `topics.md` "Used", the measures and one improvement to
`quality-log.md`. Commit the episode file and logs (not the MP4) and push.

## Get better every day

Each run starts with yesterday's "next improvement" (a new visual kind,
tighter pacing, a better thumbnail, a stronger first 15 seconds), measures
it, and names the next one. Pietro's notes outrank the metrics.

## Never

- Clone or imitate a real person's voice or face.
- Use music, footage or images we have no rights to.
- Post or schedule on YouTube: Pietro uploads.
