---
name: end-to-end-loop
description: "Run software and coding work through a disciplined delivery loop: discover, plan, execute, verify, iterate, test, optionally deploy, and report. Use when building, fixing, refactoring, debugging, testing, reviewing, shipping, or preparing a production-ready feature, script, service, tool, repo change, or release. CAVEMAN execution is mandatory for code-producing phases; if no CAVEMAN lane exists, stop before code changes and ask for an explicit exception. Live deploy only runs when the user opted in, the project is mature enough, and an applicable CI pipeline is green."
---

# End-to-End Loop

Use this skill as the operating loop for software work that must reach a
verified result. It is a portable core: follow it in Codex, Claude Code, Cursor,
AGENTS.md-compatible agents, or any coding tool with equivalent capabilities.

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
   security, deploy, or approval gates. Use deterministic scripts or the cheapest
   adequate model per phase, and escalate only when complexity, ambiguity, risk,
   repeated failure, or approval gates demand it.
9. Keep CAVEMAN ULTRA active as the compression and discipline layer throughout the
   whole run, not only during implementation. If the user's prompt evolves, grows,
   or adds new options mid-run, re-compress the working context into CAVEMAN ULTRA
   form before continuing so token use does not silently drift upward.
10. Before code-producing work, check that required CAVEMAN companion skills are
   installed and update-checked when the tool supports it. Treat skill install,
   skill update, and repo freshness checks as explicit side effects.
11. Work in an agile way: features and user stories need tightly scoped goals,
   clear skill settings/options, and precise verification layers before build.
12. Verification is the most important part of the loop. Use grilling when needed
   to define observable acceptance criteria and test/review layers before code.
13. On first run in a target project, initiate by understanding both the production
   runtime environment and the local development environment, then have the user
   confirm that environment model through a grilling routine before implementation.
14. At the start of every end-to-end-loop run and in every report, present the
   skill version from `VERSION` when available; if unavailable, say
   `end-to-end-loop version: unknown` rather than guessing.

## CAVEMAN Hard Gate

CAVEMAN is mandatory for the full run. CAVEMAN ULTRA is the default orchestration
and compression layer for DISCOVER, BACKLOG, PLAN, VERIFY, TEST, REPORT, and any
prompt-evolution handoff. CAVEMAN CODE or an adapter-equivalent lane is mandatory
for phases that produce code or repository changes.

Before each phase transition, and whenever the user adds scope mid-run:

1. Resolve the available CAVEMAN lane:
   - Preferred: CAVEMAN ULTRA for orchestration, context compression, dependency
     mapping, backlog analysis, model routing, and phase handoffs.
   - Preferred: CAVEMAN CODE for code edits.
   - Preferred: CAVEMAN REVIEW or a configured reviewer for review-only lanes.
   - If the tool exposes different CAVEMAN names, use the configured adapter.
2. Compress the working state into a compact payload: phase, mode/options,
   complexity level, plan, acceptance criteria, files, dependencies, constraints,
   verification hooks, open blockers, and token/cost budget.
3. If the prompt has grown, summarize the delta and discard irrelevant transcript
   detail before continuing. Do not let long prompts bypass CAVEMAN discipline.
4. If no CAVEMAN execution lane exists, stop before writing code or changing repo
   files and ask the user for an explicit exception. Mark the run as
   "CAVEMAN exception" in the report if the user approves.
5. Do not silently replace CAVEMAN with a generic agent, normal chat, or ad hoc
   execution.

Non-code discovery, backlog analysis, planning, research, reporting, and
documentation can run outside CAVEMAN CODE, but not outside CAVEMAN ULTRA-style
compression and phase discipline.

## Operating Options and Complexity Routing

Choose the lightest mode and options that can still produce observed evidence.
Options are additive: a task can run `backlog + github-copilot + standard`, for
example.

| Option / mode | Use for | Required behavior |
|---|---|---|
| `lean` | tiny docs, one-file fixes, deterministic checks, low risk | compact CAVEMAN ULTRA summaries, no bulk context, targeted verify |
| `standard` | normal multi-step coding or repo work | full phase gates, targeted references, staged tests |
| `deep` | architecture, security, deploy, auth, data, broad refactor, repeated failure | high-reasoning review, more helper agents, full reference/eval coverage |
| `backlog` | user supplies or asks to build a backlog before implementation | run BACKLOG before PLAN; do not start implementation until dependencies, feature interactions, ordering, complexity, model routing, and acceptance slices are explicit |
| `github-copilot` | GitHub repo work with CI/CD, PRs, or user-requested Copilot feedback | collect Copilot feedback where authenticated/available and feed it into VERIFY/TEST/ITERATE before claiming CI/CD or PR readiness |
| `grilling` | user asks to grill, stress-test, interrogate, or poke holes in a plan/design before building; or feature/user-story scope or verification is not crisp enough | use `skills/grilling/SKILL.md`; ask exactly one question at a time with a recommended answer, define goals and verification layers precisely, and inspect codebase instead of asking when the repo can answer |
| `handoff` | user asks to hand off, compact, resume later, or prepare another agent/session to continue | use `skills/handoff/SKILL.md`; write a redacted temporary handoff document with suggested skills and references to existing artifacts instead of duplicating them |

During BACKLOG or PLAN classify each workstream:

- `level_0`: mechanical/read-only/deterministic -> script, tool, or cheap/fast model.
- `level_1`: bounded implementation -> standard coding model plus CAVEMAN CODE.
- `level_2`: ambiguous architecture, safety, deploy, security, integration
  interference, or non-obvious dependency planning -> high-reasoning model or
  specialist reviewer.
- `level_3`: merge, release, deploy, admin, secrets, destructive/public claims, or
  acceptance of unresolved Copilot/security findings -> human approval gate.

Model routing must be written into the plan per backlog item or workstream. Use the
cheapest adequate model/tool, but escalate when dependency coupling, interference,
security, repeated failure, or Copilot/CI findings indicate higher reasoning is
needed. Always keep CAVEMAN ULTRA as the compact state layer across model handoffs.

## Backlog Option

Use `backlog` when the user wants to fill, triage, or sequence multiple features
before implementation.

Backlog flow:

1. Intake: normalize each backlog item into outcome, user value, rough scope,
   constraints, and done signal.
2. Feature/context fit: inspect current features, architecture, tests, CI, open
   plans, and relevant repo memory before judging implementation order.
3. Dependency round: identify prerequisites, shared files, data/API/schema changes,
   migration needs, feature flags, auth/permission impacts, and test/deploy
   dependencies.
4. Interference round: map conflicts between backlog items, including overlapping
   UI, data models, API contracts, sequencing hazards, performance impact, security
   risk, and user-experience inconsistency.
5. Slice and order: split large items into independently verifiable slices and order
   them by dependency, risk burn-down, value, and reversibility.
6. Complexity/model routing: assign `level_0`..`level_3` plus the recommended
   tool/model lane for each slice; mark human approval gates separately.
7. Plan gate: only then enter PLAN for the first selected slice or batch. Do not
   collapse backlog analysis into immediate implementation.

Backlog outputs:

- dependency graph or ordered dependency list;
- interference/conflict matrix or notes;
- ordered execution backlog with acceptance criteria per slice;
- complexity level and model/tool route per slice;
- explicit first batch and why it is safe to start.

## GitHub Copilot Option

Use `github-copilot` when GitHub CI/CD, PR readiness, or explicit Copilot review is
in scope.

Rules:

1. Check availability without installing new Copilot tooling unless installation is
   explicitly in scope. Acceptable sources include PR review comments, GitHub code
   review surfaces, `gh copilot` or `gh-copilot` when already installed, CI bot
   annotations, and authenticated GitHub API/CLI reads.
2. Treat Copilot feedback as evidence, not decoration. Categorize findings as
   must-fix, should-fix, false-positive, or blocked/unavailable, with rationale.
3. Feed must-fix Copilot findings back into ITERATE before reporting CI/CD green or
   PR-ready. Do not ignore unresolved Copilot findings because tests passed.
4. If Copilot feedback is unavailable, report the exact blocker and use normal
   review/security gates as fallback. Do not fabricate Copilot findings.
5. In CI/CD pipelines controlled by this skill, require a Copilot-feedback step or
   explicit unavailable/waived status in the pipeline report before delivery.

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
DISCOVER -> optional BACKLOG -> PLAN -> EXECUTE -> VERIFY -> ITERATE
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

`BACKLOG` is a first-class optional phase: when selected, it must complete before
PLAN and produces dependency, interference, ordering, complexity, and model-routing
evidence.

## Phase 1: DISCOVER

Goal: know what must be delivered and what would make the work unsafe or
incomplete.

Do:

- Restate the user's intended outcome, feature/user-story slice, and concrete done state.
- Present the active skill version from `VERSION` when available.
- Identify whether this is the first run in the target project. If yes, discover
  the production runtime environment and local development environment, then use
  `grilling` to get user confirmation of that environment model before build.
- Identify inputs, files, permissions, credentials, environments, target users,
  dependencies, and constraints.
- Identify side effects: filesystem writes, network calls, external services,
  installs, skill installs/updates, repo freshness checks, Copilot/GitHub API
  reads, secrets, CI, deploy, data changes, destructive operations.
- Decide whether operating options apply: `backlog`, `github-copilot`, `grilling`,
  `lean`, `standard`, or `deep`; record the selected skill settings/goals.
- If goals, scope, dependencies, or verification layers are vague, enter
  `grilling` before PLAN and resolve one decision at a time.
- Ask only material questions that cannot be safely inferred. Outside `grilling`,
  prefer one grouped question set over drip-fed clarification. Inside `grilling`,
  ask exactly one question at a time and wait for feedback.
- Record assumptions and risks.
- If present, read `.end-to-end-loop/memory.md` and
  `.end-to-end-loop/memory.local.md` for repo-specific facts, commands,
  blockers, preferences, prior outcomes, and failed approaches. Treat memory as
  context, not proof; re-verify safety or correctness facts before relying on
  them.

Exit: the goal, scope, risks, side effects, options, and needed context are known
or explicitly deferred.

## Optional Phase 1.5: BACKLOG

Goal: turn a feature backlog into a safe implementation queue before planning any
single feature.

Do when `backlog` is selected:

- Normalize backlog items into outcomes, current-feature fit, constraints, and done
  signals.
- Inspect current features, architecture, tests, CI, repo memory, and active plans
  that could affect the backlog.
- Run a dependency round: prerequisites, shared files, data/API/schema changes,
  migrations, feature flags, auth/permissions, CI/deploy needs, and required
  decisions.
- Run an interference round: conflicts between backlog items, overlapping UI/data
  changes, sequencing hazards, performance/security risks, and inconsistent UX.
- Split items into independently verifiable slices when needed.
- Assign each slice an execution order, complexity level (`level_0`..`level_3`),
  recommended tool/model route, verification hook, and human approval gate if any.
- Keep the BACKLOG payload CAVEMAN ULTRA compact before moving into PLAN.

Exit: dependency map, interference notes, ordered backlog, complexity/model routing,
and first safe batch are written. If dependencies are unknown, stop and resolve them
before implementation.

## Phase 2: PLAN

Goal: produce a concrete, verifiable path.

Do:

- Choose operating mode/options (`lean`, `standard`, `deep`, `backlog`,
  `github-copilot`, `grilling`) and classify complexity (`level_0`..`level_3`) for each
  workstream or backlog slice.
- Route work to the cheapest adequate execution path: deterministic tools/scripts
  for mechanical checks, cheap/fast models for low-risk summaries or scans,
  standard coding models for bounded implementation, and high-reasoning models or
  humans for architecture, security, deploy, auth, backlog interference, Copilot
  must-fix triage, or irreversible decisions.
- If `backlog` ran, convert its ordered slices into the first execution batch; do
  not re-order without explaining dependency or interference changes.
- If `github-copilot` applies, plan where Copilot feedback is collected and how
  must-fix findings re-enter ITERATE.
- Break work into small steps with verification hooks.
- Define acceptance criteria as pass/fail statements, with explicit verification
  layers for the slice: unit, integration, smoke, manual, security, CI, telemetry,
  reviewer, or other checks as applicable.
- Choose the delivery target: `none`, `repo-only`, `prep-only`, or `live-deploy`.
- Decide whether deploy is in scope. If yes, apply the deploy policy.
- Define test strategy: unit checks, integration checks, smoke path, security
  review, CI expectations, and any required model/agent reviewer. When running on
  Claude and a Codex connector is installed so Codex can be prompted, add a Codex
  agentic reviewer to the verification plan for code-producing work.
- Identify rollback or recovery for risky operations.

Exit: written plan, acceptance criteria, deploy classification, and test strategy.

## Phase 3: EXECUTE

Goal: implement the plan through the required execution lane.

Do:

- Pass implementation work through CAVEMAN as defined above.
- For new behavior or a bug fix that should be pinned by a test, prefer test-first
  via `skills/tdd/SKILL.md`: one failing behavioral test (red), minimal code
  (green), then refactor; test behavior through public interfaces and slice
  vertically.
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
- If `backlog` ran, verify the implemented slice still respects the dependency and
  interference plan; update the backlog if reality changed.
- If `github-copilot` applies, collect available Copilot feedback and classify each
  item before leaving VERIFY.
- Inspect the diff or artifact for correctness, edge cases, maintainability,
  portability, and instruction conflicts.
- Run the changed thing or the closest realistic verification command.
- Record findings and fixes. Do not move to TEST with must-fix issues open.

Exit: acceptance criteria pass and no must-fix review issues remain.

## Phase 5: ITERATE Toward Verify Green

Goal: close gaps found in VERIFY.

Do:

- Convert each failing criterion into a focused mini-plan.
- When a failure is a bug or regression rather than missing work, switch to
  `skills/diagnosing-bugs/SKILL.md`: build a reproducible feedback loop before
  hypothesizing or fixing, and do not fix without a failing loop.
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
- If `github-copilot` applies, ensure CI/CD or PR readiness includes Copilot
  feedback status: collected and processed, unavailable with exact blocker, or
  explicitly waived by the user.
- Treat unresolved must-fix Copilot findings like failing tests and route them back
  through ITERATE.
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
- Skill version reported for this run (`VERSION` or `unknown`).
- First-run environment status: production runtime environment, local development
  environment, and whether user confirmation happened through grilling when needed.
- Acceptance criteria and evidence.
- Tests, smoke checks, security review, reviewer status, and CI status.
- Delivery/deploy classification and result.
- Operating mode/options, complexity/model routing decisions, and CAVEMAN ULTRA
  compression status after prompt evolution.
- Backlog output when used: dependency map, interference findings, ordered slices,
  first batch, and changed ordering rationale.
- Copilot feedback status when `github-copilot` applies: source, findings processed,
  false positives, blockers/unavailability, or user waiver.
- CAVEMAN lane used or approved exception.
- Known limitations, follow-ups, and rollback/recovery notes.
- Learning update: result-log path, memory update status, durable learning
  candidates, and privacy/commit-safety decision.
- Handoff: when the `handoff` option is selected or another agent/session will
  resume the work, produce a handoff document via `skills/handoff/SKILL.md` that
  references existing artifacts instead of duplicating them, lists suggested next
  skills, and redacts secrets/PII.

Use `references/report-template.md` for larger tasks.

## Reference Routing

- Read `references/backlog-and-copilot.md` when `backlog` or `github-copilot`
  options are selected, when CI/CD feedback must include Copilot findings, or when
  long prompts need CAVEMAN ULTRA context compression.
- Read `skills/grilling/SKILL.md` when the user asks to grill, stress-test,
  interrogate, or poke holes in a plan/design before building.
- Read `skills/handoff/SKILL.md` when handing off, compacting, or preparing
  another agent/session to resume the work.
- Read `skills/diagnosing-bugs/SKILL.md` when EXECUTE/VERIFY/ITERATE turns into
  debugging a crash, wrong output, flaky test, or performance regression; build a
  reproducible feedback loop before hypothesizing or fixing.
- Read `skills/tdd/SKILL.md` when adding new behavior or locking in a bug fix
  test-first (red-green-refactor, behavior over implementation, vertical slices).
- Read `references/local-telemetry.md` when local measurement, performance
  evidence, phase/command timing, token/cost capture, CAVEMAN compliance metrics,
  Copilot availability metrics, or telemetry research is in scope. Telemetry is
  local-first and opt-in; default operation must not create network writes or
  commit raw logs.
- Read `references/mission-mode.md` when deciding whether to spawn helper agents,
  parallelize independent workstreams, or choose the model/reasoning route
  (`level_0`..`level_3`) for a workstream. Mission Mode is optional and must not
  weaken CAVEMAN, deploy, security, or approval gates.
- Read `references/phase-checklists.md` for concrete phase checklists.
- Read `references/test-and-security.md` for side-effect, CI, smoke, and security
  gates.
- Read `references/deploy-readiness.md` when a task requests live deploy,
  release readiness, hosting work, or custom-domain verification.
- Read `references/adapters.md` when installing or adapting the skill for Codex,
  Claude Code, Cursor, or AGENTS.md-only agents.
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
- `paper.md` for research findings and shareable rationale.
- Adapter handoff files under `handoff/` when product operating instructions
  change and those files exist in the package.
- `references/self-learning.md`, result-log templates, and validators when memory
  behavior changes.
- `references/backlog-and-copilot.md`, trigger evals, and report/checklist templates
  when backlog sequencing, Copilot feedback, CAVEMAN ULTRA compression, or model
  routing behavior changes.
