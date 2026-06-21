#!/usr/bin/env python3
"""Validate the end-to-end-loop skill repository without third-party deps."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"`?(references/[A-Za-z0-9_.\-/]+|handoff/[A-Za-z0-9_.\-/]+|scripts/[A-Za-z0-9_.\-/]+)`?")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md must start with YAML frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail("SKILL.md frontmatter must end with ---")

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            fail(f"Unsupported frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, "\n".join(lines[end + 1 :])


def check_frontmatter(root: Path, text: str) -> None:
    data, body = parse_frontmatter(text)
    allowed = {"name", "description"}
    extras = set(data) - allowed
    if extras:
        fail(f"Only name and description are allowed in SKILL.md frontmatter: {sorted(extras)}")
    name = data.get("name", "")
    description = data.get("description", "")
    if not NAME_RE.fullmatch(name):
        fail(f"Invalid skill name: {name!r}")
    if name != root.name:
        fail(f"Skill name {name!r} must match folder name {root.name!r}")
    if not description:
        fail("description is required")
    if len(description) > 1024:
        fail(f"description is too long: {len(description)} > 1024")
    if len(body.splitlines()) > 500:
        fail("SKILL.md body should stay under 500 lines")


def check_required_files(root: Path) -> None:
    required = [
        "SKILL.md",
        "references/phase-checklists.md",
        "references/test-and-security.md",
        "references/adapters.md",
        "references/evaluation.md",
        "references/report-template.md",
        "scripts/validate_skill.py",
        "handoff/hermes-devboss-brief.md",
        "handoff/hermes-market-research-prompt.md",
        "AGENTS.md",
        ".hermes.md",
        ".github/workflows/validate.yml",
    ]
    for rel in required:
        if not (root / rel).is_file():
            fail(f"Missing required file: {rel}")


def check_references(root: Path, text: str) -> None:
    missing: list[str] = []
    for match in REF_RE.findall(text):
        if not (root / match).exists():
            missing.append(match)
    if missing:
        fail(f"Referenced files missing: {sorted(set(missing))}")


def check_policy_terms(root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    safety = (root / "references/test-and-security.md").read_text(encoding="utf-8")
    phase = (root / "references/phase-checklists.md").read_text(encoding="utf-8")
    adapters = (root / "references/adapters.md").read_text(encoding="utf-8")
    combined = "\n".join([skill, safety, phase, adapters])
    required_terms = [
        "CAVEMAN",
        "live deploy",
        "explicit",
        "CI",
        "rollback",
        "Hermes",
        "AGENTS.md",
    ]
    for term in required_terms:
        if term not in combined:
            fail(f"Required policy term missing: {term}")


def check_json_files(root: Path) -> None:
    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {path.relative_to(root)}: {exc}")


def check_line_hygiene(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json"} and path.name not in {"SKILL.md", "AGENTS.md", ".hermes.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                fail(f"Trailing whitespace in {path.relative_to(root)}:{idx}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Skill repository root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        fail("SKILL.md not found")
    text = skill_path.read_text(encoding="utf-8")
    check_frontmatter(root, text)
    check_required_files(root)
    check_references(root, text)
    check_policy_terms(root)
    check_json_files(root)
    check_line_hygiene(root)
    print("end-to-end-loop skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
