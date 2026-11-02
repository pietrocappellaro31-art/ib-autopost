---
name: ib-autopost
description: Build, schedule and publish posts for @investmentbankinginterviews through the ib-autopost repo - render carousels and Reels, lint captions, write the manifest, and diagnose a failed or silent publishing run. Use for anything touching the publishing pipeline, a stuck post, a failed GitHub Actions run, or the renderer.
---

# The @investmentbankinginterviews publishing pipeline

Carousels publish themselves from `pietrocappellaro31-art/ib-autopost` via
GitHub Actions. Reels are handed to Pietro as files because the API cannot
attach trending audio. Nothing here depends on a Claude account.

Read `docs/brand-system.md` before rendering anything.

## Getting the repo into a session

```
# attach, then clone exactly once, with a generous timeout
add_repo(owner="pietrocappellaro31-art", repo="ib-autopost", access="push")
git clone --depth 1 https://github.com/pietrocappellaro31-art/ib-autopost
```

The GitHub **Actions API is blocked through the agent proxy**. Reading run
logs or dispatching a workflow has to be done in a browser, not with `gh api`.

## Layout

| Path | What |
|---|---|
| `publish.py` | The publisher. Carousel and Reel paths, account discovery, quota check. |
| `posts.json` | The schedule. `image_base` plus one entry per post. |
| `.github/workflows/publish.yml` | The cron. |
| `build/brand.py` | Carousel primitives: `Deck`, `check`. |
| `build/parts.py` | Shared diagram pieces: `cover`, `stake`, `ladder`, `steps`, `bars`, `formula`, `recap`, `cta`. |
| `build/reel.py` | Reel builder: `build(slug, beats)`, silent and read-paced. |
| `build/schedule.py` | Copies media in and writes the manifest entry. |
| `build/captions/` | Every caption, linted. |
| `images/` | Every rendered slide, served to Meta. |

## Building a carousel

Nine slides, always: red cover, ink stake, five `qa` slides, ink recap, red CTA.

```python
from brand import Deck, check, BOOKMARK, INK, PAPER, RED, TEAL, WHITE
from parts import cover, stake, ladder, steps, bars, formula, recap, cta

d = Deck("w2-01-slug", "Technical of the Day", 9)
d.slide(RED, WHITE, accent=WHITE, inner=cover("Headline.", ["chip", "chip"], "One line of stake."))
d.slide(INK, WHITE, inner=stake("Why it matters", "The sharpened version."))
d.qa("Question.", "keyword", ladder([("label", "value", TEAL)]), "The answer.", "The mistake.", 72)
...
paths = d.render()
print(check(paths, 9))        # must print []
```

`check()` catches what the eye cannot: wrong dimensions, a clipped bottom
edge, a file over the API size limit. **Never ship a deck with findings.**

Then look at two or three slides yourself. `check()` does not catch ugly.

## Building a Reel

```python
from reel import build
beats = [("text that sets the pace", "<h1>What is on screen</h1>"), ...]
build("w2-r01-slug", beats)
```

Seven beats, about 30 to 35 seconds, silent, no audio stream. Beat length
comes from word count, capped at 4.8s: a frame held longer reads as a stall.
Keep each frame under about a dozen words; a silent Reel is read at scroll
speed.

Deliver Reels as files named with their slot, caption in a `.txt` beside each,
plus a short note on why those times. Never schedule them in the manifest.

## Captions

Draft, then lint, then fix the named check, then re-lint:

```
python3 humanize.py draft.txt -o clean.txt --report
python3 detect.py clean.txt
```

**PASS only.** Needs 70+ overall with no single check below 55. Three traps
that cost several rounds already:

- Specificity counts digits and proper nouns. "three steps" scores nothing;
  write "3 steps".
- `20x` fails the pattern because there is no word boundary after the digit.
  Write "20 times".
- Burstiness measures sentence-length variation. Any edit that evens out
  sentence lengths drops it, so re-check after fixing something else.

One ask, at most 5 hashtags, search terms in the body, no em dashes.

## Scheduling

```
cd build && python3 schedule.py <slug> <scheduled_utc> [--reel]
```

It copies the media into `images/`, reads `build/captions/<w1-NN>.clean.txt`,
replaces any existing entry with the same id, and keeps the manifest sorted.

**Times are UTC.** US Eastern is UTC-5 from 1 Nov 2026, so 08:00 Eastern is
13:00 UTC and 12:30 Eastern is 17:30 UTC. Get this wrong and everything fires
an hour out.

Commit and push. The cron does the rest.

## Verifying before you walk away

```
# the slides must actually be served to Meta
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" \
  https://raw.githubusercontent.com/pietrocappellaro31-art/ib-autopost/main/images/<file>.jpg

# an idle run must be clean and touch no network
IG_ACCESS_TOKEN=x python3 -I publish.py     # expect "Nothing due."
```

Then in the browser: Actions, Run workflow, mode **selftest**. It creates one
container and publishes nothing; an unpublished container expires in 24 hours.
`PASS` in the log means credentials, hosting and the API all work.

## Diagnosing a silent account

Work down this list. Each line is a failure that has actually happened.

1. **Are runs happening?** Open the workflow page and read the run times.
   GitHub does not guarantee cron timing and drops runs from high-frequency
   schedules on quiet repositories: a `*/15` schedule fired once in seven
   hours. The cron is therefore concentrated into the UTC windows that contain
   post times, with an hourly sweep.
2. **Are runs failing?** Check the status, not just the count. Twenty green
   runs and twenty red runs look identical in a list of times.
3. **`API access blocked`, OAuthException 200.** Meta has restricted the
   developer account, not the app. `developers.facebook.com` redirects to a
   block page and the fix is an identity checkpoint only Pietro can complete.
   This happened on 31 Oct, hours after the first successful publish.
4. **`image_base still contains the OWNER/REPO placeholder`.** The guard fired
   before any API call. Fix the manifest.
5. **`No Instagram professional account is reachable from this token`.** The
   Page is not assigned to the system user, or the Instagram account is not
   connected to that Page.
6. **Nothing due** when something should be. Check the UTC conversion and
   check whether `published_id` is already set.

**If posts have fallen overdue, re-space them before restoring access.** The
next successful run publishes everything due at once, which on a small account
reads as spam and spends several good posts in one scroll.

## Invariants

- **JPEG only.** PNG is rejected by the API.
- **Render tall, then crop.** Chromium returns a viewport about 80px shorter
  than `--window-size`. Carousels: 1080x1500 cropped to 1080x1350. Reels:
  1080x2100 cropped to 1080x1920. The loss is invisible on a pale ground.
- **Header and footer stay `position:absolute`.** An inline `position:relative`
  overrides the class and drops the footer onto the body text.
- **Check the handle on every render.** It has shipped wrong once.
- **A post with a non-null `published_id` is never touched again.** That is the
  only thing preventing a double publish.
- **The token never enters a conversation.** It lives in the repo secret, and
  `publish.py` strips it from error bodies so public logs stay safe.
- **Never invent a number, statistic, credential or outcome.** Use a
  `{{placeholder}}` and say so.
