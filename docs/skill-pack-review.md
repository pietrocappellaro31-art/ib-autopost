# instagram-agent skill pack: review and verdict

Source: github.com/Jakeschincariol/instagram-agent-skill (MIT). 13 skills,
6 local Python tools.

## Install

```
/plugin marketplace add Jakeschincariol/instagram-agent-skill
/plugin install instagram-agent
```

The plugin route is the only one that keeps the 6 Python tools working.

## Safety review

All 13 SKILL.md files and the manifest were read.

- No network calls, no credential handling, no login-on-your-behalf, and no
  hidden instructions in any file.
- Every skill ends by saying nothing is posted; the user posts it.
- `ig-viral` drives an already-logged-in browser at reading volume and
  explicitly forbids crawlers and scraping services. Acceptable, run monthly.
- `ig-human` is honest about its limits: local heuristics, not a detector API,
  and it never claims text is undetectable. Keep that framing.

## Use for this page

| Skill | Verdict |
|---|---|
| ig-carousel | Core. Defers to our brand system instead of inventing a palette. |
| ig-caption | Core. Hashtags capped at 5; search terms in the body matter more. |
| ig-human | Core. Run on every caption before it ships. |
| ig-plan | The weekly session. Note the cadence conflict below. |
| ig-profile | Run once against the bio, name field and pinned three. |
| ig-audit | From month 2, once there are around 30 posts. |
| ig-viral | Monthly research, in Pietro's own browser, with him present. |
| ig-reel | Hook formulas and safe zones only; the rest assumes a spoken script. |
| ig-repurpose | Later, if long-form technical explainers get built. |
| ig-comment, ig-dm, ig-story | Skip. Not in the plan. |

## Conflicts with the agreed plan

1. **Cadence.** `ig-plan` prescribes 4 to 5 posts a week with at least 3 Reels.
   We run 3 a day. The skill's reasoning matches the growth research; Pietro
   chose volume knowingly.
2. **Reel safe zone.** The correct conservative figures on 1080x1920: nothing
   above y=230, nothing below y=1440, and the right 230px clear.
3. **Faceless.** The pack assumes a face, a voice and personal proof numbers.
   We have none by design, so drafts come back with `{{placeholder}}` markers.
   For this page that is correct: never invent a figure or a credential.

## State files

The pack reads and writes `~/.claude/instagram/voice.md`, `swipe.md`, `log.md`
and `plan.md`. Those live on whichever machine runs the session and do not
survive a cloud session. The brand voice therefore lives in
`docs/brand-system.md`, not in `voice.md`.
