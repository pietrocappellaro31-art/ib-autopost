# Handover: running @investmentbankinginterviews

Everything needed to operate the page lives in this repository, on purpose.
It is deliberately not held inside one Claude account: the automation runs on
GitHub Actions against Meta's API and depends on neither.

## What is where

| Path | What it is |
|---|---|
| `publish.py` | The publisher. Three-stage carousel flow and the Reels path. |
| `posts.json` | The schedule. One entry per post, times in UTC. |
| `.github/workflows/publish.yml` | The cron that runs the publisher. |
| `images/` | Every rendered slide, served to Meta over raw.githubusercontent.com. |
| `build/` | The renderer, its fonts, and every caption. |
| `docs/` | The operating knowledge: brand, strategy, schedule, decisions. |

## Reading order for a new session

1. `docs/brand-system.md` — the visual and editorial contract. Read before
   making anything.
2. `docs/automation-plan.md` — how publishing works and what is verified.
3. `docs/week-1-schedule.md` — the current schedule and the reasoning.
4. `docs/decisions-log.md` — what has been decided, and what is still open.
5. `docs/account-setup-checklist.md` — one-time Instagram settings.
6. `docs/skill-pack-review.md` — the instagram-agent skill pack and its limits.

## Credentials, and what is not in here

`IG_ACCESS_TOKEN` is a GitHub repository secret and appears nowhere in the
code or the logs. `publish.py` strips it from any error body before printing,
which is what makes a public Actions log safe to read.

Nothing in this repository is account-bound to Claude. Connecting it to a
Claude Project gives that Project the whole operating manual, and it stays in
step as the repository changes.
