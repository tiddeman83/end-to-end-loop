---
name: end-to-end-loop
description: "Run software and coding work through a disciplined delivery loop: discover, plan, execute, verify, iterate, test, optionally deploy, and report. Use when building, fixing, refactoring, debugging, testing, reviewing, shipping, or preparing a production-ready feature, script, service, tool, repo change, or release. CAVEMAN execution is mandatory for code-producing phases; if no CAVEMAN lane exists, stop before code changes and ask for an explicit exception. Live deploy only runs when the user opted in, the project is mature enough, and an applicable CI pipeline is green."
---

# End-to-End Loop

Use this skill as the operating loop for software work that must reach a
verified result. It is a portable core: follow it in Codex, Hermes, Claude Code,
Cursor, AGENTS.md-compatible agents, or any coding tool with equivalent
capabilities.

The loop is a frame, not a cage. Scale ceremony to task risk and size, but keep
the gates real: understand the task, plan it, execute through the required lane,
verify observed behavior, test and review safety, deliver only within approved
scope, then report clearly.

## Non-Negotiables

1. Preserve the user's intent. Do not shrink scope to make the loop easier.
2. Use CAVEMAN for execution and iteration where code or repository changes are
   produced. See "CAVEMAN hard gate".
3. Never claim green without observed evidence: command output, test result,
   manual verification, diff review, or documented user approval.
4. Treat external side effects as gated work: network writes, package installs,
   remote state changes, production deploys, destructive commands, credentials,
   and third-party integrations require explicit permission or a tool-level
   approval flow.
5. Live deploy is opt-in per task. If the user did not explicitly include deploy
   in scope, stop at prepared delivery and report what remains to deploy.
6. Keep this skill portable. Tool-specific behavior belongs in
   `references/adapters.md`, not in the universal core.
7. Use per-repo memory only for compact, durable, sanitized learnings. Do not
   store secrets, private user data, bulky transcripts, or unverified guesses.

## CAVEMAN Hard Gate

CAVEMAN is mandatory for code-producing phases.

Before EXECUTE or ITERATE:

1. Resolve the available CAVEMAN lane:
   - Preferred: CAVEMAN ULTRA for execution orchestration.
   - Preferred: CAVEMAN CODE for code edits.
   - If the tool exposes different CAVEMAN names, use the configured adapter.
2. Pass the current phase, plan, acceptance criteria, constraints, and verification
   hooks into that lane.
3. If no CAVEMAN execution lane exists, stop before writing code or changing repo
   files and ask the user for an explicit exception. Mark the run as
   "CAVEMAN exception" in the report if the user approves.
4. Do not silently replace CAVEMAN with a generic agent, normal chat, or ad hoc
   execution.

Non-code discovery, planning, research, reporting, and documentation can run
outside CAVEMAN when no code or repository changes are being produced.

## Deploy Policy

DEPLOY is conditional. During PLAN, classify the delivery target:

- `none`: no deploy is relevant.
- `repo-only`: commit, branch, PR, or artifact delivery only.
- `prep-only`: deployment instructions, release checklist, or staged artifacts.
- `live-deploy`: deploy to a running environment.

Live deploy is allowed only when all conditions pass:

1. The user explicitly opted into deploy for this task.
2. The project is mature enough for deployment: known target environment, required
   config, rollback path, ownership, and no unresolved blocking risks.
3. An applicable CI pipeline exists for the changed project or release path.
4. The CI pipeline is green, or the user explicitly approves proceeding despite a
   named CI gap.
5. Smoke tests and security review are green for the deployed path.
6. Required credentials and irreversible operations are approved through the
   user's normal approval mechanism.

If any condition fails, do not live deploy. Produce a deployment readiness report
instead.

## Loop

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE
                         ^             |
                         |-------------|
                         |
                         v
                       TEST -> ITERATE
                         ^        |
                         |--------|
                         |
                         v
                DELIVER / DEPLOY -> REPORT
```

## Phase 1: DISCOVER

Goal: know what must be delivered and what would make the work unsafe or
incomplete.

Do:

- Restate the user's intended outcome and concrete done state.
- Identify inputs, files, permissions, credentials, environments, target users,
  dependencies, and constraints.
- Identify side effects: filesystem writes, network calls, external services,
  installs, secrets, CI, deploy, data changes, destructive operations.
- Ask only material questions that cannot be safely inferred. Prefer one grouped
  question set over drip-fed clarification.
- Record assumptions and risks.
- If present, read `.end-to-end-loop/memory.md` and
  `.end-to-end-loop/memory.local.md` for repo-specific facts, commands,
  blockers, preferences, prior outcomes, and failed approaches. Treat memory as
  context, not proof; re-verify safety or correctness facts before relying on
  them.

Exit: the goal, scope, risks, side effects, and needed context are known or
explicitly deferred.

## Phase 2: PLAN

Goal: produce a concrete, verifiable path.

Do:

- Break work into small steps with verification hooks.
- Define acceptance criteria as pass/fail statements.
- Choose the delivery target: `none`, `repo-only`, `prep-only`, or `live-deploy`.
- Decide whether deploy is in scope. If yes, apply the deploy policy.
- Define test strategy: unit checks, integration checks, smoke path, security
  review, and CI expectations.
- Identify rollback or recovery for risky operations.

Exit: written plan, acceptance criteria, deploy classification, and test strategy.

## Phase 3: EXECUTE

Goal: implement the plan through the required execution lane.

Do:

- Pass implementation work through CAVEMAN as defined above.
- Work step by step and keep progress visible.
- Keep changes scoped to the plan and repo conventions.
- Preserve user or teammate changes. Never revert unrelated work.
- Record meaningful decisions in the development log when this is a maintained
  project or long-running skill.

Exit: planned work is implemented or the plan is renegotiated with the user.

## Phase 4: VERIFY

Goal: prove the result satisfies the plan.

Do:

- Check each acceptance criterion: pass, fail, or blocked with evidence.
- Inspect the diff or artifact for correctness, edge cases, maintainability,
  portability, and instruction conflicts.
- Run the changed thing or the closest realistic verification command.
- Record findings and fixes. Do not move to TEST with must-fix issues open.

Exit: acceptance criteria pass and no must-fix review issues remain.

## Phase 5: ITERATE Toward Verify Green

Goal: close gaps found in VERIFY.

Do:

- Convert each failing criterion into a focused mini-plan.
- Re-execute through CAVEMAN for code changes.
- Re-run verification.
- Change approach if repeated attempts do not make progress.

Exit: VERIFY is green.

## Phase 6: TEST

Goal: harden the result beyond the immediate acceptance criteria.

Do:

- Run applicable automated tests, type checks, lint checks, or CI-local
  equivalents.
- Run smoke tests for critical end-to-end paths.
- Run security review for secrets, injection, unsafe shell use, auth, data
  exposure, dependency risk, destructive operations, and unsafe defaults.
- Read `references/test-and-security.md` when the task has meaningful risk,
  external integrations, deploy, auth, data handling, or broad code changes.

Exit: tests and security review are green, or all remaining gaps are explicitly
classified as non-blocking with rationale.

## Phase 7: ITERATE After Test

Goal: fix test or security findings with the full loop, not a hidden patch.

Do:

- Plan each must-fix item.
- Execute fixes through CAVEMAN.
- Re-verify acceptance criteria.
- Re-run relevant tests and security checks.

Exit: TEST is green.

## Phase 8: DELIVER / DEPLOY

Goal: deliver within the approved scope.

Do:

- If target is `repo-only`, commit, push, open a PR, or prepare the artifact as
  requested.
- If target is `prep-only`, produce deployment instructions, release notes, or
  readiness gaps.
- If target is `live-deploy`, confirm the deploy policy is satisfied before any
  deployment action.
- Verify delivery landed: pushed branch, artifact exists, PR created, deployed
  URL responds, or handoff checklist is complete.

Exit: approved delivery is complete and verified. If live deploy was not approved
or not safe, delivery stops at readiness reporting.

## Phase 9: REPORT

Goal: make the outcome auditable and easy to continue.

Report:

- What changed and why.
- Acceptance criteria and evidence.
- Tests, smoke checks, security review, and CI status.
- Delivery/deploy classification and result.
- CAVEMAN lane used or approved exception.
- Known limitations, follow-ups, and rollback/recovery notes.
- Learning update: result-log path, memory update status, durable learning
  candidates, and privacy/commit-safety decision.

Use `references/report-template.md` for larger tasks.

## Reference Routing

- Read `references/phase-checklists.md` for concrete phase checklists.
- Read `references/test-and-security.md` for side-effect, CI, smoke, and security
  gates.
- Read `references/deploy-readiness.md` when a task requests live deploy,
  release readiness, hosting work, or custom-domain verification.
- Read `references/adapters.md` when installing or adapting the skill for Codex,
  Hermes, Claude Code, Cursor, or AGENTS.md-only agents.
- Read `references/evaluation.md` when evaluating trigger quality, output quality,
  or release readiness.
- Read `references/self-learning.md` when maintaining per-repo memory, writing
  result logs, evaluating memory quality, or improving the skill's self-learning
  behavior.
- Read `references/report-template.md` for formal delivery reports.

## Maintenance Rule

When improving this skill itself, update:

- `development.md` for decisions and iteration results.
- `memory.md` for durable user preferences and settled decisions.
- `references/self-learning.md`, result-log templates, and validators when memory
  behavior changes.
- Product adapter references when tool-specific installation or invocation
  behavior changes.
