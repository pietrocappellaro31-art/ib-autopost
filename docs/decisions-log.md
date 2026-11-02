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

- **The weekly approval session has no recurring day or time.** Asked
  repeatedly across the build and still unset. Until it exists, "approve ideas
  at the start of the week" has no slot and the following week cannot be
  scheduled without prompting.
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
