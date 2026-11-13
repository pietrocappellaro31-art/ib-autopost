# Voice decision

## Current (13 Nov 2026)

**HEART: Kokoro-82M v1.0 ONNX, voice `af_heart`, speed 0.9, language en-us**, for long videos, Shorts and Reels.

- Long videos and Shorts: Pietro, 13 Nov (`short-form-standard.md`; `voice_clone.YOUTUBE_PICK = "HEART"`).
- Reels: Pietro's cinematic-upgrade directive of 13 Nov ("use the same voice for finance Instagram Reels unless an
  explicit approved platform-specific exception exists"; the IG Reel task's own override says the same).
  `voice_clone.REEL_PICK = "HEART"`, so `next_voice()` returns HEART and the 8 Nov rotation stops early.
- Engine files: `kokoro-v1.0.onnx` and `voices-v1.0.bin` from thewh1teagle/kokoro-onnx (model-files-v1.0, MIT code),
  weights from hexgrad Kokoro-82M (Apache 2.0, LICENSE checked 13 Nov on GitHub; the Hugging Face card could not be
  opened from this workspace), misaki dictionaries (Apache 2.0). Synthetic voice; no real person is cloned.
- Measured 13 Nov (`build/narrator_check.py`, 12 finance lines): 12 of 12 said correctly (three recogniser spelling
  or number-format differences), 2.94 words a second, peak -3.2 dBFS, DNSMOS 3.49 (GEORGE 3.42, HEART at 0.97 3.51
  on the same lines). The parallel 13 Nov check: DNSMOS 3.54, about 2.7 words a second.
- **Not verified by ear.** The workspace cannot play audio, and the reference recording of the approved
  configuration was not available, so an auditory match to Pietro's reference is unconfirmed. Pietro's listening
  verdict on the proof of concept is the open item.

## History (kept, not deleted)

| Dates | Where | Voice(s) | Record |
|---|---|---|---|
| 30 Oct | Reels | a neural TTS, rejected; Reels silent | decisions-log |
| 6 Nov | Reels | Kokoro af_heart back; clones of Pietro (P1, L2 to L4) | decisions-log, `voice_log.json` |
| 7 Nov | Reels | L2 and L3 alternate; F1, F2 experiments | decisions-log |
| 8 Nov | Reels | rotation G2, BELLA, EMMA (a one-month test) | `build/voices/voice_log.json` |
| 8 to 10 Nov | YouTube | GEORGE (bm_george) always | `docs/daily/youtube-long.md`, `youtube-shorts.md` |
| 11 to 13 Nov | YouTube | daily trial of 14 Kokoro voices: HEART, MICHAEL, ISABELLA used | `docs/daily/youtube-voice-trial.md` (closed) |
| 13 Nov | everything | HEART at 0.9 | this file |

Encrypted samples of Pietro's own clones stay in `build/voices/*.flac.enc` for re-rendering old Reels only; the key
is never in the repo.

## Changing it

Only Pietro changes the narrator. Record the date and his words in `docs/decisions-log.md`, set the pick in
`build/voice_clone.py`, and update this file and `audio-standard.md`.
