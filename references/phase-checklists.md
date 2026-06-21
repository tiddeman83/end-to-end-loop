# Phase checklists & exit criteria

Use these as concrete gates. A phase is done only when its exit criteria are met.
Keep the written summaries short — they exist to carry context to the next phase.

---

## DISCOVER

Checklist:
- [ ] Goal restated in own words; "done" defined concretely.
- [ ] Inputs, files, access, credentials, target environment identified.
- [ ] Constraints captured (language, framework, perf, deadline, platform).
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

Exit: goal unambiguous, needs known, questions handled.

---

## PLAN

Checklist:
- [ ] Ordered steps, each small enough to execute and verify.
- [ ] Each step has a verification hook ("how I'll know it worked").
- [ ] Acceptance criteria for the whole task written (these drive VERIFY).
- [ ] High-level test strategy noted (smoke paths + security concerns for TEST).
- [ ] Deploy target and "successful deploy" defined.
- [ ] Plan recorded as the task list.

Acceptance criteria template:
```
AC1: <pass/fail condition>
AC2: <pass/fail condition>
...
```

Exit: written plan + acceptance criteria + deploy target.

---

## EXECUTE

Checklist:
- [ ] CAVEMAN ULTRA / CAVEMAN CODE used if available (else fallback noted once).
- [ ] Steps worked in order; task list kept current.
- [ ] Built testable; verification hooks wired in.
- [ ] Changes traceable (what changed and why).

Exit: all planned steps implemented (or plan renegotiated with user).

---

## VERIFY  (Gate 1)

Checklist:
- [ ] Each acceptance criterion checked: pass/fail.
- [ ] Technical review done: correctness, edge cases, error handling, quality.
- [ ] Code/the thing actually run — results observed, not assumed.
- [ ] Improvements listed with proposed fixes; plan updated.

Exit (Gate 1): all acceptance criteria pass AND no must-fix review issues.
If not green → ITERATE.

---

## ITERATE (toward green)

Checklist:
- [ ] VERIFY findings turned into a focused mini-plan.
- [ ] Re-executed (CAVEMAN if available) and re-verified.
- [ ] Measurable progress each pass; approach changed if stuck.

Exit: VERIFY all green → TEST.

---

## TEST

Checklist:
- [ ] Smoke tests cover critical end-to-end paths (see test-and-security.md).
- [ ] Security review done (see test-and-security.md); use `security-review` skill if available.
- [ ] All issues collected; must-fix items routed back into the loop (planned, not patched).

Exit: smoke tests pass AND security review clean. If not → ITERATE (after test).

---

## ITERATE (after test)

Checklist:
- [ ] Each TEST issue handled as a full pass: PLAN → EXECUTE → VERIFY → re-TEST.
- [ ] Loop continues until smoke + security are green with nothing outstanding.

Exit: all tests green → DEPLOY.

---

## DEPLOY

Checklist:
- [ ] Prerequisites confirmed: tests green, security clean, target reachable, rollback understood.
- [ ] Deployed to the agreed target (privileged/irreversible actions handed off to user with instructions).
- [ ] Deploy verified: artifact runs and smoke path works in target env.

Exit: deployed and confirmed working.

---

## REPORT

Checklist:
- [ ] Report written from report-template.md.
- [ ] Maps result back to the original goal and acceptance criteria.
- [ ] Test + security results, deploy location, limitations, usage/rollback included.

Exit: user has a clear, skimmable report.
