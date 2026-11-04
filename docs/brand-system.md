# Brand system

Instagram: **@investmentbankinginterviews**. Display name: Investment Banking
Interviews. Faceless, brand-only. Niche: IB interview prep. PE content is
phase two.

The handle shipped once on nine slides as a working name and was caught only
by inspecting the live account. Check it on every render.

## Profile

- **Name field:** Investment Banking Interviews. This is what Search matches on.
- **Bio (140 chars):**
  Accounting, valuation, DCF, LBO, M&A.
  Two questions a day, with the answer and the common mistake.
  For summer analyst recruiting and beyond.
- **Profile picture:** red field `#D93A12`, white "IB", black full stop,
  Source Serif 4 700, letters about 330px on 1080. Live on the account.
- **No disclaimer line.** If a post names a bank, add one caption line. Never
  use bank logos.
- **Facebook Page** "Investmentbankinginterviews" exists and is linked. It is
  plumbing for Business Suite only. Cross-posting from Instagram is on.

## Visual system

- **Colours:** paper `#F7F5F2` for body slides, ink `#0A0A0A`, red `#D93A12`,
  teal `#0F766E`. Red marks the mistake or the warning. Teal marks the correct
  answer. Teal was chosen over green because red and green is the one pair
  colourblind readers cannot separate.
- **Reels use the paper ground** from 3 Nov 2026, in the kinetic style in
  `docs/reel-style.md` (red for the mistake, teal `#0F766E` for the fix).
  Earlier Reels inverted the palette with teal `#5EC8B4` on ink.
- **Fonts:** Source Serif 4 700 for headlines, IBM Plex Sans 400 to 600 for
  body, and Source Serif 4 italic (400, 600) for the tail of a Reel lockup.
  Nothing else. Adobe's own files, SIL Open Font License. The woff2 files are in `build/fonts/`.
- **Colour rhythm across a carousel:** cover, contrasting stake, paper body
  slides, ink recap, red call to action. It makes the swipe feel designed.
- **Cover ground rotates** from November 2026 (week-1 covers are all red).
  Diagonal cycle, one grid row per day: day 1 red / ink / paper, day 2 ink /
  paper / red, day 3 paper / red / ink, for the 08:00, 12:30 and 21:30 posts.
  The stake slide never matches the cover; the CTA is red unless the cover is.
- **Grid crop:** the profile grid shows a 3:4 crop of slide 1, about 34px off
  each side. The 76/80px padding clears it.
- **Per slide (1080x1350):** 76/80px padding. Header pinned top with the IB
  mark, the series name and `NN / TT` in the accent. Content centred. Footer
  pinned bottom with the handle and a Swipe or Save cue.
- **Keyword colouring:** one key term per headline in teal. The headline ends
  in a red full stop or question mark.
- **Pills:** teal "The answer", red "Common mistake".
- **Diagrams, not decoration.** Every question slide carries a diagram of the
  mechanism. No stock imagery: it adds copyright exposure and reads as filler
  on a technical page.
- **Reels (1080x1920):** nothing above y=230 or below y=1440, and keep the
  right 230px clear for the action rail.

## Rendering, hard-won

- **Header and footer must be `position:absolute`.** An inline
  `position:relative` on the footer overrides the class, drops it into the
  flow, and collides with the body text.
- **Chromium's `--window-size` yields a viewport about 80px shorter than
  asked.** Render carousels at 1080x1500 and crop to 1080x1350; render reels at
  1080x2100 and crop to 1080x1920. Without this every slide silently loses its
  bottom padding, which is invisible on a pale ground.
- **Verify the bottom edge programmatically**, not by eye. `brand.check()`
  samples the row above the edge and fails if it is not flat.
- **Bar charts normalise their heights.** The label sits under the bar in the
  same column, so a raw height near the container height pushes the column past
  it and the tallest bar breaks out of the card.
- **JPEG only, quality 92.** The Content Publishing API rejects PNG.

## Content rules

- Series: Technical of the Day (carousel), Recruiting Playbook, Fix the Answer,
  Superday Drill (Reel), PE Corner (phase two).
- Every technical answer is worked through before it ships. Never invent a
  number, credential, outcome or statistic. Use a `{{placeholder}}` and flag it.
- **No em dashes**, on slides or in captions. They are the clearest machine
  fingerprint in written English.
- No engagement bait. Hashtags capped at 5 since 18 Dec 2025, and search terms
  in the caption body do more work.
- AI label only on realistic generated imagery. Designed graphics need none.

## Caption quality bar

Every caption runs through `ig-human` and must score **PASS** on the five-check
panel before it ships. Two traps found the hard way:

- **Spelled-out numbers do not count as concrete markers.** The specificity
  check counts digits and proper nouns, so "three steps" scores nothing and
  "3 steps" scores. First drafts of six captions came back FLAGGED on
  specificity alone for this reason.
- **`20x` fails the number pattern**, because there is no word boundary after
  the digit. Write "20 times".
- Burstiness measures sentence-length variation. Evening out sentence lengths
  while fixing something else drives it down, so re-check it after any edit.
