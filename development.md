# Development Log

This log records product-facing development decisions for the `end-to-end-loop` skill.

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
