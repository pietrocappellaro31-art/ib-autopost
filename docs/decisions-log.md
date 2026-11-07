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
