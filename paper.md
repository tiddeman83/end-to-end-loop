# End-to-End Loop Rationale

`end-to-end-loop` is a portable Agent Skill for software delivery work that must produce verified evidence rather than plausible progress reports.

## Problem

Coding agents often skip steps that human teams rely on for safe delivery: explicit scope, acceptance criteria, local verification, diff review, smoke checks, security review, and deploy approval. The result is overconfident reports that are hard to audit.

## Approach

The skill turns delivery into a lightweight gate sequence:

1. Discover the requested outcome, inputs, side effects, and risks.
2. Plan concrete acceptance criteria and a delivery/deploy classification.
3. Execute code-producing work through a CAVEMAN lane.
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
- Local telemetry: measurement starts as opt-in local JSONL plus sanitized aggregate summaries; OpenTelemetry/OTLP remains an optional adapter, not the default data path.

## Evaluation strategy

The repository includes trigger cases, outcome scenarios, a result-log schema, and sanitized example logs. Evaluation should measure whether agents:

- invoke the skill for coding, release, deploy, debugging, and repo-change tasks;
- avoid invoking it for pure brainstorming or no-code questions;
- preserve the CAVEMAN hard gate for code-producing phases;
- classify delivery target correctly;
- stop unsafe deploys and produce readiness reports;
- report evidence and blockers honestly.

## Mission Mode optional helper-agent track

Product-facing helper agents may improve adoption if kept functional and bounded. The candidate product name is **Mission Mode**: a scoped agent team around the delivery loop where each helper gets the right reasoning depth for the job and high-impact actions stay behind human approval.

- `mission-planner` drafts mission scope, acceptance criteria, agent assignments, reasoning-level choices, verification plan, and approval gates.
- `loop-verifier` checks whether a run followed the loop.
- `loop-reporter` structures evidence into a final report.
- `adapter-builder` drafts tool-specific adapter guidance.
- `loop-reviewer` reviews diffs against safety and acceptance criteria.
- `loop-eval-runner` coordinates trigger/outcome evals.
- `deploy-readiness-checker` prepares deploy-readiness reports.

Mission Mode should classify work by reasoning level: Level 0 mechanical/cheap checks, Level 1 standard implementation support, Level 2 deep review/safety/architecture, and Level 3 human approval for merge/release/deploy/admin/secrets/public claims. These helpers should not become an internal office simulation or a release-approval authority.

## Local telemetry research track

The telemetry feature supports release-readiness evidence by measuring local runs without turning raw logs into memory. The current design keeps raw JSONL local by default and shares only aggregate summaries with explicit privacy review fields. This enables timing, validation-pass, CAVEMAN-compliance, and Copilot-availability evidence while avoiding full prompts, stdout/stderr, env vars, private paths, machine identity, and public overclaims from small samples. A local stdlib privacy smoke test now checks both the happy-path aggregation fixture and rejection of forbidden raw/private keys so telemetry can mature through evidence rather than documentation alone.


## Review-improve research track

Deep review work needs its own lightweight option because it is neither pure planning nor ordinary implementation. The review-improve path treats documentation and skill changes as evidence-backed maintenance: inventory the surfaces, compare cross-document claims, rank findings by risk/value, make scoped edits, and report deferred follow-ups. This keeps broad audit requests from becoming subjective rewrites while still allowing the loop to improve itself.

## 2026 production-readiness research direction

Comparison with agent runtimes, coding harnesses, evaluation systems, and secure
delivery standards suggests that the loop's defensible role is an assurance and
delivery-policy layer, not a new general-purpose runtime. Current frameworks
already provide tool invocation, durable execution, sessions, handoffs, and
multi-agent transport. The missing contribution here is a portable,
machine-readable contract that decides which action is allowed next, what
evidence closes a gate, when to stop or escalate, and how much context and budget
the run may consume.

Accordingly, the next research hypothesis is that a stateful single-agent kernel
with risk-triggered reference loading will improve verified success per unit cost
more than adding a standing set of named helper agents. That hypothesis must be
tested with baseline-versus-skill repository tasks, repeated trials, and
sanitized measurements of success, regressions, evidence completeness, wall
time, tool calls, tokens where exposed, retries, and human interventions. Until
that evidence and multi-tool recovery tests exist, production-readiness claims
remain out of scope.
