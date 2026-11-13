---
name: "music-library"
description: "Music for the finance channel and the IB Instagram page: Pietro's reference songs (analysed, never in a file), our original scores (score.py) and any licensed tracks, each with a rights class (REFERENCE_ONLY, ORIGINAL_GENERATED, LICENSED_FOR_YOUTUBE, LICENSED_FOR_INSTAGRAM, LICENSED_FOR_ALL_REQUIRED_PLATFORMS) that decides clean or scored masters and in-app suggestions. Use when Pietro sends music, says \"add these songs\" or \"music library\", or a video needs its music chosen."
---

# Music library

Version 2026-11-13 (cinematic upgrade). Authoritative copy: `docs/skill/music-library/SKILL.md` in the ib-autopost
repo; the installed plugin is built from it (`docs/production/skill-sync.md`).

Pietro, 12 Nov: "Create a skill that will attach all these audios to a library audios - the library
will then be used for the creation of both YouTube shorts and YouTube video. The video should pick
from the library the most appropriate music. If this works, I will add more songs in the next days."

The code is `build/music_library.py` in the ib-autopost repo; the library is
`build/music_library/library.json` (committed: names, analysis, rights, use log). The audio files sit in
`build/music_library/audio/`, which is **gitignored**: the session keeps them, the repo never does.

## Rights classes (13 Nov 2026, cinematic upgrade)

Every piece of music has exactly one class (`music_library.RIGHTS`); unknown means REFERENCE_ONLY.

| Class | What it is | In a master? |
|---|---|---|
| REFERENCE_ONLY | a commercial or unverified recording (all 8 of Pietro's songs) | never; mood, tempo and key reference, and the in-app suggestion for Shorts |
| ORIGINAL_GENERATED | composed by our code for a video (`build/score.py`, old `music.py` beds), logged in `library.json` "originals" | yes, any platform |
| LICENSED_FOR_YOUTUBE | a licence on record covering monetised YouTube | YouTube masters only |
| LICENSED_FOR_INSTAGRAM | a licence on record covering Instagram | Instagram masters only |
| LICENSED_FOR_ALL_REQUIRED_PLATFORMS | a licence on record covering both | yes |

`music_library.mixable(track, platform)` decides, and fails closed: a LICENSED_ class without `proof=` (where the
licence is recorded in `docs/rights/ledger.md`) is not mixable. Never claim a right that is not on record.
`python3 build/music_library.py set <id> rights=<CLASS> proof="ledger: ..."` refuses any other class name.

## Clean or scored master

The picture is rendered once; a **clean master** (voice, effects, ambience) is always made and, when the music's
class covers the platform, a **scored master** (`docs/production/audio-standard.md` section 3): long videos through
`youtube.mix` (the score gate picks the recommended file), filmed shorts through `build/master.py dual`, and a
finished Levels Short or Reel through `python3 build/master.py scored <clean.mp4> [-16] <mood> ...`. Shorts and
Reels: the clean master is the deliverable (Pietro adds a sound in the app); a scored alternative is offered when
feasible, as unheard until Pietro approves a score.py cue. Optional manual platform audio is always possible on the
clean file. A master
carrying YouTube-library audio is never uploaded to Instagram, and the reverse.

## The rule that shapes everything

The songs Pietro sends are commercial recordings. Mixing one into a master gets the video claimed by
Content ID (the money goes to the rights holder, or the video is blocked in some countries), and the
compliance gate treats it as STOP. Pietro asked for "a way around" (12 Nov). The library uses each song
in two lawful ways and **never evades Content ID**: no pitch shifting, speed changes, chopping or
re-recording a song to get past detection.

1. **Shorts**: the picked song goes first in the "Music for this Short" block. Pietro adds it with
   "Add sound" in the YouTube app, which YouTube licenses for Shorts. The block names the words to
   search (`search`), the start time (`calm_start`, the calmest 15 s that does not run into the
   ending) and the volume.
2. **Long videos: not used as a source** (12 Nov, later the same day, Pietro: "the music is terrible.
   From now on, I will add the music myself. You will provide me with a line to fill in the description
   to give credits for it"). Long videos ship with no music in the file; Pietro adds his own track and
   fills in the credit line the engine writes (see youtube-videos-creator, section 6). The library-matched
   bed (`music_library.bed()`) stays in the code only for re-rendering an old video with `music=True`.
   A library song is commercial, so it cannot go on a long video without a Content ID claim.
   **13 Nov:** long videos now ship a clean MP4 and a scored MP4 with an original score
   (`build/score.py`, fallback `music.py`; `docs/production/audio-standard.md`, `score=` reflective, suspense or
   light). The library is still not a source for long videos: the score is written from the film's mood, not
   from a library song.

A song Pietro truly holds a licence for (a written licence from the artist, or an Epidemic Sound or
Artlist subscription that covers it) gets the LICENSED_ class its licence covers, with `proof=` and the licence
in `docs/rights/ledger.md`. Only then may it be mixed (`mixable()`), and only after the content-compliance gate
passes. A reference song may describe broad qualities for our own score (calm piano, tense strings, a tempo);
the score never takes its melody, chord progression, arrangement or audio, and is never built as a soundalike.

## Adding songs (when Pietro sends music)

1. Run `python3 build/music_library.py add <files...>` from the repo root. Each new file is copied into
   the audio folder (duplicates are skipped by hash) and analysed: BPM, key and mode, percussion share,
   loudness, dynamics, brightness, energy and valence (0 to 1), mood tags, the calmest and the fullest
   15 s.
2. Fix the names. Ripped files carry the uploader in the artist tag and junk such as "Visualizer" in the
   title. Correct them with
   `python3 build/music_library.py set <id> title="..." artist="..." search="..."`, where `search` is
   what to type in "Add sound".
3. Check `python3 build/music_library.py list`. Listen-check is not possible here, so sanity-check the
   tags against what the song is known to be (a solo piano piece should read "no drums, calm"). After
   changing `analyse()`, run `reanalyse`, which needs the audio, so it only works in the session that
   holds the files.
4. Commit `library.json` and any code change, never the audio. Log the additions in
   `docs/rights/ledger.md` (one line: references only, not in masters).
5. Reply to Pietro with a short table: each song, its tempo, key, mood tags and the moods it will be
   picked for.

## How a video picks

- An episode sets `mood=` (one of: calm, reflective, melancholy, curious, warm, hopeful, playful,
  upbeat, tense, dark, dramatic, story). Pick the mood from the script, not from habit: a history
  story is often "story" or "reflective", a quiz "playful" or "curious", a crash "tense".
- `music_library.pick(mood, kind, slug)` returns the nearest song on energy and valence. A song used
  for the same kind in the last 3 days loses a little, so the channel does not play one song all
  week. The use log is `used` in `library.json`.
- **Long video**: not used (12 Nov; from 13 Nov the scored MP4 uses an original score from the film's
  `score=` mood, see `docs/production/audio-standard.md`).
- **Short** (`levels.make`): automatic for slugs starting with `shorts-`. The render prints the pick
  and writes `music_pick.json`. Put that song first in the music block, then add one or two sounds
  trending on Shorts that week (web search). The pick's `others` are the runner-ups.

## Original scores

`build/score.py` composes per video (moods per section, seeded motif, sampled instruments from the GeneralUser GS
SoundFont, free for commercial music). Each delivered cue is logged with `music_library.register_original(...)`
(class ORIGINAL_GENERATED). Metadata kept: mood per section, BPM, key, instruments, engine, video.

## Never

- A library song in a master unless its class covers that platform and the proof is in the ledger.
- Audio files in git.
- Any edit meant to stop Content ID from recognising a song.
