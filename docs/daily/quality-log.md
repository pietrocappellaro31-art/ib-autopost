# Quality log

Each daily run reads this file first, makes the one improvement it names as
next, measures the result, and adds a row. The point is that every day is
measurably better than the last (Pietro, 8 Nov).

Measures: **DNSMOS** (overall speech quality, 1 to 5; clean studio speech is
about 3.1 to 3.5), **exact lines** (lines the recogniser heard word for word),
**range** (intonation, semitones, F0 10 to 90 percentile), **safe-area**
problems, **loudness** (LUFS, true peak), and any note from Pietro.

| Date | Run | Voice | DNSMOS | Exact lines | Range st | Safe-area | Loudness | Improved today | Next improvement |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-08 | IG Reel | G2 | 3.29 | 13/13 (2 re-said) | | 0 after chip fix | -16.4 LUFS, -1.4 dBTP | First Reel of the rotation | Short verdict lines ("Nothing.") came out unclear in G2 on the first pass: check them first and redo early |
| 2026-11-08 | YouTube long (test) | GEORGE | 3.34 | | | 0 | -14.3 LUFS, -1.5 dBTP | Drawn scene on most beats, red chapter cards, 2 thumbnails, .srt, original music bed | Go to 8 to 12 minutes and add new sketch scenes for the topic |
| 2026-11-09 | IG Reel | BELLA | 3.34 voice / 2.87 mix | 23/23 (each line cut from the final voice track and transcribed on its own) | | 0 after shortening the hook and the level 4 answer | -16.2 LUFS, -1.5 dBTP | Short verdicts ("Five.", "No.", "Two dollars.") checked alone first: all heard exactly. Kokoro renders had no takes.json; now written per line from the final track. Hook kept short so it sits in 3 lines (a hyphenated hook broke badly over 6) | DNSMOS on the mix (2.87) is well below the voice alone (3.34), so the effects and room tone under speech cost quality: duck the SFX bed by about 6 dB while the voice is speaking and re-measure the mix, aiming for 3.1+ |
