---
name: diagnosing-bugs
description: Diagnose hard bugs and regressions by building a reproducible feedback loop before hypothesizing or fixing. Use when debugging a failing test, crash, wrong output, flaky behavior, or performance regression.
---

# Diagnosing Bugs

Use this subskill inside the end-to-end loop whenever EXECUTE, VERIFY, or ITERATE
turns into debugging: a crash, wrong output, flaky test, or performance
regression. The discipline is feedback-loop-first.

## Hard Rule

Do not hypothesise or fix without a working feedback loop that reliably triggers
the bug. If you cannot build one, stop and ask the user for captured artifacts,
logs, or access, and record the blocker instead of guessing at a fix.

## Phase 1 — Build a feedback loop (the critical step)

Establish one command you have already run that is:

- red-capable: fails specifically on this bug;
- deterministic: same result every run;
- fast: seconds, not minutes;
- unattended: runnable without manual steps.

A failing test is ideal; a repro script or bisection harness also works. Build
the right loop and the bug is most of the way fixed.

## Phase 2 — Reproduce and minimise

Run the loop to confirm the user's exact symptom. Then strip the scenario until
removing any one remaining element makes the loop go green. The minimal repro is
the bug's surface.

## Phase 3 — Hypothesise

Write 3-5 ranked, falsifiable hypotheses, each with an explicit prediction,
before testing any of them. Share them with the user for domain knowledge.

## Phase 4 — Instrument

Probe one hypothesis at a time with debuggers or targeted logs. Change one
variable per run. Tag temporary logs with a unique prefix so they are easy to
remove later.

## Phase 5 — Fix and regression-test

Write the regression test before the fix, at a correct architectural seam rather
than coupled to internals. Apply the fix. Confirm both the new test and the
original feedback loop now pass.

## Phase 6 — Clean up and post-mortem

Remove debug instrumentation. Record the root cause as a compact learning
candidate (`FIX`/`AVOID`). Note what would have caught the bug earlier.

## Loop integration

- Route confirmed fixes back through the normal VERIFY then TEST gates.
- Code changes still go through the required CAVEMAN lane.
- The regression test added here is verification evidence, not a hidden patch.
- Pair with `skills/tdd/SKILL.md` to drive the fix test-first.
