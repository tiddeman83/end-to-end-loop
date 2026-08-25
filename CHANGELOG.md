# Changelog

All notable changes to `end-to-end-loop` are recorded here. Versions are tracked
in `VERSION` and follow semver-like alpha labeling until a stable release.

## v0.1.0-alpha.3 — 2026-08-25

Documentation and research consolidation release. No production behavior changed
since the `review-improve` option landed; this release makes the version, the
honest status, and the research direction consistent across every document.

### Added

- `review-improve` operating option in `SKILL.md`, with phase-checklist and
  report-template coverage for reviewed surfaces, ranked findings, applied
  changes, deferred follow-ups, and validation evidence (merged after
  `v0.1.0-alpha.2`).
- `research/competitive-production-assessment.md` — comparison against agent
  runtimes, coding harnesses, evaluation systems, and secure-delivery standards,
  with a `17/40` evidence-rubric score, the mandatory gates for a production
  candidate, and an ordered backlog.
- `research/state-graph-adoption-plan.md` — how state-machine research (typed
  state, reducers, node/router separation, bounded cycles, checkpointing,
  interrupt-before) applies here, plus a scoped plan for a later graph-based
  operating mode and its boundary against work-graph orchestration skills.

### Changed

- Release numbering: the executable run-state kernel moves from `0.1.0-alpha.3`
  to `0.1.0-alpha.4`, and the graph-mode phases shift with it. This release is
  documentation and research only; the kernel has not been built.
- `README.md`, `paper.md`, `memory.md`, and the research plans now state the same
  status, version, and next milestone.
- Resolved the recorded blocker that the checkout had no configured Git remote;
  push, remote CI, and release publication now work.

### Notes

- Still an early alpha. Runtime agency, measured cost, comparative evals, and
  multi-tool portability evidence remain the release blockers named in the
  production assessment — this release does not close any of them.
- Performance claims remain scoped to auditability and reviewability until
  backed by measured results.

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
