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

## 1b. A natural voice, not a processed one (Pietro, 14 Nov)

Pietro, on the first cash machine Short: "from tomorrow on voice should feel more natural"; asked what was least
natural, he chose **robotic / processed sound**. HEART at 0.9 stays; what changed is what we did to it after Kokoro.

- **Narrator chain** (`voice.MASTER`, used by Shorts, Reels, long videos and cine films): `highpass=f=70` and a 1.5 dB
  dip at 7.2 kHz, nothing else. No compressor, no echo or "room" on the voice, no warmth boost. The 8 Nov chain
  (`voice.MASTER_8NOV`: 2.5:1 compression and a 19/31 ms echo, a comb filter on a dry voice) is kept only to re-render
  an old video exactly.
- **No limiter before the master.** The 0.4 pre-limiter of the no-music masters cut 16% of the narration by up to
  2 dB; every no-music master (Shorts -14, Reels -16) now runs `levels.two_stage`: one plain gain, one true-peak
  limiter at 4x sample rate. `ep["limit"] = .4` restores the old behaviour for a re-render.
- **Stems never clip.** `levels.mux` writes voice and effects with one common gain so the peak is 0.89 at most
  (the voice levelled to RMS 0.12 had reached full scale and was clipped in `voice.wav`).
- **Gate, printed by every render** (`sound.json`): `sig_drop` (DNSMOS SIG of the voice stem minus SIG of the clean
  mix) 0.15 or less, and `voice_stem_clipped` 0.
- **The gate is level-matched (16 Nov).** DNSMOS scores the same voice lower just for being louder: the raw HEART stem
  of the 50% Short, only turned up, scored SIG 3.68 at -30 LUFS, 3.71 at -23 and -20, 3.68 at -17 and 3.60 at -14.
  `build/sig_stages.py` rebuilt that Short's master stage by stage from its raw takes: raw 3.71, int16 stem 3.71,
  narrator chain 3.70, plain gain to -14 LUFS 3.59, true-peak limiter 3.61, AAC 3.61; with effects and room 3.72,
  3.61, 3.63, 3.63. So the 0.10 to 0.16 "drop" of 14 and 15 Nov was the master's loudness, not damage: the chain,
  limiter, encode and effects cost nothing measurable. `sig_drop` now scores voice stem and mix both at -23 LUFS
  (`quality.score_at`); the old figure stays in `sound.json` as `sig_drop_raw`. Gate unchanged: 0.15 or less.
  Raw takes are kept per render (`out/<slug>/parts/*.npy`, `story.keep_parts`) and remixes reuse them.
- Measured 14 Nov on the cash machine narration, voice alone at -14 LUFS: old chain OVRL 3.29 (SIG 3.55), new chain
  3.40 (SIG 3.62), untouched Kokoro 3.40; short-term loudness spread 9.8 dB (squashed) to 12.4 dB (raw 12.5). The
  same Short remixed: mix OVRL 3.12 to 3.29, SIG 3.49 to 3.57, BAK 3.83 to 4.03, SIG drop 0.16 to 0.10, -14.2 LUFS,
  -1.7 dBTP. Not yet heard by anyone but Pietro's A/B clips.
- Delivery (the Reel note of the same day, `decisions-log.md`, applies to Shorts and long videos too): whole passages
  synthesised together (the story engine says each beat in one pass); a beat split sentence by sentence
  (`split=True`) only when the recogniser hears a word wrong in context and rewording cannot fix it; lines written to
  be said (contractions, short sentences, how a person explains it aloud).

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

Drawn beats (16 Nov, YouTube #10; closes the gap of 13 Nov): every `sketch.py` drawing reports its actions read off its
own SVG (`sketch.actions`: a stamp landing, a coin landing, a bar finishing, a marker passage, a shape popping in, a
paper appearing), `youtube.visual()` does the same for the HTML kinds (compare values, list and flow items, counts,
verdict stamps), and `youtube.scenes()` puts the matching sound (`sfx.SOUNDS`: stamp, clink, tock, marker, paper,
hit, softpop) on each action while that visual is on screen. Chapter cards get a low mallet as the title lands plus
their drawing's own sounds, not a ding. Thinned so a drawing never chatters (0.12 s apart at most, 3 marker passages,
3 generic pops). `ep["fx"] = "pops"` restores the old pop-per-visual sound for an exact re-render. Measured by
`python3 build/sfx_sync.py build/youtube_ep<NNN>.py` (both modes on the same script): on #10, key actions with a
sound within 0.15 s 0% (pops) to 99% (action); 2 sounds to 8; on #9's script 0% to 98%.
Stems: `youtube.make` caps the voice stem at a peak of 0.89 (16 Nov: on #10 the RMS-levelled voice peaked at 1.51 and
61 samples clipped in voice.wav).

## 6. Mix and loudness

- Stems: voice, foley, ambience, music. Voice through the narrator chain (`voice.MASTER`, the natural chain of 1b).
- Music ducks about 11 dB while the voice speaks (attack 60 ms, release 350 ms); ambience about 4 dB.
- Target voice over music while speaking: at least 15 dB (measured, `voice_over_music_db`).
- Two-stage loudness: measure, normalise linear with the measured values, true-peak limiter, check, trim if off.
  Long video and Short about -14 LUFS; Reel about -16 LUFS; the limiter ceiling is -1.5 dBTP and a file fails above
-1.0 dBTP. AAC 192 kb/s, 48 kHz.
- Measured on the written files, never assumed from settings: LUFS, true peak, LRA, clipped samples, silences over
  1.2 s, DNSMOS of each master, word errors of the master itself (whole film for short ones, a narrated excerpt
  for long ones). Report: `sound.json` (long videos), `<slug>-masters.json` (`master.dual`).
- Where nobody could listen, say so; the numbers are evidence, not a listening verdict.
