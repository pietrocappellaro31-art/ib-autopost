# Decisions log

What has been settled, and what is still open. Newest first.

## 27 Nov 2026: Pixabay music library in every video

Pietro: use the music library (27 Pixabay tracks, `build/music_library/library.json`, audio in the "IB Music Library" artifact, skill ib-music-access) for all Reels, YouTube films and Shorts, the best-suited track per video, cut to fit, credited in the description ("Music: <title> by <artist> (Pixabay)"). The 8 commercial reference songs are removed and never used.

## Current state, 2 November 2026

- **Meta has blocked the app's API access.** Every workflow run since the first
  successful publish fails with `API access blocked` (OAuthException 200), and
  the developer dashboard redirects to a block page: *"Conferma dell'account
  necessaria. Abbiamo notato attività insolite su questo account sviluppatore."*
  Pietro has to complete identity confirmation to restore access. Likely
  trigger: a brand-new developer account minting a system user token and
  publishing through the API from a cloud IP within hours.
- **One post is live.** `w1-01-statements` published 31 Oct 02:15 UTC, fifteen
  minutes after its slot. The pipeline itself is proven.
- **Thirteen posts are queued**, re-spaced two a day from 3 November so that
  the first successful run after the block lifts does not publish six at once.

## Settled

- **YouTube music from Pietro's library, every video (27 Nov, Pietro).** "Use our library"; source "Pixabay"; Content
  ID risk "OK, keep the licence proof"; then: "Load my music from the private artifact 'IB Music Library' (slug
  331a2c60-239a-4b00-acd3-dffde353a56a). Read files.json and library.json with read_file, download only the tracks you
  need (join any .p00/.p01 parts in order), pick by the video's mood, trim to fit, and credit 'Music: <title> by
  <artist>' in the description." Done: master.library_alternative (cut from calm_start, fades, ducked under speech,
  -14 LUFS, word check; a list of tracks is chained with a 2.5 s crossfade for long films); build/yt_short_from_reel.py
  now picks the mixable track nearest the Reel's mood (not a Short's track of the last 3 days), and `--film` does the
  same for a long film's <slug>-clean.mp4 (<slug>-music.mp4, credits added to description.txt). Tested on the
  depreciation Reel with "Chain Reaction" by Whvle: -14.1 LUFS, -1.8 dBTP, 0 clipped, word check 0, voice 19.6 dB over
  the music. The audio lives only in the artifact and build/music_library/audio/ (gitignored); this repository is
  public, so audio never goes in it. Credits use the track's note ("Music: <title> by <artist> (Pixabay)"). This
  replaces our original score as the YouTube music (the 17 Nov one-file rule now means the library-music file); the
  score stays as the fallback (--score) when the artifact cannot be read. Reels keep Instagram's trending tracks.

- **YouTube from 27 Nov (Pietro): no subtitles, at most 5 minutes, EMMA, spark-yellow thumbnails, Shorts = the Reels,
  "what if" films.** His words: "For youtube please follow these guidelines moving forward: 1. Eliminate subtitles 2. 5
  mins and not any longer than that (current about 10 mins and too long) 3. Use voice from 'can share holders equity be
  negative?' ... 4. Thumbnail with yellow spark color 5. for the short youtube video make sure to use the same reels.
  Simply when you produce the instagram reels, please provide the same description and tabs for youtube." Asked to
  confirm, he added the "what if" series (list in long-form-standard.md "FIRST"). Asked again the same evening he
  chose: keep the .srt for CC; EMMA on YouTube until 4 Dec, then decide; thumbnails on a yellow background only; the
  Shorts' music from our royalty-free library (see the music entry). First reading, now superseded where it differs: (a) no words burned into the picture, the .srt still written for optional CC; (b) EMMA on YouTube with no
  end date ("moving forward"); (c) both thumbnail options yellow: a bright #FFD400 ground, and black with yellow key
  words; (d) the YouTube copy of a Reel carries our original score (the 17 Nov one-file rule; Instagram's licensed
  track never goes to YouTube); what-if films alternate with documentaries from 30 Nov. Done: youtube.SUBTITLES False,
  youtube.MAX_SECONDS 300 (the build stops above it), voice_clone.YOUTUBE_PICK EMMA, youtube.SPARK_LOOKS,
  build/yt_short_from_reel.py (tested on w3-depreciation-cash: -14.0 LUFS, -1.8 dBTP, scored vs clean WER 0; that Reel
  is not delivered as a Short because it predates the no-subtitles rule). The "YouTube Short daily" task stays off.

- **EMMA for a week on every video, two Reels a day, no subtitles, the follow ask said and shown (27 Nov, Pietro,
  after the first full-frame Reel).** His words: "do you remember the reel called 'Can Shareholders' Equity Be
  Negative'? We want to start using that voice again. ... From now on, for the next week, we're going to use that voice
  in all the videos, in all the reels created. Also, make sure we're posting only two reels a day. I saw the new reel
  version that you created, which is great, but we don't need subtitles. We don't want subtitles in the videos. Make
  sure, at the end of the video, to include an invitation to follow, and make sure that invitation is not just visual
  but also verbal." That Reel was w2-levels-11 (12 Nov), voice EMMA (Kokoro bf_emma, speed 0.97). Asked the same
  evening, he chose: the second Reel at 12:30 ET (slot A), and EMMA on YouTube too (long films and Shorts), not only
  Reels. Read as: 27 Nov to 4 Dec inclusive, then HEART again unless he extends it (the 4 Dec Reel run reminds him).
  Done: `voice_clone.NARRATOR_WINDOWS` + `narrator()` (Reels, story.make) and `youtube_voice()` return EMMA in the
  window; `publish.py` caps Reels at 2 per Eastern day (slots A 12:30 and B 18:00 ET); `reel_film.SUBTITLES = False`;
  `reel_film.narration()` refuses a script whose last line has no follow ask and `film()` refuses a last shot without
  `follow_ask()` (avatar, handle, a + FOLLOW button tapped to FOLLOWING); the reference Reel ends on "Tell me in the
  comments, and follow for a new interview question every day." (WER 0 in EMMA, 44.2 s). The scheduled task prompts
  were NOT changed (the change to "IG Reel daily" was refused for lack of permission in that session): their old
  wording (ONE Reel, HEART) is overridden by CLAUDE.md and this entry, and the code makes EMMA, no subtitles and the
  follow ask the default whatever the prompt says. Pending Pietro: the "IG Reel daily" prompt rewritten for two Reels
  a run and moved to 05:47 ET so slot A is queued well before 12:30. The 27 Nov Reel (depreciation, HEART, subtitles, no spoken follow ask) was already
  live at 18:05 ET and is left as it is.

- **The first full-frame Reel is the floor, and every Reel has music (26 Nov, Pietro, after seeing w3-depreciation-cash:
  "This is great. Keep this level from now on and make sure to add the music.").** reel_queue.py now refuses a Reel
  without a track and stores two backups; publish.py tries the backups before ever posting without music.

- **Reels: one fully animated Reel a day, trending music through Instagram, Trial Reels, hidden counts (26 Nov,
  Pietro).** His words: "Reels are underperforming. We need, when we post reels from now on, to hide like and share
  count. We need to have better storytelling. The music is terrible, so we need to find ways to access trending music
  ... without having trouble with copyright. I also don't like the blurred background ... there will not be an image in
  an image. It will just be the whole video completely animated. ... post only one or two reels per day of high quality
  ... We need to grow at least 100 a week." Answers the same evening: one a day; he hides the counts in the app himself
  (the API cannot); test some as Trial Reels; YouTube unchanged for now. Done: publish.py caps Reels at one per Eastern
  day from 27 Nov (26 Nov's slot C still posted), sets `audio_configuration` (Instagram Audio API, tracks authorised for
  third-party use, verified live on 26 Nov: 25 trending tracks returned) and `trial_params` on the container, and has an
  `audio` mode; slot B (18:00 ET) chosen on the data (6 of 7 breakouts; on 3-Reel days only one Reel a day broke out).
  New engine build/reel_film.py and standard docs/production/reel-film-standard.md (full frame, no blur, story shape,
  layout bands, checks); first Reel build/reelf_depreciation.py queued for 27 Nov 18:00 ET with "Breath Between Thoughts"
  (Lucent Hours). The scored master and the card formats are retired for Reels.

- **YouTube Shorts paused for the rest of this week too** (24 Nov, Pietro: "Stop also youtube shorts for this week.").
  The "YouTube Short daily" scheduled task (trig_01FjzT23zvvYe6cudn7gafpL) was disabled on 24 Nov after that day's Short
  (shorts-hedge-own-shares) had been delivered; no Shorts on 25 to 29 Nov. Read as: back on Monday 30 Nov with the long film,
  but nothing switches it on automatically (a one-off reminder to resume it was not created in that session), so it
  stays off until Pietro says to resume it. Instagram (three Reels, one carousel, one Story a day) continues.

- **Every Reel asks for the follow, and the hooks get stronger (23 Nov, Pietro: "Make sure all the reels created
  from today on have a call to follow action. We want to improve conversion rate. Also, we want stronger hooks. We
  want to go viral! We want 1 million views!").** Read as a standing rule for every Instagram Reel from 23 Nov.
  (1) The follow ask in three places: the close's last spoken line ("Answer in the comments, and follow for
  tomorrow's."); an end card on every -16 LUFS Reel (`build/story.py` FOLLOW: the handle, a + FOLLOW button that is
  tapped and turns to FOLLOWING, "A new IB interview question, worked out, every day.", 1.4 s longer than the old
  brand card; make() prints a CHECK if the last close line has no follow ask); and a caption line after the comment
  ask, "Follow @investmentbankinginterviews for a new IB interview question, worked out, every day."
  (`build/reel_queue.py` refuses a caption without "Follow @investmentbankinginterviews"). The caption keeps the
  comment question; the old one-ask caption rule gives way to this. Not "follow for more" (the ig-human lexicon
  marks it as reflex bait): the line says what a follower gets. 23 Nov's Reel A had posted (17:35 UTC) before the
  message, so it keeps its caption (a live post is not edited without Pietro); B and C were re-rendered with the
  spoken ask and the card, their captions carry the line, and they were re-queued at the same slots.
  (2) Stronger hooks, from 24 Nov: the hook standard in `docs/skill/ib-voiced-reel/SKILL.md` ("Hooks, from 24 Nov"):
  the clash on screen from frame 0, a number in the first three words, at most 13 words on screen, five candidate
  hooks written and scored before one is chosen (logged in the episode docstring), topics picked for whether a viewer
  would send them to a friend preparing for interviews, and each hook type tracked against reach in
  `docs/daily/performance.md`. Never an invented statistic to sharpen a hook ("most candidates get this wrong" only
  with a source). Said plainly: 1 million views is the aim, not a forecast. Our Reels reach 120 to 1,600 accounts
  today (performance.md, 22 Nov), so the measure of progress is reach, shares and follows per Reel rising week on
  week; shares are the best lever we have seen (the 63-share equity Reel is our top reach).

- **Weekly usage: Instagram first; the daily long video is paused to Sunday 29 Nov** (23 Nov, Pietro: "How come we
  are already at 29% of usage for this week? Make sure we arrive at Sunday with at least IG covered. ... Prioritize
  and suspend creation of certain content if needed."). Measured from the scheduled runs of 23 Nov (session length as
  the proxy for usage): the long video ran 2 h 53 min, the Short 1 h 33 min, the three Reels 1 h 37 min, each
  dispatch 2 to 3 min. The long video was close to half of each day. Its scheduled task is disabled from 24 Nov, to be
  switched back on on Monday 30 Nov. Three Reels a day, the carousel, the Story and the YouTube Short continue.
  While no new film is made, the Short makes a standalone number puzzle (its own rule when no film has a usable one).

- **This week (22 to 29 Nov): three Reels a day, one carousel a day, one Story a day; Reels must keep posting
  automatically** (22 Nov, Pietro: "Make sure the reels continue to be autoposted. I did not see reels yesterday.
  Remember that for this week we are going for three reels a day, one carousel a day and one story a day.").
  Why there were no Reels on 21 Nov: no Reel was queued for that day. The scheduled tasks of 21 Nov failed with
  "usage limit reached" (the 12:33 and 18:03 ET dispatches, and the Reel run itself made nothing that day); the
  carousels still went out, late, through GitHub's own cron. The pipeline is sound (the 20 Nov Reels posted at 12:36
  and 18:05 ET); what failed is the Claude usage that the daily Reel run needs. Changes: (1) Reel slots A 12:30,
  B 18:00 and a new C 21:00 ET (`posts.json` reel_slots_et; evening Reels have done well: 19:58 1,096, 21:00 1,206);
  C is covered by a new dispatch task at 21:03 ET and by GitHub's 02-03 UTC cron window; `publish.py`
  MAX_REELS_PER_EASTERN_DAY 3; `build/reel_queue.py --slot C`. (2) One carousel a day at 08:00 ET: the 16 queued
  12:30 and 17:30 decks of 22 to 29 Nov were moved, in order, to one a day at 08:00 ET from 30 Nov to 15 Dec
  (`moved_from_utc` keeps the old time), so nothing built is lost and the queue is full to mid December. (3) One
  Story a day: Stories for 26 to 29 Nov added (the chain had ended on 25 Nov). (4) The "IG Reel daily" task makes
  three Reels (A, B, C) through 29 Nov; the "IB carousel weekly build" task fills one carousel a day through 29 Nov.
  After 29 Nov the counts are Pietro's call; until he says otherwise the runs keep this week's counts.
  Risk said plainly: three Reels a day uses more of the same usage that ran out on 21 Nov.
  Scheduled tasks changed on 22 Nov with Pietro's go-ahead (the first attempt from the session was refused by the
  permission check): "IG Reel daily" prompt (three Reels, each queued as soon as it passes), "IB carousel weekly
  build" prompt (one carousel a day plus the Story), and a new "IB reel 21:00 send" dispatch at 21:03 ET.

- **At least 1% better every day; #14 is the bar** (22 Nov, Pietro on YouTube #14, Silicon Valley Bank: "Is actually a
  very good video, very high quality. Continue to increase the quality in the next days. Your goal is to create better
  material every day and improve by at least 1% each day"). Read as: from 22 Nov every daily run (long films first; the
  same spirit for Shorts and Reels) is measured against the previous one of its format, and the quality-log row names
  at least one measured figure that is 1% or more better than the previous film's (motion: static share, windows under
  1.2, lowest 6 s window, mean motion; variety: drawing-beside-text share, filmed share of the running time; sound:
  DNSMOS, voice over score; takes: lines word for word), with no gate going backwards. If a run cannot show it, it says
  so plainly rather than counting a cosmetic change. #14 is the reference for the long films. His praise was for the
  film as a whole; it is not read as a verdict on the harp score in particular.

- **Carousels never run dry: a weekly scheduled task builds the next batch** (19 Nov, Pietro: "Why this carousel is
  not publishing anymore since 2 days? Make sure this carousel is published each day."). Cause: the 10 to 16 Nov batch
  (`build/nov1.py`) was the last one queued, so 17 and 18 Nov had no carousel and no Story; the publisher and the
  dispatch tasks were working and found nothing due. Same failure as 9 Nov; the weekly builder proposed on 10 Nov was
  never created. Fix: (1) `build/nov2.py` queued 21 carousels for 19 to 25 Nov (3 a day, 08:00, 12:30 and 17:30 ET,
  rotation continued by calendar day) and Stories for the same days; (2) a weekly scheduled task "IB carousel weekly build"
  (Mondays 15:23 ET) that builds and queues every day without a carousel through today + 10 days, so the queue always
  has at least 3 days in hand. Creating it from the 19 Nov session was denied (permission), as on 10 Nov; its full
  prompt is in `docs/daily/carousel-weekly-task-prompt.md` for Pietro to create it, or to approve it in a live session.
  Until then nothing refills the queue. A second session answered the same request in parallel; its decks that do
  not repeat a nov2 topic were queued as `build/nov3.py`, 12 carousels for 26 to 29 Nov, so the queue now ends on 29 Nov.
  **Created 19 Nov** at Pietro's go-ahead ("Do it now."): scheduled task "IB carousel weekly build", Mondays 15:23 ET,
  automatic approval, push notifications; first run 23 Nov. Prompt as in `docs/daily/carousel-weekly-task-prompt.md`.

- **YouTube from 19 Nov: number-puzzle Shorts cut from the films; daily films with the effort on the opening minute and
  the thumbnail** (18 Nov, Pietro: "Make this changes starting tomorrow - November 19", on the analytics reading in
  `docs/daily/youtube-analytics.md`; asked how many films a week, he answered "1 a day"). From the 19 Nov runs:
  (1) **Shorts are number puzzles** (Format C or D) for at least the week of 19 to 25 Nov, modelled on the two Shorts
  that travelled (50% down then 50% up: 627 views; the $2.04bn jackpot paid $997.6m: 99): a counter-intuitive result of
  arithmetic, asked as a question in the title and shown as the first frame (no setup before the question), whose maths
  holds in any country (90% of views came from outside the US; no answer that depends on one country's tax, prices or
  lottery). Stories, myths, choices and topical quizzes wait until the week's numbers are read again.
  (2) **Every Short is cut from a long film and points to it.** The Short run takes the newest long film that has no
  Short yet (normally the previous day's) and turns its sharpest number puzzle into the Short, with that film's sources;
  this replaces the rule that the Short's topic differs from the films'. The delivery names the film and tells Pietro to
  set it as the Short's **Related video** in Studio (the Short, Details, Related video), and the pinned comment points
  to it. Every long film is written with at least one such puzzle in it.
  (3) **The long film stays daily**, and the run spends its extra effort on the opening minute and the thumbnail: the
  film opens on the filmed hook with the puzzle or the surprising number on screen within 5 s (no chapter card, title
  or context before it; chapter 1's card comes after the hook); the question the film answers is said by 0:15; the title
  and both thumbnails carry the same number or question; a thumbnail has at most five words and one large number, is
  checked at 168 x 94 px (the size of a search result) and both are offered for Studio's thumbnail Test & compare. The
  first 60 s are written and checked before the rest (opening shots looked at frame by frame, no static second in them).
  These items come before the quality log's "next improvement" on 19 Nov. Changed in the same session: the two scheduled
  task prompts (YouTube Short daily, YouTube long video daily), `short-form-standard.md`, `long-form-standard.md`,
  CLAUDE.md.

- **YouTube: one file, with music; a different kind of music every video** (17 Nov, Pietro: "I don't know why, but
  you're always outputting two videos. I just want you to output the one with the music, and I also want you to
  experiment with different kinds of music and not always use the same music. Update the skill if necessary, do what
  is necessary, but this is what is going to happen from now on."). From 17 Nov, for every YouTube video (long films
  and Shorts; read as both because he said "YouTube video creation"):
  (1) **one MP4 is delivered, the scored one** (`<slug>.mp4`, our original `score.py` score under the voice). The
  clean mix may still be made inside `build/out/<slug>/` as the score gate's reference, but it is never sent, offered
  or described as an option. If the gate fails, the music goes down 3 dB and is mixed again (up to three times,
  `youtube.make`); the run never falls back to a file without music. Description credit: `Music: original score made
  for this video.`
  (2) **the music changes from video to video**: `score.py` now has seven styles (orchestral, noir_jazz, solo_piano,
  ambient, acoustic, mallets, harp: `score.STYLES`), and `score.pick()` chooses one that none of the last three scored
  videos used, with a key none of them used and the tempo moved up to 8%; the choice is logged with the style in
  `build/music_library/library.json` "originals" and in `music.json`. Until 16 Nov every score was the orchestral
  palette in F. Each delivery names the style so Pietro can say which ones he likes; a style he rejects gets removed.
  Reels are unchanged (clean master, Instagram music in the app) unless he says otherwise. Supersedes the "clean and
  scored MP4" delivery of 13 Nov and the "clean master is the one delivered" Shorts rule of 13 Nov.

- **Reel covers are designed for the profile grid** (16 Nov, Pietro: "the cover of the reel is not perfectly readable
  or centred, or both, on the home page ... part of the thing written there is cut"). The grid shows a Reel as the
  middle 3:4 of its 9:16 cover, cutting 240 px top and bottom; the automatic Reels used a frame of the video, laid out
  for the player (header near the top, text kept left of the action rail), so the header was cut and the text sat off
  centre. From 17 Nov `build/reel_queue.py` gives every Reel a cover from `build/reel_cover.py`: the carousel covers'
  style (IB mark and series on top, the question large and centred in Source Serif, level chips for the quiz, handle
  and Watch cue at the bottom), on the Reel's ground, everything inside y 240 to 1680; the render refuses a cover with
  text outside that band and writes `cover_grid_preview.jpg`, the exact tile. The API cannot change the cover of a
  Reel already posted, so the 16 Nov Reel keeps its frame unless Pietro swaps it in the app.

- **Two Reels a day, posted automatically, no approval** (16 Nov, Pietro: "We will post two each days. You won't
  need my approval. You will use your own intelligence to analyze the top performing reels and make improvements if
  necessary. You will decide at what time to post each day - based on the most convenients times for our nieche.").
  Replaces "Reels are scheduled by Pietro in the Instagram app" (2 Nov) and the hand-posted 21:30 Reel.
  How: the daily Reel run makes Reels A and B, queues each with `build/reel_queue.py` (video and cover on a temporary
  `reel/<slug>` branch, never on main); `publish.py` uploads them through Meta's resumable upload with the AI info
  label set at creation (`is_ai_generated`, added to the API 22 Jun 2026), posts the comment question, deletes the
  branch; its own cap of 2 Reels a day, separate from the 3 carousels. Music: our scored master (nobody adds in-app
  music now). Slots: A 12:30 and B 18:00 ET (`posts.json` `reel_slots_et`): published studies disagree (finance:
  early morning and evening; education: late morning; general: midweek afternoons and evenings), the account's own
  data is not yet readable, and these two times are the ones a dispatch reliably covers (12:33 and 18:03 ET; GitHub's
  cron fired about 7 times a day with gaps up to 10 hours, 1 to 16 Nov). The runs move them on evidence from
  `docs/daily/performance.md` (insights recorded daily by the publisher) and log why here. No approval: the
  content-compliance gate decides; a Reel that fails it is not queued.
  **Same day: Meta blocked the app's API access again** (12:33 ET dispatch, "API access blocked", subcode 5258005;
  the 08:06 ET carousel had published). This was before any Reel touched the API. The publisher now records the block
  and stops calling the API except one probe every 6 hours (`api_block` in `posts.json`); while it lasts, Reels are
  delivered for hand posting and nothing is queued. Pietro restores access in Meta's developer dashboard as on 2 Nov.

- **Black background is the rule for Reels AND YouTube Shorts** (16 Nov, evening, Pietro after the black preview of
  Levels #15: "Amazing. Set this as the rule from now on for both IG reels and YouTube shorts."). Black is now the
  default of both engines: `build/levels.py` (`set_theme`, THEMES) and `build/story.py` (the Shorts engine for
  formats B to F) render on black unless an episode sets `theme="paper"` (only to re-render something made before
  17 Nov). On black: no per-part colour grounds (`bg=` is ignored), light text on the ground, bright teal `#5EC8B4`
  for answers and teal words, white cards kept, every drawing (level scenes, story beat art, answer-zone art, hook
  art, the close picture) on a paper panel, filmed windows unchanged, grain in screen mode. Older one-off engines
  (`reels_motion.py`, `reels_two-ways-to-pay.py`, `reels_story.py`) are not used for new work; if one is, render it
  with `theme="ink"`. YouTube long videos (16:9) and carousels are not changed. Supersedes the "colour ground per part"
  of the 10 Nov Shorts and the paper ground of `docs/reel-style.md` for new work.

- **Reels: black background from 17 Nov, same format and quality** (16 Nov, Pietro after Levels #15: "From tomorrow
  on - same exact format and quality but black background please."). Every Instagram Reel renders with
  `ep["theme"] = "black"` (`build/levels.py` THEMES): a black ground (motion.py's own dark page, `#0A0A0A`); what sits
  on the ground turns light (kicker, HUD, level meter, numerals and tails, answers in bright teal `#5EC8B4`, THINK
  bar, close, brand). Unchanged: the format (Levels and formats B to F), the white question cards with ink text, the
  red accent, the filmed windows, HEART, sound, every gate. Each level drawing sits on a paper panel (`#F7F5F2`,
  rounded like the cards), because our drawings are ink on paper and their outlines and labels would vanish on
  black. Scope: Instagram Reels; YouTube Shorts and long videos are not changed by this note. Reels made before
  17 Nov stay on paper. Preview: Levels #15 re-rendered black (`w2-levels-15-black`), sent the same evening.

- **Shorts and every voiced video: a natural, unprocessed HEART** (14 Nov, evening, Pietro after the first cash
  machine Short: "Video looks good but from tomorrow on voice should feel more natural. Make the appropriate updates to
  the skill if and when necessary." Asked what felt least natural, he chose "Robotic / processed sound"). From 15 Nov:
  the narrator chain is a highpass and a 1.5 dB dip at 7.2 kHz only (no compressor, no echo, no limiter before the
  master), stems are written with headroom, and every render reports the SIG drop from voice to mix (gate 0.15) and
  any clipped voice sample (gate 0). HEART and 0.9 unchanged. Applies to Shorts, Reels, long videos and cine films
  (`voice.MASTER` is shared). The delivery rules of the Reel note below apply to Shorts and long videos too.
  Details and measures: `docs/production/audio-standard.md` 1b.

- **Reels: more animated, drawn scenes everywhere, a more natural HEART** (14 Nov, afternoon, Pietro after Levels #13: "From tomorrow on make the reel even more animated and with more images kind of style. Also, the voice should feel more natural." Asked which: drawn scenes everywhere, and keep HEART but fix the delivery). From 15 Nov every Reel:
  (1) **pictures in every beat**: no card is ever text alone. Every level or beat carries a large drawn scene (`sketch.py`, our own illustrations) or a filmed `cine.py` shot, in the question, the think time AND the answer (not a drawing that fades as the answer lands); drawings fill at least 85% of their box; at least two filmed beats per Reel. Our own drawings only: no stock photos, no AI images, no licensed photos.
  (2) **more animation**: the drawings act out the idea (things move, build, split, count) rather than pop in and sit; mean motion above the 1.62 of Levels #13 and no beat with only a push-in.
  (3) **a more natural voice, still HEART** (af_heart, 0.9 unless a listen says otherwise): whole passages synthesised together rather than line by line where the timings allow, natural pauses and emphasis, spoken-style script lines (contractions, short sentences, how a person explains it aloud), fewer read-out constructions. No voice change without Pietro.

- **Reels follow the same cinematic standards** (13 Nov, evening, Pietro: "Do the new standards apply to reels as
  well? They should."). Every Instagram Reel follows `docs/production/` exactly as Shorts and long videos do: the
  cinematic standard (real motion that explains, filmed segments from `cine.py` where a story or a person helps,
  reconstructions badged), the audio standard (HEART at 0.9, action-timed effects, clean master at -16 LUFS plus an
  original-scored alternative when feasible), the quality gates (motion checked in motion, not only stills; facts,
  rights, disclosure judged on the finished Reel) and the formats A to F (the Levels quiz is one of them). The proof
  of concept is the bar. `docs/reel-style.md` stays the Reel's visual base (paper, kinetic type); the cinematic
  standard adds to it. Reel-specific gates: `quality-gates.md` section 9.

- **The cinematic proof of concept is the quality reference** (13 Nov, evening, Pietro, after watching the Newton
  1720 proof (16:9 scored and clean, the 9:16 cut) and the long-video integration test: "This is amazing - this is
  exactly the quality we are looking for."). `build/cine_poc_newton.py` is now the bar every long video, Short and
  Reel aims at: filmed scenes, HEART at 0.9, the `score.py` score under the voice, action-timed foley. This counts
  as his approval of a `score.py` cue, the condition the standards set before calling a scored master more than an
  unheard candidate: from 14 Nov a scored master that passes its gate is offered as approved music, and the clean
  file stays alongside it.

- **Cinematic upgrade: one coherent rule set; older rules superseded, history kept** (13 Nov, afternoon, Pietro's
  "Cinematic finance video production system" directive, arriving after the long-form and Shorts standards of the
  same morning). The finance brand stays independent: another channel was named only as a reference for production
  quality; nothing of it (brand, characters, palette, music, files, schedules, repo) is used or touched.
  What wins now, and what it replaces:

  | Topic | Superseded rule (date) | Rule now | Where |
  |---|---|---|---|
  | YouTube narrator | GEORGE always (8 Nov); a different trial voice each day (10 Nov) | HEART: Kokoro v1.0 af_heart, speed 0.9, en-us; trial closed, its log kept | `docs/production/voice-decision.md` |
  | Reel narrator | G2, BELLA, EMMA rotation for a month (8 Nov) | HEART too (the directive: same narrator for Reels unless Pietro approves an exception); `voice_clone.REEL_PICK`; the rotation's record stays in `build/voices/voice_log.json` | `voice-decision.md` |
  | Voice allowlist (content-compliance) | P1 and F3 only (8 Nov copy) | HEART current; older voices for re-renders; no real person ever | content-compliance skill |
  | Long-video music | none in the file (12 Nov) | a clean MP4 and a scored MP4 with an original score; the gate picks the recommendation; the clean file keeps Pietro's own-track route | `audio-standard.md` |
  | Score engine | `music.py` oscillator beds | `build/score.py`: written notes per chapter mood on sampled instruments (GeneralUser GS SoundFont, free for commercial music); `music.py` is the fallback | `audio-standard.md` |
  | Shorts music | clean only, a scored file only after Pietro likes a bed (13 Nov morning) | clean is still the delivered master; a scored alternative is prepared when practical and offered as unheard | `short-form-standard.md` |
  | Reel music | never in the file | still clean by default (Instagram music in the app); a scored alternative only with an ORIGINAL_GENERATED or LICENSED_FOR_INSTAGRAM score | `ib-voiced-reel` |
  | Music rights | `rights=licence` or not | five classes: REFERENCE_ONLY, ORIGINAL_GENERATED, LICENSED_FOR_YOUTUBE, LICENSED_FOR_INSTAGRAM, LICENSED_FOR_ALL_REQUIRED_PLATFORMS; unknown means REFERENCE_ONLY; `mixable()` fails closed | music-library skill |
  | AI disclosure | tick "altered or synthetic" on every video (8 Nov) | a recommendation per finished video with its reason (currently Yes for our synthetic narrator); Instagram AI label on realistic AI voiceovers stays | `quality-gates.md` 6 |
  | Short and Reel formats | the four-level quiz as the only format | the quiz stays a series; formats B to F (story, concept, calculation, myth, choice) too | `short-form-standard.md` |
  | Long-video visuals | a drawing for every sentence (8 Nov) | visual progression: one evolving filmed scene may carry several sentences; variety test and motion preview | `cinematic-standard.md` |
  | Animation engine | `motion.py`, `levels.py`, `sketch.py` only | plus `build/cine.py` (camera, depth layers, articulated people, light, action-timed foley) on the same browser renderer; Remotion considered and not adopted | `animation-engine.md` |

  Proof of concept rendered and measured the same day (`build/cine_poc_newton.py`, 20.6 s, both masters at -14.0
  LUFS and -1.8 dBTP, every word heard by the recogniser in both). Nobody has listened to it: the workspace cannot
  play audio. Pietro's verdict on the narrator, the score and the motion is the open item.

- **Long-form YouTube is a cinematic documentary, to a written standard** (13 Nov, Pietro's permanent instructions
  for long videos, adopted as the standard the same day; no new film made that day). Written into
  `docs/production/` (long-form, cinematic, audio, quality gates); they override the YouTube skill for long videos.
  Changes from the earlier rules: (1) **narrator**: HEART, Kokoro af_heart, speed 0.9, en-us (set the same day by the Shorts standard,
  `YOUTUBE_PICK = "HEART"`, for long videos and Shorts; the trial log stays as history);
  (2) **music back, as a second file**: every film ships a clean MP4 (voice and effects) and a scored MP4 with an
  original score from `music.py` in a mood that fits (`score=` reflective, suspense or light), recommended only if it
  passes a gate (voice 18 dB over the music, DNSMOS SIG within 0.3 of clean, 20 s word check); this reverses the
  12 Nov "no music in the file" rule for the scored file only, and the clean file keeps Pietro's own-track route;
  (3) a visual plan per beat before rendering, a variety test, a motion preview, five title candidates,
  transcript.txt; (4) AI disclosure is a reasoned recommendation, not an automatic Yes: YouTube Help (checked 13 Nov)
  asks for it on realistic content and exempts animation; synthetic narration is not addressed, disclosure costs
  nothing, so the recommendation is Yes with that reason. The engine cannot yet do articulated characters,
  environments with parallax, a camera, lighting or sound tied to actions: `cinematic-standard.md` lists the build
  order, one step per daily run.

- **Pietro's music library for YouTube** (12 Nov, Pietro: "Create a skill that will attach all these
  audios to a library ... used for the creation of both YouTube shorts and YouTube video. The video
  should pick from the library the most appropriate music."; on the rights question: "Find a way
  around - we just want to use the music, not their videos."). The 8 songs he sent (Einaudi's
  Experience, Flawed Mangoes' Swimming and Missing Pieces, GOTH, Luminary, the Bloody Mary slowed
  instrumental, Ethereal slowed, the September instrumental loop) are commercial recordings, so the
  lawful way around is: never in our file, never in git, never edited to dodge Content ID. Each one
  is analysed (`build/music_library.py`; `library.json` committed, audio gitignored) and every video
  picks the song closest to its `mood`. A Short gets the song first in the music block, added with
  "Add sound" in the YouTube app (licensed for Shorts) from its calmest stretch. A long video gets our
  own `music.py` bed written in the song's tempo, key, mode and feel (no melody, chords or audio
  taken). A song with a real licence on record can be set to `rights=licence` and mixed in. Skill:
  `docs/skill/music-library/SKILL.md`; the YouTube skill points to it.
- **No "That's level 4. Keep score." on any video** (12 Nov, Pietro: "'That's level 4, keep score' is
  useless and should be removed from all videos." Then: "Keep it in mind for tomorrow."). From the
  13 Nov runs, every Levels hook (Reels and YouTube Shorts) says and shows the last question alone;
  the close still asks for the score. On a Short the hook drawing sits centred under the question
  and larger (about 600 px wide; `levels.py` centres it when the hook has no lines). Today's Short
  (shorts-cent-doubled-30-days) was delivered with the old hook and is not re-rendered.
- **Reel hooks are the question alone** (11 Nov, Pietro: "From now on eliminate from all reels
  'That's level 4, keep score'. This part is not needed."). The Levels hook says and shows only the
  last question (plus the small "4 interview questions. Each one harder." line); the close still asks
  for the score. Applied to Levels #10 before delivery (53.9 s, was 56.1). Extended to YouTube Shorts
  on 12 Nov (above).
- **Six viral reference Reels to study** (11 Nov, Pietro): one proposal per reference over the next
  days, modelled on their design, music and structure more than their plot. Links and status in
  `docs/daily/viral-references.md`. Instagram blocks automated fetching, so the study needs the
  videos (screen recordings or downloads) from Pietro. Videos received and studied the same day;
  six proposals and a build order written in that file. **Approved by Pietro (11 Nov: "I approve
  your proposal")**: from 12 Nov each daily Reel run builds the next proposal in order, with the
  day's rotation voice (none for the R2 loop), until all six are done; then Pietro picks what stays.

- **3 carousels a day, built and queued weekly** (10 Nov, Pietro: "post three
  times a day from now on", then "increase from 2 a day to 3 a day" and "build
  and queue now"). Slots 08:00, 12:30 and 17:30 ET; the hand-posted Reel at
  21:30 ET is on top, so the feed carries 4 posts a day plus the Story.
  `publish.py` cap raised to 3 with a 17:30 default slot. A third Claude
  scheduled task at 17:33 ET could not be created from the 10 Nov session
  (permission denied); until it exists, the 17:30 carousel goes out on the
  GitHub cron (runs every 10 minutes 22:00 to 23:59 UTC) or, at the latest,
  with the 18:03 ET Story dispatch. Why it was needed:
  the week-1 queue ended on 8 Nov and the monthly plan that was meant to start
  on 9 Nov was never built (the planning task only runs on the first Monday),
  so 9 Nov had no carousel. To stop that recurring, a weekly scheduled task
  that builds and queues the next 7 days every Thursday is proposed; it could
  not be created on 10 Nov (permission denied) and needs Pietro's go-ahead.
  First batch: `build/nov1.py`, 10 to 16 Nov. Cover rotation restarted at
  day 1 on 10 Nov for the three carousel slots. The live bio still says "Two
  questions a day"; Pietro to change it by hand.

- **Monthly planning session: first Monday of each month, 9:00 ET** (set 2 Nov,
  replacing the weekly session). Claude proposes the month's topics, slots,
  times and cover colours, asks personalisation questions, then builds and
  queues the month after approval. Runbook: `docs/skill/ib-month-plan`. A
  scheduled run starts 8:35 ET so the draft is ready at 9:00. Each plan runs
  to the Sunday after the next first Monday, a one-week buffer.
- **Carousels are triggered by Claude scheduled tasks** (2 Nov) at 08:03 and
  12:33 ET daily, because GitHub's own cron started only about 20 runs in
  three and a half days. The tasks call workflow_dispatch, which GitHub labels
  "Manually run"; that label does not mean a person did it. The GitHub cron
  stays on as a backup. Fully independent option still open: an external
  cron service with a fine-grained token.
- **Comment replies are fully automatic** (2 Nov). A daily job in the private
  repo `ib-comments` drafts every reply with Claude and sends it, technical
  ones included. Coaching and collab questions get a standard reply pointing
  to DMs and are listed in a weekly report issue. Risk controls instead of a
  human check: one run a day, a reply cap that ramps 10 then 20 then 30 a day,
  random pauses between replies, skips spam and emoji-only, stops on any
  rate-limit or block error.
- **Reels are scheduled by Pietro in the Instagram app** with trending audio,
  from files and a schedule delivered at the monthly session. The Planned tab
  route was re-asked on 2 Nov and is still not possible.
- **Week-1 queue kept** (option A, 2 Nov): it runs 3 to 8 Nov and the monthly
  plan starts 9 Nov.
- **Voiceover is back** (6 Nov, Pietro's call, reversing 30 Oct). Kokoro-82M,
  voice `af_heart` (warm, confident, kind), run locally by `build/voice.py`
  with misaki's own pronunciation dictionaries; unknown words fail loudly and
  get hand-written phonemes. Mixed to -16 LUFS, -1.5 dB true peak, so music
  added in the app sits under it. **Every voiced Reel must carry Instagram's
  AI label**: Meta requires it for realistic AI voiceovers.
- **Sound effects are the standard on every Reel** (6 Nov, Pietro's call,
  after Levels #1). Synthesised in `build/sfx.py` (no licensing), mixed under
  the voice and under the music Pietro adds. Reels without voice now ship
  with an effects track rather than silent. Same day: the whoosh on swipes is
  retired (Pietro found it annoying, the only one), and more effects are
  welcome: pops when a level number, chip or score lands, ticks when the
  meter fills and the score spins, a soft ding on the brand. Levels #1, its
  cloned-voice cut and #2 were remixed without it (`levels.remix`).
- **Voice cloning: Pietro's own voice only** (6 Nov). Cloning a real
  person's voice is possible here (Kyutai Pocket TTS run locally through
  sherpa-onnx, about 20 to 30 seconds of clean reference audio; weights CC BY
  4.0, credit Kyutai). Its terms forbid cloning anyone without their explicit
  consent, so cloning a public figure (the JPMorgan CEO was asked about) is
  ruled out: it would be impersonation. Pietro's own voice, or someone who
  has explicitly agreed, is fine. Until a recording arrives, Reels use `af_heart`.
  Checked 6 Nov against Kyutai's own model card (huggingface.co/kyutai/pocket-tts):
  licence CC BY 4.0, which allows commercial use with credit; prohibited uses
  include cloning without explicit and lawful consent and presenting generated
  audio as a genuine recording, so the AI label stays on. Tested on Kyutai's
  sample voice: a take can drop or add a word, so `voice_clone.py` transcribes
  every line (`voice_check.py`) and retakes it until the words match, and the
  reference must be cut at a pause (`prepare_reference`). When a cloned-voice Reel ships, its
  caption ends with the credit "Voice model: Pocket TTS by Kyutai".
  First clone from Pietro's own recordings (6 Nov, two memos, 55 s and 25 s,
  quiet room, no clipping). Measured with a speaker-ID model (WeSpeaker, in
  `voice_check.similarity`): two real recordings of Pietro score 0.89, a
  different voice about 0.5, the clone 0.74 to 0.83, so it reads as him.
  Reference length made no difference (11 s, 22 s and 47 s references all
  averaged 0.74 to 0.75), so longer recordings do not help this model; the
  delivery and recording conditions of the sample are what it copies. The
  transcript check uses Parakeet (6% word error on Pietro's real voice, where
  Moonshine tiny misheard him), and every line is spoken after a throwaway
  "Okay." that is cut, because the model swallowed first words. Sentence
  timings for a cloned voice come from the recogniser's word times (a real
  voice's pauses are too irregular for Kokoro's pause matching). Levels #1
  in the clone: 13 of 13 lines word-perfect, 21 of 22 caption onsets within
  0.15 s, likeness 0.82 against a held-out real recording.
  Refined 6 Nov with three longer memos (about 4.5 minutes, seven delivery
  styles). `voice_refsearch.py` cut them into 12 windows of 14 to 20 s,
  cloned the same lines from each and scored them against real speech from
  the other memos (real against real across memos: 0.92). Best: the quiz-host
  window from the first new memo (0.785 likeness over 8 takes and the
  fewest slipped words; one story window scored 0.80 but slipped more), against 0.71
  for the first memo's sample on the same test), now the reference for quiz
  formats. Levels #2 is the first Reel voiced with it. Pietro's recordings
  and references stay out of this public repo.
- **Pietro's real voice is now a third option** (6 Nov). He reads a Reel's
  script in one memo; `voice_real.py` transcribes it with word timings,
  aligns the script, cuts each passage, shortens pauses over 0.45 s to 0.3 s
  and hands the passages to the Reel engine (`real:/path/to/memo`). No AI
  label needed. Measured on the same 34 held-out clips of his real speech:
  real-voice Levels #2 0.914 and #3 0.901, the cloned Levels #2 0.867, the
  first clone 0.794, the stock Kokoro voice 0.551. A second reference
  search over 13 memos (34 windows) found nothing meaningfully better than
  the last one (0.794 against 0.784, within take-to-take noise of about
  0.04): the clone has plateaued, and only the real recording closes the gap.
  The real reads run longer (Levels #2 71 s against 62 s cloned) because
  Pietro speaks more slowly than the clone.
- **Every Reel is voiced in Pietro's clone, alternating two voices** (7 Nov,
  Pietro's call): L2 (the Levels #2 voice) and L3 (the Levels #3 voice), one
  then the other, to test which goes more viral; a named voice overrides the
  rotation. The record is `build/voices/voice_log.json`. The procedure is the
  `ib-voiced-reel` skill (copy in `docs/skill/ib-voiced-reel/SKILL.md`).
  Clarity: both clones were duller than his real recordings (less presence
  above 4 kHz, more mud at 150 to 500 Hz); each now gets an EQ curve matched
  to his real voice (tone gap 2.8 to 1.2 dB for L2, 2.2 to 1.3 dB for L3,
  likeness unchanged), a light de-esser and gentle compression. The two
  samples are encrypted in `build/voices/`; the key is in the claude.ai
  Project (`claude/voice-samples-key.md`), and `build/setup_voice.sh` sets up
  a fresh session.
- **Captions are burned in, word by word**, on every voiced Reel, because most
  people watch muted.
- **Reel style: kinetic typography on paper** (3 Nov), modelled on a
  reference Reel Pietro chose. The standard is `docs/reel-style.md`; every
  Reel from now on follows it.
- **One automated Story a day: question of the day** (3 Nov), 18:00 ET.
  Each story answers yesterday's question and asks today's, so the chain
  gives people a reason to come back. Rendered by `build/stories.py` (questions
  and worked answers live there), queued in `posts.json` as `type: story`,
  published by `publish.py` outside the two-carousel daily cap. The API cannot
  add polls, links or other stickers, so the image carries everything. The
  monthly plan includes a story per day, and the chain must never end on an
  unanswered question.
- **Highlights are manual** (3 Nov): the API cannot manage them. Three, in
  this order: Start here (red), Question of the day (ink), Dates (paper,
  recruiting timeline). Covers are in brand; Pietro adds each daily story to
  Question of the day with one tap, or weekly from the Archive.
- **Every post gets an engagement question in the comments** (3 Nov).
  Carousels: `first_comment` in `posts.json`; `publish.py` posts it as the
  page's own comment right after publishing, and records `first_comment_id`
  (or `first_comment_error`, never failing the run). Needs
  `instagram_manage_comments` on the token. Reels: the question is delivered
  with each Reel for Pietro to post when he uploads. Questions are specific to
  the post and answerable in a line, never "comment YES" bait.
- **Cover colours rotate, palette does not** (2 Nov). Slide 1's ground follows
  a diagonal rotation of red, ink and paper so the grid is not one colour.
  Chosen over rows or columns because no evidence ties grid layout to reach,
  and a diagonal stays mixed when a post is late or missing.
- **Daily cap enforced in code** (2 Nov). `publish.py` publishes at most 2
  manifest posts per Eastern day, and no more than the slots already passed
  that day (the day's scheduled times plus 08:00 and 12:30 ET). Backlog after
  an outage drains two a day, oldest first, at slot times, instead of going out
  in one run. The third daily post is the hand-uploaded Reel, which never goes
  in the manifest. Hard caps: 2 posts on Mon 2 Nov, 3 a day from Tue 3 Nov.
- **Cadence: 3 posts a day.** Was 2 a day, raised on 2 Nov. The researched
  recommendation was 7 to 8 a week with Reels for reach; Pietro chose volume.
  Flagged twice, decided twice, no longer an open question.
- **Carousels are automated, Reels are manual.** The Content Publishing API has
  no draft or scheduled state, and the Business Suite composer has no
  `input[type=file]` to target, so nothing can be placed in Instagram's Planned
  tab. Pietro uploads the Reels himself and adds a trending track, which the
  API cannot do and which matters more on that format than anything else.
- **Synthetic voiceover rejected** (30 Oct). A neural TTS voice was built and
  the quality was not acceptable. Reels now ship silent and read-paced.
- **Follow/unfollow growth abandoned** on terms-of-use and ban risk.
- **AI label** only for realistic generated imagery, not for designed graphics.
- **Faceless, brand-only.** Not tied to Pietro personally.
- **Visual identity:** palette G, fonts A. See `brand-system.md`.
- **Format and fonts stay identical across the whole account.** Standing
  instruction.
- **Co-founder and partner:** Emanuele Sesia. Pietro wants the page on his
  LinkedIn as co-founder, and a LinkedIn company page first.

## Open

- **Posting times are hypotheses, not findings.** 08:00 and 12:30 Eastern for
  carousels, 21:30 for Reels, reasoned from how each format is ranked rather
  than measured on this account. Re-time from the account's own insights after
  two or three weeks.
- **Distribution reality check.** The account had 2 followers when 21 posts a
  week were scheduled. Carousels reach existing followers; Reels reach
  non-followers. If the manual Reel session slips, the carousels are mostly
  talking to an empty room.
- **Collabs are the strongest untried lever.** A Collab post lands on both
  grids and reaches both audiences. Candidates: other prep accounts of similar
  size, university finance societies, student investment clubs.
- **Alt text** is not settable through the publishing API. Add in-app on the
  posts that matter.
- **Experiment: a woman's voice made from Pietro's own** (7 Nov, Pietro's
  request, awaiting his pick). `build/voice_feminise.py` raises the formants
  (spectral envelope warp) and the pitch of one of his samples, and Pocket TTS
  clones the result, keeping his delivery. No real woman's voice is used, so
  there is nobody else's consent to get; the AI label still applies. Three
  candidates were put in a lineup: A calm (about 182 Hz, the clearest, 4% word
  errors over 8 takes), B bright (215 Hz, 10%), C warm (202 Hz, 9%); his male
  clone runs about 11%. A full Levels #3 in voice A: 14 of 14 lines
  word-perfect, pitch 154 to 210 Hz by passage. A feminised voice can drift
  back towards a male pitch in some takes, so `CloneVoice(min_pitch=...)`
  retakes any take below the floor.
  Pietro's verdict (7 Nov): not there yet; one sounded Indian, the Reel was
  too fast with an "h" breath before words, and not clear enough. Measured on
  the same three lines (6 takes each): voices made from his voice slipped 22
  to 28% of words; the same clone engine given a clean synthetic woman's
  sample (Kokoro af_heart, Apache 2.0, the voice he liked on 6 Nov) slipped
  3%. The clone also spoke at 3.0 to 3.4 words a second against his own 1.9
  to 2.3. New voices F1 (af_heart sample) and F2 (af_heart and af_bella
  blend): 16 flow steps instead of 8, every take slowed to 0.76 with
  rubberband (pitch and tone kept), a pitch floor, and a presence EQ matched
  to the clean sample. Levels #3 in F1: 14 of 14 lines word-perfect, 13 on the
  first take, pitch 170 to 192 Hz throughout, 2.6 words a second. Trade-off:
  F1 and F2 are no longer made from Pietro's voice, and nobody real is
  cloned. Awaiting his pick; L2 and L3 stay the rotation until then.
- **A third clone of Pietro, L4, from five new memos** (7 Nov, about 7.5
  minutes, read in a quieter setting: noise floor -75 to -84 dB against about
  -60 before). The new memos sound different from the earlier ones (likeness
  between them about 0.80 against 0.90 among the earlier ones), so every
  sample was judged against both sets. 21 windows searched; L4 is the 21 to
  41 s window of the first new memo. Levels #4 voiced in L4: 14 of 14 lines
  word-perfect; likeness 0.86 to the new memos and 0.83 to the earlier ones,
  where L2 and L3 score about 0.86 to the earlier memos and 0.79 to 0.81 to
  the new. Tested on the same lines, L4 slipped fewer words than L2 and L3.
  L4 also gets 16 quality steps, a pace matched to Pietro's (every take
  slowed to 0.82; he reads at about 2.3 words a second, the raw clone at
  about 3) and its own tone match. Not in the L2/L3 rotation until Pietro
  says so.
- **One default voice, and a female voice on request** (8 Nov, Pietro). P1, cloned from
  Pietro's own read of the Levels #1 script (levels-1-pietro-voice.mp4, first 20.6 s), is
  the voice of every Reel and YouTube video from now on; the L2/L3 alternation ends
  (`next_voice()` returns P1). F3, cloned from the Levels #1 Reel voice (levels-1.mp4, the
  synthetic Kokoro af_heart voice, nobody real), is used only when Pietro asks for a female
  voice. Both run at 16 quality steps with a tone match measured against the original
  recording; F3 is also slowed to 0.84 (the raw clone read 4.1 words a second against 3.5)
  with a pitch floor of 165 Hz. P1 is encrypted like L2 to L4; F3 is synthetic, kept plain.
- **"The voice is no good" (8 Nov), measured.** DNSMOS (Microsoft's speech
  quality model, 1 to 5) on whole tracks: Pietro's first memos 3.3; the L2
  and L3 Reels 3.33 and 3.26; Levels #4 and #5 in L4 2.84 and 2.80; F1 2.74;
  the stock Kokoro voices 3.27 to 3.54. Two causes: the five 7 Nov memos score
  low themselves (3.02 and 2.83, consistent with phone noise reduction), and
  slowing takes with rubberband costs quality. P1's sample comes from a clone,
  not a raw recording. Free voices from the web are only usable when no real
  person is cloned, so the licence-clean pool is Kokoro's own voices (Apache
  2.0); eight were auditioned (`voice-audition.mp4`), all 0 to 3% word errors,
  DNSMOS 3.27 to 3.54. Rights recorded in `docs/rights/ledger.md`.
- **Reels rotate three voices for a month; YouTube is GEORGE; daily automation** (8 Nov,
  Pietro). From the 8 Nov auditions: Reels alternate, one per Reel and in this order, G2
  ("E, slower": Kokoro bm_george read at 0.82, re-spoken by Pocket TTS, 8 exact takes per
  line, the most consistent kept), BELLA (Kokoro af_bella, bright and warm, US) and EMMA
  (Kokoro bf_emma, British, calm), for one month; then Pietro picks one from the results.
  `next_voice()` runs the rotation from `build/voices/voice_log.json`. YouTube long-form and
  Shorts always use GEORGE (Kokoro bm_george, British, measured). All four are synthetic;
  no key is needed. P1 and F3 end as defaults. Three scheduled tasks now make the content
  every day, posting stays manual: YouTube long video and YouTube Short (6:35 and 6:40am New
  York, ready by 7) and the IG Reel (8:16am, ready by about 8:30). Each delivers in its own
  task thread, logs to `docs/daily/`, and starts from the previous run's "next improvement"
  in `docs/daily/quality-log.md`. New long-form engine: `build/youtube.py` (1920x1080,
  chapters, captions, sound effects, -14 LUFS, thumbnail, description with chapter times).
  YouTube rule checked 8 Nov: an AI voice that does not imitate a real person needs no label
  on its own, and the label does not affect earnings; we tick "altered or synthetic" anyway.
  The monetisation risk is "inauthentic content" (mass-produced, template-identical), so
  every video carries original, sourced analysis and varies in structure and visuals.
- **YouTube visuals: a drawing on every beat** (8 Nov, Pietro: "the visuals were much
  better in the other YouTube videos ... quality should go up, not down, and the videos
  should include as much visuals as possible"). The first `youtube.py` test was text-led.
  The engine now draws a hand-made scene for most sentences (`build/sketch.py`: clocks,
  bricks, dominoes, charts, figures, stamped documents, towers and more, drawn on in time
  with the voice), keeps the icon, timeline, flow, stamp and quote layouts, opens each
  chapter on a red card with a drawing, and outputs two thumbnails and an .srt, like the
  Lehman and 100% videos.
- **Music on every YouTube video, made by us** (8 Nov, Pietro: "always put some viral
  music in the background"). Trending songs are copyrighted and would be claimed by Content
  ID (revenue to the rights holder, or blocked), so `build/music.py` makes an original
  track for each video in the trending style (vi-IV-I-V loop, four-on-the-floor kick,
  clap, off-beat hats, pluck arpeggio, bass, sidechain pump, 96 to 118 BPM; the seed
  varies key, tempo and pattern). It drops out at chapter cards and is ducked under the
  voice; mixed at -14 LUFS. Long-form always; Shorts with `music=True`. Instagram Reels
  are unchanged: no music in the file, Pietro adds it in the app.
- **YouTube music is piano and cello, dramatic; Shorts get pictures and colour** (10 Nov,
  Pietro on the first Short: "The music is terrible, we are not at a lunapark. We prefer
  piano or cello. Something more dramatic. Also, make the video more engaging with
  pictures and colors and more animated"). `music.track()` now writes a slow minor-key
  piece (66 to 80 BPM, piano ostinato with left-hand octaves, a cello line in its low
  register from bar 3, a soft low drum every fourth bar, hall reverb), synthesised from
  scratch like before; the pop style is retired (`track_pop()`, re-renders only). Sample
  libraries were not an option in the build environment, so the instruments are modelled
  (additive piano with stretched, decaying partials; bowed cello with body resonances and
  late vibrato). Voice sits about 16 dB over the bed while speaking at the default level.
  Shorts now carry a colour ground per part, a drawing in each level's answer zone, coins
  drifting at the edges and an animated close (`levels.py`: `bg`, `art`, `art_after`,
  `floaters`; `sketch.py`: coin, pricetag, receipt, card_tap, lineup, last_coin;
  `motion.py`: coinflip). Instagram Reels keep the paper ground and no music unless
  Pietro says otherwise.
- **The penny Short is the standard; viral music only through YouTube's library** (10 Nov,
  Pietro: "The quality of the video is much better - that is what we are gonna use as
  standard from now on. For the music, try to find the most viral ones and use it. This
  was even too dramatic."). Every Short matches or beats `shorts_penny-one-year.py`
  (colour grounds, drawings, motion). Viral songs are copyrighted, so they never go in our
  file: Shorts ship with voice and effects only and each run suggests two or three sounds
  trending on Shorts that week, which Pietro adds with "Add sound" in the YouTube app at
  upload (licensed for Shorts). Long-form keeps an original bed, lighter than the 10 Nov
  piano and cello (warm, mid tempo, not dramatic), or an Audio Library track Pietro adds.
  Pietro agreed (10 Nov): he adds the music in the YouTube app himself; every Short
  delivery gives him clear step-by-step music instructions (template in the
  youtube-videos-creator skill, section 7).
- **Long-form music is the warm bed; drawings fill their boxes** (10 Nov, YouTube #3). Following Pietro's
  note that the piano and cello was "even too dramatic", `music.track()` now writes a warm, mid-tempo,
  major-key bed (soft electric piano, pad, round bass, soft kick, rim and shaker, sparse bell; 88 to 100
  BPM), ducked under the voice (20.1 dB below it while speaking on #3). The piano and cello is kept as
  `track_drama()` for re-renders. `youtube.py` now zooms each drawing onto what is drawn (`fitSketches`),
  puts a drawing on thumbnail B, checks the 16:9 layout during the render (`layout.json`) and writes
  `sound.json` (voice over music, DNSMOS, loudness) on every render. Waiting on Pietro's view of the new bed.
- **Where the AI label and the music are (10 Nov, Pietro: "I cannot find how to add the AI
  label and music").** The phone upload flow may not show the AI question; it is set in
  YouTube Studio on a computer after upload (Content, Shorts, the Short, Show more,
  "Altered content", or Attributes, "AI use", in newer Studio). The sound button is on the
  Shorts editor screen reached with "Next" after the trim screen; YouTube Help says library
  audio on uploaded videos is limited to 15 second clips. The music template in the
  youtube-videos-creator skill now says both.
- **Source links in every YouTube description; tags go in Studio, hashtags in the description** (10 Nov,
  Pietro: "since my channel is verified, make sure to add links to the sources and references").
  Episodes list `sources=[(label, url)]`; `youtube.describe()` writes a "Sources and references" list
  with links, the chapters, the disclosure lines and the episode's `hashtags` (2 or 3). The `tags` list
  is for the Tags field in Studio (Details, Show more), pasted by Pietro; `redescribe(ep)` rewrites
  description.txt without a re-render. Applied to YouTube #3 the same day.
- **YouTube voice trial: a different voice every day** (10 Nov, Pietro: "From now on for the
  YouTube videos you will experiment with different voices. A different one each day, until
  we find the perfect one. All the other rules stay the same. Starting tomorrow."). From 11
  Nov the day's long video and Short share one voice from `voice_clone.youtube_voice()`, in
  the `youtube_trial` order in `build/voices/voices.json`: 14 Kokoro voices (Apache 2.0)
  auditioned on 10 Nov, US and British, male and female, each set to about GEORGE's pace. The
  Reel voices stay out of it. The list repeats until Pietro picks; then `YOUTUBE_PICK` is set
  and the trial ends. Each delivery names the voice and asks for his verdict; the log is
  `docs/daily/youtube-voice-trial.md`. GEORGE is the baseline. Everything else is unchanged.
- **Long videos: no music in the file, Pietro adds it; thumbnails change look every day** (12 Nov, Pietro:
  "the music is terrible. From now on, I will add the music myself. You will provide me with a line to fill
  in the description to give credits for it", and "make sure to provide thumbnails of different colors and
  styles each day"). `youtube.mix` now ships voice and effects only (`music=False` default; `music=True` keeps
  the `music.py` bed for old re-renders), and the description carries `Music: [song title] by [artist], from
  the YouTube Audio Library` for him to fill in or delete. `youtube.THUMB_LOOKS` holds seven thumbnail looks;
  each day uses two, never one from the day before. YouTube #4 remixed without music (mix DNSMOS 2.48 to 3.20)
  and #5 re-rendered without music in the new looks the same day.
- **Shorts production standard; HEART is the YouTube narrator** (13 Nov, Pietro sent the permanent Shorts
  instructions). Saved as `docs/production/short-form-standard.md`, which every Shorts run reads first. Pietro
  chose (13 Nov): install it as the standing rules (no remake of the day's Short); HEART (Kokoro af_heart,
  en-us, speed 0.9) for long videos and Shorts, so the daily voice trial ends (`YOUTUBE_PICK = "HEART"`, HEART
  speed 0.97 to 0.9; the trial log stays as history); one clean master only, with an original-scored master
  waiting until there is a `music.py` bed he likes. New in the standard: formats B to F beside the
  four-level quiz, 35 to 55 s for most Shorts, two alternative titles, a QA report, music suggestions only when
  verified, and the AI setting and audience judged on the actual video. Checked the same day: no Remotion or other
  engine in the repo, no `docs/production/cinematic-standard.md` or `audio-standard.md`; the standard says so
  and builds new formats on `levels.py`, `motion.py` and `sketch.py`. A one-line check of HEART at 0.9: word for
  word, DNSMOS 3.54, about 2.7 words a second.
