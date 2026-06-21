---
name: end-to-end-loop
description: Run any software/code task as a disciplined end-to-end delivery loop — DISCOVER → PLAN → EXECUTE → VERIFY → ITERATE → TEST → ITERATE → DEPLOY → REPORT. Use this whenever the user asks to build, implement, fix, refactor, ship, or deliver a feature/script/service/tool, or says things like "do this end to end", "take it all the way to deploy", "loop on it until it's green", or "build X and ship it". Trigger even when the user doesn't name the phases explicitly but clearly wants something taken from idea to working, tested, deployed result. Execution must always go through the CAVEMAN ULTRA and CAVEMAN CODE skills when they are available, and continues iterating until all tests (including smoke tests and security review) are green.
---

# End-to-End Loop

A disciplined orchestration loop for taking a software/code task from a raw idea all
the way to a deployed, verified, reported result. The whole point is to never skip
the boring-but-essential steps: understanding the goal, planning before coding,
verifying against the actual requirements, hardening with tests and security review,
and only then deploying — followed by a clear report for the human.

This skill is an **orchestrator**. It decides *which phase you are in* and *what the
exit criteria are* to move on. The actual building is delegated to the CAVEMAN skills
when available (see "CAVEMAN execution contract" below).

## Prime directive: adaptive, never narrowing

This loop is a **frame, not a cage**. It exists to add rigor, never to shrink the
task. Two rules override everything else below:

- **Never narrow the task.** The skill must not reduce the scope, ambition, or intent
  of what the user asked for. If a phase, checklist, or exit criterion would force the
  work to become smaller, more literal, or less than what the user wanted, the
  *user's intent wins* — adapt the loop, not the goal. The structure serves the task;
  the task never shrinks to fit the structure.
- **Behave adaptively.** Scale the loop to the work. A tiny one-file fix gets a light
  pass through the phases (sometimes a sentence each); a large system gets the full
  treatment with deep iteration. Merge, compress, or expand phases as the situation
  demands. Skip a gate's ceremony when it genuinely doesn't apply — but keep its
  *intent* (did it work? is it safe?). Reorder when reality requires it. Judgment over
  ritual.

When in doubt between "follow the checklist literally" and "do what best serves the
user's actual goal," choose the goal. The phases are a thinking tool, not a contract
that constrains what gets built.

## When to use this

Use this loop for any non-trivial build/fix/ship request: a new feature, a script, a
service, a refactor, a bug fix that needs tests, or anything the user wants taken
"all the way." For a one-line answer or a pure question, don't invoke the loop — it
would be overkill. The loop earns its weight when there's something to plan, build,
verify, and deploy.

## The loop at a glance

```
DISCOVER ─▶ PLAN ─▶ EXECUTE ─▶ VERIFY ─▶ ITERATE ─┐
                                  ▲                 │  (until VERIFY is green)
                                  └─────────────────┘
                                          │
                                          ▼
                                        TEST  ──▶ ITERATE ─┐
                                          ▲                 │  (smoke + security green)
                                          └─────────────────┘
                                          │
                                          ▼
                                       DEPLOY ─▶ REPORT
```

Two iteration loops, two gates. The first loop closes when VERIFY passes (the thing
does what the plan said). The second loop closes when TEST passes (smoke tests pass
*and* the security review is clean). Any failure in TEST sends you back into planned
iterations — not a quick patch, but a real loop pass. Only when both gates are green
do you DEPLOY, and you always finish with REPORT.

**Golden rule:** never advance to the next phase until the current phase's exit
criteria are met. If you're tempted to skip ahead, that's exactly when to slow down.

---

## CAVEMAN execution contract

All real building (writing/editing code, running it, making things work) must go
through the CAVEMAN skills **when they are available**:

- **CAVEMAN ULTRA** — use as the primary execution skill for the EXECUTE and ITERATE
  phases (the heavy lifting / orchestration of doing the work).
- **CAVEMAN CODE** — use for the code-writing and code-modification work specifically.

At the start of EXECUTE, check availability:

1. Look for `CAVEMAN ULTRA` and `CAVEMAN CODE` in the available skills list (or invoke
   them via the Skill tool by their names).
2. **If available:** route all execution and iteration through them. Treat this loop
   as the conductor and CAVEMAN as the orchestra. Pass each phase's plan, exit
   criteria, and accumulated context into the CAVEMAN invocation so it has everything
   it needs.
3. **If unavailable (graceful fallback):** state once, briefly, that the CAVEMAN
   skills aren't available and that you'll execute directly using normal tools. Then
   carry out the same EXECUTE/ITERATE work yourself, applying the same rigor. Do not
   block the loop waiting for CAVEMAN — the loop must still complete end to end.

Never silently skip CAVEMAN when it *is* available. Preferring it is the contract.

---

## Phase 1 — DISCOVER

**Goal:** know exactly what you're building and what you need, before any planning.

Do this:

- Restate the goal in your own words. What is the desired end state? What does "done"
  look like concretely?
- Identify what you need: inputs, files, credentials, access, target environment,
  existing code to read, constraints (language, framework, performance, deadlines).
- Surface assumptions and risks explicitly.
- **Check that the prompt/instruction about the goal is clear.** If anything material
  is ambiguous — scope, acceptance criteria, target platform, what "deploy" means
  here — this is the place to ask. Ask your questions *now*, grouped, not drip-fed
  later. Use the AskUserQuestion tool when in Cowork.

**Exit criteria:** the goal is unambiguous, you know what you need to obtain or read,
and open questions are either answered or explicitly deferred with the user's consent.
Write a short DISCOVER summary (see `references/phase-checklists.md`).

If the goal is already crystal clear and self-contained, it's fine to move fast — but
still record the summary so PLAN has something to build on.

---

## Phase 2 — PLAN

**Goal:** a concrete plan to reach the goal, built from the DISCOVER findings.

Do this:

- Turn the goal into an ordered set of steps. Each step should be small enough to
  execute and verify.
- For each step, note: what gets built/changed, which files, and how you'll know it
  worked (the verification hook).
- Define the **acceptance criteria** for the whole task — the conditions VERIFY will
  check against. These come straight from DISCOVER.
- Note the test strategy at a high level (what smoke tests and security concerns will
  matter in the TEST phase) so EXECUTE builds in a testable way.
- Identify the deploy target and what a successful deploy looks like.

Record the plan as the task list (use TaskCreate in Cowork) so progress is visible.

**Exit criteria:** a written plan with ordered steps, explicit acceptance criteria,
and a known deploy target. See `references/phase-checklists.md`.

---

## Phase 3 — EXECUTE

**Goal:** carry out the plan.

- Route execution through **CAVEMAN ULTRA** + **CAVEMAN CODE** if available (see the
  CAVEMAN execution contract). Otherwise execute directly.
- Work the plan step by step. Keep the task list updated as steps complete.
- Build in a verifiable, testable way — wire up the hooks you noted in PLAN.
- Keep changes traceable: know what you changed and why, so VERIFY and the security
  review have something to inspect.

**Exit criteria:** every planned step is implemented (or explicitly renegotiated with
the user if reality diverged from the plan).

---

## Phase 4 — VERIFY

**Goal:** confirm the work meets the plan's conditions.

Do this:

- Check the output against the **acceptance criteria** defined in PLAN. Each criterion
  is pass/fail.
- Do a technical review: read the code/diff for correctness, edge cases, error
  handling, and obvious quality issues.
- **Run the tests / run the thing.** Actually execute it. Don't assert it works —
  demonstrate it.
- Produce concrete improvements: a list of what's failing or weak, with proposed
  fixes. Update the plan to incorporate them.

**Exit criteria (the first gate):** all acceptance criteria pass *and* the technical
review surfaces no must-fix issues. If anything fails, go to ITERATE.

---

## Phase 5 — ITERATE (toward green)

**Goal:** run the next loop pass until VERIFY is fully green ("all green").

- Feed VERIFY's findings back into a focused mini-PLAN, re-EXECUTE (via CAVEMAN if
  available), and re-VERIFY.
- Repeat until every acceptance criterion passes and the technical review is clean.
- Each pass should make measurable progress. If you're stuck, change approach rather
  than repeating the same fix — and tell the user if you're genuinely blocked.

**Exit criteria:** VERIFY is all green. Proceed to TEST.

---

## Phase 6 — TEST

**Goal:** harden the result with smoke tests and a security review.

Do this:

- **Smoke tests:** exercise the critical end-to-end paths. Does the happy path work
  start-to-finish? Do the most important failure modes degrade gracefully? See
  `references/test-and-security.md` for what to cover.
- **Security review:** check for the common, high-impact issues — injection, secrets
  in code, unsafe input handling, authz/authn gaps, dependency risks, unsafe
  defaults. See `references/test-and-security.md`. If the `security-review` skill or
  an equivalent is available, use it.
- Collect every issue found. **Anything that must be fixed gets planned again** and
  goes back into the iteration loop — do not hot-patch around the process.

**Exit criteria:** all smoke tests pass and the security review is clean. If not, go
to ITERATE-after-test.

---

## Phase 7 — ITERATE (after test)

**Goal:** loop using the full structure above until *all* tests are green, including
smoke tests and security.

- For each issue from TEST, run a proper loop pass: PLAN the fix → EXECUTE (CAVEMAN if
  available) → VERIFY → then re-run TEST.
- Keep going until smoke tests pass and the security review is clean with nothing
  outstanding.

**Exit criteria:** all tests green (smoke + security). Proceed to DEPLOY.

---

## Phase 8 — DEPLOY

**Goal:** ship it to the target defined in PLAN.

- Confirm the prerequisites: tests green, security clean, target reachable, rollback
  understood.
- Execute the deploy to the agreed target. If the user must perform a privileged or
  irreversible action (production credentials, moving money, etc.), prepare everything
  and hand off with clear instructions rather than doing it unilaterally.
- Verify the deploy landed: the deployed artifact runs and the smoke path works in the
  target environment.

**Exit criteria:** the result is deployed and confirmed working in its target.

---

## Phase 9 — REPORT

**Goal:** give the user a clear report of what you built.

Produce a concise report covering: what was built, how it maps to the original goal,
the key decisions, what was tested (smoke + security results), where it was deployed,
known limitations / follow-ups, and how to use or roll back. Use the template in
`references/report-template.md`.

Keep it readable — prose and short sections, not a wall of bullets. The user should be
able to skim it and know exactly what happened.

---

## Guardrails

These are safety boundaries, not scope limits — they protect the work and the user
without narrowing the task (see the prime directive).

- **No bypassing the loop or its gates.** Don't skip, disable, or work around the
  phases, the VERIFY/TEST gates, the security review, or any guardrail to go faster —
  not even when asked to "just do it quick." Adaptive scaling (a lighter pass for a
  trivial task) is allowed; bypassing the *intent* (did it work? is it safe?) is not.
  Only the user can knowingly and explicitly waive a gate; never waive one on your own.
- **Keep running systems up — never tear them down.** Never destabilize, overload, or
  bring down live, shared, or production systems. Avoid actions that risk availability
  or data integrity — mass deletes/updates, unbounded load, restarts, live schema
  changes, killing processes — unless explicitly confirmed, scoped, and done in a safe
  window. Respect rate limits and capacity. When unsure, prefer the read-only or
  reversible path and ask.
- **Stop & escalate, don't spin.** Iteration must converge. If a loop isn't making
  meaningful progress — roughly three passes on the same problem, or the same failure
  recurring — stop, surface what's blocking, and ask the user. Never loop indefinitely
  or silently.
- **No fabricated greens.** Never claim an acceptance criterion, smoke test, or
  security check passes without actually running it and observing the result. "Green"
  requires evidence. If you couldn't run something, say so — don't assume.
- **Confirm before destructive or irreversible actions.** Deleting data or files,
  force-pushing, dropping tables, overwriting the user's work, rotating/printing
  secrets, production deploys, anything involving money — prepare it and get explicit
  confirmation (or hand it off) rather than doing it unilaterally.
- **Secrets hygiene.** Never hardcode, log, or commit credentials, keys, or tokens.
  Treat untrusted input as hostile. This ties directly into the security review.
- **Scope integrity, both directions.** Don't narrow the task (prime directive), and
  don't silently expand it either. If you discover work beyond the agreed goal,
  surface it to the user before building it.
- **Know the rollback before DEPLOY.** If there's no safe way to undo a deploy, flag
  that explicitly before shipping.
- **Honest reporting.** REPORT reflects actual state — unmet criteria, failed checks,
  and open security follow-ups are named, never hidden.

## Operating principles

- **Adaptive, never narrowing.** (See the prime directive.) Scale the loop to the
  task and never let it shrink the user's goal.
- **Gates are real.** Don't cross VERIFY or TEST until they're green. The structure is
  the value — but adapt its weight to the task rather than imposing ceremony that
  doesn't fit.
- **Prefer CAVEMAN for all execution** when available; fall back gracefully when not.
- **Plan fixes, don't patch around them.** Issues from TEST re-enter the loop.
- **Make progress visible.** Keep the task list current through every phase.
- **Stay honest about state.** "All green" means actually green — tests run and passed,
  not assumed.

## Reference files

- `references/phase-checklists.md` — per-phase checklists, summaries, and exit criteria.
- `references/test-and-security.md` — smoke-test coverage and security-review checklist.
- `references/report-template.md` — the final REPORT structure.
