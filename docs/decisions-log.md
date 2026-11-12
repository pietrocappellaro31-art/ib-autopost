# Decisions log

What has been settled, and what is still open. Newest first.

## Current state, 2 November 2026

- **Meta has blocked the app's API access.** Every workflow run since the first
  successful publish fails with `API access blocked` (OAuthException 200), and
  the developer dashboard redirects to a block page: *"Conferma dell'account
  necessaria. Abbiamo notato attività insolite su questo account sviluppatore."*
  Pietro has to complete identity confirmation to restore access. Likely
  trigger: a brand-new developer account minting a system user token and
  publishing through the API from a cloud IP within hours.
- **One post is live.** `w1-01-statements` published 31 Oct 02:15 UTC, fifteen
  minutes after its slot. The pipeline itself is proven.
- **Thirteen posts are queued**, re-spaced two a day from 3 November so that
  the first successful run after the block lifts does not publish six at once.

## Settled

- **Pietro's music library for YouTube** (12 Nov, Pietro: "Create a skill that will attach all these
  audios to a library ... used for the creation of both YouTube shorts and YouTube video. The video
  should pick from the library the most appropriate music."; on the rights question: "Find a way
  around - we just want to use the music, not their videos."). The 8 songs he sent (Einaudi's
  Experience, Flawed Mangoes' Swimming and Missing Pieces, GOTH, Luminary, the Bloody Mary slowed
  instrumental, Ethereal slowed, the September instrumental loop) are commercial recordings, so the
  lawful way around is: never in our file, never in git, never edited to dodge Content ID. Each one
  is analysed (`build/music_library.py`; `library.json` committed, audio gitignored) and every video
  picks the song closest to its `mood`. A Short gets the song first in the music block, added with
  "Add sound" in the YouTube app (licensed for Shorts) from its calmest stretch. A long video gets our
  own `music.py` bed written in the song's tempo, key, mode and feel (no melody, chords or audio
  taken). A song with a real licence on record can be set to `rights=licence` and mixed in. Skill:
  `docs/skill/music-library/SKILL.md`; the YouTube skill points to it.
- **No "That's level 4. Keep score." on any video** (12 Nov, Pietro: "'That's level 4, keep score' is
  useless and should be removed from all videos." Then: "Keep it in mind for tomorrow."). From the
  13 Nov runs, every Levels hook (Reels and YouTube Shorts) says and shows the last question alone;
  the close still asks for the score. On a Short the hook drawing sits centred under the question
  and larger (about 600 px wide; `levels.py` centres it when the hook has no lines). Today's Short
  (shorts-cent-doubled-30-days) was delivered with the old hook and is not re-rendered.
- **Reel hooks are the question alone** (11 Nov, Pietro: "From now on eliminate from all reels
  'That's level 4, keep score'. This part is not needed."). The Levels hook says and shows only the
  last question (plus the small "4 interview questions. Each one harder." line); the close still asks
  for the score. Applied to Levels #10 before delivery (53.9 s, was 56.1). Extended to YouTube Shorts
  on 12 Nov (above).
- **Six viral reference Reels to study** (11 Nov, Pietro): one proposal per reference over the next
  days, modelled on their design, music and structure more than their plot. Links and status in
  `docs/daily/viral-references.md`. Instagram blocks automated fetching, so the study needs the
  videos (screen recordings or downloads) from Pietro. Videos received and studied the same day;
  six proposals and a build order written in that file. **Approved by Pietro (11 Nov: "I approve
  your proposal")**: from 12 Nov each daily Reel run builds the next proposal in order, with the
  day's rotation voice (none for the R2 loop), until all six are done; then Pietro picks what stays.

- **3 carousels a day, built and queued weekly** (10 Nov, Pietro: "post three
  times a day from now on", then "increase from 2 a day to 3 a day" and "build
  and queue now"). Slots 08:00, 12:30 and 17:30 ET; the hand-posted Reel at
  21:30 ET is on top, so the feed carries 4 posts a day plus the Story.
  `publish.py` cap raised to 3 with a 17:30 default slot. A third Claude
  scheduled task at 17:33 ET could not be created from the 10 Nov session
  (permission denied); until it exists, the 17:30 carousel goes out on the
  GitHub cron (runs every 10 minutes 22:00 to 23:59 UTC) or, at the latest,
  with the 18:03 ET Story dispatch. Why it was needed:
  the week-1 queue ended on 8 Nov and the monthly plan that was meant to start
  on 9 Nov was never built (the planning task only runs on the first Monday),
  so 9 Nov had no carousel. To stop that recurring, a weekly scheduled task
  that builds and queues the next 7 days every Thursday is proposed; it could
  not be created on 10 Nov (permission denied) and needs Pietro's go-ahead.
  First batch: `build/nov1.py`, 10 to 16 Nov. Cover rotation restarted at
  day 1 on 10 Nov for the three carousel slots. The live bio still says "Two
  questions a day"; Pietro to change it by hand.

- **Monthly planning session: first Monday of each month, 9:00 ET** (set 2 Nov,
  replacing the weekly session). Claude proposes the month's topics, slots,
  times and cover colours, asks personalisation questions, then builds and
  queues the month after approval. Runbook: `docs/skill/ib-month-plan`. A
  scheduled run starts 8:35 ET so the draft is ready at 9:00. Each plan runs
  to the Sunday after the next first Monday, a one-week buffer.
- **Carousels are triggered by Claude scheduled tasks** (2 Nov) at 08:03 and
  12:33 ET daily, because GitHub's own cron started only about 20 runs in
  three and a half days. The tasks call workflow_dispatch, which GitHub labels
  "Manually run"; that label does not mean a person did it. The GitHub cron
  stays on as a backup. Fully independent option still open: an external
  cron service with a fine-grained token.
- **Comment replies are fully automatic** (2 Nov). A daily job in the private
  repo `ib-comments` drafts every reply with Claude and sends it, technical
  ones included. Coaching and collab questions get a standard reply pointing
  to DMs and are listed in a weekly report issue. Risk controls instead of a
  human check: one run a day, a reply cap that ramps 10 then 20 then 30 a day,
  random pauses between replies, skips spam and emoji-only, stops on any
  rate-limit or block error.
- **Reels are scheduled by Pietro in the Instagram app** with trending audio,
  from files and a schedule delivered at the monthly session. The Planned tab
  route was re-asked on 2 Nov and is still not possible.
- **Week-1 queue kept** (option A, 2 Nov): it runs 3 to 8 Nov and the monthly
  plan starts 9 Nov.
- **Voiceover is back** (6 Nov, Pietro's call, reversing 30 Oct). Kokoro-82M,
  voice `af_heart` (warm, confident, kind), run locally by `build/voice.py`
  with misaki's own pronunciation dictionaries; unknown words fail loudly and
  get hand-written phonemes. Mixed to -16 LUFS, -1.5 dB true peak, so music
  added in the app sits under it. **Every voiced Reel must carry Instagram's
  AI label**: Meta requires it for realistic AI voiceovers.
- **Sound effects are the standard on every Reel** (6 Nov, Pietro's call,
  after Levels #1). Synthesised in `build/sfx.py` (no licensing), mixed under
  the voice and under the music Pietro adds. Reels without voice now ship
  with an effects track rather than silent. Same day: the whoosh on swipes is
  retired (Pietro found it annoying, the only one), and more effects are
  welcome: pops when a level number, chip or score lands, ticks when the
  meter fills and the score spins, a soft ding on the brand. Levels #1, its
  cloned-voice cut and #2 were remixed without it (`levels.remix`).
- **Voice cloning: Pietro's own voice only** (6 Nov). Cloning a real
  person's voice is possible here (Kyutai Pocket TTS run locally through
  sherpa-onnx, about 20 to 30 seconds of clean reference audio; weights CC BY
  4.0, credit Kyutai). Its terms forbid cloning anyone without their explicit
  consent, so cloning a public figure (the JPMorgan CEO was asked about) is
  ruled out: it would be impersonation. Pietro's own voice, or someone who
  has explicitly agreed, is fine. Until a recording arrives, Reels use `af_heart`.
  Checked 6 Nov against Kyutai's own model card (huggingface.co/kyutai/pocket-tts):
  licence CC BY 4.0, which allows commercial use with credit; prohibited uses
  include cloning without explicit and lawful consent and presenting generated
  audio as a genuine recording, so the AI label stays on. Tested on Kyutai's
  sample voice: a take can drop or add a word, so `voice_clone.py` transcribes
  every line (`voice_check.py`) and retakes it until the words match, and the
  reference must be cut at a pause (`prepare_reference`). When a cloned-voice Reel ships, its
  caption ends with the credit "Voice model: Pocket TTS by Kyutai".
  First clone from Pietro's own recordings (6 Nov, two memos, 55 s and 25 s,
  quiet room, no clipping). Measured with a speaker-ID model (WeSpeaker, in
  `voice_check.similarity`): two real recordings of Pietro score 0.89, a
  different voice about 0.5, the clone 0.74 to 0.83, so it reads as him.
  Reference length made no difference (11 s, 22 s and 47 s references all
  averaged 0.74 to 0.75), so longer recordings do not help this model; the
  delivery and recording conditions of the sample are what it copies. The
  transcript check uses Parakeet (6% word error on Pietro's real voice, where
  Moonshine tiny misheard him), and every line is spoken after a throwaway
  "Okay." that is cut, because the model swallowed first words. Sentence
  timings for a cloned voice come from the recogniser's word times (a real
  voice's pauses are too irregular for Kokoro's pause matching). Levels #1
  in the clone: 13 of 13 lines word-perfect, 21 of 22 caption onsets within
  0.15 s, likeness 0.82 against a held-out real recording.
  Refined 6 Nov with three longer memos (about 4.5 minutes, seven delivery
  styles). `voice_refsearch.py` cut them into 12 windows of 14 to 20 s,
  cloned the same lines from each and scored them against real speech from
  the other memos (real against real across memos: 0.92). Best: the quiz-host
  window from the first new memo (0.785 likeness over 8 takes and the
  fewest slipped words; one story window scored 0.80 but slipped more), against 0.71
  for the first memo's sample on the same test), now the reference for quiz
  formats. Levels #2 is the first Reel voiced with it. Pietro's recordings
  and references stay out of this public repo.
- **Pietro's real voice is now a third option** (6 Nov). He reads a Reel's
  script in one memo; `voice_real.py` transcribes it with word timings,
  aligns the script, cuts each passage, shortens pauses over 0.45 s to 0.3 s
  and hands the passages to the Reel engine (`real:/path/to/memo`). No AI
  label needed. Measured on the same 34 held-out clips of his real speech:
  real-voice Levels #2 0.914 and #3 0.901, the cloned Levels #2 0.867, the
  first clone 0.794, the stock Kokoro voice 0.551. A second reference
  search over 13 memos (34 windows) found nothing meaningfully better than
  the last one (0.794 against 0.784, within take-to-take noise of about
  0.04): the clone has plateaued, and only the real recording closes the gap.
  The real reads run longer (Levels #2 71 s against 62 s cloned) because
  Pietro speaks more slowly than the clone.
- **Every Reel is voiced in Pietro's clone, alternating two voices** (7 Nov,
  Pietro's call): L2 (the Levels #2 voice) and L3 (the Levels #3 voice), one
  then the other, to test which goes more viral; a named voice overrides the
  rotation. The record is `build/voices/voice_log.json`. The procedure is the
  `ib-voiced-reel` skill (copy in `docs/skill/ib-voiced-reel/SKILL.md`).
  Clarity: both clones were duller than his real recordings (less presence
  above 4 kHz, more mud at 150 to 500 Hz); each now gets an EQ curve matched
  to his real voice (tone gap 2.8 to 1.2 dB for L2, 2.2 to 1.3 dB for L3,
  likeness unchanged), a light de-esser and gentle compression. The two
  samples are encrypted in `build/voices/`; the key is in the claude.ai
  Project (`claude/voice-samples-key.md`), and `build/setup_voice.sh` sets up
  a fresh session.
- **Captions are burned in, word by word**, on every voiced Reel, because most
  people watch muted.
- **Reel style: kinetic typography on paper** (3 Nov), modelled on a
  reference Reel Pietro chose. The standard is `docs/reel-style.md`; every
  Reel from now on follows it.
- **One automated Story a day: question of the day** (3 Nov), 18:00 ET.
  Each story answers yesterday's question and asks today's, so the chain
  gives people a reason to come back. Rendered by `build/stories.py` (questions
  and worked answers live there), queued in `posts.json` as `type: story`,
  published by `publish.py` outside the two-carousel daily cap. The API cannot
  add polls, links or other stickers, so the image carries everything. The
  monthly plan includes a story per day, and the chain must never end on an
  unanswered question.
- **Highlights are manual** (3 Nov): the API cannot manage them. Three, in
  this order: Start here (red), Question of the day (ink), Dates (paper,
  recruiting timeline). Covers are in brand; Pietro adds each daily story to
  Question of the day with one tap, or weekly from the Archive.
- **Every post gets an engagement question in the comments** (3 Nov).
  Carousels: `first_comment` in `posts.json`; `publish.py` posts it as the
  page's own comment right after publishing, and records `first_comment_id`
  (or `first_comment_error`, never failing the run). Needs
  `instagram_manage_comments` on the token. Reels: the question is delivered
  with each Reel for Pietro to post when he uploads. Questions are specific to
  the post and answerable in a line, never "comment YES" bait.
- **Cover colours rotate, palette does not** (2 Nov). Slide 1's ground follows
  a diagonal rotation of red, ink and paper so the grid is not one colour.
  Chosen over rows or columns because no evidence ties grid layout to reach,
  and a diagonal stays mixed when a post is late or missing.
- **Daily cap enforced in code** (2 Nov). `publish.py` publishes at most 2
  manifest posts per Eastern day, and no more than the slots already passed
  that day (the day's scheduled times plus 08:00 and 12:30 ET). Backlog after
  an outage drains two a day, oldest first, at slot times, instead of going out
  in one run. The third daily post is the hand-uploaded Reel, which never goes
  in the manifest. Hard caps: 2 posts on Mon 2 Nov, 3 a day from Tue 3 Nov.
- **Cadence: 3 posts a day.** Was 2 a day, raised on 2 Nov. The researched
  recommendation was 7 to 8 a week with Reels for reach; Pietro chose volume.
  Flagged twice, decided twice, no longer an open question.
- **Carousels are automated, Reels are manual.** The Content Publishing API has
  no draft or scheduled state, and the Business Suite composer has no
  `input[type=file]` to target, so nothing can be placed in Instagram's Planned
  tab. Pietro uploads the Reels himself and adds a trending track, which the
  API cannot do and which matters more on that format than anything else.
- **Synthetic voiceover rejected** (30 Oct). A neural TTS voice was built and
  the quality was not acceptable. Reels now ship silent and read-paced.
- **Follow/unfollow growth abandoned** on terms-of-use and ban risk.
- **AI label** only for realistic generated imagery, not for designed graphics.
- **Faceless, brand-only.** Not tied to Pietro personally.
- **Visual identity:** palette G, fonts A. See `brand-system.md`.
- **Format and fonts stay identical across the whole account.** Standing
  instruction.
- **Co-founder and partner:** Emanuele Sesia. Pietro wants the page on his
  LinkedIn as co-founder, and a LinkedIn company page first.

## Open

- **Posting times are hypotheses, not findings.** 08:00 and 12:30 Eastern for
  carousels, 21:30 for Reels, reasoned from how each format is ranked rather
  than measured on this account. Re-time from the account's own insights after
  two or three weeks.
- **Distribution reality check.** The account had 2 followers when 21 posts a
  week were scheduled. Carousels reach existing followers; Reels reach
  non-followers. If the manual Reel session slips, the carousels are mostly
  talking to an empty room.
- **Collabs are the strongest untried lever.** A Collab post lands on both
  grids and reaches both audiences. Candidates: other prep accounts of similar
  size, university finance societies, student investment clubs.
- **Alt text** is not settable through the publishing API. Add in-app on the
  posts that matter.
- **Experiment: a woman's voice made from Pietro's own** (7 Nov, Pietro's
  request, awaiting his pick). `build/voice_feminise.py` raises the formants
  (spectral envelope warp) and the pitch of one of his samples, and Pocket TTS
  clones the result, keeping his delivery. No real woman's voice is used, so
  there is nobody else's consent to get; the AI label still applies. Three
  candidates were put in a lineup: A calm (about 182 Hz, the clearest, 4% word
  errors over 8 takes), B bright (215 Hz, 10%), C warm (202 Hz, 9%); his male
  clone runs about 11%. A full Levels #3 in voice A: 14 of 14 lines
  word-perfect, pitch 154 to 210 Hz by passage. A feminised voice can drift
  back towards a male pitch in some takes, so `CloneVoice(min_pitch=...)`
  retakes any take below the floor.
  Pietro's verdict (7 Nov): not there yet; one sounded Indian, the Reel was
  too fast with an "h" breath before words, and not clear enough. Measured on
  the same three lines (6 takes each): voices made from his voice slipped 22
  to 28% of words; the same clone engine given a clean synthetic woman's
  sample (Kokoro af_heart, Apache 2.0, the voice he liked on 6 Nov) slipped
  3%. The clone also spoke at 3.0 to 3.4 words a second against his own 1.9
  to 2.3. New voices F1 (af_heart sample) and F2 (af_heart and af_bella
  blend): 16 flow steps instead of 8, every take slowed to 0.76 with
  rubberband (pitch and tone kept), a pitch floor, and a presence EQ matched
  to the clean sample. Levels #3 in F1: 14 of 14 lines word-perfect, 13 on the
  first take, pitch 170 to 192 Hz throughout, 2.6 words a second. Trade-off:
  F1 and F2 are no longer made from Pietro's voice, and nobody real is
  cloned. Awaiting his pick; L2 and L3 stay the rotation until then.
- **A third clone of Pietro, L4, from five new memos** (7 Nov, about 7.5
  minutes, read in a quieter setting: noise floor -75 to -84 dB against about
  -60 before). The new memos sound different from the earlier ones (likeness
  between them about 0.80 against 0.90 among the earlier ones), so every
  sample was judged against both sets. 21 windows searched; L4 is the 21 to
  41 s window of the first new memo. Levels #4 voiced in L4: 14 of 14 lines
  word-perfect; likeness 0.86 to the new memos and 0.83 to the earlier ones,
  where L2 and L3 score about 0.86 to the earlier memos and 0.79 to 0.81 to
  the new. Tested on the same lines, L4 slipped fewer words than L2 and L3.
  L4 also gets 16 quality steps, a pace matched to Pietro's (every take
  slowed to 0.82; he reads at about 2.3 words a second, the raw clone at
  about 3) and its own tone match. Not in the L2/L3 rotation until Pietro
  says so.
- **One default voice, and a female voice on request** (8 Nov, Pietro). P1, cloned from
  Pietro's own read of the Levels #1 script (levels-1-pietro-voice.mp4, first 20.6 s), is
  the voice of every Reel and YouTube video from now on; the L2/L3 alternation ends
  (`next_voice()` returns P1). F3, cloned from the Levels #1 Reel voice (levels-1.mp4, the
  synthetic Kokoro af_heart voice, nobody real), is used only when Pietro asks for a female
  voice. Both run at 16 quality steps with a tone match measured against the original
  recording; F3 is also slowed to 0.84 (the raw clone read 4.1 words a second against 3.5)
  with a pitch floor of 165 Hz. P1 is encrypted like L2 to L4; F3 is synthetic, kept plain.
- **"The voice is no good" (8 Nov), measured.** DNSMOS (Microsoft's speech
  quality model, 1 to 5) on whole tracks: Pietro's first memos 3.3; the L2
  and L3 Reels 3.33 and 3.26; Levels #4 and #5 in L4 2.84 and 2.80; F1 2.74;
  the stock Kokoro voices 3.27 to 3.54. Two causes: the five 7 Nov memos score
  low themselves (3.02 and 2.83, consistent with phone noise reduction), and
  slowing takes with rubberband costs quality. P1's sample comes from a clone,
  not a raw recording. Free voices from the web are only usable when no real
  person is cloned, so the licence-clean pool is Kokoro's own voices (Apache
  2.0); eight were auditioned (`voice-audition.mp4`), all 0 to 3% word errors,
  DNSMOS 3.27 to 3.54. Rights recorded in `docs/rights/ledger.md`.
- **Reels rotate three voices for a month; YouTube is GEORGE; daily automation** (8 Nov,
  Pietro). From the 8 Nov auditions: Reels alternate, one per Reel and in this order, G2
  ("E, slower": Kokoro bm_george read at 0.82, re-spoken by Pocket TTS, 8 exact takes per
  line, the most consistent kept), BELLA (Kokoro af_bella, bright and warm, US) and EMMA
  (Kokoro bf_emma, British, calm), for one month; then Pietro picks one from the results.
  `next_voice()` runs the rotation from `build/voices/voice_log.json`. YouTube long-form and
  Shorts always use GEORGE (Kokoro bm_george, British, measured). All four are synthetic;
  no key is needed. P1 and F3 end as defaults. Three scheduled tasks now make the content
  every day, posting stays manual: YouTube long video and YouTube Short (6:35 and 6:40am New
  York, ready by 7) and the IG Reel (8:16am, ready by about 8:30). Each delivers in its own
  task thread, logs to `docs/daily/`, and starts from the previous run's "next improvement"
  in `docs/daily/quality-log.md`. New long-form engine: `build/youtube.py` (1920x1080,
  chapters, captions, sound effects, -14 LUFS, thumbnail, description with chapter times).
  YouTube rule checked 8 Nov: an AI voice that does not imitate a real person needs no label
  on its own, and the label does not affect earnings; we tick "altered or synthetic" anyway.
  The monetisation risk is "inauthentic content" (mass-produced, template-identical), so
  every video carries original, sourced analysis and varies in structure and visuals.
- **YouTube visuals: a drawing on every beat** (8 Nov, Pietro: "the visuals were much
  better in the other YouTube videos ... quality should go up, not down, and the videos
  should include as much visuals as possible"). The first `youtube.py` test was text-led.
  The engine now draws a hand-made scene for most sentences (`build/sketch.py`: clocks,
  bricks, dominoes, charts, figures, stamped documents, towers and more, drawn on in time
  with the voice), keeps the icon, timeline, flow, stamp and quote layouts, opens each
  chapter on a red card with a drawing, and outputs two thumbnails and an .srt, like the
  Lehman and 100% videos.
- **Music on every YouTube video, made by us** (8 Nov, Pietro: "always put some viral
  music in the background"). Trending songs are copyrighted and would be claimed by Content
  ID (revenue to the rights holder, or blocked), so `build/music.py` makes an original
  track for each video in the trending style (vi-IV-I-V loop, four-on-the-floor kick,
  clap, off-beat hats, pluck arpeggio, bass, sidechain pump, 96 to 118 BPM; the seed
  varies key, tempo and pattern). It drops out at chapter cards and is ducked under the
  voice; mixed at -14 LUFS. Long-form always; Shorts with `music=True`. Instagram Reels
  are unchanged: no music in the file, Pietro adds it in the app.
- **YouTube music is piano and cello, dramatic; Shorts get pictures and colour** (10 Nov,
  Pietro on the first Short: "The music is terrible, we are not at a lunapark. We prefer
  piano or cello. Something more dramatic. Also, make the video more engaging with
  pictures and colors and more animated"). `music.track()` now writes a slow minor-key
  piece (66 to 80 BPM, piano ostinato with left-hand octaves, a cello line in its low
  register from bar 3, a soft low drum every fourth bar, hall reverb), synthesised from
  scratch like before; the pop style is retired (`track_pop()`, re-renders only). Sample
  libraries were not an option in the build environment, so the instruments are modelled
  (additive piano with stretched, decaying partials; bowed cello with body resonances and
  late vibrato). Voice sits about 16 dB over the bed while speaking at the default level.
  Shorts now carry a colour ground per part, a drawing in each level's answer zone, coins
  drifting at the edges and an animated close (`levels.py`: `bg`, `art`, `art_after`,
  `floaters`; `sketch.py`: coin, pricetag, receipt, card_tap, lineup, last_coin;
  `motion.py`: coinflip). Instagram Reels keep the paper ground and no music unless
  Pietro says otherwise.
- **The penny Short is the standard; viral music only through YouTube's library** (10 Nov,
  Pietro: "The quality of the video is much better - that is what we are gonna use as
  standard from now on. For the music, try to find the most viral ones and use it. This
  was even too dramatic."). Every Short matches or beats `shorts_penny-one-year.py`
  (colour grounds, drawings, motion). Viral songs are copyrighted, so they never go in our
  file: Shorts ship with voice and effects only and each run suggests two or three sounds
  trending on Shorts that week, which Pietro adds with "Add sound" in the YouTube app at
  upload (licensed for Shorts). Long-form keeps an original bed, lighter than the 10 Nov
  piano and cello (warm, mid tempo, not dramatic), or an Audio Library track Pietro adds.
  Pietro agreed (10 Nov): he adds the music in the YouTube app himself; every Short
  delivery gives him clear step-by-step music instructions (template in the
  youtube-videos-creator skill, section 7).
- **Long-form music is the warm bed; drawings fill their boxes** (10 Nov, YouTube #3). Following Pietro's
  note that the piano and cello was "even too dramatic", `music.track()` now writes a warm, mid-tempo,
  major-key bed (soft electric piano, pad, round bass, soft kick, rim and shaker, sparse bell; 88 to 100
  BPM), ducked under the voice (20.1 dB below it while speaking on #3). The piano and cello is kept as
  `track_drama()` for re-renders. `youtube.py` now zooms each drawing onto what is drawn (`fitSketches`),
  puts a drawing on thumbnail B, checks the 16:9 layout during the render (`layout.json`) and writes
  `sound.json` (voice over music, DNSMOS, loudness) on every render. Waiting on Pietro's view of the new bed.
- **Where the AI label and the music are (10 Nov, Pietro: "I cannot find how to add the AI
  label and music").** The phone upload flow may not show the AI question; it is set in
  YouTube Studio on a computer after upload (Content, Shorts, the Short, Show more,
  "Altered content", or Attributes, "AI use", in newer Studio). The sound button is on the
  Shorts editor screen reached with "Next" after the trim screen; YouTube Help says library
  audio on uploaded videos is limited to 15 second clips. The music template in the
  youtube-videos-creator skill now says both.
- **Source links in every YouTube description; tags go in Studio, hashtags in the description** (10 Nov,
  Pietro: "since my channel is verified, make sure to add links to the sources and references").
  Episodes list `sources=[(label, url)]`; `youtube.describe()` writes a "Sources and references" list
  with links, the chapters, the disclosure lines and the episode's `hashtags` (2 or 3). The `tags` list
  is for the Tags field in Studio (Details, Show more), pasted by Pietro; `redescribe(ep)` rewrites
  description.txt without a re-render. Applied to YouTube #3 the same day.
- **YouTube voice trial: a different voice every day** (10 Nov, Pietro: "From now on for the
  YouTube videos you will experiment with different voices. A different one each day, until
  we find the perfect one. All the other rules stay the same. Starting tomorrow."). From 11
  Nov the day's long video and Short share one voice from `voice_clone.youtube_voice()`, in
  the `youtube_trial` order in `build/voices/voices.json`: 14 Kokoro voices (Apache 2.0)
  auditioned on 10 Nov, US and British, male and female, each set to about GEORGE's pace. The
  Reel voices stay out of it. The list repeats until Pietro picks; then `YOUTUBE_PICK` is set
  and the trial ends. Each delivery names the voice and asks for his verdict; the log is
  `docs/daily/youtube-voice-trial.md`. GEORGE is the baseline. Everything else is unchanged.
