# Audio standard: voice, music, effects, mix

Pietro, 13 Nov 2026: his long-form documentary instructions (morning) and the cinematic-upgrade directive (the same
day), merged. Applies to long videos, Shorts and Reels unless a format file says otherwise. History of every earlier choice stays in `docs/decisions-log.md`.

## 1. Narrator

**HEART: Kokoro v1.0 ONNX (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), voice `af_heart`, speed 0.9, en-us** for long
videos, Shorts and Reels (`voice_clone.YOUTUBE_PICK = REEL_PICK = "HEART"`). Synthetic, not a person, Apache 2.0.
Why and the trial history: `voice-decision.md`. A platform-specific exception needs Pietro's approval in the
decisions log.

- The narrator has no name, face, credentials or past. Never "when I worked at Goldman Sachs".
- The daily voice trial is closed and must not be resumed; its results stay in `docs/daily/youtube-voice-trial.md`.
- Every line is checked by the recogniser (`yt_timing.py --takes`, `takes.json`). A real slip gets reworded; a proper
  name the recogniser cannot spell is logged, not reworded. "Heard word for word" means the recogniser, not a person.
- Every line is cached (`synth.pkl` in long videos, `keep_voice`/`redo` in the Levels engine, `lines/` in cine
  films): editing one line re-says only that line and keeps every other timing.

## 2. Pronunciation

`build/voice.py` `PHONEMES` is the pronunciation dictionary (misaki notation; plurals, -ed and -ing are derived).
An unknown word stops the render, so nothing is guessed. Covered: bank terms and acronyms (EBITDA, EBIT, DCF, WACC,
IRR, MOIC, LBO, IPO, EV, FCF, LTV), historical names (Aislabie, Odlyzko, Southwark, Threadneedle, Garraway's),
companies (JPMorgan, Goldman Sachs, Alibaba, Experian, Affirm). Numbers, currency and maths are written as words in
the script ("three hundred and fifty pounds", "twenty percent"); the screen shows digits.

`python3 build/narrator_check.py` says 12 fixed finance lines and reports word errors, words per second, peak,
longest gap and DNSMOS: the regression set for the narrator. 13 Nov, af_heart at 0.9: 12 of 12 said correctly
(3 recogniser spelling or format differences, not slips: "20%" for "twenty percent", "WAC", "Aisleby"), 2.94 words
a second, peak -3.2 dBFS, DNSMOS 3.49 (SIG 3.70, BAK 4.20); GEORGE on the same lines 3.42. Nobody listened: the
workspace has no audio playback. Pietro's ear is the final check.

## 3. Masters

| | CLEAN | SCORED |
|---|---|---|
| Contains | narration, sound effects, ambience | the same plus our original score, ducked |
| Use | Pietro adds platform-library music in the app or Studio; the safe default anywhere | only where the score's rights cover the platform |
| Long video file | `<slug>-clean.mp4` | `<slug>-scored.mp4` |
| Made by | long videos: `youtube.mix`; filmed shorts and films: `master.dual` | the same (same picture, same timing) |

The picture is rendered once; both masters copy the same video stream. `<slug>.mp4` is a copy of the recommended one.

**Long-video score gate** (`youtube.SCORE_GATE`, measured by `youtube.sound_report` into `sound.json`, field
`recommended`): the scored mix is recommended only if the voice sits at least 18 dB over the ducked music while
speaking, DNSMOS SIG (the speech itself) of the scored mix is within 0.3 of the clean mix, and 20 seconds of the
scored mix are heard by the recogniser within 5% of the same 20 seconds of the clean mix. DNSMOS OVRL and BAK are
reported, not gated: the model counts any music under a voice as background noise (13 Nov: #6 remixed, BAK 4.07
clean and 2.46 scored with the music 24.6 dB under the voice; the 20 s proof of concept, OVRL 2.44 clean and 2.06
scored while the recogniser heard every word of both). `score="none"` makes the clean mix only.

**Description line.** Scored: `Music: original score made for this video.` Clean with Pietro's track: `Music: [song
title] by [artist], from the YouTube Audio Library` (fill in, paste the library's own attribution text if the track
page shows one, or delete it if none is needed). Any added track must be licensed for monetised YouTube.

| Format | Default delivery |
|---|---|
| Long video | both; `<slug>.mp4` is the scored one if it passes the score gate (`quality-gates.md` 4), else the clean one |
| YouTube Short | clean is the one delivered (Pietro, 13 Nov, `short-form-standard.md`: he adds a sound in the app); a scored alternative from `score.py` is prepared when practical and offered as unheard until he approves a cue |
| Instagram Reel | clean (Pietro adds Instagram music in the app); a scored alternative when he asks or when the score is cleared and suits it |

Never a commercial or trending song in a file. A version with YouTube-library audio is never uploaded to Instagram,
and the reverse. No pitch, speed or re-recording tricks to get past Content ID.

## 4. Original score

`build/score.py`: notes, not loops. Harmony with voice leading, a seeded motif that is stated and answered, one mood
per section aligned to shots or chapters, sampled instruments from the GeneralUser GS SoundFont (free for commercial
music; `docs/rights/ledger.md`) rendered offline with TinySoundFont, a synthetic hall. Moods: bustle, explain,
discover, mystery, decide, peak, crash, reflect, resolve, quiz, reveal. Long videos pick a plan with
`score="reflective" | "suspense" | "light"` (`youtube.SCORE_PLANS`; `youtube.SCORES` sets tempo and level). If the
SoundFont is missing the render falls back to the `music.py` bed (synthesised, nothing sampled) and says so;
`score_engine="music"` forces it. Pietro's music-library songs are commercial recordings and stay out of every file
(`music-library` skill).

Rules: support the content, not movie-trailer drama under every sentence (Pietro found the 10 Nov piano and cello
"too dramatic" and the pop bed "a lunapark"); change the cue when the chapter or emotion changes; never the melody,
progression or arrangement of a commercial song. Pietro has not yet heard a `score.py` cue: until he likes one, the
scored master is offered, not pushed.

## 5. Sound effects and ambience

`build/sfx.py`, all synthesised (nothing to license). Reels and Levels: tick, pop, ding, thump. Filmed scenes
(48 kHz stereo): footsteps on stone (timed from the walk cycle itself, `cine.footsteps`), paper, quill, coin clinks
(with a glass jar's ring), a soft mallet for numbers and flags landing, a pendulum clock; ambience for an old street
(distant air, a murmur of many people with no words, carts) and a quiet room. Every effect belongs to an action on
screen. **No whoosh on routine transitions** (Pietro, 6 Nov).

Gap still open in the drawn (non-filmed) parts of a long video: `youtube.scenes` puts a pop on every beat and visual
change and a ding on every chapter card. Filmed beats carry action-timed foley; the drawn beats should move to
action-timed sound too (build step in `cinematic-standard.md`).

## 6. Mix and loudness

- Stems: voice, foley, ambience, music. Voice through the narrator chain (`voice.MASTER`).
- Music ducks about 11 dB while the voice speaks (attack 60 ms, release 350 ms); ambience about 4 dB.
- Target voice over music while speaking: at least 15 dB (measured, `voice_over_music_db`).
- Two-stage loudness: measure, normalise linear with the measured values, true-peak limiter, check, trim if off.
  Long video and Short about -14 LUFS; Reel about -16 LUFS; the limiter ceiling is -1.5 dBTP and a file fails above
-1.0 dBTP. AAC 192 kb/s, 48 kHz.
- Measured on the written files, never assumed from settings: LUFS, true peak, LRA, clipped samples, silences over
  1.2 s, DNSMOS of each master, word errors of the master itself (whole film for short ones, a narrated excerpt
  for long ones). Report: `sound.json` (long videos), `<slug>-masters.json` (`master.dual`).
- Where nobody could listen, say so; the numbers are evidence, not a listening verdict.
