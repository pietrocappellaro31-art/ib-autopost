---
name: "music-library"
description: "Pietro's music library for the YouTube channel: add the songs he sends, analyse each one (tempo, key, mood, calmest stretch), and have every YouTube Short pick the best-fitting song from it. The songs never go into our files. A Short gets the pick to add with \"Add sound\" in the YouTube app. Long videos no longer use it (12 Nov: Pietro adds long-video music himself). Use when Pietro sends music, says \"add these songs\", \"music library\", or asks which song a video should use."
---

# Music library

Pietro, 12 Nov: "Create a skill that will attach all these audios to a library audios - the library
will then be used for the creation of both YouTube shorts and YouTube video. The video should pick
from the library the most appropriate music. If this works, I will add more songs in the next days."

The code is `build/music_library.py` in the ib-autopost repo; the library is
`build/music_library/library.json` (committed: names, analysis, rights, use log). The audio files sit in
`build/music_library/audio/`, which is **gitignored**: the session keeps them, the repo never does.

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
2. **Long videos: not used any more** (12 Nov, later the same day, Pietro: "the music is terrible.
   From now on, I will add the music myself. You will provide me with a line to fill in the description
   to give credits for it"). Long videos ship with no music in the file; Pietro adds his own track and
   fills in the credit line the engine writes (see youtube-videos-creator, section 6). The library-matched
   bed (`music_library.bed()`) stays in the code only for re-rendering an old video with `music=True`.
   A library song is commercial, so it cannot go on a long video without a Content ID claim.
   **13 Nov:** long videos now ship a clean MP4 and a scored MP4 with an original score from `music.py`
   (`docs/production/audio-standard.md`, `score=` reflective, suspense or light). The library is still not
   used for long videos: the score is written from the film's mood, not from a library song.

A song Pietro truly holds a licence for (a written licence from the artist, or an Epidemic Sound or
Artlist subscription that covers it) can be set to `rights=licence`, with the proof added to
`docs/rights/ledger.md`. Only those songs may ever be mixed into a master (`mixable()`), and only after
the content-compliance gate passes.

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

## Never

- A library song in a master unless `rights` is `licence` with the proof in the ledger.
- Audio files in git.
- Any edit meant to stop Content ID from recognising a song.
