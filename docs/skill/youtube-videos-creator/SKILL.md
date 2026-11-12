---
name: "youtube-videos-creator"
description: "Daily YouTube run for the finance channel: research a topic that could travel, write and render one long-form 16:9 video and one Short in the day's trial voice, with thumbnail, title, description, chapters and tags, checked against YouTube's AI and monetisation rules. Posting stays manual."
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

**A different voice every day, until Pietro picks one** (Pietro, 10 Nov: "experiment with
different voices. A different one each day, until we find the perfect one"; from 11 Nov).
Today's voice, the same for the day's long video and Short:

    python3 -c "import sys; sys.path.insert(0,'build'); from voice_clone import youtube_voice; print(youtube_voice())"

The order is `youtube_trial` in `build/voices/voices.json` (14 Kokoro voices, Apache 2.0,
auditioned 10 Nov; the Reel voices BELLA, EMMA and G2 are left out so the channels stay
distinct). It goes round again when the list ends. `youtube.make` uses it by default; render
a Short with `python3 build/shorts_<slug>.py <VOICE>`. In every delivery say which voice it
was and ask Pietro for a one-line verdict; log the voice and the measures in
`docs/daily/youtube-voice-trial.md`. When he picks one, set `YOUTUBE_PICK` in
`build/voice_clone.py` and the trial ends. GEORGE (every video to 10 Nov) is the baseline.
Every voice is synthetic, not a person. The narrator has no name, face or invented
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
  description. **Every source in the description carries its link** (Pietro, 10 Nov: "since my
  channel is verified, make sure to add links to the sources and references"): put them in the
  episode as `sources=[(label, url), ...]` (only URLs actually opened or returned by a search in the
  run), with `source_note=` for anything that is our own illustration; the engine writes the
  "Sources and references" list. **Never invent a number, statistic, quote or credential.** If
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

Check the length and every word before the long render: `python3 build/yt_timing.py build/youtube_ep<NNN>.py --takes` (12 Nov: `--takes`
transcribes each line once, cached, and writes takes.json; the render does the same and a final second loudness stage brings the master to about -14 LUFS) (11 Nov;
the voice is cached per line in `synth.pkl`, so the render reuses it and a one-line edit re-says only that line).
Aim for 8 to 12 minutes; vary the scenes and structure so no two videos look
alike. Render: `python3 build/youtube_ep<NNN>.py`. Outputs in
`build/out/<slug>/`: the MP4 (-14 LUFS, sound effects, a light original music bed), two
thumbnails, `<slug>.srt` captions, `metadata.json`, `description.txt` with
chapter times. Look at a contact sheet of frames before delivering: if it
looks plainer than the last video, it is not done.

## 4. Short (9:16)

**Shorts ship without music in the file** (`music=False`, the default): Pietro adds a
trending sound in the YouTube app when he uploads (see section 6, Music).

A four-level quiz with the Levels engine (`build/levels.py`, copy the latest
`build/reels_levels<N>.py` to `build/shorts_<slug>.py`), rendered with
the day's trial voice, under 60 seconds, on a finance topic for a general audience. Or a
single sharp idea from the long-form, said in its own words (not a cut of the
same file). Title under 70 characters with #Shorts in the description.

**Pictures, colour and motion on every Short (Pietro, 10 Nov: "make the video more
engaging with pictures and colors and more animated"; after seeing it: "much better,
that is what we are gonna use as standard from now on").** The penny Short,
`build/shorts_penny-one-year.py`, is the minimum standard: every Short matches or beats
it. Copy its structure:
- a colour ground per part (`bg=` on the hook, each level and the close), cross-faded
  at the swipes;
- a drawing in each level's empty answer zone while the question is read and the clock
  runs (`art=`, with `ans_min` about 520), fading as the answer lands; `art_after=` for a
  small picture beside the answer; `art=` on the hook sits beside "That's level 4";
- `floaters=` (faint shapes drifting at the edges) and `art=` on the close (coins falling
  in under the score);
- drawings from `build/sketch.py`, sized for 9:16 with `picture(name, t0, dur, w=650)`;
  add a new scene for the topic when none fits (coins, receipt, card and terminal, price
  tag, coin line-up and a stamped last coin exist; for buy now, pay later: shopping bag,
  price tag split in four, payment timeline, credit report, interest stack).
- the master is two-stage at -14 LUFS (12 Nov, `levels.two_stage`): it lands within 0.2 LU of the
  target, where the single loudnorm stopped at -14.6 to -15.2; a label like "Last one." is said on
  its own, and the last level can show the hook's question without reading it again (`("", text)`).
Keep the safe area clear (the render lists any problem) and look at a contact sheet.

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
- **Music (Pietro, 10 Nov: "try to find the most viral ones and use it"; the piano and
  cello bed was "even too dramatic").** Viral songs are copyrighted, so they never go into
  our file (Content ID would claim the video, and the compliance gate treats it as STOP).
  The way to use them is YouTube's own licensed library:
  - **Shorts**: the MP4 has voice and sound effects only (`music=False`). Each run
    searches the web for the sounds trending on YouTube Shorts that week and suggests two
    or three in the delivery, with the mood that fits the video. Pietro picks one with
    "Add sound" in the YouTube app at upload (licensed for Shorts) and keeps it low under
    the voice. If a suggested song is not in the app's library, he picks another from it.
    Pietro confirmed this way (10 Nov) and asked for **clear instructions every time**:
    every Short delivery ends with the block below, filled in for that video.
  - **Long-form**: popular songs cannot be added to long videos without a claim. Use our
    own bed from `build/music.py` (`track()`, the warm bed since 10 Nov, YouTube #3), lighter than the 10 Nov piano and cello: warm, mid
    tempo, not dramatic, low under the voice; or a YouTube Audio Library track Pietro adds
    in Studio (log any attribution). Never a commercial song in the master.
  - Instagram Reels stay without music (Pietro adds it in the app).
- No third-party footage, logos or photos of real
  people. Fonts, sounds and visuals are ours (see `docs/rights/ledger.md`).
- Not "made for kids".
- Rights block in `docs/rights/posts/<slug>.md`.

## 7. Deliver

**Music instructions, in every Short delivery** (Pietro, 10 Nov: "make sure to give me
clear instructions each time"). Fill in the songs and the times; keep the steps:

```
Music for this Short (add it in the YouTube app on your phone)
Suggested sounds, trending on Shorts this week:
  1. <song - artist>: <why it fits, one line>
  2. <song - artist>: <...>
  3. <song - artist>: <...>
Steps:
  1. Open the YouTube app, tap +, then "Upload a video", and pick <slug>.mp4.
  2. In the Shorts editor tap "Add sound" (the music note), search the first song.
     If it is not there, try the next; if none is, pick any song the app offers that
     fits <mood>.
  3. Choose the part of the song to use: start it on <a calm or instrumental stretch>,
     not on a vocal chorus, so it does not fight the voice.
  4. Tap "Volume": keep "Original sound" at 100 and set the added track to about 15 to 25,
     then play the first 10 seconds. The voice must be easy to follow; lower the track if not.
     If you see no sound button: you went past the editor. After picking the file, the
     trim screen must get "Next" (not "Add details"); the sound button is on the editor
     screen that follows. Songs from the app's library may be cut to a short clip
     (YouTube Help says 15 seconds for uploaded videos): place it on the hook.
  5. Tap Next, paste the title and description, set "No, it's not made for kids", and upload.
  6. AI label (the phone app may not show it): on a computer open studio.youtube.com,
     Content, the Shorts tab, click the Short, "Show more", and under "Altered content"
     (newer Studio: Attributes, "AI use") answer Yes. Save.
The app's labels can differ slightly between versions; the order stays the same.
```

For a long video, when Pietro wants to swap our bed for an Audio Library track, give the
Studio steps: YouTube Studio, Content, the video, Editor, Audio, pick the track, set it
low under the voice, Save. Only Audio Library tracks there (log any attribution).

**Tags and hashtags are different things.** `tags=` is the list for the **Tags** field in
YouTube Studio (Content, the video, Details, Show more, Tags; 500 characters at most, the engine
checks it); give it to Pietro as one comma-separated line (`tags_for_studio` in metadata.json).
`hashtags=` (two or three, no spaces) are written by the engine at the end of the description, so
Pietro does nothing extra for them.

Send with SendUserFile: the MP4, both thumbnails, the `.srt` and `description.txt`. In the
reply paste the title, the description (with chapters), the tags, and the
pinned-comment question, plus the Studio settings to tick and, for a Short, the
two or three trending sounds to try in the app. Add a row to the
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
