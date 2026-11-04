---
name: ib-month-plan
description: Run the monthly planning session for @investmentbankinginterviews on the first Monday of each month - health check, personalisation questions, the month's topics, slots, times and cover colours, then build and queue it after Pietro approves. Use for the monthly session or when asked to plan the month.
---

# ib-month-plan

Once a month, first Monday, 9:00 ET. A scheduled run starts at 8:35 ET so the
draft is ready when Pietro sits down. This session decides the whole month;
everything after it runs on its own.

Claude is the creative lead. Propose, do not wait to be told: topics, order,
times, cover colours, Collab candidates. Then ask what only Pietro and
Emanuele can answer.

## 0. Read first, every time

In the `ib-autopost` repo (attach with push access, clone once):
`docs/brand-system.md`, `docs/decisions-log.md`, `docs/week-1-schedule.md`,
and the previous `docs/plans/*.md`. The decisions log outranks this file. Do
not re-propose anything it lists as settled or ruled out, including the
cadence of three posts a day.

## 1. Health check before planning

Run status, not run count. Twenty green runs and twenty red ones look alike.

```
gh run list -R pietrocappellaro31-art/ib-autopost -L 30 \
  --json conclusion,event,createdAt
```

- Any failure since the last session: read its log
  (`gh run view <id> --log`) and report the cause in one line.
- Overdue unpublished entries in `posts.json`: the daily cap in
  `publish.py` drains them two a day at slot times, so do not re-space by
  hand unless Pietro asks.
- Selftest if anything failed: `gh api -X POST
  repos/pietrocappellaro31-art/ib-autopost/actions/workflows/publish.yml/dispatches
  -f ref=main -f 'inputs[mode]=selftest'`. `gh workflow run` fails here
  (GraphQL is blocked); the REST call works.

Report health in three lines at most, then move on.

## 2. Window

Plan from the day after the last queued post through the **Sunday after the
next first Monday**. That keeps one week of buffer, so the session day itself
is covered and a missed session never leaves the page dark.

## 3. Personalisation questions

Ask up to four with AskUserQuestion, each standing on its own. Pick the ones
that matter this month; never ask what the docs already answer. Candidates:

- What happened in recruiting this month that the page should speak to
  (superday season, a deadline, a bank in the news)?
- Any topic they want, or want to stop?
- Insights: which posts did best and worst? Ask them to paste the numbers.
  The account's own data beats every general rule here. If they paste
  insights, use `ig-audit` on them.
- A Collab target they already know, or approval of the one proposed.
- Holidays or exam periods to plan around.

If no one answers within the session, take the most reasonable reading, say
which at the top of the plan, and still stop before scheduling.

## 4. The proposal

### Cadence and slots (Eastern)

| Slot | Format | Published by |
|---|---|---|
| 08:00 | Carousel | cron |
| 12:30 | Carousel | cron |
| 21:30 | Reel | Pietro, by hand with trending audio |

Hard caps: 3 posts per Eastern day, of which at most 2 come from the manifest.
Never put a Reel in the manifest. Friday is the weakest evening for this
audience; say so if a Friday Reel matters, and offer midday.

The times are hypotheses until the account's insights say otherwise. When
insights exist, re-time from them and say what changed and why. Never present
a reasoned time as a measured one.

### Topics

- Every post is a question with an answer, because the bio promises it.
- Mix per week, roughly: 9 technical, 3 recruiting, 2 built to pull comments.
- Carousels take deep technicals that need a diagram. Reels take punchy,
  list-shaped and recruiting topics.
- No repeats of anything in previous plans or `posts.json`. Build arcs: a
  question named in one post gets its own post later.
- Dated recruiting claims (deadlines, application windows) must be checked
  with a web search in the session and cited in the plan. Never invent a
  number, statistic, credential or outcome.

### Cover colours: diagonal rotation

The palette never changes (red `#D93A12`, ink `#0A0A0A`, paper `#F7F5F2`,
teal accents). Only the first slide's ground rotates so the grid is not one
colour. The grid is three wide and each day posts three, so each day is one
grid row:

| Day in cycle | 08:00 | 12:30 | 21:30 Reel |
|---|---|---|---|
| 1 | Red | Ink | Paper |
| 2 | Ink | Paper | Red |
| 3 | Paper | Red | Ink |

Then repeat. No two neighbours share a colour across or down, every row mixes
all three, and one late or missing post leaves the rows mixed, unlike bands
or columns. Continue the cycle from where last month ended (record the next
day number in the plan file).

Rendering notes:
- Covers are set per deck: `d.slide(RED, WHITE, accent=WHITE, ...)`. Ink
  cover: `d.slide(INK, WHITE, accent=RED, ...)`. Paper cover:
  `d.slide(PAPER, INK, accent=RED, ...)`. Check the `cover()` helper's text
  colour against the ground before rendering a whole month.
- Slide 2 must not match the cover's ground. Keep the CTA red unless the
  cover is red, then use ink.
- The grid shows a 3:4 crop of slide 1, shaving about 34px each side. The
  76/80px padding already clears it; keep cover text inside it.
- Reel cover colour is the first frame's ground. Tell Pietro to set the cover
  to the first frame.

### Output

1. A table in the reply, one line per post:
   `Mon 09 Nov  08:00  CAROUSEL  Red   Technical of the Day  <question>`
2. Collab candidate of the month and a one-line pitch.
3. What changed from last month and why, in three lines at most.
4. Publish the same plan as one artifact page so it can be read on a phone.

Then stop. Nothing is built or scheduled without Pietro's yes.

## 5. After approval: build and queue

Build in weekly batches and push each batch, so a session cut short still
leaves complete weeks queued.

1. Carousels: `build/carousels.py` patterns, `build/brand.py` primitives,
   cover colour from the rotation. Every technical answer worked through.
2. Captions through `ig-human`, PASS only. Every post also gets a
   `first_comment`: one specific question about that post, answerable in a
   line, no em dashes, never bait. Reels deliver theirs as a file for Pietro.
   Caption traps: digits not words, "20
   times" not "20x", re-check burstiness after edits. No em dashes.
3. `build/schedule.py <slug> <scheduled_utc>`. UTC: Eastern is UTC-5 from the
   first Sunday of November and UTC-4 from the second Sunday of March. Convert
   each date individually; never assume one offset across a DST change.
4. Stories: one per day at 18:00 ET in `build/stories.py` (question plus a
   worked answer). Each day's story answers the previous day's question, so
   the last story of the window must still be answered by the next plan.
   Queue them as `type: story` entries.
5. Reels: `build/reels_motion.py` in the style in `docs/reel-style.md`
   (kinetic typography, paper theme). Older `build/reel.py`, silent, read-paced, 1080x1920. Deliver to
   Pietro's Mac in `Downloads/IB <Month> Reels/` if the computer is linked,
   otherwise send them. Filenames carry the correct slot date. Include each
   caption and a `SCHEDULE.md`.
5. Verify before the final push: at most 2 manifest posts per Eastern day, no
   Reel in the manifest, every image path exists, slide 1 colours follow the
   rotation, `raw.githubusercontent.com` serves one new image.
6. Write `docs/plans/<yyyy-mm>.md` (the table, the questions and answers, the
   next rotation day) and add any new decision to `docs/decisions-log.md`.

## Close

One short message: what is queued (count, first and last date), what Pietro
must do (the Reels, with the folder), and anything that failed. No recap.
