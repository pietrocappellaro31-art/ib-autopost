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
3 to 6 beats; each beat is one or two spoken sentences.

**Visuals on everything (Pietro, 8 Nov: "as much visuals as possible";
quality only goes up).** The reference is the style of the earlier videos
(Lehman's Last Weekend, 100% Is the Only Standard): a drawn scene for every
moment. Rules:
- Give each sentence its own visual with `shows=[...]` (one per sentence).
- Most beats use a hand-drawn scene from `build/sketch.py` (`kind="sketch"`,
  a drawing that draws itself beside the line, or `kind="scene"`, the drawing
  alone): clock, calendar, bricks, dominoes, chart, bars, figures (with
  magnifying glasses), document with a stamp, tower (cracked), bank, seesaw,
  scale, coins, flow, phone, magnifier, ship, book, speech bubble, bulb,
  globe, arrows, house with a price tag, pie, tulip. Add a new scene to
  `sketch.py` when the story needs one (that is a good daily improvement).
- Mix in the other kinds for rhythm: icon, icons, split, timeline, flow,
  verdict (claim plus MYTH/TRUE stamp), quote, number, compare, list.
- No more than one text-only beat per chapter. Every chapter card gets an
  `art=` drawing.
- Thumbnail: `thumb=dict(art=..., big=..., big_a=..., small=...)` gives two
  options, `thumbnail_a.jpg` (red, with the drawing) and `thumbnail_b.jpg`
  (paper, big type), for YouTube's Test & compare.

Aim for 8 to 12 minutes; vary the scenes and structure so no two videos look
alike. Render: `python3 build/youtube_ep<NNN>.py`. Outputs in
`build/out/<slug>/`: the MP4 (-14 LUFS, sound effects, original music bed), two
thumbnails, `<slug>.srt` captions, `metadata.json`, `description.txt` with
chapter times. Look at a contact sheet of frames before delivering: if it
looks plainer than the last video, it is not done.

## 4. Short (9:16)

Set `music=True` in the Short's EP so it carries the music bed.

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
- **Music on every YouTube video (Pietro, 8 Nov), and always our own**: `build/music.py`
  synthesises an upbeat track per video in the style that trends (four-chord pop loop,
  kick, clap, hats, pluck, bass), ducked under the voice. Never a real song, however
  viral: Content ID would claim the video's revenue. Shorts: `music=True` in the EP.
  Instagram Reels stay without music (Pietro adds it in the app).
- No third-party footage, logos or photos of real
  people. Fonts, sounds and visuals are ours (see `docs/rights/ledger.md`).
- Not "made for kids".
- Rights block in `docs/rights/posts/<slug>.md`.

## 7. Deliver

Send with SendUserFile: the MP4, both thumbnails, the `.srt` and `description.txt`. In the
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
