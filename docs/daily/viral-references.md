# Viral reference Reels (Pietro, 11 Nov 2026)

Pietro: "These are some examples of high quality reels that went viral. Study these and in the next
days, propose a similar video for each of these. When I say similar, I do not mean the plot necessary
- you can still take inspiration from the plot as well but I would focus more on the design and music
and architecture of the video itself. You are free to experiment. Free to use all the credits you need
to produce a high quality work."

The six videos arrived as downloads on 11 Nov (kept out of the repo: they are other creators' work).
Studied the same day: contact sheets every 2 to 5 s plus close-ups of transitions, cuts counted
(ffmpeg scene detection), every voice transcribed (Parakeet), loudness and the music bed measured.
We copy none of their footage, audio, characters or wording; we borrow structure and design moves,
mapped onto our brand. Every number in a proposal is worked or sourced before it is built.

## How the daily Reel run uses this file

Approved by Pietro on 11 Nov ("I approve your proposal").

From 12 Nov, each Reel run builds the next proposal in the build order below as that day's Reel
(instead of a Levels quiz), with the day's rotation voice, sound effects, no music in the file, and
the usual checks, caption and logs. It records what was built in the table and in quality-log.md.
Pietro picks what stays after the six. If a proposal needs an engine that cannot be finished in one
run, build the engine that day, deliver a Levels Reel as usual, and finish the proposal the next day.

| Order | Ref | Proposal | Status |
|---|---|---|---|
| 1 | R2 | "Same $100. Two ways to pay." (no voice, 12 s loop) | Built 12 Nov: `build/reels_two-ways-to-pay.py`, 12.6 s, delivered alongside Levels #11 (EMMA) so the voice rotation stays intact |
| 2 | R5 | "Same superday. Same answer. One line more." | |
| 3 | R6 | "3 valuation methods" fast colour-block explainer | |
| 4 | R4 | "Britain's loan with no end date" (sourced story) | |
| 5 | R1 | Cartoon riddle with a 10 s countdown | |
| 6 | R3 | Glow-on-black explainer: why $100 today beats $100 next year | |

## What all six share

- **One visual world per video**, held from first frame to last (a building, a dark room with a glow,
  a white desk). Nothing generic: every scene is a picture of the idea.
- **The words on screen are a short top line, not a caption block**: 2 to 6 words at a time, and the
  key word is marked (an italic serif word in R4, a highlight box with selection handles in R6, a
  grey-to-black karaoke in R5, a blue accent line in R5's headline).
- **A picture changes every 2 to 4 seconds** (R1: 23 hard cuts in 88 s; R6: 25 in 57 s; R3 and R4
  have no hard cuts at all: the camera glides and objects morph into the next one).
- **A character or a pair** carries most of them (the short man and Frank the guard, two stick
  figures, Bob, Sarah and Steve, a lone glowing figure).
- **Voice pace about 2.6 words a second** in R1, R3, R4 and R5 (R6 is faster, about 3.5).
- **Loudness about -14 LUFS** on all six.
- **Music**: R2, R3, R4 and R6 carry a continuous bed, loud (the quietest moment of each second sits
  about 22 to 27 dB below the peaks, so the music is close under the voice); R5 a quiet bed; R1 none
  (voice and effects, true silence between lines). R2 is music only, with a strong beat (about 100 BPM
  measured). We cannot name the tracks; Pietro picks a similar sound in the app.
- **The ending asks one specific thing** ("Are you a Sarah or a Steve?", "Did you get it right?",
  "are you waiting for a crash?").

## R1: cartoon riddle in a building cross-section (88 s, voice, no music)

What it does: flat cartoon (thick outlines, pastel walls), a tower drawn in cross-section with a lift
shaft and stairs, floor numbers, a floor counter at the top. Story riddle: a man rides the lift to 10
and walks to 20, except on rainy days. Frank the security guard watches on CCTV (monitor frames,
timestamp overlay). Weather changes the whole palette (sun to rain). Then a pause: two side-by-side
panels with a 10 s countdown ring and "Comment your answer". Reveal through the CCTV: he cannot reach
the 20 button; on rainy days he presses it with his umbrella. Close: "Did you get it right? Follow".
Sound: voice, small effects, silence between lines. Pill-shaped captions (dark, 2 to 5 words).

Proposal (order 5): **"Every January, Mia's gym loses money. And her bank account is the fullest it
has been all year. How?"** Same architecture: a gym drawn in cross-section (front desk, treadmills,
the office with a laptop), Mia's accountant as the watcher, a month counter at the top, winter
palette. 10 s countdown with two panels ("Profit" falling, "Cash" rising) and "Comment your answer".
Reveal on the laptop: members pay a year's fee up front in January; the cash arrives now, the revenue
is earned month by month (deferred revenue), while January's costs land in full. Example numbers
worked in the episode file, nothing claimed about real gyms. New engine pieces: a cartoon character
set (outlined, flat) and a cross-section scene in sketch.py; the countdown exists (findgame.py).

## R2: split-screen race, no voice (10.5 s loop, music only)

What it does: dark ground, a two-word headline ("Same $10K. Two moves."), two stacked panels, the
same stick figure in each. Top: the money goes into a thing that loses value; bottom: into a thing
that pays. Counters tick in red (-$500 a step) and teal (+$1,000 a step) together, the figures react
(slump, cheer), coins drop, a glow, then a two-line moral replaces the headline. No voice: the story
reads in 3 s and loops, which is why it gets rewatched. Music with a strong beat.

Proposal (order 1): **"Same $100 company. Two ways to pay."** Paper ground (or ink, to match R2's
contrast; test both), two panels. Top: a buyer pays $100 all in equity. Bottom: $40 of equity and
$60 of debt. The company is sold for $150 in both. Counters run together: top equity $100 to $150
(1.5x); bottom equity $40, then $150 - $60 debt = $90 (2.25x). The bottom figure cheers, the top one
shrugs; the moral line: "Same company. More debt. Bigger multiple on your money." (and the small
print that debt also raises the risk, so the post stays honest). No voice, effects on every tick,
built to loop at 12 s. Caption carries the worked numbers.

## R3: glow on black, one figure, no cuts (72 s, voice, music bed)

What it does: near-black ground with soft white glow and light grain, white line icons (calendar,
calculator, phone, launch button, jar, staircase, a machine with gears), one small glowing figure.
No hard cuts: the camera pans and zooms through one dark space, objects morph into the next (a snowball
becomes a coin, a line chart becomes stairs). Tiny caps labels on pill tags. Voice calm, music bed
constant. The idea is one metaphor developed to the end (stairs, then the machine).

Proposal (order 6): **"Why $100 today is worth more than $100 next year."** Ink ground with our glow,
teal and red used once each. One figure, one coin. Camera journey: the coin on a calendar, a 10% rate
tag, the coin grows to $110 after a year and $121 after two (worked), then the camera turns round and
walks back: $121 in two years is worth $100 today (discounting), which is what a DCF does to every
year's cash flow. Ends on the machine image of a DCF: cash flows in, today's value out. Needs a
continuous-camera mode in motion.py (one long scene with a moving viewport, no whips).

## R4: data story with a character, light and dark (115 s, voice, music bed)

What it does: "Meet Bob, the worst market timer in history." Real index data drawn as a glowing line
on black; each buy is a dot with a label and an amount; the drop is drawn in red with the percentage.
Every few beats the ground flips to a soft white studio with metallic 3D objects (a savings book, a
vault, shelves holding amounts, a split-flap counter, a stopwatch and hourglass, a pile of newspaper
front pages). A glass-bubble mascot with a face. Words on screen: one short top line, one word in
italic serif. An "honest part" names the source and says Bob is a thought experiment. Ends on a
question to the viewer and a follow line.

Proposal (order 4): **"Britain borrowed £100 from a saver in 1927, with no date to pay it back. In
real terms, it paid back £1.82."** Built from the sources already checked for YouTube #4
(`build/youtube_ep004.py`, source [6], MoneyWeek 2014): the 1917 War Loan slogan ("the investor runs
no risk"), the 1927 roll-over of war bonds into a 4% undated Consolidated loan, the 1932 cut from 5% to
3.5%, and "in real terms GBP 100 lent in 1927 is bought back for the equivalent of GBP 1.82" when it
was repaid in 2015. Careful: the £1.82 belongs to the 1927 loan, not the 1917 War Loan. Every figure
re-checked against the source; the honest part names it, like R4 names its writer. Dark data scenes (a glowing
line for the price of the bond) alternate with light studio objects (a bond certificate, a
split-flap counter going from 100 to 1.82, newspaper pages). Our own mascot idea: a small paper bond
with a face (ours, not theirs). Long for us (about 75 s): test against the 60 s guideline.

## R5: two people, one difference (48 s, voice, quiet bed)

What it does: white page, a serif headline at the top that changes per beat ("Same start date at
McKinsey.", "The difference was tiny.", "One line on top.") with a blue second line, a bold caption at
the bottom lit word by word (grey to black). Flat characters side by side, then UI cards: an email
"Re: the numbers" with a table, the extra line highlighted in yellow, a checklist ticked, a clock
for "waiting to get noticed". Ends on a choice, "Are you a Sarah or a Steve?", the two cards
selectable, then a navy end card with the offer. A number badge for "#2 The one nobody does".

Proposal (order 2): **"Same superday. Same correct answer. Only one got the offer."** Two candidates
(our own flat characters, named for the story; no firm named, no outcome claimed as fact: it is
framed as an illustration). Both answer "Walk me through a DCF" correctly (the steps on a card).
Candidate B adds one line on top: what drives the value and what she would sanity-check (for
example, how much of the value sits in the terminal value). #2: B asks the interviewer at the end
what a strong analyst does in the first month. Close: "Are you A or B?", two cards. Serif headline
top in ink with a teal second line, word-lit caption bottom, paper ground, red only for the miss.
No firm names, so no bank line needed.

## R6: fast colour-block explainer (57 s, voice about 3.5 words a second, music bed)

What it does: the ground colour changes on every beat (black, blue, yellow, white, green, navy), the
top line shows 1 to 3 words with the key word in a box with selection handles (like a design tool)
and a small emoji, faint numbers drift in the background, and each beat has one object: a volatility
chart, falling paper confetti revealing three numbered cards, a spreadsheet filling row by row with
the edited cell outlined, a 3D bar on a grid, a rubik's cube, a debt and equity tank, a briefcase, a
balance scale tipping (cost against value, "+14.5% EPS"). Ends on a mascot. List format: "These 3
financial models".

Proposal (order 3): **"3 ways bankers value a company, in under a minute."** Comparable companies,
precedent transactions, DCF. Ground changes per beat in our colours plus two tints (paper, ink, red,
teal, a pale teal and a pale red); the key word in a selection box; each method gets one object and
one live spreadsheet beat (a comps table filling, a deal list, a DCF row with the discount factor),
and the close is a football field chart drawing the three ranges (illustrative ranges, labelled as
such). Faster voice speed (Kokoro speed about 1.1), a beat every 2 s. Needs: colour per beat (Shorts
already have it), the selection-box word style, a spreadsheet component in motion.py.

## Studied

| Ref | File (upload order) | Length | Cuts | Voice | Music |
|---|---|---|---|---|---|
| R1 | 2ec9b8da | 87.7 s | 23 | yes, story narrator | none, silence between lines |
| R2 | b85f2a23 | 10.5 s | 0 (one scene) | none | yes, strong beat |
| R3 | 1492fbfe | 72.4 s | 0 (camera moves) | yes, calm | continuous bed |
| R4 | 299b5327 | 114.9 s | 0 (morphs, ground flips) | yes | continuous bed |
| R5 | 4aac6e02 | 48.1 s | 3 | yes | quiet bed |
| R6 | ffdfe9cc | 57.2 s | 25 | yes, fast | continuous bed |

The order of the six links Pietro sent is not certain to match the upload order, so the refs are
named R1 to R6 by upload order. Links:
https://www.instagram.com/reel/DezQJ5DIq1r/, https://www.instagram.com/reel/Dff4yiTDgS8/,
https://www.instagram.com/reel/DeaMZ9SosDZ/, https://www.instagram.com/reel/DfXFCjXN6GU/,
https://www.instagram.com/reel/DfOxfoKAFpC/, https://www.instagram.com/reel/DfLF1TVgTXf/
