# Long-form YouTube standard: cinematic finance documentaries

Pietro, 13 Nov 2026. Applies to **long-form YouTube videos only** (not Shorts, not Instagram). It overrides any
older rule in `docs/skill/youtube-videos-creator/SKILL.md`, a synced skill or a scheduled-task prompt where they
conflict. If Pietro later changes a rule explicitly, his newer instruction wins and gets recorded in
`docs/decisions-log.md`.

The companion files:

- `cinematic-standard.md`: animation, scene variety, what the engine can do today, and what to build next
- `audio-standard.md`: narrator, the clean and scored mixes, the score, sound effects
- `quality-gates.md`: the checks a film has to pass before delivery

## Mission

Make original, accurate, educational finance documentaries for a general adult audience: a fully produced
animated film, not a slideshow. The channel is independent. It uses the IB editorial identity
(`docs/brand-system.md`) and nothing from any other channel, brand or fictional universe.

## Every run, in order

1. Read `docs/brand-system.md`, `docs/decisions-log.md`, the four `docs/production/` files,
   `docs/daily/README.md`, `quality-log.md`, `topics.md`, `youtube-long.md`, `youtube-voice-trial.md` (closed,
   history), `youtube-shorts.md`, the YouTube skill, content-compliance, music-library and ig-human.
2. **Yesterday's "Next improvement"** for YouTube long in `quality-log.md` is the first job. Build it, measure it,
   and say what it changed. A cosmetic change does not count as an improvement.
3. Pick the topic, then research it.
4. Write the screenplay and the visual plan (`build/plans/ep<NNN>.md`, see below) **before** rendering.
5. Write `build/youtube_ep<NNN>.py`, run `python3 build/yt_timing.py build/youtube_ep<NNN>.py --takes`, fix the
   misses, then render.
6. Pass every gate in `quality-gates.md`.
7. Deliver, log, commit, push (`git pull --rebase` first: the Short run writes the same logs). Never commit MP4s,
   recordings, credentials or keys. Never overwrite a released episode's output.

## Topic

Categories: financial history, market bubbles, banking crises, behavioural finance, investment banking, private
equity, financial modelling, money and wealth, business strategy, economic history, corporate finance, scandals,
decision-making, careers in finance.

A good topic has a surprising central question, a story, clear things to show, credible sources, and appeal beyond
finance people. Not in `topics.md` "Used" within 60 days. Not the same as the day's Short, and not an Instagram
Reel subject without a reason. Trending is not a reason on its own: it has to make a good film.

## Research

Source order: original documents, company filings, central-bank material, academic research, credible financial
press, historical primary sources, institutional data. Every material claim has a source in the episode docstring
and a link in the description. Only URLs actually opened or returned by a search in the run.

Keep these four apart, in the script and on screen:

- **documented fact**
- **widely repeated but uncertain anecdote** (say so: "is supposed to have said", "attributed")
- **interpretation** (ours: "our reading")
- **illustrative reconstruction** (a stylised scene or a made-up example, labelled as such)

Never invent a price, date, profit, percentage, quote or event. Check every calculation independently (a short
script, not by eye). Charts keep true units and honest scales, no truncated axis for drama; approximate data is
labelled approximate.

## Length

8 to 12 minutes: as long as the explanation needs, no padding, no cutting a complex topic short.

## Story structure

1. **Hook**, first 5 to 15 seconds: a factual surprise, a question, a visual contradiction. No branded intro.
2. **Context**: the people, institutions, dates and money involved, only as much as needed.
3. **Mechanism**: how the financial process actually works, shown (charts, transactions, models). This is the
   central teaching job.
4. **Escalation**: complications, incentives, the unexpected.
5. **Turning point**: the decision, event or insight.
6. **Analysis**: why it happened; evidence separated from opinion; a misconception challenged where it fits.
7. **Conclusion**: a real takeaway, no motivational filler. The viewer should leave understanding something new.

## Screenplay

Natural, confident, plain English; a story, not a list of facts. Few rhetorical questions, no exaggeration, no
em dashes, spoken numbers that sound natural. The narrator never claims to have lived through anything or worked
anywhere, and has no invented credentials.

## Visual plan (before rendering)

`build/plans/ep<NNN>.md`, one row per beat: narration, teaching objective, scene family (see
`cinematic-standard.md`), assets, what moves and how, camera, data shown and its source, sound effects, score mood,
expected seconds. A beat solved by a title card or a still drawing needs a reason.

## Deliverables

Per film, in `build/out/<slug>/`: the scored MP4 (the recommendation when it passes the audio gate), the clean MP4,
thumbnails A and B, the English `.srt`, `transcript.txt`, `description.txt`, `metadata.json`, `sound.json`
(quality figures), a motion-preview sheet, the rights record `docs/rights/posts/<slug>.md`, and a quality report
(the quality-log row plus the gate results in the delivery message).

Video: 1920 x 1080, 16:9, H.264, AAC, 24 fps. Audio about -14 LUFS integrated, true peak at or under -1 dBTP.

## Metadata

Five title candidates and one recommended title; the full description with real chapter times, "Sources and
references" with links, the source and rights note, the music line, the AI-narration line and the
not-financial-advice line; 2 or 3 hashtags; Studio tags (500 characters at most); a pinned-comment question; the
AI-disclosure recommendation with its reason (`quality-gates.md`). Never an invented URL, a credential or a
promised return. Title and description must score PASS on ig-human.

## Final message to Pietro

The title, the full description, the chapters, the tags, the hashtags, the pinned comment, the voice, the music
(scored or clean, and the credit line), the Studio settings, a source summary, the quality results, today's
verified improvement, and anything that needs his review. Files go by SendUserFile: the scored MP4, the clean MP4,
both thumbnails, the SRT, description.txt, the motion-preview sheet and the rights record. Nothing is posted or
uploaded: Pietro uploads.

## Logs

`docs/daily/youtube-long.md`, `topics.md` ("Used"), `quality-log.md` (run "YouTube long": measures, the
improvement, the next one), the rights record, and the narrator's measures in the quality-log row (`youtube-voice-trial.md` is closed,
kept as history).

## The aim

Each film more engaging to watch, better researched, more cinematic, better animated, better narrated, better
mixed, more educational, more original. These do not trade against each other: a beautiful film that teaches a
wrong fact fails, and a correct film that looks like an eight-minute slideshow fails too.
