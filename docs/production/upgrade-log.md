# Upgrade log: the cinematic finance studio

What was built, how it was checked, and what it measured. Newest first. Numbers are from files written in the run;
"not checked" says so. Nobody has listened to any of this audio: the build workspace cannot play sound.

## 13 Nov 2026: cinematic-upgrade directive (Pietro)

Started from: the long-form standard committed the same morning (`0b2866e`: clean and scored mixes from `music.py`,
the score gate, transcript, variety test, motion sheets, AI disclosure as a reasoned recommendation) and the Shorts
standard (`0fb455c`: HEART at 0.9). Both were kept; this work was rebased onto them and merged into one rule set
(`docs/decisions-log.md`, top entry).

### Architecture

Remotion was considered and not adopted (`animation-engine.md`): the existing engine already renders the way
Remotion does (HTML and SVG, one deterministic `seek(t)`, a headless browser screenshot per frame, FFmpeg), so a
second toolchain, a React rewrite of the drawings and episode scripts and a licence to track would buy no better
picture. The cinematic layer is `build/cine.py` on the same machinery.

### Built

| Part | Files | What it does |
|---|---|---|
| Camera, depth, light | `build/cine.py` | keyed camera with per-layer parallax, depth of field with an in-focus band, handheld drift, colour grades, vignette, grain, dust motes, steam, flicker; transitions cut, dissolve, flash, iris |
| People | `build/cine.py` rig | articulated figures (hips, torso, head, two-segment arms and legs, hands, shoes), 14 poses, walk with phase from distance (no foot skating), faces (brows, mouth shapes, blinks), breathing, held props kept upright; looks: 1700s coats and wigs, working clothes, dresses, modern suits |
| Sets and props | `build/cine_lib.py` | London 1720 street with crowds and a foreground, a study; newspaper price list (unsourced prices drawn as pen marks), letter with ink reveal, quill, coins, jars, certificate, ledger, candle, cup, phone, card, terminal; `price_line` chart that draws on with flags and sourced points only |
| Foley and ambience | `build/sfx.py` | footsteps timed from the walk cycle, paper, quill, coin clinks, soft mallet, clock; street murmur and room tone; all synthesised |
| Score | `build/score.py` | written notes per section in 11 moods, voice leading, a seeded motif, sampled instruments (GeneralUser GS SoundFont, free for commercial music) via TinySoundFont, a synthetic hall |
| Masters | `build/master.py` | stems, RMS-based balance, ducking, two-stage loudness, clean and scored masters from one picture, every file measured; `scored` CLI adds an original score to a finished clean Short or Reel |
| Long-video integration | `build/youtube.py` | `kind="cine"` beats spliced over their slot with their foley and ambience in both mixes; `score=` now writes the score with `score.py` (fallback `music.py`), level 0.22; scores logged in the music library; music provenance in metadata |
| Previews | `build/yt_preview.py` | variety test (40% rule, three-in-a-row rule, text-only beats, drawing-beside-text share, filmed beats), motion sheets, motion measures for any clip |
| Narrator check | `build/narrator_check.py`, `build/voice.py`, `build/voice_check.py` | 12-line finance regression set; 13 new pronunciations (LBO, IPO, EV, FCF, LTV, JPMorgan, Goldman Sachs, Threadneedle, Garraway's ...) |
| Setup | `build/setup_voice.sh` | fetches the SoundFont (checksum verified) and its licence, installs TinySoundFont |
| Skills | `docs/skill/*`, `build/skill_pack.py` | four skills rewritten or updated; installable `.plugin` packages built and validated (`skill-sync.md`) |
| Music rights | `build/music_library.py` | five rights classes, `mixable()` fails closed, `register_original()` |

### Checked

**Narrator** (`build/out/narrator-check/`, 12 finance lines): HEART 12 of 12 said correctly (3 recogniser spelling
or number-format differences), 2.94 words a second, peak -3.2 dBFS, DNSMOS 3.49 (SIG 3.70, BAK 4.20); GEORGE 3.42 on
the same lines. Not compared by ear with Pietro's reference recording (not available here).

**Proof of concept** (`build/cine_poc_newton.py`, 20.6 s, 1920 x 1080, 30 fps, five shots): rendered in about 5 min
on 2 CPUs (0.52 s a frame). Clean and scored masters at -14.0 LUFS, -1.8 dBTP, no clipped samples, no silences over
1.2 s; the recogniser heard the whole narration word for word in both (WER 0). Voice 18.6 dB over the music and 27.6
dB over the ambience while speaking. DNSMOS OVRL 2.44 clean, 2.06 scored (SIG 3.43 and 3.35): ambience, foley and
music read as "noise" to that model, which is why OVRL is not gated. Motion: no static second in 20 (mean 10.3 grey
levels a second; the lowest second 1.3). A prop that showed two unsourced prices (Bank, East India) was fixed before
the final render.

**Long-video integration** (`build/youtube_cine_test.py`, 22.6 s, 2 chapters, one filmed beat between drawn beats,
`score="reflective"`): the normal `youtube.make` path ran end to end in 4 min 45 s: 5 of 5 lines heard word for word,
layout 0 problems, the filmed beat rendered in 110 s and spliced at 2.8 s, clean and scored MP4 at -14.1 and -14.2
LUFS, -1.4 dBTP, thumbnails, SRT, transcript, description. Score gate: at level 0.32 the voice sat 21 dB over the
score but DNSMOS SIG fell 0.89 and the gate chose clean; at 0.22, 24.2 dB and SIG 3.25 against 3.28, gate passed and
`<slug>.mp4` is the scored file; at 0.16, 27 dB. Default set to 0.22. Motion in the same file: the filmed seconds
(2 to 8) moved 8.7 to 34 grey levels a second; the drawn beats after it were static (under 0.5) in 4 of 13 seconds.

**Short segment** (`cine_poc_newton.py --vertical`, 1080 x 1920, 30 fps, same world reframed): first render had real
framing faults (Newton off the frame in the study, captions over the price tags and jars, the chart cropped to March
to June with its title and sources off the frame); the cameras and a screen-space chart title were redone and the
segment re-rendered (4 min 50 s). Same audio measures as the 16:9 proof. Still weak: the chart is small in the
frame, and the opening title sits over the hawker for half a second.

**Scored alternative for a finished clean file** (`master.py scored` on the proof's clean master): -14.0 LUFS,
-1.8 dBTP, voice 18.4 dB over the music, recogniser heard the scored file exactly as the clean one (WER 0), 50 s.

**Regression**: see the commit message and the quality-log row of 13 Nov for the existing-Short render.

### Not done or not verified

- Nobody listened: the score, the narrator's delivery and the foley balance wait for Pietro's ear.
- The 3/4 view, finger poses, modern sets (trading floor, bank office, boardroom) and the balance-sheet, waterfall,
  LBO and debt-schedule scenes are specified in `scene-library.md`, not built.
- A fully filmed 10-minute film would take 2 to 3 hours to render here; long films stay hybrid.
- The installed plugins are updated only when Pietro installs the `.plugin` files.

## 14 Nov 2026: YouTube #8 (the gold window, 1971)

### Built

- **Thumbnails from the film** (`youtube.film_still`, `youtube.film_panel`; `thumb=dict(film_a=..., film_b=...)`): the shot is built
  as in the film without overlays or captions, a still is taken at a chosen second and laid as a full-height panel on the art
  side of the look, faded into its ground and labelled RECONSTRUCTION. Drawings remain the fallback.
- **Sets, step 3** (`build/cine_1971.py`): `living_room_1971` with a console TV (`tv_screen(items=, quote=)`), `vault_1971`,
  `dealing_room` (split-flap board rows that count on cue, phones that ring), `lodge_1971` (easel that writes on cue); props
  (gold bars, bundles, a generic bill, typewriter, desk phone); looks `suit_1971` to `suit_1971d`, `home_1971`, `lady_1971`.
- **Foley** (`sfx.py`): `ring`, `clank`, `flap`, `office_ambience`.
- **`youtube.patch_span(ep, t0, t1)`**: re-render a drawn stretch of a finished film into both masters when timings are unchanged.
- **Word check** (`voice_check.words`): adviser/advisor, judgement/judgment, Connally/Connolly, spoken decades ("the nineteen
  seventies" = 1970s). Names in `voice.PHONEMES`: Bretton, Triffin, Connally, Kissinger, Smithsonian, Paul, Volcker, IMF, Knox, Bordo.

### Checked

Thumbnails: flat area 57% / 57% against 78% / 78% for #7's drawn ones (8x8 blocks with grey-level spread under 2), edge density
7.2 / 6.2 against 5.4 / 6.6. Film: 165 s filmed out of 593 s (28%, #7 v2 14%); static share 17.2%, longest static run 6 s.

### Not done or not verified

- Nobody listened: the workspace cannot play audio.
- Each patch_span pass re-encodes both masters once more (crf 20): fine for a fix, not for repeated use.
