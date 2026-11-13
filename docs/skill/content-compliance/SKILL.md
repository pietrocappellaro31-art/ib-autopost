---
name: "content-compliance"
description: "Mandatory release gate for every post, Reel, carousel, Short or YouTube video: rights (visuals, fonts, voice model, score, effects), historical accuracy of reconstructions, AI disclosure judged on the finished video, music per platform, originality, financial claims and Pietro's approval before anything is queued or handed over."
---

# Content compliance gate

Source: the team handbook "AI Content on Instagram & YouTube" (reference date 8 Nov 2026). It applies to every piece of content made for @investmentbankinginterviews / @coachingfinance and The Banker's Notebook: carousels, Reels, Shorts, long-form videos, captions, descriptions, thumbnails, comments and DMs.

This skill runs **alongside** ib-page, ib-carousel, ib-caption, ib-voiced-reel, ib-week-plan, ib-month-plan and ib-autopost. It never replaces them. Run it at two points: when a post is planned (stage 1-2) and before it is scheduled, pushed or handed to Pietro (stage 6-8). A post that fails a STOP item is not scheduled, not pushed and not delivered as final.

This is operational guidance, not legal advice, and no check guarantees monetization or reach.

**Updated 13 Nov 2026 (cinematic upgrade).** The authoritative copy is `docs/skill/content-compliance/SKILL.md` in
the ib-autopost repo; the production rules it checks against are `docs/production/*.md`. Older copies of this skill
that allow only P1 or F3 voices, or that make one disclosure setting automatic, are out of date.

## The go / no-go test

Ship only when all six are true:

1. We created meaningful, original value in this specific post.
2. We hold the rights to every element (visuals, fonts, voice, music, SFX).
3. No viewer is materially deceived.
4. Disclosures (AI, sponsorship, affiliate, unaffiliated bank) are correct.
5. Account behaviour is authentic.
6. Pietro has approved the **finished** post, not only the topic.

## Risk levels

| Level | Examples | Action |
|---|---|---|
| STOP | Unlicensed popular music in a master; a real person's voice or face cloned; fake endorsement or testimonial; realistic fake scene presented as real; a reconstruction shown without its badge or with invented dialogue presented as fact; scraped clips; bought engagement | Do not publish. Fix first. |
| REVIEW | Asset or SFX with unknown licence; unverified fact; unclear tool terms; realistic synthetic audio not yet labelled | Get the document or revise, then re-check. |
| APPROVE WITH CHECKS | Original script and design, owned or licensed assets, own-voice clone properly labelled | Proceed after Pietro's approval. |

## 1. Originality (YouTube inauthentic-content risk)

- Each post must carry a distinct question, worked answer and common mistake. A shared series format is fine; template substitution (same narration and visuals, one name swapped) is not.
- Before building, check the topic against `posts.json`, previous `docs/plans/*.md` and recent YouTube uploads. Reject near-duplicates.
- For YouTube long-form and Shorts: the value must be obvious in the first 15 seconds, and the episode must contain authored analysis or a worked example, not a read-out of a generic fact list.
- Never repost or lightly edit third-party clips (news, films, other creators).
- Cinematic production is judged on substance, not complexity: each film needs its own question, research, analysis
  and visuals. A run that reuses a set or a rig is fine; a film that differs from another only by its topic label
  is not.

## 1b. Advertiser-friendly content (YouTube)

- Crises, crashes, fraud and scandals are fine as education: no graphic violence, no gratuitous shock imagery, no
  profanity in titles or thumbnails, no sensational claims the film does not support.
- Title, thumbnail and first 30 seconds match the content; no misleading "you will get rich" framing.
- A sensitive event (a suicide linked to a crash, a war) is mentioned factually and briefly, or not at all.

## 2a. Reconstructions and historical accuracy (13 Nov)

- Every reconstructed scene carries the on-screen badge RECONSTRUCTION; a real person drawn is labelled "our
  illustration" and is not a portrait or likeness.
- No invented dialogue or quotes. A figure may act out what the records say was done; a document on screen
  paraphrases recorded actions and is badged.
- Legends are told as legends (who first recorded them, when). Verified facts, uncertain anecdotes, our
  interpretation and illustrative reconstruction stay distinguishable in the script and on screen.
- Charts: sourced data only, units and sources on screen, approximate values labelled, no invented points.
- No real institution's logo or branding; nothing that implies a bank endorses or produced the video.

## 2. Accuracy and claims

- Every technical answer worked through and checked against a second source (already required by ib-carousel). Dated recruiting claims checked by web search in the session.
- Never invent a figure, statistic, credential, outcome or testimonial. Use `{{placeholder}}` and flag it.
- No income, investment or job-outcome promises. No bank logos, no implied affiliation; when a bank is named, add the educational-and-unaffiliated line.
- Titles, thumbnails, covers and hashtags must match the content. No clickbait that misstates it.
- Captions, titles and descriptions (with ig-human, which scores the style; this gate owns the substance): the
  financial concept stated correctly and plainly; curiosity that the video actually pays off; no fabricated personal
  experience ("when I was an analyst", "my MD told me"); hashtags relevant to the topic, at most the count the
  format allows (Reels 4, long videos 2 or 3, Shorts #Shorts plus 1 or 2); no promised returns, salaries or offers.

## 3. Voice

| Voice | Status | Requirement |
|---|---|---|
| HEART: Kokoro af_heart, 0.9, en-us | **Current narrator for long videos, Shorts and Reels (13 Nov)** | Synthetic, no real person; Kokoro-82M Apache 2.0 (ledger). The narrator never claims to be a person, to have a career or credentials. |
| Other stock Kokoro voices (GEORGE, BELLA, EMMA, MICHAEL, ISABELLA ...) | History; re-renders or Pietro's explicit request | Apache 2.0, synthetic |
| G2 (Pocket TTS from a synthetic sample) | History; re-renders | CC BY 4.0: credit line `Voice model: Pocket TTS by Kyutai` |
| P1, L2, L3, L4 (Pietro's own clones) | Re-renders only | Pietro's consent on record; samples encrypted, never in the repo |
| F1 to F3 (clones of synthetic samples) | Re-renders or on request | Apache 2.0 source, synthetic |
| Any other real person, celebrity or public figure | STOP | Never. Not even as parody. |

Voice-model licence checked once per model and recorded in `docs/rights/ledger.md` (model file, source, licence,
date checked).

## 4. Music and sound

- **No master contains platform-library or commercial music.** A clean master carries voice, effects we own and
  ambience; a scored master adds only music whose rights class (music-library skill) covers that platform: our own
  `score.py` scores are ORIGINAL_GENERATED (sampled instruments from GeneralUser GS, licence permits commercial
  music, ledger). Long videos: clean and scored, the score gate recommends; Shorts and Reels: the clean master is the deliverable
  and a scored alternative is offered when feasible (`build/master.py scored`). A scored file is never called
  approved music until Pietro has heard a score.py cue and said so.
- Instagram: a track may be added in-app by Pietro, only from what Instagram offers his account and only within that licence. Never in a sponsored or paid-partnership Reel unless the track is cleared for commercial use.
- YouTube: only Audio Library tracks (log any attribution) or Creator Music within its YouTube-only terms, added on YouTube or in a YouTube-specific master.
- **Never cross-post an Instagram download to YouTube** or a YouTube download to Instagram. Each platform gets its own upload from the clean master.
- SFX and ambience: every sound used by `build/sfx.py` (Reel effects, foley, street and room ambience) must be
  generated by our own code or carry a recorded licence permitting commercial social use. Unknown source = REVIEW.
- No pitch, speed, chopping or re-recording to get a song past Content ID; no soundalike of a protected song.
- "Royalty-free", giving credit, short length or owning a streaming subscription does not clear a track.

## 5. Visuals and fonts

- Original renders only. Fonts: Source Serif 4 and IBM Plex Sans (both SIL OFL, record once in the ledger).
- No stock images, screenshots, logos or AI images without a recorded licence and the generator's commercial-use terms.
- No photos of real people.

## 6. AI disclosure (judged on the finished video, never a blanket setting)

Check the platform's current rules in the run (YouTube Help "Disclosing altered or synthetic content"; Meta's AI
labelling), then decide per video and give the reason:

| Content | Instagram | YouTube |
|---|---|---|
| Carousel (text graphics, AI-assisted writing) | No label required | n/a |
| Video voiced by a realistic synthetic narrator (HEART) | **Turn on the AI label** (realistic AI voiceover). Caption line `Narration: AI-generated voice; script is our original work.` | Current recommendation "Altered or synthetic content: Yes": a viewer could take the voice for a real person. Description names the AI narration. |
| Clearly drawn 2D animation, stylised reconstruction, badged | Not by itself a label trigger | Not by itself "realistic"; the voice decides (above) |
| A realistic synthetic scene, person or event (photoreal, could pass as footage) | Label + caption line | Yes, required |
| AI-assisted script, research or editing only | No label | Not required on its own |

Disclosure does not reduce monetisation by itself; a missing required one can. Pietro sets it at upload; runs
recommend, they do not tick boxes for him.

## 7. Sponsorships, gifts, affiliates

- Paid: `Ad / Paid partnership with [brand].` in the caption's first line, spoken in video, plus the platform's paid-partnership tool.
- Gifted: `I received this product for free from [brand].`
- Affiliate: `Some links are affiliate links. I may earn a commission.`
- Paid coaching promoted by the page is Pietro's own offer: say so plainly. Never an AI "customer" or invented testimonial.
- A new sponsor triggers a fresh rights and disclosure review.

## 8. Authentic growth (already settled, keep it that way)

No bought followers, likes or views; no pods; no follow/unfollow loops; no automated comments or DMs; no fake personas; no engagement bait. Publishing only through the official Instagram Graph API app in ib-autopost and native YouTube Studio. Tokens never enter a conversation.

## 9. Records (proof of rights)

Keep a rights ledger in the ib-autopost repo, `docs/rights/ledger.md`, plus one block per post in `docs/rights/posts/<slug>.md`:

```
slug / platform / publish date
concept: the unique takeaway
sources checked: links
voice: HEART (Kokoro af_heart 0.9) | <other, licence ref> | none
masters: clean | clean + scored (score.py, ORIGINAL_GENERATED) ; recommended: <which, score gate>
music: none in clean master | IG in-app (added by Pietro) | YT Audio Library <track, attribution> | our score
sfx/ambience: generated (sfx.py) | <file, licence>
reconstruction: none | badged scenes <list> ; real people drawn: <names, "our illustration">
visuals/fonts: original, OFL fonts
AI label: IG on/off, YT setting on/off
sponsorship: none | <brand, terms ref>
approved by Pietro: <date>
```

Never put voice samples, the voice key or tokens in the repo.

## 10. Release checklist (print this in every delivery)

```
[ ] Original value clear; not near-identical to an earlier post
[ ] Facts and numbers checked; no invented figures
[ ] Every visual, font, SFX and voice owned or licensed (ledger updated)
[ ] No platform-library or commercial music in any master; scored master only with ORIGINAL_GENERATED or a covering licence; no cross-platform music reuse
[ ] Voice is HEART (or a recorded exception); narrator claims no personal experience; credit line if a CC BY model
[ ] Reconstructions badged; no invented dialogue; legends labelled; charts sourced
[ ] AI disclosure recommended per platform with the reason (section 6); audience setting stated
[ ] Sponsorship/affiliate/unaffiliated-bank lines present where needed
[ ] Title, cover, caption, hashtags accurate
[ ] Pietro approved the finished post
```

Each line gets PASS, FIX (with what changed) or N/A. Any STOP item ends the run for that post and is reported in one line.

## 11. What only Pietro can do (remind, never automate)

- Turn on the Instagram AI label and the YouTube AI-use setting at upload, and keep a screenshot.
- Add in-app music.
- Weekly: Instagram Account Status and monetization notices; YouTube Studio Checks, Copyright and Channel violations. Also after any unusual spike.
- Claims and strikes: read the notice, compare against the ledger, remove/replace or dispute only with evidence.

## 12. Monthly policy review

At every ib-month-plan session, before planning: ask whether the handbook has a newer version, and remind Pietro to re-read the platform pages it cites (YouTube monetization, AI disclosure, Audio Library, Creator Music, YPP; Meta AI labelling). Record any change in `docs/decisions-log.md` and here.