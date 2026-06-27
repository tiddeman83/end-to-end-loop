---
name: end-to-end-loop
description: "Use for building, fixing, refactoring, debugging, testing, reviewing, shipping, release prep, scripts, services, tools, repo changes, and production-ready coding delivery that needs plan -> execute -> verify -> test -> deliver/report. Requires CAVEMAN, lean token use, model routing by complexity, helper-agent consideration, and opt-in gated live deploy."
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
8. Minimize token, time, and model cost without weakening evidence, CAVEMAN,
   security, deploy, or approval gates. Use the cheapest adequate model or
   deterministic script for each phase and escalate only when complexity demands it.
9. Before code-producing work, check that required CAVEMAN companion skills are
   installed and update-checked when the tool supports it. Treat skill install,
   skill update, and repo freshness checks as explicit side effects.

## Operating Modes and Complexity Routing

Choose the lightest mode that can still produce observed evidence:

| Mode | Use for | Token/speed policy |
|---|---|---|
| `lean` | tiny docs, one-file fixes, deterministic checks, low risk | compact DISCOVER/PLAN, no bulk context, targeted verify, compact report |
| `standard` | normal multi-step coding or repo work | full phase gates, targeted references, staged tests |
| `deep` | architecture, security, deploy, auth, data, broad refactor, repeated failure | high-reasoning review, more helper agents, full reference and eval coverage |

During PLAN classify each workstream:

- `level_0`: mechanical/read-only/deterministic -> script, tool, or cheap/fast model.
- `level_1`: bounded implementation -> standard coding model plus CAVEMAN.
- `level_2`: ambiguous architecture, safety, deploy, security -> high-reasoning model or specialist reviewer.
- `level_3`: merge, release, deploy, admin, secrets, destructive/public claims -> human approval gate.

Always consider helper agents for independent discovery, implementation, tests,
security review, diff review, or eval/report compression. Spawn them only when
parallelism or specialized review beats the context/coordination cost.

## CAVEMAN Hard Gate

CAVEMAN is mandatory for code-producing phases.

Before EXECUTE or ITERATE:

1. Run the CAVEMAN install/update preflight from `references/adapters.md` when the
   tool supports skill discovery, install, or update checks:
   - Preferred: CAVEMAN ULTRA for execution orchestration.
   - Preferred: CAVEMAN CODE for code edits.
   - Preferred: CAVEMAN REVIEW or a configured reviewer for review-only lanes.
   - If the tool exposes different CAVEMAN names, use the configured adapter.
2. If a required CAVEMAN companion skill is missing or outdated, install/update it
   when permissions and approval allow. If that is blocked, report the exact
   blocker before any code-producing work.
3. Pass a compact payload into that lane: phase, mode, complexity level, plan,
   acceptance criteria, files, constraints, and verification hooks. Do not resend
   full transcripts or unrelated files.
4. If no CAVEMAN execution lane exists after install/update discovery, stop before
   writing code or changing repo files and ask the user for an explicit exception.
   Mark the run as "CAVEMAN exception" in the report if the user approves.
5. Do not silently replace CAVEMAN with a generic agent, normal chat, or ad hoc
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
  installs, skill installs/updates, repo freshness checks, secrets, CI, deploy,
  data changes, destructive operations.
- Ask only material questions that cannot be safely inferred. Prefer one grouped
  question set over drip-fed clarification.
- Record assumptions and risks.
- Identify the active `end-to-end-loop` source/version/commit. If an upstream repo
  or source package is configured and network access is allowed, check freshness
  before relying on stale installed instructions.
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

- Choose operating mode (`lean`, `standard`, `deep`) and classify complexity
  (`level_0`..`level_3`) for each workstream.
- Route work to the cheapest adequate execution path: deterministic tools/scripts
  for mechanical checks, cheap/fast models for low-risk summaries or scans,
  standard coding models for bounded implementation, and high-reasoning models or
  humans for architecture, security, deploy, auth, or irreversible decisions.
- Consider helper agents for parallelizable discovery, implementation, review,
  testing, security, or reporting; skip them when coordination/context cost is
  higher than the expected speed or quality gain.
- Break work into small steps with verification hooks.
- Define acceptance criteria as pass/fail statements.
- Choose the delivery target: `none`, `repo-only`, `prep-only`, or `live-deploy`.
- Decide whether deploy is in scope. If yes, apply the deploy policy.
- Define test strategy: unit checks, integration checks, smoke path, security
  review, and CI expectations.
- Identify rollback or recovery for risky operations.
- Plan skill install/update and repo freshness side effects explicitly, including
  approval requirements, reload/fresh-session needs, and blocked fallbacks.

Exit: written plan, acceptance criteria, deploy classification, and test strategy.

## Phase 3: EXECUTE

Goal: implement the plan through the required execution lane.

Do:

- Pass implementation work through CAVEMAN as defined above, using compact
  workstream payloads and the selected model/agent route.
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
- Run the fastest targeted verification first, then broaden only when change
  scope, risk, or failing evidence warrants it. Parallelize independent checks
  when the tool supports it.
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
  equivalents. Start with targeted cheap checks, then expand to full suites for
  broad, risky, release, or deploy-bound changes.
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
- CAVEMAN lane used, install/update status, or approved exception.
- `end-to-end-loop` source/version and repo freshness/self-update status.
- Operating mode, model-routing decisions, helper agents considered/used, and any
  token/time/cost measurements or stated measurement limits.
- Known limitations, follow-ups, reload/fresh-session needs, and rollback/recovery notes.
- Learning update: result-log path, memory update status, durable learning
  candidates, and privacy/commit-safety decision.

Use a compact report by default: outcome, changed files, evidence, tests/CI/security,
CAVEMAN/update status, routing decisions, blockers/next. Use
`references/report-template.md` only for larger, high-risk, or audited tasks.

## Reference Routing

Reference budget: start with `SKILL.md` only, then load the smallest needed
reference for the active trigger. Do not load all references by default. When a
reference is loaded, compress its operational impact to <=5 bullets before
continuing.

- Read `references/phase-checklists.md` for concrete phase checklists.
- Read `references/test-and-security.md` for side-effect, CI, smoke, and security
  gates.
- Read `references/deploy-readiness.md` when a task requests live deploy,
  release readiness, hosting work, or custom-domain verification.
- Read `references/adapters.md` when installing or adapting the skill for Codex,
  Hermes, Claude Code, Cursor, or AGENTS.md-only agents, including CAVEMAN
  companion install/update and `end-to-end-loop` freshness checks.
- Read `references/evaluation.md` when evaluating trigger quality, output quality,
  or release readiness.
- Read `references/self-learning.md` when maintaining per-repo memory, writing
  result logs, evaluating memory quality, or improving the skill's self-learning
  behavior.
- Read `references/report-template.md` for formal delivery reports.
- Read `references/mission-mode.md` when a task is parallelizable, repeatedly
  failing, broad enough for specialized review/evals, or explicitly asks for
  faster/more-agent execution.

## Maintenance Rule

When improving this skill itself, update:

- `development.md` for decisions and iteration results.
- `memory.md` for durable user preferences and settled decisions.
- `references/self-learning.md`, result-log templates, and validators when memory
  behavior changes.
- Product adapter references when tool-specific installation, invocation,
  CAVEMAN install/update, model routing, or repo freshness behavior changes.
- `README.md`, evals, and validators when install/update, optimization, helper
  agent, or self-update behavior changes.
