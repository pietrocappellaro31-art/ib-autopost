# Quality gates

Pietro, 13 Nov 2026: his long-form documentary instructions (morning) and the cinematic-upgrade directive (the same
day), merged. Long-form gates first; the Shorts gates in `short-form-standard.md` and the Reel gates in section 9 add to them.

A film is delivered only when every gate passes, or when the delivery message names the gate that did not pass and
why. Every run reports each gate as PASS, FAIL (with what was done) or NOT CHECKED (with why). A number is
evidence, not a verdict on taste: no subjective pass mark is invented here before it has been measured for some days
and agreed by Pietro. Attractive screenshots do not pass a film on their own.

## 1. Facts and sources

- Every material claim is in the episode docstring with its source; every source in the description has a link
  that was opened or returned by a search in the run.
- Fact, anecdote, interpretation and reconstruction are kept apart on screen and in the narration.
- Every number on screen and in the script is checked by a short script against its source (sums, differences,
  multiples, percentages).
- Charts: sourced points only, real units, honest scales, approximate data labelled approximate, no invented
  in-between points, the source named on screen or in the description. Props in a filmed scene (a price list, a
  ledger, a newspaper) show only sourced figures; anything else is illegible or blank.

## 2. Picture

- **Variety test** (before rendering): `python3 build/yt_preview.py build/youtube_ep<NNN>.py` passes
  (`cinematic-standard.md` section 5); the drawing-beside-text share and filmed-beat count go in the log row.
- **Contact sheet**: both thumbnails, every chapter card, the opening, the ending, at least two beats per chapter.
  It must look at least as rich as the previous film.
- **Motion preview**: `python3 build/yt_preview.py build/youtube_ep<NNN>.py --motion` writes a motion sheet per
  chapter (frames 0.25 s apart) and `motion.json` (share of static seconds, longest static run, mean motion, hard
  changes). Look at the hook, one mechanism scene and one later chapter in motion. A filmed beat that does not move
  is a failure even if every still is pretty.
- Reject: missing or black frames, broken geometry, empty compositions, clipped or overlapping text, captions on top
  of the action, things popping in after their sentence ends, dead frames between beats, abrupt jumps, frozen
  characters, limbs bending the wrong way, feet skating, loops that read as loops, fake animation (pans and zooms
  over a still).
- The render's layout check reads 0 (`layout.json`: no text off the frame, under the header or on the caption line);
  the pacing check has no step visual late for its sentence.

## 3. Voice and sound

- Every line word for word in `takes.json`, or the misses named (a real slip is reworded; a recogniser spelling
  difference is taught to `voice_check.words`; a name it cannot spell is logged).
- 12 to 20 seconds of the final mix transcribed word for word.
- DNSMOS of voice.wav (about 3.4 to 3.5 for HEART) and of both mixes (`sound.json`). A mix with ambience, effects
  or music scores lower on DNSMOS by design; that is why the score gate below does not use OVRL.
- Both files: about -14 LUFS (Reels -16), true peak at or under -1.5 dBTP where achievable and never above -1.0,
  no clipped samples, no unintended silence over 1.2 s, both decode to the end (ffprobe duration matches
  timing.json within 1 s).
- Effects tied to their actions (same timing data as the picture); no whoosh on routine transitions.
- **Score gate** (`audio-standard.md` section 3): voice at least 18 dB over the music, DNSMOS SIG within 0.3 of the
  clean mix, 20 s word check within 5%. The gate cannot say whether the music is good: until Pietro has approved a
  `score.py` cue by ear, every delivery calls the scored file a candidate for his judgement.
- Nobody claims to have listened unless a person did. This workspace cannot play audio.

## 4. Files

- 1920 x 1080, H.264, AAC, 24 fps, plays to the end; the render is not called finished until the file exists and
  decodes.
- The SRT matches the narration and its times; transcript.txt matches the script.
- A released film's output is never overwritten: a new cut gets a new slug or a `-v2` suffix.

## 5. Rights, originality, monetisation (content-compliance skill)

- No third-party music, footage, logos, photos or likenesses of real people. Historical figures appear only as
  clearly stylised drawn reconstructions badged RECONSTRUCTION, and are never given a synthetic voice or made to say
  words they did not say or write (quotes are shown as text with their source, and read by the narrator as a quote).
- The script is our own analysis with a point of view, not a template rewrite of a source.
- Fonts, sounds, score, voice model and drawings are ours or open-licensed (`docs/rights/ledger.md`); the rights
  record `docs/rights/posts/<slug>.md` names the narrator, the score and its engine.
- No investment advice, no promised returns, no promised job outcomes; "education, not financial advice" said and in
  the description; sponsorship lines when relevant.
- Monetisation is never promised in a delivery message.

## 6. AI disclosure (checked 13 Nov 2026 against YouTube Help, "Disclosing use of altered or synthetic content",
support.google.com/youtube/answer/14328491)

YouTube asks creators to disclose content that **seems realistic** and was made or altered with AI: a real person
made to appear to say or do something they did not; footage of a real event or place altered; a realistic scene
that did not happen; AI-generated music that is the main focus. It lists as **not** needing disclosure: clearly
unrealistic content, animation ("an AI-generated or altered animation of a missile in a fully animated video"),
cloning one's own voice for voice-overs, and AI help with scripts, thumbnails, titles or infographics. It says
disclosing "won't limit a video's audience or impact its eligibility to earn money", and that creators who
consistently fail to disclose when required may be penalised.

Our films are drawn animation narrated by a synthetic voice that imitates nobody, with no real person shown or
voiced. The page does not address a synthetic narrator of that kind. **Recommendation per film: "Altered or
synthetic content" / "AI use" = Yes**, because it is not clearly excluded, costs nothing in reach or earnings, and
removes the risk. The delivery states that reasoning rather than calling it mandatory, and judges each finished
video (a film with no AI voice may need no disclosure). Re-check the page every month or when YouTube announces a
change; if a film ever includes a realistic reconstruction of a real person or event, Yes is required.

Instagram: Meta asks for its AI label on realistic AI-generated audio such as an AI voiceover; voiced Reels carry
it (`ib-voiced-reel`).

## 7. Audience

The channel is made for a general adult audience. "Made for kids": No, unless a film's content is actually aimed
at children (it should not be).

## 8. Approval and operations

- Nothing is uploaded, scheduled or published by a run: Pietro approves the finished file and uploads it himself.
- Existing episodes still render; generated MP4s, stems and recordings never committed; no secrets in git; logs
  updated; `git pull --rebase`, never force-push; render time and file sizes logged.

## 9. Instagram Reels (Pietro, 13 Nov: the new standards apply to Reels too)

A Reel passes sections 1, 2, 3, 5, 6 and 8 as a film does, adapted to 9:16, plus:

- **Motion in motion**: `python3 build/yt_preview.py --clip build/out/<slug>/<slug>.mp4` (static share, longest static
  run) and a contact sheet of the hook, every level or beat, the transitions and the close. A Reel that reads as
  cards with a push-in fails, as a long video does.
- **Format and story**: the best of formats A to F for the topic (`short-form-standard.md` section 3); the hook in
  the first second; one teaching idea, shown moving.
- **Layout**: safe-area, `clear.json` and `WRAP` at zero; captions never over the action.
- **Voice**: HEART at 0.9, every line word for word in `takes.json`.
- **Sound and masters**: action-timed effects, no whoosh; the clean master at about -16 LUFS, true peak at or under
  -1.5 dBTP; the scored alternative (`python3 build/master.py scored build/out/<slug>/<slug>.mp4 -16 <mood> <mood>`)
  when feasible, measured, never with platform-library or commercial music.
- **Caption**: PASS on ig-human, the substance checks in content-compliance, the AI-narration line; Instagram's AI
  label recommended for the synthetic narrator.
