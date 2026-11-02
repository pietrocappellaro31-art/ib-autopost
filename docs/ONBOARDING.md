# Onboarding a new Claude account to this page

Read this first. It tells you what to read, in what order, and what to do in
your first session.

## What exists, and where

The page is **@investmentbankinginterviews**: faceless, brand-only, investment
banking interview prep. Carousels publish themselves from this repository
through GitHub Actions. Reels are handed to Pietro as files, because the
publishing API cannot attach trending audio.

**None of the machinery depends on a Claude account.** GitHub runs the cron,
Meta runs the API, and both kept working across a weekend with no session
open. Changing Claude accounts changes nothing about publishing.

## Reading order

1. **`docs/brand-system.md`** — the visual and editorial contract. It encodes
   several failures that are invisible until they ship. Read it before making
   anything, every time.
2. **`docs/decisions-log.md`** — what is settled, what has been tested and
   ruled out, and what is still open. Read it before proposing anything, or
   you will propose something already rejected for a good reason.
3. **`docs/automation-plan.md`** — how publishing works and which facts are
   verified rather than assumed.
4. **`docs/week-1-schedule.md`** — the slots and the reasoning behind them.
5. **`docs/account-setup-checklist.md`** — one-time Instagram settings.
6. **`docs/skill-pack-review.md`** — the instagram-agent pack, and which of its
   13 skills to use.

The two skills, `ib-page` and `ib-autopost`, are in `docs/skill/`. Upload both.
`ib-page` is the editorial runbook; `ib-autopost` is the machinery and the
failure diagnosis list.

## The transcript

A full transcript of the build is supplied separately as `transcript.md`, with
a second copy that keeps tool output. It is **deliberately not in this public
repository**: a transcript is a record, not documentation, and this repo is
public because Meta has to fetch images from it.

Read the transcript for *why*, not *what*. The docs already carry every
decision; the transcript carries the arguments, the dead ends and the
corrections that produced them. The parts worth your time:

- Where a proposal was refused and why, so you do not re-propose it.
- The failures and how they were found. Most of what is valuable here was
  learned by something breaking.
- How Pietro pushes back, and which pushbacks were right. At least twice he
  was right and the earlier position was wrong.

The transcript opens with a summary of the sessions before 30 October, which
no longer exist as logs. From 30 October onward it is verbatim.

## How Pietro works

- He states a decision and expects it carried out in that turn, not discussed.
- He corrects in short cues and expects the fix applied everywhere at once.
- Quality over speed. No filler, no redundancy, no restating his question.
- **Never invent a number, statistic, credential or outcome.** Flag uncertainty
  instead. This is a standing instruction and it has teeth on a page that
  teaches technical answers.
- If genuinely in doubt, ask rather than assume.

He will also, reasonably, push for things that are not possible. Three have
already been tested to destruction: posting through Instagram's consumer
interface, automating the Business Suite file picker, and placing Reels in
Instagram's Planned tab. Each is documented with the evidence. Say so plainly
rather than attempting them again.

## Your first session

1. Attach and clone the repo, then read the files above.
2. Check the pipeline is actually alive: open the Actions tab and look at run
   **status**, not just run times. Twenty green runs and twenty red ones look
   identical in a list of timestamps, which is how the account went dark for
   two and a half days without anyone noticing.
3. Check `posts.json` for anything overdue. If posts have stacked up, re-space
   them before restoring publishing, or the first successful run ships all of
   them into one scroll.
4. Ask Pietro for the thing nobody has pinned down: **a recurring day and time
   for the weekly approval session.** It has been asked for repeatedly and is
   still unset, and without it the weekly cycle has no trigger.

## Current state, as of 2 November 2026

- **Meta has blocked API access.** The developer account is in an identity
  checkpoint and only Pietro can clear it. Nothing publishes until he does.
- One post is live. Thirteen are queued, re-spaced two a day from 3 November.
- Seven Reels are built and sitting on Pietro's Mac awaiting his upload.
- Cadence is three a day, chosen by Pietro against a recommendation of seven
  to eight a week. The counter-argument is in the decisions log; it was made
  twice and settled. Do not relitigate it unprompted.
