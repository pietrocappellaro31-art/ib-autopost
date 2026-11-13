# Skill sync: repo skills and installed plugins

13 Nov 2026, cinematic upgrade.

## Which copy is authoritative

The repo copy of each production skill is the one maintained:

| Skill | Authoritative copy | Installed as |
|---|---|---|
| youtube-videos-creator | `docs/skill/youtube-videos-creator/SKILL.md` | plugin `youtube-videos-creator` |
| ib-voiced-reel | `docs/skill/ib-voiced-reel/SKILL.md` | plugin `ib-voiced-reel` |
| music-library | `docs/skill/music-library/SKILL.md` | plugin `music-library` |
| content-compliance | `docs/skill/content-compliance/SKILL.md` | plugin `content-compliance` |
| ig-human | installed plugin only (a general style checker, not IB-specific) | plugin `ig-human`, unchanged 13 Nov: the IB substance checks for captions and titles live in content-compliance |

The installed copies are what a scheduled run loads first. They can lag behind the repo, so every production
skill opens with a line saying the repo copy and `docs/production/` win, and each scheduled-task prompt tells the
run to follow the repo where a loaded copy disagrees.

## Updating an installed skill

1. Edit the repo copy. Keep the frontmatter: `name` equals the folder name, `description` says what is current
   (never a retired rule such as "the day's trial voice" or "YouTube uses GEORGE").
2. `python3 build/skill_pack.py` (or name the skills). It validates each one (name, description, no credentials, no
   retired rule in the description), writes `build/out/plugins/<name>.plugin` (a zip of
   `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md` and a README; version 2.0.0 for the 13 Nov set), and checks
   the archive. `claude plugin validate <dir>/.claude-plugin/plugin.json` on the unzipped folder passes; its only
   warnings (no icon, no marketplace install line) are for the public plugin directory, not for a private install.
3. Send the `.plugin` files to Pietro. **Installing is his step**: he opens each file in Claude and accepts it,
   which replaces the installed plugin of the same name. A session cannot install or overwrite his plugins, and the
   synced skill folder in a session is a read-only cache. Until he installs, a run may load the older copy; the
   repo-wins line and the task prompts cover that gap.
4. Record the version and date in `docs/production/upgrade-log.md`.

## Checks after installing

Start a new session and confirm the skill list shows the new descriptions (HEART, clean and scored masters, rights
classes, disclosure judged per video). If an old description still shows, the install did not take.
