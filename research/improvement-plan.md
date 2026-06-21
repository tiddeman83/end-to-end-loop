# Improvement Research Plan

This plan follows the first production-ready preparation pass. It defines the next
research and improvement program for the skill.

## Current product thesis

`end-to-end-loop` should become the portable delivery discipline for coding agents:
it keeps agents from skipping discovery, tests, safety checks, CI, deployment
approval, and reporting. Its differentiator is strict CAVEMAN execution plus a
deploy policy that blocks unsafe live changes.

## Improvement tracks

### Track 1: Trigger precision

Goal: ensure the skill activates for delivery work and stays quiet for pure Q&A.

Work:
- Add `evals/trigger-cases.json`.
- Include near-miss negatives: "explain CI", "write a commit message only",
  "summarize this code", "brainstorm deployment options".
- Run three passes per query where the tool supports invocation logs.

### Track 2: CAVEMAN adapter maturity

Goal: make CAVEMAN enforcement usable across tools.

Work:
- Define exact CAVEMAN adapters for Codex, Hermes, Claude Code, and Cursor.
- Decide whether "CAVEMAN exception" should fail CI/release readiness.
- Add examples of compliant and non-compliant execution reports.

### Track 3: Deploy-readiness scoring

Goal: make the deploy gate objective.

Work:
- Create a readiness rubric: target env, CI, tests, rollback, secrets, owner,
  monitoring, user approval.
- Add `references/deploy-readiness.md` if the rubric grows beyond
  `test-and-security.md`.
- Add scenario evals for deploy requested/no CI, deploy not requested, and deploy
  approved/CI green.

### Track 4: Hermes DevBoss operations

Goal: make Hermes capable of maintaining the repo with minimal ambiguity.

Work:
- Test the handoff prompt in Hermes.
- Verify `skills.write_approval` and external skill directory setup.
- Confirm Todoist routing through the user's AI Assistant.
- Define board decision log location if Todoist IDs need repo persistence.

### Track 5: Website and market positioning

Goal: prepare a Firebase-hosted website after user environment setup.

Work:
- Market scan adjacent skills and rule systems.
- Draft landing page, install pages, safety page, research page, and changelog.
- Decide whether website source belongs in this repo or a separate Firebase repo.

## Proposed next release milestones

### v0.2.0 - Production candidate

- Universal core and adapter references.
- CI validation.
- Hermes DevBoss handoff.
- Research prompt.

### v0.3.0 - Eval-backed release

- Trigger evals.
- Outcome scenario evals.
- Deploy-readiness rubric.
- CAVEMAN compliance examples.

### v0.4.0 - Hermes-managed operating model

- DevBoss office running.
- Todoist routing confirmed.
- Website plan approved.
- First Firebase implementation branch prepared.

### v1.0.0 - Public/shareable release

- Evals pass.
- Paper polished.
- Website live if approved.
- Installation instructions tested for Codex, Hermes, Claude Code, Cursor, and
  AGENTS.md-only agents.

## Research questions for Hermes

1. Which public skills or rules already solve parts of this loop?
2. Where do users complain most about coding-agent reliability?
3. Which marketplaces or registries matter for distribution?
4. What security claims can be made responsibly, and what must remain caveated?
5. What website messaging makes this useful without overpromising?

## Overnight priority order

1. README landing page — high impact, low risk.
2. Evaluation rubric and result schema — high impact, low risk.
3. Paper cleanup and validation-status note — medium/high impact, low risk.
4. Hermes first-day/overnight research mode — medium impact, low risk.
5. CAVEMAN compliance examples — medium impact, low risk.
6. Deploy-readiness rubric — medium impact, low risk; can later become `references/deploy-readiness.md`.

## Not overnight-safe without explicit approval

- Live Firebase deploys.
- Public release or marketplace publication.
- Broad skill package restructuring.
- Validator behavior changes that weaken release checks.
- Auth, token, Firebase rules, or production data changes.
- Code-producing repo changes without a CAVEMAN lane or approved exception.

## Research-backed additions for v0.3.0

The next version should borrow from ReAct, Reflexion, Self-Refine, SWE-agent,
SWE-bench, SLSA, OpenSSF Scorecard, and NIST SSDF without overclaiming. Practical
translation for this repo:

- make inspect/reproduce/plan/implement/verify/reflect/finalize explicit;
- record fail-to-pass and pass-to-pass behavior where tests exist;
- track wall time, tool calls, files touched, diff size, and human interventions;
- separate author, reviewer, CI, security, and release governance roles in DevBoss;
- require source links and uncertainty notes for research conclusions;
- keep live deploy blocked unless the release gate is explicitly satisfied.
