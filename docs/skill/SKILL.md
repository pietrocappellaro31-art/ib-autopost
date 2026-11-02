---
name: ib-page
description: Run the @investmentbankinginterviews Instagram page - plan a week, build carousels and Reels, lint captions, and schedule them through the ib-autopost repo. Use whenever the user asks about the Instagram page, a post, a carousel, a Reel, a caption, or the weekly approval session.
---

# Running @investmentbankinginterviews

A faceless Instagram page on investment banking interview prep. Carousels
publish themselves through GitHub Actions; Reels are uploaded by hand so a
trending track can be added.

**Read `docs/brand-system.md` in the `ib-autopost` repo before making anything.**
It is the visual and editorial contract and it encodes several failures that
are invisible until they ship.

## The weekly cycle

1. **Pietro approves ideas.** Present the week as a compact table: slot, format,
   topic. One line each. He scans it in under a minute.
2. **Build.** Carousels with `build/carousels.py` patterns and `build/brand.py`
   primitives. Reels with `build/reel.py`, silent and read-paced.
3. **Lint every caption** through `ig-human`. It must score **PASS** on the
   five-check panel. Never ship a REVIEW or a FLAGGED caption.
4. **Schedule** with `build/schedule.py <slug> <scheduled_utc>`, then commit and
   push. The cron does the rest.
5. **Hand the Reels over** as files with their slot in the filename and the
   caption beside them.

## Non-negotiables

- **Verify every technical answer before writing it.** Work the numbers
  through. Never invent a figure, a statistic, a credential or an outcome; use
  `{{placeholder}}` and say so.
- **No em dashes**, on slides or in captions.
- **JPEG only**, 1080x1350 for carousels, 1080x1920 for Reels.
- **Check the handle on every render.** It has shipped wrong once.
- **One ask per caption**, at most 5 hashtags, search terms in the body.
- Render carousels at 1080x1500 and crop; render Reels at 1080x2100 and crop.
  Chromium returns a shorter viewport than requested and the loss is invisible.

## Caption scoring traps

The specificity check counts digits and proper nouns. Spelled-out numbers score
nothing, so write "3 steps" not "three steps". `20x` fails the pattern because
there is no word boundary after the digit; write "20 times". Burstiness
measures sentence-length variation, so re-check it after any edit that evens
out sentence lengths.

## What cannot be automated

- **Trending audio on Reels.** The publishing API cannot attach a track, and a
  silent Reel is throttled. Reels are therefore uploaded by hand.
- **Drafts or planned posts.** `media_publish` publishes immediately. Nothing
  can be placed in Instagram's Planned tab, and the Business Suite composer has
  no file input to target.
- **Alt text.** Add it in the app.

Do not propose working around these. They have each been tested.

## Honest counsel

Carousels reach existing followers. Reels reach non-followers. If the account
is small and the Reel uploads slip, the carousels are talking to an empty room,
and that is worth saying out loud rather than quietly producing more carousels.

Posting times in `docs/week-1-schedule.md` are reasoned, not measured. Once the
account has a few weeks of insights, re-time from its own data and say that the
earlier times were a hypothesis.
