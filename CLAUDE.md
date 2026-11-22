# ib-autopost: working rules

The finance content operation for @investmentbankinginterviews (Instagram) and its YouTube channel. Independent: no
brand, characters, files, music or schedules from any other project. Carousels, Stories and (from 16 Nov) two Reels a
day post automatically through `publish.py`; YouTube uploads stay manual (Pietro).

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
- **YouTube, long films and Shorts (Pietro, 17 Nov): deliver ONE video file, the one with our original score.** Never
  send or offer a clean MP4 as well (it stays in `build/out/` only as the score gate's reference). The score's style,
  key and tempo change every video (`score.pick`: never a style or key of the last three; name the style in the
  delivery). This overrides any scheduled-task prompt step that still says to deliver a clean MP4 or "music=False".
  Filmed beats from `build/cine.py` where the story has people, places or a mechanism. Reels: unchanged (clean master
  with Instagram music in the app, plus the scored alternative).
- **YouTube from 19 Nov (Pietro, 18 Nov):** Shorts are number puzzles cut from the newest long film without a Short,
  linked to it as Related video; films stay daily, opening on the hook (puzzle or number on screen within 5 s, no card
  first) with title and thumbnail carrying the same number. `docs/decisions-log.md` 18 Nov.
- **Week of 22 to 29 Nov (Pietro, 22 Nov): three Reels a day (slots A 12:30, B 18:00, C 21:00 ET), one carousel a day
  (08:00 ET), one Story a day.** `docs/decisions-log.md` 22 Nov.
- AI disclosure: a recommendation per finished video with its reason, never an automatic tick.
- Never invent a number, quote, source or credential. Reconstructions are badged. No commercial music in any file.

## Setup and safety

- `bash build/setup_voice.sh && source ~/voice-tools/env.sh` once per session.
- Never commit MP4s, WAVs, stems, `build/out/`, voice samples, keys or tokens to main. A queued Reel's video lives only on
  its temporary `reel/<slug>` branch (`build/reel_queue.py`), deleted once posted. `git pull --rebase` before pushing;
  never force-push; three daily runs write the same logs.
- Do not change scheduled tasks, upload to YouTube, or alter live posts without Pietro. Never queue anything while
  `posts.json` records an `api_block`.
