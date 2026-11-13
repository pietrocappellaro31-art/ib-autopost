# Audio standard: narrator, score, sound

Pietro, 13 Nov 2026, for long-form YouTube. Read with `long-form-standard.md`.

## Narrator

**HEART: Kokoro ONNX, voice af_heart, speed 0.9, en-us**, for every long video (and every Short, per
`short-form-standard.md`) from 13 Nov 2026: `YOUTUBE_PICK = "HEART"` in `build/voice_clone.py`, HEART at 0.9 in
`build/voices/voices.json`, the default for `youtube.make` and `yt_timing.py`. The daily voice trial is closed and
must not be resumed; its results stay archived in `docs/daily/youtube-voice-trial.md`. If Pietro names a different
narrator later, his newest explicit instruction wins.

- Synthetic, imitates nobody, never cloned from a real person.
- Names said correctly: add any new name to `PHONEMES` in `build/voice.py` (the synthesiser refuses unknown
  words rather than guessing).
- Every line is checked by the recogniser (`yt_timing.py --takes`, `takes.json`). A real slip gets reworded; a
  proper name the recogniser cannot spell is logged, not reworded.
- Never claim the voice was listened to unless a person listened. "Heard word for word" means the recogniser.

## Two mixes, every film

| File | What is in it | When it is the one to upload |
|---|---|---|
| `<slug>-scored.mp4` | voice, sound effects, original score | the recommendation, when it passes the gate below |
| `<slug>-clean.mp4` | voice and sound effects, no music | when the score fails the gate, or Pietro wants to add his own track |
| `<slug>.mp4` | a copy of the recommended one | |

`youtube.mix` writes both; `youtube.sound_report` measures both and picks one (`sound.json`, field
`recommended`). `score="none"` in the episode makes the clean mix only.

## The score

Original, synthesised from scratch by `build/music.py` for each film: nothing sampled, no third-party melody,
chords copied from nobody, nothing for Content ID to claim, no licence needed. Never a commercial song, never a
protected melody or a distinctive arrangement imitated. Pietro's music library songs are commercial recordings and
stay out of every long-video file.

Pick the mood with `score=` in the episode:

| `score=` | For | Settings (`youtube.SCORES`) |
|---|---|---|
| `"reflective"` (default) | history, a story looked back on | 72 BPM, minor, no drums, no bell, level 0.11 |
| `"suspense"` | a crisis, a run, a collapse (controlled, never melodramatic) | 84 BPM, minor, sparse bell, level 0.12 |
| `"light"` | a technical explainer | 96 BPM, major, soft drums and bell, level 0.10 |

The score drops out at each chapter card and is ducked by the voice (side-chain). Pietro found the 8 to 10 Nov
beds "terrible" and "even too dramatic"; the score is therefore kept low and plain, and the clean file always
ships beside it.

**Gate** (`youtube.SCORE_GATE`): the scored mix is recommended only if

- the voice sits at least 18 dB over the ducked music while speaking,
- DNSMOS SIG (the speech itself) of the scored mix is within 0.3 of the clean mix, and
- 20 seconds of the scored mix are heard by the recogniser within 5% of the same 20 seconds of the clean mix.

DNSMOS OVRL and BAK are reported but not used for the gate: the model counts any music under a voice as
background noise (13 Nov, #6 remixed: BAK 4.07 clean, 2.46 scored with the music 24.6 dB under the voice).

**Description line.** Scored: `Music: original score made for this video.` Clean with Pietro's track: `Music:
[song title] by [artist], from the YouTube Audio Library` (fill in, paste the Audio Library's own attribution
text if the track page shows one, or delete the line if none is needed). Any added track must be licensed for
monetised YouTube.

## Sound effects

Sound follows things that happen on screen: a document placed on a desk, coins falling, footsteps, paper, a
clock, typing, a stamp, a mechanical till, news arriving, a quiet confirmation when a calculation lands, period
ambience under a historical scene, a trading-floor bed under a market scene. They support, never distract. No
automatic whoosh, pop or ding on every transition.

Today the engine puts a pop on every beat and every visual change and a ding on every chapter card
(`youtube.scenes`); that is the gap that `cinematic-standard.md` build step 4 (sound on actions) closes.

## Master

About -14 LUFS integrated, true peak at or under -1 dBTP (the second loudness stage), AAC 192 kb/s, 48 kHz,
for both files.
