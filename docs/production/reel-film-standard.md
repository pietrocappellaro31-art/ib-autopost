# Reel standard from 27 Nov 2026: fully animated Reels, two a day from 28 Nov

## Pietro, 27 Nov (wins over the rest of this file where they differ)

"We want to start using that voice again [the 12 Nov 'Can shareholders' equity be negative?' Reel] ... for the next
week, we're going to use that voice in all the videos, in all the reels created. Also, make sure we're posting only two
reels a day. I saw the new reel version that you created, which is great, but we don't need subtitles. We don't want
subtitles in the videos. Make sure, at the end of the video, to include an invitation to follow, and make sure that
invitation is not just visual but also verbal." He chose the second slot (12:30 ET) and EMMA on YouTube too.

- **Voice: EMMA** (Kokoro `bf_emma`, speed 0.97, the 12 Nov voice) on every Reel, long film and Short made from 27 Nov to
  4 Dec (`voice_clone.NARRATOR_WINDOWS`; `narrator()`, `youtube_voice()`, `next_voice()` and `story.make` all read it).
  From 5 Dec HEART again unless Pietro extends it; the 4 Dec Reel run reminds him the week ends.
- **Two Reels a day**: slot A 12:30 ET and slot B 18:00 ET (`publish.py` cap 2 per Eastern day). Each slot gets its
  own topic and its own track; at most one of the two is a Trial Reel.
- **No subtitles**: `reel_film.SUBTITLES = False`; `captions()` gives only the screen-text CSS. The band they used
  (screen y 1390 to 1540) now holds the follow ask at the end and is otherwise free.
- **The follow ask, said and shown**: the last spoken line asks for the follow ("... and follow for a new interview
  question every day."; `narration()` refuses a last line without "follow"), and the last shot carries
  `follow_ask(at_word(b, last, "follow", last), d)`: the IB avatar, the handle and a + FOLLOW button that is tapped and
  turns to FOLLOWING, in the 1388 to 1530 band (`film()` refuses a last shot without it). The last shot runs 1.7 s after
  the last word so the tap reads.

Pietro, 26 Nov: "Reels are underperforming. We need, when we post reels from now on, to hide like and share count. We
need to have better storytelling. The music is terrible, so we need to find ways to access trending music and just use
that trending music without having trouble with copyright. I also don't like the blurred background in the videos. From
now on, we're going to try to animate the whole video a lot, so there will not be an image in an image. It will just be
the whole video completely animated. [...] post only one or two reels per day of high quality [...] We need to grow at
least 100 a week." His answers the same evening: one Reel a day; he hides the counts himself in the app; test some Reels
as Trial Reels; YouTube unchanged for now.

This file wins over every older Reel rule that disagrees (the Format A to F card layouts of build/story.py, the black
ground, the scored master, three a day). The other standards (audio, accuracy, AI label, compliance, the follow ask of
23 Nov) still apply.

## What the data said (26 Nov, docs/daily/performance.json)

- Reels split in two: about half stopped at 115 to 145 views (shown only to the first test audience), the rest reached
  800 to 1,800. The ones that broke out held viewers about twice as long (average watch 10 to 16 s against 5 to 9 s).
- On two-Reel days (17 to 20 Nov) 6 of 8 Reels broke out. On three-Reel days (22 to 25 Nov) one or none a day did.
  The account gets roughly one Reel a day pushed; more Reels split the same test audience.
- Slot B (18:00 ET) broke out on 6 of the 7 days it ran. One Reel a day goes there.

## The picture

1. The whole 1080 x 1920 frame is one filmed world, made with `build/reel_film.py` on the cine engine: depth layers, a
   moving camera, rigged people, props that act. No card or panel, no picture inside the picture, no slide headings, no
   black ground. `reel_film.full_frame_check` must pass on every still (it fails the old card-on-ground look).
2. No blur anywhere: depth of field 0 on every shot, every layer noblur (`reel_film.check_shots` refuses otherwise).
3. Numbers live in the world (a board written as the narrator says them, a sheet, coins, a screen) and are inked or
   counted at the moment they are said. One payoff number may be big, but it is the world's number, not a second card.
4. A camera move in every shot; `yt_preview.py --clip` static share 0.
5. Layout bands (screen px): hook text 230 to 650; action and numbers above 1390; the follow ask 1388 to 1530 in the
   last shot (no subtitles since 27 Nov); nothing below 1540 or in the right-hand 150 px column (Instagram's buttons and
   caption). Faces and numbers never under the follow ask.
6. People: invented, no likeness. Each shot gives its figures their own ids (the runtime animates the first id only).

## The story (every Reel)

- 0 to 2 s: the hook is said and shown. A person with something at stake (an interview, a deal, a bill, a bonus) and the
  question, plus a short on-screen promise that clashes with intuition ("An expense that ADDS cash?"). Motion from frame 0.
- The wrong answer most people give, shown and struck out.
- The mechanism, one step per line, each step visible as it is said.
- The turn ("but ..."), then the payoff in one number.
- One line on what it means, then the question back to the viewer (comment bait that loops to the start) and the follow
  ask, spoken in the last line and shown by follow_ask() (23 Nov, said and shown since 27 Nov).
- 30 to 45 s. Delay the payoff to the last third; never give the answer in the first 10 s of the video.
- The caption's first line repeats the hook; the answer may be in the caption body (after "more").

## Sound and music

- The MP4 carries voice (the narrator of the day: EMMA 27 Nov to 4 Dec, else HEART), room tone and action-timed effects only; one clean master at -16 LUFS, true peak at or
  under -1.5 dBTP, recogniser word error 0. No score, no music in the file.
- The music is a trending licensed track attached by Instagram at posting: `python publish.py --audio [words]` (the
  workflow's audio mode, dispatched with `gh api ... dispatches -f 'inputs[mode]=audio'`) writes
  `docs/daily/trending-audio.json`; pick a track there and queue with `--audio-id <id> --audio-title "<title - artist>"`.
  Choose: no explicit words in the title or artist name, a mood that sits under a voice (calm, instrumental-leaning,
  lo-fi, piano, deep house), no holiday novelty outside its season, not the same track twice in seven days. A search
  (`audio_query`, e.g. "lofi", "piano") gives more instrumental choices than the trending list.
- `--music-volume` (default 15 of 100) is one level for the whole Reel; Instagram does no ducking. Raise it only if Pietro
  says the music is too quiet.
- Music on every Reel (Pietro, 26 Nov: "Keep this level from now on and make sure to add the music"): reel_queue.py
  refuses a Reel without `--audio-id` (`--no-music` only if Pietro asks) and stores two backup tracks from
  trending-audio.json. If Meta refuses the track at posting, publish.py tries the backups first; only if all fail does it
  post without music, recording `dropped` in posts.json. Note any replacement or drop in the next quality-log row.
- The level of the 27 Nov reference Reel (build/reelf_depreciation.py) is the floor for every Reel (Pietro, 26 Nov: "This
  is great. Keep this level from now on").

## Trial Reels (Pietro: "test some as trials")

- `--trial` posts a Trial Reel: shown to non-followers first; Instagram shares it with followers if it performs
  (graduation SS_PERFORMANCE). It does not appear on the grid unless it graduates.
- Use it for a risky hook or a new story shape, about two days a week, never two days in a row, never the first Reel of a
  new format. Log which Reels were trials; compare their reach to normal Reels in the quality log.

## Cadence and posting

- Two Reels a day from 28 Nov, slots A (12:30 ET) and B (18:00 ET) (`publish.py` holds a third). 27 Nov had one, in B.
- Hidden like and share counts: Instagram's API cannot set them. Pietro opens each new Reel in the app and taps
  ... > Hide like and share counts. The daily run's message reminds him with the posting time.

## Checks (in place of quality-gates section 9's card checks)

lines wer 0 (takes in `out/<slug>/lines/*.json`), whole-master wer 0, DNSMOS, -16 LUFS and true peak, full_frame_check all
ok, check_shots empty, `yt_preview.py --clip` static share 0, a contact sheet of 16 frames from the MP4 looked at (no
subtitles; the follow ask in the last frames, not over a face or a number), the grid cover preview looked at, caption PASS on ig-human, rights record written.
`entry_check.py` belongs to the old engine (it reads timeline.json) and does not apply.

## YouTube Short copy of every Reel (Pietro, 27 Nov)

`reel_queue.py` runs `build/yt_short_from_reel.py <slug>` after queueing (run it by hand if it printed YOUTUBE SHORT NOT
MADE or LOAD THE TRACK FIRST). The YouTube copy carries a track from Pietro's library (long-form-standard.md FIRST,
item 7): load the track it names from the IB Music Library artifact with the ib-music-access skill, then run
`python3 build/yt_short_from_reel.py <slug> --mood <the Reel's mood>` again. Deliver with each Reel: `build/out/<slug>/<slug>-youtube.mp4` (SendUserFile) and, in the message, the contents of
`build/out/<slug>/youtube.txt` (title, description, tags) and the score's style. Log a row in
docs/daily/youtube-shorts.md ("made from Reel <slug>"). Pietro uploads by hand.

## Reference Reel

`build/reelf_depreciation.py` (27 Nov): one interview room, seven beats, board writing, a desk insert with coins, 44 s,
render about 3.5 minutes on 4 workers. Copy its structure: LINES, one shot function per line timed by `at_word`, events
for the effects, `build()`.
