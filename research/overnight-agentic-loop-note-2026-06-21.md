# Overnight DevBoss Research Note — Agentic Coding Loops

Date: 2026-06-21
Scope: private DevBoss Office sprint for `tiddeman83/end-to-end-loop`; documentation/research only; no Firebase deploy, public release, or destructive changes.

## Todoist context ingested

Current DevBoss context from `/opt/data/devboss-end-to-end-loop-poller-state.json` says:

- Repo `tiddeman83/end-to-end-loop` is private and accessible.
- The user confirmed repo-first development, always via worktrees, with a good README before eventual release.
- Board/office decisions should route through Todoist, with parallel Telegram mirroring, and a dedicated DevBoss project/sections.
- Firebase is intended for a public information website, not the core product backend.
- Desired domain: `dev-boss.nl`.
- Firebase project context: `tijmensassistant` / project number `873713423755`; do not commit credentials or deploy without explicit approval.
- Public site audience: AI researchers and AI users who want efficient ways of working.
- Website purpose: explain the skill as a self-learning for-loop that keeps running until a code component or app is completed safely and tested.
- Backend/statistics access should be restricted to `tijmenbaas83@gmail.com`.
- Open prerequisite task remains: Firebase website prerequisites and explicit deploy readiness.

## Focused research scan

Network research used arXiv API queries for recent work on software-engineering agents, testing/evaluation, self-improving agents, and multi-agent workflows. Relevant papers surfaced:

1. **Probe-and-Refine Tuning of Repository Guidance for Coding Agents** (`arXiv:2606.20512`, 2026-06-18)
   - Claim of interest: coding agents need repository-level operational guidance: subsystem maps, test commands, and known wrong-fix patterns.
   - Design implication: `end-to-end-loop` should treat `.hermes.md`, `AGENTS.md`, handoff files, and validation commands as first-class inputs in DISCOVER, not optional context.

2. **Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs** (`arXiv:2606.20243`, 2026-06-18)
   - Claim of interest: issue-to-PR systems benefit from layered safety controls plus baseline-aware test evaluation.
   - Design implication: DevBoss Office should separate planner, implementer, reviewer, security, and release roles; every role must produce evidence, not confidence-only status.

3. **SEAGym: An Evaluation Environment for Self-Evolving LLM Agents** (`arXiv:2606.17546`, 2026-06-16)
   - Claim of interest: self-evolving agents improve by changing the harness around the base model: prompts, memory, tools, middleware, runtime state, and model-tool loops.
   - Design implication: this skill's self-improvement target is the loop/harness, not only code output. Metrics should track harness changes and whether they improve validation pass rate, iteration count, and safety outcomes.

4. **AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning** (`arXiv:2606.20373`, 2026-06-18)
   - Claim of interest: evidence-guided multi-agent optimization is useful when measurements are noisy.
   - Design implication: the loop should prefer baseline comparisons, repeated checks where relevant, and explicit evidence artifacts for optimization-style tasks.

5. **Tool Programs as an Interface for Flexible Agentic Web Services** (`arXiv:2606.19992`, 2026-06-18)
   - Claim of interest: long-horizon agents need tools that express loops, joins, retries, and stateful workflows rather than only static endpoints.
   - Design implication: DevBoss automation should model board routing, PR retry, validation, and deploy readiness as durable workflows with explicit state.

## Release/readiness metrics proposed

Track these before public release:

- **Loop completion rate:** percentage of tasks that reach REPORT with all acceptance criteria mapped to evidence.
- **Validation pass rate:** local validator, `git diff --check`, CI status, and task-specific tests.
- **Iteration efficiency:** number of VERIFY/TEST/ITERATE cycles before green.
- **Safety gate hit rate:** count of deploy/credential/destructive/network actions blocked or prepared instead of executed.
- **CAVEMAN compliance:** code-producing phases record a CAVEMAN lane or approved exception.
- **Context freshness:** whether Todoist, repo status, and project context were read before changing docs/code.
- **PR readiness:** branch pushed, manual PR URL available if token cannot create PR, CI observable.

## Safe multi-agent office workflow

Recommended DevBoss lanes:

- **Jared Dunn / Nous-class coordinator:** summarize Todoist, set scope, keep final report operational.
- **Daniela / Opus-class safety analyst:** research safety, threat models, side-effect gates.
- **Ilya / Opus-class eval analyst:** design metrics, eval cases, baseline comparisons.
- **Richard Hendricks / GPT-Codex implementation lane:** make repo edits through worktrees and validation gates.
- **Gilfoyle / GPT-Codex or Opus review lane:** inspect diff, secrets, deploy-policy compliance.

Operational rule: multi-agent output is advisory until the implementation lane has merged it into a worktree, run validation, reviewed diff, and pushed a branch.

## Website readiness snapshot

Observed on 2026-06-21:

- `https://tijmensassistant.web.app` returns HTTP 200 and appears to serve **TinTin — Tijmen's Assistant Cockpit**, not a DevBoss public information site.
- `https://dev-boss.nl` fails TLS hostname validation: certificate does not match `dev-boss.nl`.
- Therefore a live Firebase-hosted site exists for the broader assistant project, but no verified DevBoss public preview/live URL is ready to show.

Before `dev-boss.nl` can be shown:

1. Choose whether DevBoss gets a separate Firebase Hosting site/target under the existing project or a separate project/repo.
2. Build a public marketing/info site with no private cockpit exposure.
3. Configure custom domain `dev-boss.nl` and TLS certificate correctly.
4. Configure visitor statistics with backend/admin access restricted to `tijmenbaas83@gmail.com`.
5. Add CI build/deploy route and secret handling.
6. Get explicit deploy approval, run smoke/security checks, then deploy.
