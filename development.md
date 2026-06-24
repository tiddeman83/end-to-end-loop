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
- Added a product-facing helper-agent strategy in `research/product-helper-agents.md`.
- Replaced private historical eval examples with sanitized product examples.
- Updated validator expectations so outcome scenarios use generic hosting/custom-domain language rather than private site specifics.

Validation plan:

- `python3 scripts/validate_skill.py .` from a temporary folder named `end-to-end-loop`.
- `git diff --check`.
- JSON parse validation through the skill validator.
