# Quality gates: long-form YouTube

Pietro, 13 Nov 2026. A film is delivered only when every gate passes, or when the delivery message names the gate
that did not pass and why. Attractive screenshots do not pass a film on their own.

## 1. Facts and sources

- Every material claim is in the episode docstring with its source; every source in the description has a link
  that was opened or returned by a search in the run.
- Fact, anecdote, interpretation and reconstruction are kept apart on screen and in the narration.
- Every number on screen and in the script is checked by a short script against its source (sums, differences,
  multiples, percentages).
- Charts: real units, honest scales, approximate data labelled approximate, the source named on screen or in the
  description.

## 2. Picture

- **Contact sheet**: both thumbnails, every chapter card, at least two beats per chapter. It must look at least as
  rich as the previous film.
- **Motion preview**: at least three 10 to 20 second stretches (the hook, one mechanism scene, one later chapter)
  looked at in motion, as frames 0.25 s apart on a sheet or a short clip. Reject frozen or repeated static
  scenes, broken geometry, things popping in after their sentence ends, and dead frames between beats.
- The render's layout check reads 0 (no text off the frame, under the header, or on the caption line).
- The render's pacing check: no step visual late for its sentence.
- **Variety test** in `cinematic-standard.md` passes.

## 3. Sound

- Every line word for word in `takes.json`, or the misses named (a real slip is reworded; a name the recogniser
  cannot spell is logged).
- 12 to 20 seconds of the final mix transcribed word for word.
- DNSMOS of voice.wav and of both mixes (`sound.json`); the score gate in `audio-standard.md`.
- About -14 LUFS, true peak at or under -1 dBTP, on both files.
- No missing audio: both files decode from start to end (ffprobe duration matches timing.json within 1 s).

## 4. Files

- 1920 x 1080, H.264, AAC, 24 fps, plays to the end; the render is not called finished until the file exists and
  decodes.
- The SRT matches the narration and its times; transcript.txt matches the script.
- A released film's output is never overwritten: a new cut gets a new slug or a `-v2` suffix.

## 5. Rights, originality, monetisation (content-compliance skill)

- No third-party music, footage, logos, photos or likenesses of real people. Historical figures appear only as
  clearly stylised drawn reconstructions, and are never given a synthetic voice or made to say words they did not
  say or write (quotes are shown as text with their source, and read by the narrator as a quote).
- The script is our own analysis with a point of view, not a template rewrite of a source.
- Fonts, sounds, score and drawings are ours or open-licensed (`docs/rights/ledger.md`); the rights record
  `docs/rights/posts/<slug>.md` names the narrator and the score.
- No investment advice, no promised returns; "education, not financial advice" said and in the description.
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
removes the risk. The delivery states that reasoning rather than calling it mandatory. Re-check the page every
month or when YouTube announces a change; if a film ever includes a realistic reconstruction of a real person or
event, Yes is required.

## 7. Audience

The channel is made for a general adult audience. "Made for kids": No, unless a film's content is actually aimed
at children (it should not be).
