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

- 14 Nov 2026: ib-voiced-reel 2.2.0 (repo copy and plugin): Pietro's Reel notes (a drawn scene or filmed shot in every beat through question, think and answer, at least two filmed beats, drawings at 85%+ of their box and acting the idea out; HEART kept with a natural delivery and a spoken-style script). Plugin sent to Pietro to install.

## 14 Nov 2026, evening: a natural, unprocessed narrator (Pietro)

Pietro on the cash machine Short: "from tomorrow on voice should feel more natural"; least natural: "robotic / processed sound".

### Built

- `voice.MASTER` (shared by Shorts, Reels, long videos, cine films): highpass 70 Hz and a 1.5 dB dip at 7.2 kHz only. The 8 Nov
  chain (2.5:1 compressor, 19/31 ms echo, warmth boost) kept as `voice.MASTER_8NOV` for exact re-renders.
- `levels.shorts_mix`: no 0.4 pre-limiter by default; every no-music master (Shorts and Reels) runs `levels.two_stage`
  (its default target now -16 LUFS like `mux`, Shorts set -14).
- `levels.mux`: stems written with headroom (peak 0.89), so `voice.wav` never clips.
- `levels.sound_report`: `sig_drop` (DNSMOS SIG voice stem minus clean mix; gate 0.15) and `voice_stem_clipped` (gate 0),
  printed with a CHECK by the Levels and story engines.
- Skills: youtube-videos-creator and ib-voiced-reel 2.3.0 (repo copies and plugins), `audio-standard.md` 1b,
  `short-form-standard.md` 6, `voice-decision.md`, decisions log.

### Checked

Cash machine narration, voice alone at -14 LUFS: old chain OVRL 3.29 / SIG 3.55, new 3.40 / 3.62 (raw Kokoro 3.40); the pre-limiter
had been cutting 16% of the speech (p95 2.2 dB); loudness spread 9.8 dB to 12.4 dB. The Short remixed with the new chain (same picture
and takes): mix OVRL 3.12 to 3.29, SIG 3.49 to 3.57, BAK 3.83 to 4.03, SIG drop 0.16 to 0.10, -14.2 LUFS, -1.7 dBTP, 0 clipped.

### Not done or not verified

- Nobody here can listen. Two 13 s A/B clips (old and new chain, same lines, both -14 LUFS) went to Pietro.
- A naturalness predictor (UTMOS) could not be fetched in this workspace; DNSMOS SIG is the proxy.
- The plugins are updated only when Pietro installs the `.plugin` files.

## 16 Nov 2026: action-timed sound in the drawn beats (YouTube #10)

The 15 Nov next improvement. Before: one generic pop per visual change and a ding per chapter card, whatever the
drawing did (audio-standard.md 5, open since 13 Nov). Now each drawing's own actions are read off its SVG and each gets
a sound at the moment it happens (stamp, coin, bar, marker, paper, card); HTML visuals report theirs too; cards get a
low mallet and their drawing's sounds. Measured with the new `build/sfx_sync.py` on the same scripts: key actions
heard within 0.15 s, #10 0% to 99% (88 actions), #9 0% to 98% (53); sounds used 2 to 8; effects per drawn scene 2.1
to 7.4, the markers at -23 dB under the pops' level. Shown on a timing strip (`build/out/yt-010-salad-oil/sfx_strip.jpg`:
frames 0.25 s apart with the effects that start in each). Also: the voice stem is capped at a 0.89 peak (61 clipped
samples on #10's first mix), and `sketch.receipt` fits a long total and can drop the prices on its coins.

### Not done or not verified

- Nobody here can listen; the sound placement is measured, not heard.

## 17 Nov 2026: one YouTube file with music; a different style of score every video (Pietro)

Pietro: "you're always outputting two videos. I just want you to output the one with the music, and I also want you
to experiment with different kinds of music and not always use the same music." Done the same night, before the next
runs:

- `build/score.py`: seven styles (`STYLES`: orchestral, noir_jazz, solo_piano, ambient, acoustic, mallets, harp), each
  a swap of the instruments that play the same written harmony, an optional drum part (brushes, or a folk kick and
  shaker on GM drum kits), a tempo factor and its own hall; `pick(slug, ...)` avoids every style and key of the last
  three scored videos (`library.json` originals, now with `style`); `master_music` normalises by loudness (RMS 0.08)
  instead of peak, so every style sits about as far under the voice. Measured on one 40 s plan: spectral centroid
  800 Hz (mallets) to 2,080 Hz (noir_jazz), all at RMS 0.079 to 0.080. Until 16 Nov all six scored films were the
  orchestral palette in F.
- `build/youtube.py`: `pick_music` per film (style, key, tempo +-8%), logged in `music.json` and the library;
  `<slug>.mp4` is always the scored mix; a failed score gate lowers the music 3 dB and remixes (up to three times)
  instead of falling back to clean; `trim_loudness` tries a lower limiter when a plucked style overshoots after AAC
  (the harp test: -0.6 dBTP at the first limit). `build/master.py scored` (Shorts) picks and logs a style the same way.
- Tested end to end on #10's stems: harp in G (-14.1 LUFS, -1.3 dBTP, voice 21.9 dB over the music before the
  loudness normalisation, gate passed) and noir_jazz (below in the quality notes of the next run).
- Standards, skills (youtube-videos-creator and music-library 2.4.0), CLAUDE.md and the decisions log say: one file,
  with music, style named in the delivery. The scheduled-task prompts still list the clean MP4: changing a scheduled
  task needs Pietro's approval; CLAUDE.md tells the runs that his 17 Nov decision overrides those steps.
- Nobody here can listen: Pietro's verdict per style decides which stay.

## 17 Nov 2026, YouTube #11 (Herstatt): held life for finished drawings, a 1974 world

- `build/sketch.py` `held_life` (on by default; `ep["held_life"] = False` re-renders #1 to #10 exactly): once a drawing
  has drawn itself, every part boils (re-drawn up to 1.8 px off its place six times a second, independently, the way
  hand-drawn animation keeps a held drawing alive) and the whole drawing sways up to 0.45 degrees about its base. Both
  ease in over half a second after the drawing's last part lands; silent (sounds are read before the layer is added).
  Runtime: `boil` and `sway` in `motion.JS`.
- Measured by `build/held_life_check.py` on #10's own script and timings (79 s of drawn beats, rendered both ways):
  static share 26.5% to 20.2%, mean motion 1.45 to 1.55, longest static run 4 s to 4 s. The seconds still static are
  HTML text visuals (compare, number, list), which the layer does not reach yet: the next step.
- `build/cine_1974.py`: a payments room with two moving wall clocks (Frankfurt and New York) and a printing telex; two
  bank counters either side of the sea with their own clocks and window light; a New York account desk with ledger,
  phone and safe; a settlement desk for payment versus payment; 1974 looks; `sfx.telex`. `sketch.day_bars`: two banking
  days five hours apart on one clock, and the CLS window.

## 18 Nov 2026 (YouTube Short, the raise and the 22% bracket)

- `build/entry_check.py`: the beat-entry gate. For each story beat and the close it finds the paper panel in the beat's
  last frame and compares the panel's ink in the first 0.3 s after the beat lands with the finished drawing; under 20%
  is an empty entry. 17 Nov coin toss Short: 15/24 empty; today's: 0/28. Run it after every story-engine render.
- `sketch.py`: `_pre` (pen-drawn pieces and the trader fully drawn before the swipe), `_trader_poses` (the trader
  changes pose on the words), `_cnt` (counters with separators from 1,000), `_fr`; scenes `tb_*`.

## 19 Nov 2026, YouTube #13 (GameStop 2021): score separation found and fixed, the first present-day sets

- The 18 Nov next improvement said the voice sat only 18.8 to 19.3 dB over the mallets and harp scores (#11, #12)
  against 26 to 29 dB for the orchestral ones, and asked for a measured level per style. `build/score_levels.py`
  measured all seven styles on #13's narration with the film's own voice chain and ducking: 23.4 to 24.4 dB at level
  .22, within 0.6 dB. **The style was not the cause.** The voice's own level is: since 16 Nov voice.wav is levelled to
  RMS .12 but capped at a .89 peak, so the loudest sample sets the whole voice's level (on #13 the cap costs 4.5 dB) and
  it moves from film to film. Fix: `youtube.vom_level` solves each film's music level on its own voice.wav and
  music.wav for `VOM_TARGET` = 24 dB (one probe: the sidechain gain depends only on the voice, so the ducked music
  scales linearly). #13: 22.6 dB at the probe level, level 0.1757, **24.0 dB measured by the score gate**.
  `score.STYLE_LEVEL` keeps the measured per-style probe levels.
- `score.pick` (the other half): the style and key come from a daily rotation by format slot (long 0, Short 1, Reel
  A 2, Reel B 3): `STYLE_ORDER[(4 d + k) % 7]` and `KEYS[(4 d + (k + d) % 4) % 8]`, so the four videos of a day never
  share a style or key even when picked in parallel in different sessions, and none repeats one of yesterday's four;
  the pick is written to library.json at pick time (reserved), and a video already logged keeps its music on a
  re-render. 19 Nov is the transition day (yesterday's picks were random), so #13 sets noir jazz in D by hand.
- `youtube.make` `hook_first=True`: the film opens on chapter 1's first beat (the filmed hook) and chapter 1's card
  follows; YouTube's first chapter stays at 0:00. Number kind `count_d="sentence"`: the count runs across the sentence.
- `build/cine_2021.py`: the first present-day sets (build order step 3): `street_today` (night and day, a billboard
  that takes content, a traffic light that changes), `kitchen_2021`, `ops_room_dawn`; props `phone_screen`,
  `hand_phone`, `laptop`, `notice_screen`, `prints_chart` (sourced prints on a true time axis, dashed where nothing
  is sourced); 2021 looks; a scene across two beats with the second opening on the first's end state (`_fold`).
  `sfx.city_ambience`, `tap`, `buzz`. Filmed render 0.21 to 0.40 s a frame with 2 workers.
