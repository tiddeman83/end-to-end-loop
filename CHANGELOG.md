# Changelog

All notable changes to `end-to-end-loop` are recorded here. Versions are tracked
in `VERSION` and follow semver-like alpha labeling until a stable release.

## v0.1.0-alpha.2 — 2026-06-28

First tagged alpha prerelease.

### Added

- Packaged subskills under `skills/`:
  - `grilling` — one-question-at-a-time plan/design stress-testing.
  - `handoff` — redacted, temp-dir continuation handoffs.
  - `diagnosing-bugs` — feedback-loop-first bug/regression diagnosis.
  - `tdd` — test-first red-green-refactor.
- Reference-routing and phase-level wiring so the loop reaches each subskill at
  the right moment (DISCOVER/PLAN, EXECUTE, ITERATE, REPORT).

### Changed

- **Documentation rewritten for honesty.** Removed an inaccurate
  governance/management narrative: the "maintainer/owner approval board," the
  mandatory external review gate, and references to private office automation,
  dashboards, and task-routing. The repo is maintained by its owner working
  through coding agents (Claude Code); there is no separate agent fleet governing
  it.
- README reworked into a clear what / why / how-to-use guide.
- Fixed cross-document inconsistencies between `SKILL.md`, the references, and the
  validator (repository layout, package tree, reference routing, eval gates).

### Removed

- **Hermes** dropped as a supported target tool and from all positioning: deleted
  `.hermes.md`, removed the Hermes adapter section and sync recipe, and removed
  Hermes from tool lists, the validator's required files/policy terms, the
  result-log tool enum, and example values.

### Notes

- This is an early alpha: the loop, gates, subskills, validator, and CI are in
  place; broader benchmarks and multi-tool evidence are still being built.
- Performance claims remain scoped to auditability/reviewability until backed by
  measured results.

## v0.1.0-alpha.1 — baseline

Initial portable delivery-loop skill: the DISCOVER→REPORT loop, evidence and
deploy gates, CAVEMAN execution-lane convention, per-repo self-learning memory,
opt-in local telemetry, eval artifacts, and the dependency-free validator with CI.
