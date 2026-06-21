# Project Instructions

This repo develops the `end-to-end-loop` Agent Skill. The production skill entry is
`SKILL.md`; supporting operational references live in `references/`.

## Required Workflow

- Follow `SKILL.md` for all build, fix, refactor, test, release, or handoff work.
- CAVEMAN is mandatory for code-producing phases. If no CAVEMAN lane is available,
  stop before repo changes and request an explicit exception.
- Run `python3 scripts/validate_skill.py .` before committing.
- Keep every iteration committed and pushed to GitHub.
- Update `development.md`, `memory.md`, and `paper.md` when decisions or research
  change.

## Delivery Policy

- Live deploy is not automatic.
- Deploy requires explicit user opt-in for the task, project maturity, applicable
  green CI, rollback, credentials approval, and smoke/security checks.
- Without those conditions, produce a deployment readiness report instead.

## Hermes Handoff

- Hermes-specific operations are documented in `.hermes.md` and `handoff/`.
- DevBoss office instructions live in `handoff/hermes-devboss-brief.md`.
- Market research prompt lives in `handoff/hermes-market-research-prompt.md`.
