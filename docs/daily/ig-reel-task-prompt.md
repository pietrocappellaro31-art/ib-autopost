# Prompt for the "IG Reel daily" scheduled task (16 Nov 2026)

Written for Pietro's decision of 16 Nov (two Reels a day, posted automatically, no approval). A session could not
edit scheduled tasks, so paste the block below into the task "IG Reel daily" (keep its time, 8:16am New York).

```
Daily IG Reels for the Instagram page @investmentbankinginterviews (Pietro's page): make TWO Reels (A and B) and queue them for automatic posting. Pietro decided on 16 Nov 2026: "We will post two each days. You won't need my approval. You will use your own intelligence to analyze the top performing reels and make improvements if necessary. You will decide at what time to post each day." Pietro is not watching: do not ask questions, take the most reasonable reading and say which at the top.

Repo: pietrocappellaro31-art/ib-autopost (if it is not already in this session, attach it with add_repo access "push", clone it, and work from its root). Inspect the working tree and keep any changes already there.

THE STANDARD: every Reel follows docs/production/ exactly as Shorts and long videos do (cinematic-standard.md, audio-standard.md, quality-gates.md section 9, the formats A to F of short-form-standard.md, voice-decision.md); docs/reel-style.md is the visual base; the bar is the cinematic proof of concept (build/cine_poc_newton.py). The procedure is docs/skill/ib-voiced-reel/SKILL.md, section "Two Reels a day, posted automatically": follow it. Where a loaded skill copy disagrees with the repo, the repo wins.

1. Read: CLAUDE.md, docs/skill/ib-voiced-reel/SKILL.md, the docs/production files above, docs/brand-system.md, docs/decisions-log.md, docs/reel-style.md, docs/daily/README.md, docs/daily/quality-log.md (the last Reel row's "Next improvement" is the first job), docs/daily/topics.md, docs/daily/ig-reels.md and docs/daily/performance.md. Load the skills ib-voiced-reel, content-compliance and ig-human if listed.
2. Setup: bash build/setup_voice.sh && source ~/voice-tools/env.sh
3. Check posts.json for "api_block". If it is there, Meta is blocking the app: still make both Reels, do NOT queue them, and deliver them to Pietro for hand posting (files, captions, comment questions, the reminder to turn on Instagram's AI label), saying the block is still on.
4. Read the performance: from docs/daily/performance.md name the best and worst Reels of the last two weeks and what differs (hook, format, topic, length, slot); turn a pattern seen in at least three Reels into today's choices; write the reasoning in the quality-log row. Move a slot in posts.json "reel_slots_et" only on that evidence and only to a time a reliable dispatch covers, and record why in docs/decisions-log.md.
5. Make Reel A, then Reel B, on two different topics not in topics.md "Used" for Reels, each in the best format for it (vary across the week). Voice HEART (next_voice() prints it). Work every answer in the docstring; never invent a number, statistic or credential; no em dashes. Run every check in the skill and quality-gates.md section 9: takes.json all wer 0, motion measured (python3 build/yt_preview.py --clip build/out/<slug>/<slug>.mp4) plus a contact sheet, DNSMOS, safe-area, clear.json and WRAP at zero, about -16 LUFS with true peak at or under -1.5 dBTP, action-timed effects, no whoosh.
6. Make the scored master for each (python3 build/master.py scored build/out/<slug>/<slug>.mp4 -16 <mood> <mood>). Run the content-compliance gate and write docs/rights/posts/<slug>.md. A Reel that fails any gate is not queued.
7. Queue each passing Reel: python3 build/reel_queue.py <slug> --slot A (or B) --caption <caption file> --comment "<question>". The caption must PASS ig-human and include "Narration: AI-generated voice; script is our original work."; at most 4 hashtags. Commit posts.json with the episode files, captions, rights records, logs and build/voices/voice_log.json (never MP4s or WAVs on main), git pull --rebase first, never force-push, then push. The publisher posts each Reel at its slot with the AI label and the comment question; do not post anything yourself.
8. Deliver with SendUserFile both MP4s and covers (for the record), then one SendUserMessage: for each Reel the topic, format, slot and posting time, which master was queued, caption and comment, the measures, and what the performance data changed today; if a Reel was not queued, why.
9. Log: one row per Reel in docs/daily/ig-reels.md (voice, format, slot), the topics in docs/daily/topics.md "Used", and one row in docs/daily/quality-log.md with the measures, the performance reading, what improved today and the next improvement. Commit and push.

The goal is visible improvement in quality and results every day.
```
