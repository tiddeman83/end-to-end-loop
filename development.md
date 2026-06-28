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
