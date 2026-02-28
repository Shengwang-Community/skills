#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$REPO_ROOT" <<'PY'
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
skills_root = repo / "skills"

if not skills_root.exists():
    print("ERROR: skills/ directory not found")
    sys.exit(1)

skill_files = sorted(skills_root.rglob("SKILL.md"))
md_files = sorted(skills_root.rglob("*.md"))

errors = []
skill_names = []

for path in skill_files:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        errors.append(f"{path}: missing YAML frontmatter")
        continue
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        errors.append(f"{path}: unterminated YAML frontmatter")
        continue

    fm = "\n".join(lines[1:end])
    name_match = re.search(r"^name:\s*(.+?)\s*$", fm, re.MULTILINE)
    desc_match = re.search(r"^description:\s*", fm, re.MULTILINE)
    author_match = re.search(r"^metadata:\s*(?:\n[ \t]+.+)*\n[ \t]+author:\s*(.+?)\s*$", fm, re.MULTILINE)
    version_match = re.search(r"^metadata:\s*(?:\n[ \t]+.+)*\n[ \t]+version:\s*(.+?)\s*$", fm, re.MULTILINE)

    if not name_match:
        errors.append(f"{path}: frontmatter missing 'name'")
    else:
        skill_names.append((name_match.group(1).strip().strip('"').strip("'"), path))
    if not desc_match:
        errors.append(f"{path}: frontmatter missing 'description'")
    if not author_match:
        errors.append(f"{path}: frontmatter missing 'metadata.author'")
    if not version_match:
        errors.append(f"{path}: frontmatter missing 'metadata.version'")

name_to_paths = {}
for name, path in skill_names:
    name_to_paths.setdefault(name, []).append(path)
for name, paths in name_to_paths.items():
    if len(paths) > 1:
        errors.append(f"duplicate skill name '{name}': " + ", ".join(str(p) for p in paths))

link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
skip_prefixes = ("http://", "https://", "mailto:", "docs://")

for path in md_files:
    text = path.read_text(encoding="utf-8")
    for raw_target in link_re.findall(text):
        target = raw_target.strip()
        target = target.split(" ", 1)[0]
        target = target.split("#", 1)[0]
        target = target.split("?", 1)[0]
        if not target:
            continue
        if target.startswith(skip_prefixes):
            continue
        if target.startswith("#"):
            continue

        if target.startswith("/"):
            resolved = repo / target.lstrip("/")
        else:
            resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: broken link -> {raw_target}")

if errors:
    print("Validation failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print(f"Validation passed: {len(skill_files)} skills, {len(md_files)} markdown files checked.")
PY
