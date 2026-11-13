"""
Build installable Claude plugins from the repo's skill copies (13 Nov 2026, cinematic upgrade).

The repo copy of each skill, docs/skill/<name>/SKILL.md, is the authoritative one (docs/production/skill-sync.md).
Pietro's installed skills are plugins, one skill per plugin, named like the skill. This script packages each repo
skill as <name>.plugin (a zip with .claude-plugin/plugin.json and skills/<name>/SKILL.md), validates it, and writes
them to build/out/plugins/ (gitignored). Installing is Pietro's step: open the .plugin file in Claude and accept it.

    python3 build/skill_pack.py                      the four production skills
    python3 build/skill_pack.py music-library ...    only these
"""
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ["youtube-videos-creator", "ib-voiced-reel", "music-library", "content-compliance"]
VERSION = "2.0.0"                     # 13 Nov 2026: the cinematic-upgrade versions
SECRET = re.compile(r"(gh[pousr]_[A-Za-z0-9]{20,}|EAA[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|VOICE_KEY=\S{6,})")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("no YAML frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"')
    return fm


def validate(name, text):
    """What the plugin validator checks, plus our own rules: name matches, description present and not stale,
    no credentials, no rule the cinematic upgrade retired stated as current."""
    problems = []
    fm = frontmatter(text)
    if fm.get("name") != name:
        problems.append(f"frontmatter name {fm.get('name')!r} is not {name!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        problems.append("name is not kebab-case")
    d = fm.get("description", "")
    if not d or len(d) > 1024:
        problems.append(f"description missing or too long ({len(d)} characters)")
    if re.search(r"day's trial voice|YouTube uses GEORGE|voice rotates G2", d):
        problems.append("description states a retired rule as current")
    if SECRET.search(text):
        problems.append("looks like a credential")
    return problems


def pack(name, out_dir):
    src = ROOT / "docs" / "skill" / name / "SKILL.md"
    text = src.read_text()
    problems = validate(name, text)
    if problems:
        raise SystemExit(f"{name}: " + "; ".join(problems))
    fm = frontmatter(text)
    manifest = dict(name=name, version=VERSION, description=fm["description"][:300],
                    author=dict(name="Pietro Cappellaro"), license="LicenseRef-Proprietary", repository="https://github.com/pietrocappellaro31-art/ib-autopost")
    out = out_dir / f"{name}.plugin"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(".claude-plugin/plugin.json", json.dumps(manifest, indent=2) + "\n")
        z.writestr(f"skills/{name}/SKILL.md", text)
        z.writestr("README.md", f"# {name}\n\n{fm['description']}\n\nThis plugin holds one skill, built from "
                                f"docs/skill/{name}/SKILL.md in the private repository pietrocappellaro31-art/ib-autopost "
                                f"(version {VERSION}, the cinematic upgrade of 13 November 2026). The repository copy is the "
                                f"authoritative one; docs/production/skill-sync.md explains how the two are kept in step. "
                                f"Setup for production runs: bash build/setup_voice.sh in that repository.\n")
    with zipfile.ZipFile(out) as z:                    # re-open: the archive must list exactly what Claude expects
        names = set(z.namelist())
        assert {".claude-plugin/plugin.json", f"skills/{name}/SKILL.md"} <= names, names
        assert json.loads(z.read(".claude-plugin/plugin.json"))["name"] == name
    return out


if __name__ == "__main__":
    out_dir = ROOT / "build" / "out" / "plugins"
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or SKILLS:
        p = pack(n, out_dir)
        print(f"{n}: valid, {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")
