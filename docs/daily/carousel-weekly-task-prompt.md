# Scheduled task: IB carousel weekly build

Schedule: Mondays 15:23 America/New_York (`CRON_TZ=America/New_York 23 15 * * 1`). Push notifications on.
Why: Pietro, 19 Nov 2026, "Make sure this carousel is published each day." The queue ran out on 9 Nov and 17 Nov.

## Prompt

Weekly carousel build for the Instagram page @investmentbankinginterviews. Purpose (Pietro, 19 Nov 2026: "Make sure this carousel is published each day"): the carousel queue in posts.json must never run dry. It ran out on 9 Nov and again on 17 Nov because nobody built the next batch. Pietro is not watching: do not ask questions, take the most reasonable reading and say which at the top.

Repo: pietrocappellaro31-art/ib-autopost (if it is not already in this session, attach it with add_repo access "push", clone it, and work from its root). Keep any changes already in the working tree.

1. Read CLAUDE.md, docs/brand-system.md, docs/decisions-log.md (newest decision wins), and the latest batch builder (the highest build/novN.py or similar, e.g. build/nov2.py) with its docstring. Load the skills ib-carousel, ib-caption and ig-human if listed.
2. If posts.json records an "api_block", build nothing, and send Pietro one SendUserMessage saying the block is still on. Stop.
3. Target window: every Eastern day from tomorrow through today + 10 days that has fewer than 3 carousels (non-reel, non-story entries) in posts.json. If the window is already full, stop silently.
4. Write the next batch builder (next file name, same structure as the latest one, importing build() from nov1.py): 3 decks per missing day, slots 08:00, 12:30 and 17:30 ET (13:00, 17:30, 22:30 UTC while Eastern is UTC-5; 12:00, 16:30, 21:30 UTC under daylight time), Technical of the Day with about 1 Recruiting Playbook deck a day, cover rotation by calendar day from 10 Nov 2026 = day 1 (day n uses pattern (n-1) mod 3: red/ink/paper, ink/paper/red, paper/red/ink). Topics must not repeat any carousel id already in posts.json. Work every technical in the docstring and check the arithmetic with a script; never invent a number, statistic, source or credential; no em dashes.
5. Render (python3 build/<file>.py), check every deck reports problems: none, and look at contact sheets of all slides for overflow or clipped text.
6. Captions in build/captions/<prefix>-NN.txt: hook line under 125 characters, digits not spelled-out numbers, one ask, 4 hashtags. Run ig-human humanize.py to make the .clean.txt and detect.py; every caption must score PASS (rewrite and rescore until it does).
7. Queue with python3 build/schedule.py <slug> <scheduled_utc> for each deck, set "series" to "Recruiting Playbook" where it applies, and add one Story per new day to build/stories.py STORIES (question plus worked answer), render it, and add the story-YYYY-MM-DD entry at 23:00 UTC (22:00 under daylight time) if missing.
8. git pull --rebase, commit the builder, captions, images (JPGs only), stories.py, posts.json, never force-push, push. Then dispatch a selftest: gh api -X POST repos/pietrocappellaro31-art/ib-autopost/actions/workflows/publish.yml/dispatches -f ref=main -f 'inputs[mode]=selftest' and confirm the run says PASS.
9. Send Pietro one short SendUserMessage only if something failed or the window could not be filled; on success, finish with a one-line summary of the days and topics queued.
