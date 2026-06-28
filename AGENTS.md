# Project Instructions

This repo develops the `end-to-end-loop` Agent Skill. The production skill entry is
`SKILL.md`; supporting operational references live in `references/`.

## Required Workflow

- Before editing, check repo freshness against `origin`/upstream when network and permissions allow; record if blocked.
- Follow `SKILL.md` for all build, fix, refactor, test, release, or handoff work.
- CAVEMAN is mandatory for code-producing phases. Install/update-check companion
  CAVEMAN skills before use. If no current CAVEMAN lane is available, stop before
  repo changes and request an explicit exception.
- Scale ceremony with lean/standard/deep mode; use the cheapest adequate model and
  helper agents only when they reduce wall time or improve evidence.
- Run `python3 scripts/validate_skill.py .` before committing.
- Keep every iteration committed and pushed to GitHub.
- Update `development.md`, `memory.md`, and `paper.md` when decisions or research
  change.

## Delivery Policy

- Live deploy is not automatic.
- Deploy requires explicit user opt-in for the task, project maturity, applicable
  green CI, rollback, credentials approval, and smoke/security checks.
- Without those conditions, produce a deployment readiness report instead.

## Maintenance

- This repo develops and validates the `end-to-end-loop` Agent Skill. It is
  maintained by the repository owner, working through coding agents such as
  Claude Code. There is no separate agent fleet or approval board that governs it.
- Keep examples generic. Do not add secrets, private repo names, access details,
  or invented internal personas/processes to any doc.
- Describe only what the skill actually does. Do not document aspirational
  capabilities, teams, or governance as if they exist.
