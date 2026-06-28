# Phase checklists and exit criteria

Use these as concrete gates. A phase is done only when its exit criteria are met.
Keep the written summaries short — they exist to carry context to the next phase.

---

## DISCOVER

Checklist:
- [ ] Goal restated in own words; "done" defined concretely.
- [ ] Inputs, files, access, credentials, target environment identified.
- [ ] Constraints captured (language, framework, perf, deadline, platform).
- [ ] Side effects identified: writes, network, installs, external services, data,
      credentials, destructive actions, deploy, GitHub/Copilot reads.
- [ ] Operating options selected: `lean` / `standard` / `deep`, plus `backlog` and/or
      `github-copilot` and/or `review-improve` when applicable.
- [ ] CAVEMAN ULTRA state packet initialized for compact phase handoffs.
- [ ] Assumptions and risks listed.
- [ ] Ambiguities resolved or explicitly deferred with user consent.

DISCOVER summary template:
```
GOAL: <one or two sentences>
DONE LOOKS LIKE: <observable end state>
NEED: <inputs / access / files / env>
CONSTRAINTS: <...>
ASSUMPTIONS / RISKS: <...>
OPEN QUESTIONS: <answered | deferred | none>
```

Exit: goal unambiguous, needs known, side effects classified, questions handled.

---

## BACKLOG (optional, before PLAN)

Use when `backlog` is selected.

Checklist:
- [ ] Backlog items normalized into outcomes, constraints, and done signals.
- [ ] Current features/architecture/tests/CI/repo memory inspected for context fit.
- [ ] Dependencies mapped: prerequisites, shared files, data/API/schema, auth,
      migrations, feature flags, CI/deploy, and required decisions.
- [ ] Interference mapped: cross-item conflicts, overlap, sequencing hazards,
      performance/security risks, and UX inconsistencies.
- [ ] Large items split into independently verifiable slices.
- [ ] Each slice assigned order, complexity (`level_0`..`level_3`), model/tool route,
      verification hook, and human approval gate if applicable.
- [ ] CAVEMAN ULTRA state packet updated before PLAN.

BACKLOG summary template:
```
BACKLOG_OPTION: selected
DEPENDENCIES: <ordered map/list>
INTERFERENCE: <conflict matrix/notes>
ORDERED_SLICES: <slice -> reason>
COMPLEXITY/MODEL: <slice -> level + route>
FIRST_BATCH: <what starts first and why>
BLOCKERS: <unknown deps / approval needs>
```

Exit: dependencies/interference/order/complexity/model routing are explicit and the
first safe execution batch is known.

---

## REVIEW-IMPROVE (optional, before or inside PLAN)

Use when `review-improve` is selected.

Checklist:
- [ ] Review surfaces inventoried: production skill, references, subskills, README,
      evals, validators, install scripts, release notes, memory/research docs as applicable.
- [ ] Cross-document claims compared for naming, version/status, packaged files,
      trigger conditions, CAVEMAN, deploy, security, telemetry, and self-learning behavior.
- [ ] Maintenance risks checked: stale claims, duplication, unsupported aspirations,
      private/internal details, weak examples, and validator/documentation mismatch.
- [ ] Findings ranked by blocker/high/medium/low/follow-up with evidence.
- [ ] Accepted improvements converted into scoped changes with verification hooks.

REVIEW-IMPROVE summary template:
```
REVIEWED: <files/commands/surfaces>
FINDINGS: <ranked evidence-backed list>
CHANGES_PLANNED: <small scoped edits>
DEFERRED: <follow-ups and why>
VERIFY: <commands/checks>
```

Exit: findings are evidence-backed, ranked, and either implemented, deferred, or
reported.

---

## PLAN

Checklist:
- [ ] Operating mode/options and complexity level chosen per workstream or backlog
      slice.
- [ ] Model/tool route selected per slice using cheapest adequate route, with
      escalation rationale for high-reasoning or human-gated work.
- [ ] If BACKLOG ran, first execution batch follows the dependency/interference order.
- [ ] Ordered steps, each small enough to execute and verify.
- [ ] Each step has a verification hook ("how I'll know it worked").
- [ ] Acceptance criteria for the whole task written (these drive VERIFY).
- [ ] High-level test strategy noted (smoke paths + security concerns for TEST).
- [ ] Delivery target classified: `none`, `repo-only`, `prep-only`, or `live-deploy`.
- [ ] Deploy opt-in checked. If live deploy is requested, deploy prerequisites are
      listed: CI, maturity, rollback, credentials, approvals, target env.
- [ ] Plan recorded as the task list.

Acceptance criteria template:
```
AC1: <pass/fail condition>
AC2: <pass/fail condition>
...
```

Exit: written plan + acceptance criteria + delivery classification.

---

## EXECUTE

Checklist:
- [ ] CAVEMAN lane resolved before code/repo changes.
- [ ] CAVEMAN ULTRA / CAVEMAN CODE, or configured equivalents, used for code
      changes; if unavailable, explicit user exception recorded before edits.
- [ ] Steps worked in order; task list kept current.
- [ ] Built testable; verification hooks wired in.
- [ ] Changes traceable (what changed and why).

Exit: all planned steps implemented (or plan renegotiated with user).

---

## VERIFY  (Gate 1)

Checklist:
- [ ] Each acceptance criterion checked: pass/fail.
- [ ] If BACKLOG ran, dependency/interference assumptions still hold or backlog was
      updated with changed ordering rationale.
- [ ] If `github-copilot` applies, Copilot feedback collected/classified or exact
      blocker recorded.
- [ ] Technical review done: correctness, edge cases, error handling, quality.
- [ ] Code/the thing actually run — results observed, not assumed.
- [ ] Improvements listed with proposed fixes; plan updated.

Exit (Gate 1): all acceptance criteria pass AND no must-fix review issues.
If not green → ITERATE.

---

## ITERATE (toward green)

Checklist:
- [ ] VERIFY findings turned into a focused mini-plan.
- [ ] Re-executed through the required CAVEMAN lane or an explicit user-approved
      exception, then re-verified.
- [ ] Measurable progress each pass; approach changed if stuck.

Exit: VERIFY all green → TEST.

---

## TEST

Checklist:
- [ ] Smoke tests cover critical end-to-end paths (see test-and-security.md).
- [ ] Security review done (see test-and-security.md); use `security-review` skill if available.
- [ ] CI status checked when a CI pipeline is applicable.
- [ ] If `github-copilot` applies, Copilot feedback is processed, unavailable with
      exact blocker, or explicitly waived; unresolved must-fix findings route to ITERATE.
- [ ] All issues collected; must-fix items routed back into the loop (planned, not patched).

Exit: smoke tests pass, security review clean, and applicable CI is green or
explicitly waived by the user. If not -> ITERATE (after test).

---

## ITERATE (after test)

Checklist:
- [ ] Each TEST issue handled as a full pass: PLAN → EXECUTE → VERIFY → re-TEST.
- [ ] Loop continues until smoke + security are green with nothing outstanding.

Exit: all tests green → DEPLOY.

---

## DELIVER / DEPLOY

Checklist:
- [ ] Delivery classification followed: `none`, `repo-only`, `prep-only`, or
      `live-deploy`.
- [ ] For live deploy: user explicitly opted in for this task.
- [ ] For live deploy: project maturity, applicable CI, rollback, credentials, and
      environment readiness confirmed.
- [ ] Approved delivery completed: commit/push/PR/artifact/readiness report/deploy.
- [ ] Delivery verified: branch pushed, artifact exists, PR opened, or deployed
      target smoke-tested.

Exit: approved delivery completed and verified. If live deploy conditions fail,
deliver readiness report instead.

---

## REPORT

Checklist:
- [ ] Report written from report-template.md.
- [ ] Maps result back to the original goal and acceptance criteria.
- [ ] Operating mode/options, complexity/model routing, and CAVEMAN ULTRA packet
      status recorded.
- [ ] Backlog dependency/interference/order output reported when BACKLOG ran.
- [ ] If `review-improve` applies, reviewed surfaces, ranked findings, applied
      improvements, deferred follow-ups, and validation evidence reported.
- [ ] CAVEMAN lane or approved exception recorded.
- [ ] Test, CI, security results, delivery target, limitations, usage/rollback included.

Exit: user has a clear, skimmable report.
