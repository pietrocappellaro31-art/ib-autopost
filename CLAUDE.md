# ib-autopost: working rules

The finance content operation for @investmentbankinginterviews (Instagram) and its YouTube channel. Independent: no
brand, characters, files, music or schedules from any other project. Posting and uploading stay manual (Pietro).

## Where the rules are

- `docs/decisions-log.md`: Pietro's decisions, newest first. A newer explicit decision wins over everything below.
- `docs/production/`: the standards since 13 Nov 2026. `long-form-standard.md`, `short-form-standard.md`,
  `cinematic-standard.md`, `audio-standard.md`, `quality-gates.md`, `scene-library.md`, `animation-engine.md`,
  `voice-decision.md`, `skill-sync.md`, `upgrade-log.md`.
- `docs/skill/<name>/SKILL.md`: the authoritative skill copies (youtube-videos-creator, ib-voiced-reel,
  music-library, content-compliance). An installed copy that disagrees is out of date.
- `docs/brand-system.md`, `docs/reel-style.md`, `docs/daily/` (logs; the last "Next improvement" is each run's
  first job), `docs/rights/` (ledger and per-post records).

## Current defaults (13 Nov 2026)

- Narrator HEART: Kokoro v1.0 `af_heart`, speed 0.9, en-us, everywhere. Earlier voices and trials are history.
- Long videos: clean and scored MP4 (original `build/score.py` score, gate in `audio-standard.md`); filmed beats
  from `build/cine.py` where the story has people, places or a mechanism. Shorts and Reels: the clean master is
  delivered; a scored alternative when feasible (`build/master.py scored`).
- AI disclosure: a recommendation per finished video with its reason, never an automatic tick.
- Never invent a number, quote, source or credential. Reconstructions are badged. No commercial music in any file.

## Setup and safety

- `bash build/setup_voice.sh && source ~/voice-tools/env.sh` once per session.
- Never commit MP4s, WAVs, stems, `build/out/`, voice samples, keys or tokens. `git pull --rebase` before pushing;
  never force-push; three daily runs write the same logs.
- Do not change scheduled tasks, publish, upload, or alter live posts without Pietro.
