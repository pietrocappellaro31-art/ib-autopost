# ib-autopost: working rules

The finance content operation for @investmentbankinginterviews (Instagram) and its YouTube channel. Independent: no
brand, characters, files, music or schedules from any other project. Carousels, Stories and (from 28 Nov) TWO Reels a
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
- **27 Nov to 4 Dec (Pietro, 27 Nov): EMMA (Kokoro `bf_emma`, speed 0.97, the 12 Nov voice) on EVERY video: Reels,
  long films and Shorts.** `voice_clone.narrator()` / `youtube_voice()` return it; this overrides any scheduled-task
  prompt step that still says HEART. HEART again from 5 Dec unless Pietro extends it.
- **Reels from 28 Nov (Pietro, 27 Nov): TWO a day, 12:30 ET (slot A) and 18:00 ET (slot B); NO subtitles; the follow
  ask spoken in the last line AND shown on screen (`reel_film.follow_ask`).** This overrides "ONE Reel a day" below.
- **YouTube, long films and Shorts (Pietro, 17 Nov): deliver ONE video file, the one with our original score.** Never
  send or offer a clean MP4 as well (it stays in `build/out/` only as the score gate's reference). The score's style,
  key and tempo change every video (`score.pick`: never a style or key of the last three; name the style in the
  delivery). This overrides any scheduled-task prompt step that still says to deliver a clean MP4 or "music=False".
  Filmed beats from `build/cine.py` where the story has people, places or a mechanism.
- **YouTube from 27 Nov (Pietro): NO subtitles in the picture, long videos AT MOST 5 MINUTES, EMMA to 4 Dec, thumbnails on a
  spark-yellow background only, the .srt kept for CC, "what if" films alternating with documentaries, and the Shorts ARE the Reels (`build/yt_short_from_reel.py`
  after each Reel: same picture, our score, the Reel's description and tags).** `docs/production/long-form-standard.md`
  "FIRST". This overrides the 19 Nov line below and any task prompt that says 8 to 12 minutes or HEART for YouTube.
- **YouTube from 19 Nov (Pietro, 18 Nov), history for Shorts:** Shorts are number puzzles cut from the newest long film without a Short,
  linked to it as Related video; films stay daily, opening on the hook (puzzle or number on screen within 5 s, no card
  first) with title and thumbnail carrying the same number. `docs/decisions-log.md` 18 Nov.
- **Reels from 27 Nov (Pietro, 26 Nov): ONE fully animated Reel a day at 18:00 ET (slot B), made with
  `build/reel_film.py` to `docs/production/reel-film-standard.md`: the whole frame is the animated world (no card, no
  picture in a picture, no blur), story first, voice and effects only in the file, a trending licensed track attached by
  Instagram at posting (`--audio-id`), some Reels as Trial Reels (`--trial`). Pietro hides like and share counts in the
  app. One carousel a day (08:00 ET), one Story a day.** `docs/decisions-log.md` 26 Nov.
- AI disclosure: a recommendation per finished video with its reason, never an automatic tick.
- Never invent a number, quote, source or credential. Reconstructions are badged. No commercial music in any file (Instagram's licensed tracks are attached by Instagram at posting, never put in a file).

## Setup and safety

- `bash build/setup_voice.sh && source ~/voice-tools/env.sh` once per session.
- Never commit MP4s, WAVs, stems, `build/out/`, voice samples, keys or tokens to main. A queued Reel's video lives only on
  its temporary `reel/<slug>` branch (`build/reel_queue.py`), deleted once posted. `git pull --rebase` before pushing;
  never force-push; three daily runs write the same logs.
- Do not change scheduled tasks, upload to YouTube, or alter live posts without Pietro. Never queue anything while
  `posts.json` records an `api_block`.
