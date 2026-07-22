# Development Log

This log records product-facing development decisions for the `end-to-end-loop` skill.

## 2026-07-22 — Competitive research and production assessment

Goal: assess comparable agent frameworks and determine whether the current skill
is ready for production before planning a new release.

Decisions:

- Classify `0.1.0-alpha.2` as a usable alpha, not production-ready; the documented
  assessment score is `17/40` and lacks comparative, multi-tool, recovery, and
  cost evidence.
- Position the product as a portable assurance/delivery-policy layer over agent
  runtimes rather than another general orchestration runtime.
- Prioritize a versioned run state, deterministic transitions, risk-triggered
  reference routing, explicit budgets/termination, and comparative evaluations.
- Defer a broad named helper-agent fleet until a bounded specialist protocol and
  evidence of positive coordination value exist.
- Target `0.1.0-alpha.3` for the next vertical slice; do not make production or
  major-version claims yet.
- Record the research limitation: configured web access returned 401 and direct
  HTTPS returned 403, so primary-source URLs are indexed but require a refresh
  in a network-enabled release pass.
- Record the repository limitation: this checkout has no Git remote or branch
  upstream, so freshness comparison, push, remote CI, and release publication
  cannot be completed from the current environment.

Validation plan:

- `python3 scripts/validate_skill.py .`.
- `python3 scripts/test_telemetry_privacy.py`.
- `python3 -m py_compile scripts/*.py`.
- install smoke test against a temporary home.
- `git diff --check` and focused diff review.

## Settled product direction

- The repository packages a portable delivery-loop skill for coding agents.
- The core loop is: discover, plan, execute through CAVEMAN, verify, test, deliver or prepare deploy, report.
- Live deploy remains opt-in and gated by explicit approval, target maturity, CI/local validation, rollback, smoke checks, and security review.
- Tool-specific behavior belongs in `references/adapters.md`; universal policy stays in `SKILL.md`.
- Per-repo memory/result logs must stay compact, sanitized, and safe to commit.

## 2026-06-24 — Product/operations boundary cleanup

Goal: keep this repository focused on the public-facing delivery-loop tool and move internal office/backoffice operations elsewhere.

Changes:

- Rewrote repository context docs with generic maintainer/product language.
- Removed internal governance, dashboard, and private task-routing instructions from product docs.
- Added a product-facing Mission Mode helper-agent strategy in `research/product-helper-agents.md`, including reasoning levels and approval gates.
- Replaced private historical eval examples with sanitized product examples.
- Updated validator expectations so outcome scenarios use generic hosting/custom-domain language rather than private site specifics.

Validation plan:

- `python3 scripts/validate_skill.py .` from a temporary folder named `end-to-end-loop`.
- `git diff --check`.
- JSON parse validation through the skill validator.

Follow-up product decision:

- Decide whether Mission Mode should remain a research note or become a packaged optional helper-agent layer with `mission-planner`, `loop-verifier`, `loop-reporter`, `adapter-builder`, `loop-reviewer`, `loop-eval-runner`, and `deploy-readiness-checker`.

## 2026-06-27 — Token, speed, model-routing, and update preflight

Goal: optimize the loop for lower token use, faster development, cheaper model use, more effective helper-agent use, and safer skill freshness.

Decisions:

- Add lean/standard/deep operating modes and level_0..level_3 complexity routing.
- Prefer deterministic scripts or cheap/fast models for mechanical work; escalate to standard/high-reasoning/human routes only when complexity, risk, or approval gates require it.
- Always consider helper agents, but use them only when parallelism, specialization, or context compression beats coordination cost.
- CAVEMAN companion skills are mandatory prerequisites for code-producing phases and must be installed/update-checked when supported before blocking or proceeding.
- `end-to-end-loop` should check its own source/repo freshness where feasible before maintained repo work.

Validation plan:

- Validate from a temporary folder named `end-to-end-loop`.
- Run JSON validation through `scripts/validate_skill.py`.
- Run `git diff --check`.

## 2026-06-28 — Local telemetry aggregation slice

Goal: advance the telemetry research feature from recorder-only evidence to deterministic, shareable aggregation without weakening privacy.

Changes:

- Added `scripts/telemetry_aggregate.py`, a stdlib-only helper that reads an explicitly supplied local JSONL file and emits aggregate `telemetry-summary-v0` JSON.
- Kept aggregation local-first and privacy-safe: forbidden raw/private event keys include prompts, stdout/stderr, env, cwd, host/user/home identity, raw commands, and raw args.
- Extended the telemetry fixture with a CAVEMAN compliance quality gate and updated the example summary as fixture-only evidence.
- Updated validation/install coverage so documented helper scripts are packaged and validator checks Copilot-identified privacy/install gaps.

Validation plan:

- `python3 -m py_compile scripts/validate_skill.py scripts/telemetry_record.py scripts/telemetry_aggregate.py`.
- `python3 scripts/telemetry_aggregate.py evals/telemetry-events.fixture.jsonl --source fixture --claim-scope fixture-only`.
- Validate from a temporary folder named `end-to-end-loop`.
- `git diff --check`.

## 2026-06-28 — Telemetry privacy self-test slice

Goal: harden the telemetry measurement feature with a local smoke test that proves recorder/aggregator privacy guards work, not just that the happy-path fixture aggregates.

Changes:

- Added `scripts/test_telemetry_privacy.py`, a stdlib-only local test for fixture aggregation plus forbidden raw/private key rejection.
- Documented the test in `references/local-telemetry.md` and included it in installed helper packaging.
- Extended the validator so the helper must exist and be copied by `scripts/install.sh`.
- Ignored Python `__pycache__/` artifacts created by local validation.

Validation plan:

- `python3 -m py_compile scripts/validate_skill.py scripts/telemetry_record.py scripts/telemetry_aggregate.py scripts/test_telemetry_privacy.py`.
- `python3 scripts/test_telemetry_privacy.py`.
- Validate from a temporary folder named `end-to-end-loop`.
- `git diff --check`.

## 2026-06-28 — Grilling subskill slice

Goal: package a pre-build plan/design stress-test mode as a subskill of the end-to-end loop.

Changes:

- Added `skills/grilling/SKILL.md` with one-question-at-a-time interviewing, recommended answers, and codebase-first exploration rules.
- Wired the root skill, README, install script, trigger evals, and validator to recognize packaged subskills.
- Kept grilling as pre-execution shared-understanding work, not a replacement for CAVEMAN execution or validation gates.

Validation plan:

- Validate from a temporary folder named `end-to-end-loop`.
- Run telemetry privacy smoke test.
- Run `git diff --check`.

## 2026-06-28 — Agile verification and Codex reviewer policy

Goal: make the end-to-end loop stricter at the feature/user-story level, with grilling used to define tight goals and precise verification before build.

Changes:

- Elevated grilling from explicit trigger only to the default refinement path when feature scope, user story, dependencies, or verification layers are unclear.
- Added root-skill requirements for explicit skill settings/goals and layered verification planning.
- Added Claude adapter guidance: when a Codex connector is installed and promptable, include a Codex agentic reviewer in VERIFY/TEST for code-producing work.

Validation plan:

- Validate from a temporary folder named `end-to-end-loop`.
- Run telemetry privacy smoke test.
- Run install smoke test against a temporary home.
- Run `git diff --check`.

## 2026-06-28 — First-run environment and version policy

Goal: make every loop run auditable from startup by reporting the skill version and confirming the target environments before first implementation.

Changes:

- Added `VERSION` and required the loop to present it at run start and in reports.
- Added first-run discovery of production runtime and local development environment.
- Required first-run user confirmation of that environment model through grilling before implementation.
- Extended validator/install/evals to package and enforce the version/environment policy.

Validation plan:

- Validate from a temporary folder named `end-to-end-loop`.
- Run telemetry privacy smoke test.
- Run install smoke test against a temporary home.
- Run `git diff --check`.

## 2026-06-28 — Handoff subskill slice

Goal: package a compact continuation handoff mode as a subskill of the end-to-end loop.

Changes:

- Added `skills/handoff/SKILL.md` with user-provided frontmatter and behavior.
- Handoff writes a redacted document to the OS temporary directory, not the workspace.
- Handoff suggests skills for the next agent and references existing artifacts instead of duplicating PRDs, plans, ADRs, issues, commits, or diffs.
- Validator now accepts supported subskill frontmatter fields such as `argument-hint` and `disable-model-invocation`.

Validation plan:

- Validate from a temporary folder named `end-to-end-loop`.
- Run telemetry privacy smoke test.
- Run install smoke test against a temporary home.
- Run `git diff --check`.

## 2026-06-28 — Diagnosing-bugs and TDD subskills; finish handoff wiring

Goal: enrich the loop with technique disciplines adapted from the open
`mattpocock/skills` library, and finish wiring the handoff subskill that was
packaged but not routed.

Changes:

- Added `skills/diagnosing-bugs/SKILL.md`: a feedback-loop-first debugging
  discipline (build a red-capable, deterministic, fast, unattended repro before
  hypothesizing or fixing). Wired into ITERATE-toward-verify-green and Reference
  Routing.
- Added `skills/tdd/SKILL.md`: red-green-refactor, behavior-over-implementation,
  vertical slices. Wired into EXECUTE and Reference Routing.
- Finished handoff integration: added a Reference Routing pointer to
  `skills/handoff/SKILL.md` and a REPORT bullet (reference-don't-duplicate,
  suggested next skills, redact secrets/PII).
- Grilling was already integrated upstream; left unchanged.
- Updated README repository layout with the two new subskills.

Validation plan:

- `python3 scripts/validate_skill.py .` from a folder named `end-to-end-loop`.
- `git diff --check`.

## 2026-06-28 — v0.1.0-alpha.2 release: honest docs, Hermes removed

Goal: cut the first tagged alpha and make the documentation truthful. Earlier
docs (authored under the prior agent setup) described a governance/management
apparatus — an owner/maintainer approval board, a mandatory external review gate,
and a private "operations repo" with internal agents, dashboards, and
task-routing — that does not exist. This repo is maintained by its owner via
Claude Code.

Changes:

- Rewrote `README.md` into a clear what / why / how-to-use guide; replaced the
  governance "release posture/baseline/maintenance" sections with an honest
  Status, Evaluation, and Maintenance section.
- Removed Hermes entirely as a supported target tool: deleted `.hermes.md`,
  removed the Hermes adapter section and sync recipe, and dropped Hermes from
  tool lists, the validator's required files and policy terms, the result-log
  tool enum, and example values across docs, evals, and scripts.
- Deleted `research/product-office-separation-plan.md` (described the fictional
  operations apparatus).
- De-personalized release-approval language (named-person gate -> owner/release).
- Added `CHANGELOG.md`; bumped `VERSION` to `0.1.0-alpha.2`.
- Folded in the diagnosing-bugs/tdd subskills and handoff wiring merged in #8.

Validation plan:

- `python3 scripts/validate_skill.py .` from a folder named `end-to-end-loop`.
- `python3 -m py_compile scripts/*.py` and `python3 scripts/test_telemetry_privacy.py`.
- `git diff --check`.


## 2026-06-28 — Deep review/improvement option

Goal: make integral skill and documentation reviews first-class so broad audit requests produce ranked evidence-backed findings rather than subjective rewrites.

Changes:

- Added a `review-improve` operating option to `SKILL.md` for deep documentation/skill audits.
- Added phase-checklist and report-template coverage for reviewed surfaces, ranked findings, applied changes, deferred follow-ups, and validation evidence.
- Updated README positioning and paper rationale to describe review-improve as a maintenance discipline.
- Fixed stale `CAVEMAN/Cavekit` terminology in the rationale.

Validation plan:

- `python3 scripts/validate_skill.py .`.
- `python3 scripts/test_telemetry_privacy.py`.
- `git diff --check`.
