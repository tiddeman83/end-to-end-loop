# Improvement Research Plan

This plan defines the next research and improvement program for the public-facing `end-to-end-loop` skill.

## Current product thesis

`end-to-end-loop` should become a portable delivery discipline for coding agents: it keeps agents from skipping discovery, tests, safety checks, CI, deployment approval, and reporting. Its differentiator is strict CAVEMAN execution plus a deploy policy that blocks unsafe live changes.

## Improvement tracks

### Track 1: Trigger precision

Goal: ensure the skill activates for delivery work and stays quiet for pure Q&A.

Work:

- Maintain `evals/trigger-cases.json` with near-miss negatives.
- Include prompts for explanation-only, commit-message-only, summary-only, planning-only, coding, PR, and deploy-gated work.
- Run repeated passes where the tool supports invocation logs.

### Track 2: CAVEMAN adapter maturity

Goal: make CAVEMAN enforcement usable across tools.

Work:

- Define exact CAVEMAN adapters for Codex, Claude Code, and Cursor.
- Decide whether a "CAVEMAN exception" should fail release readiness.
- Add examples of compliant and non-compliant execution reports.

### Track 3: Deploy-readiness scoring

Goal: make the deploy gate objective.

Work:

- Keep the readiness rubric focused on target environment, CI, tests, rollback, secrets, owner, monitoring, and user approval.
- Add scenario evals for deploy requested/no CI, deploy not requested, and deploy approved/CI green.
- Keep provider-specific hosting details generic unless an adapter file owns them.

### Track 4: Product helper agents

Goal: decide whether optional public helper agents add value beyond `SKILL.md`.

Candidate agents:

- `loop-verifier`
- `loop-reporter`
- `adapter-builder`
- `loop-reviewer`
- `loop-eval-runner`
- `deploy-readiness-checker`

Guardrail: these are functional public helpers, not internal office agents.

### Track 5: Website and market positioning

Goal: prepare public product messaging after an approved hosting target exists.

Work:

- Market scan adjacent skills and rule systems.
- Draft landing page, install pages, safety page, research page, and changelog.
- Decide whether website source belongs in this repo or a separate site repo.

## 2026-07-22 production research decision

The competitive and production assessment in
`research/competitive-production-assessment.md` supersedes the dates and release
ordering below where they conflict. The current skill scored `17/40` on the
evidence rubric: usable alpha, not production-ready. The immediate priority is
an executable, budgeted, resumable single-agent kernel plus comparative evals,
not a helper-agent fleet.

### Ordered backlog

| Order | Slice | Complexity / route | Acceptance signal |
|---:|---|---|---|
| 1 | Versioned run-state and transition schema | `level_2`; high-reasoning design, CAVEMAN CODE implementation | Interrupted run resumes at an allowed phase; invalid transitions fail deterministically. |
| 2 | Capability preflight and risk-triggered reference router | `level_1`; standard implementation | Lean tasks avoid unrelated references while safety/deploy triggers load required gates. |
| 3 | Budget, retry, escalation, and termination contract | `level_2`; high-reasoning design and reviewer | A run stops on success, hard block, retry ceiling, or budget ceiling and reports the reason. |
| 4 | Comparative evaluation harness and held-out tasks | `level_2`; independent evaluator | Baseline/current task success, regressions, evidence, time, calls, tokens when available, retries, and interventions are recorded. |
| 5 | Minimal runtime package manifest | `level_1`; deterministic size checks plus standard implementation | Runtime and maintainer artifacts are separated; install/context size is measured and regression-tested. |
| 6 | Bounded specialist protocol | `level_2`; only after slices 1-4 | Specialist has typed input/output, scoped tools, budget, evidence, and termination; coordinator owns final state. |
| 7 | Release candidate | `level_3`; maintainer approval | Production gates in the assessment pass with green remote CI and authenticated release evidence. |

First batch: slices 1-2. They create the control plane needed for cheaper context
routing and later agent specialization without prematurely paying multi-agent
coordination cost.

## Proposed next release milestones

### v0.1.0-alpha.3 - Executable-kernel experiment

- Run-state and transition schema.
- Capability/risk preflight.
- Budget and termination fields.
- Minimal-package measurement.
- First baseline-versus-current evaluation pairs.

### v0.3.0 - Eval-backed release

- Trigger evals.
- Outcome scenario evals.
- Deploy-readiness rubric.
- CAVEMAN compliance examples.
- Sanitized product result logs.

### v0.4.0 - Bounded specialist MVP

- One common specialist protocol before named helper roles.
- Optional helper-agent specs only where measured coordination value is positive.
- Agent output schemas.
- Helper-agent eval coverage.

### v1.0.0 - Public/shareable release

- Evals pass.
- Paper polished.
- Website live if approved.
- Installation instructions tested for Codex, Claude Code, Cursor, and AGENTS.md-only agents.

## Research questions

1. Which public skills or rules already solve parts of this loop?
2. Where do users complain most about coding-agent reliability?
3. Which marketplaces or registries matter for distribution?
4. What security claims can be made responsibly, and what must remain caveated?
5. What website messaging makes this useful without overpromising?

## Not safe without explicit approval

- Live deploys.
- Public release or marketplace publication.
- Broad skill package restructuring.
- Validator behavior changes that weaken release checks.
- Auth, token, provider rules, or production data changes.
- Code-producing repo changes without a CAVEMAN lane or approved exception.

## Research-backed additions

The next version should borrow from ReAct, Reflexion, Self-Refine, SWE-agent, SWE-bench, SLSA, OpenSSF Scorecard, and NIST SSDF without overclaiming. Practical translation for this repo:

- make inspect/reproduce/plan/implement/verify/reflect/finalize explicit;
- record fail-to-pass and pass-to-pass behavior where tests exist;
- track wall time, tool calls, files touched, diff size, and human interventions;
- require source links and uncertainty notes for research conclusions;
- keep live deploy blocked unless the release gate is explicitly satisfied.
