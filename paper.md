# End-to-End Loop Rationale

`end-to-end-loop` is a portable Agent Skill for software delivery work that must produce verified evidence rather than plausible progress reports.

## Problem

Coding agents often skip steps that human teams rely on for safe delivery: explicit scope, acceptance criteria, local verification, diff review, smoke checks, security review, and deploy approval. The result is overconfident reports that are hard to audit.

## Approach

The skill turns delivery into a lightweight gate sequence:

1. Discover the requested outcome, inputs, side effects, and risks.
2. Plan concrete acceptance criteria and a delivery/deploy classification.
3. Execute code-producing work through a CAVEMAN/Cavekit lane.
4. Verify each criterion with observed evidence.
5. Iterate on failures.
6. Run broader tests, smoke checks, and security review.
7. Deliver only within approved scope.
8. Report changes, evidence, limitations, and follow-ups.

## Design principles

- Portable core: keep universal loop rules in `SKILL.md`.
- Adapter boundary: put tool-specific commands and caveats in `references/adapters.md`.
- Evidence first: no green status without real command output, artifact review, smoke evidence, or documented approval.
- Deploy safety: live deploy is never implied by code completion.
- Sanitized learning: durable memory and result logs must be compact and safe to commit.
- Product boundary: public docs describe the delivery-loop tool, not private office operations.

## Evaluation strategy

The repository includes trigger cases, outcome scenarios, a result-log schema, and sanitized example logs. Evaluation should measure whether agents:

- invoke the skill for coding, release, deploy, debugging, and repo-change tasks;
- avoid invoking it for pure brainstorming or no-code questions;
- preserve the CAVEMAN hard gate for code-producing phases;
- classify delivery target correctly;
- stop unsafe deploys and produce readiness reports;
- report evidence and blockers honestly.

## Optional helper-agent track

Product-facing helper agents may improve adoption if kept functional and bounded:

- `loop-verifier` checks whether a run followed the loop.
- `loop-reporter` structures evidence into a final report.
- `adapter-builder` drafts tool-specific adapter guidance.
- `loop-reviewer` reviews diffs against safety and acceptance criteria.
- `loop-eval-runner` coordinates trigger/outcome evals.
- `deploy-readiness-checker` prepares deploy-readiness reports.

These helpers should not become an internal office simulation or a release-approval authority.
