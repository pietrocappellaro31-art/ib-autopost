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
- **Voice cloning: Pietro's own voice only** (6 Nov). Cloning a real
  person's voice is possible here (Kyutai Pocket TTS run locally through
  sherpa-onnx, about 20 to 30 seconds of clean reference audio; weights CC BY
  4.0, credit Kyutai). Its terms forbid cloning anyone without their explicit
  consent, so cloning a public figure (the JPMorgan CEO was asked about) is
  ruled out: it would be impersonation. Pietro's own voice, or someone who
  has explicitly agreed, is fine. Until a recording arrives, Reels use `af_heart`.
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
