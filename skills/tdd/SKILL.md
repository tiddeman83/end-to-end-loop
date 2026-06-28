---
name: tdd
description: Build features and fix bugs test-first with red-green-refactor, testing behavior through public interfaces rather than implementation details. Use when adding new behavior or locking in a bug fix with a test.
---

# Test-Driven Development

Use this subskill inside the end-to-end loop when EXECUTE produces new behavior or
a bug fix that should be pinned by a test. It strengthens the VERIFY and TEST
gates by making tests the driver, not an afterthought.

## Core Principle

Tests verify behavior through public interfaces, not implementation details. Good
tests read like specifications and survive internal refactors unchanged. If a
behavior-preserving refactor breaks a test, that test was coupled to internals.

## Red-Green-Refactor

1. RED: write one test that fails, capturing a single behavioral requirement.
2. GREEN: write the minimal code that makes that test pass, nothing more.
3. REFACTOR: only with all tests green, remove duplication, deepen modules, and
   apply design principles. Never refactor while a test is red.

## Vertical slices, not horizontal

Do not write all tests up front and then implement everything. That tests
imagined behavior and overcommits to untested structure. Work one slice at a time
(one test, one implementation, repeat), letting each cycle inform the next. This
mirrors the BACKLOG slicing rule.

## Rules

- Test one behavior at a time.
- Write only enough code to pass the current test.
- Do not anticipate future requirements.
- Confirm with the user which behaviors matter most before starting.
- Code changes still go through the required CAVEMAN lane.

## Loop integration

- A failing-then-passing test is verification evidence for VERIFY.
- The resulting suite feeds the TEST gate as automated and regression coverage.
- Pair with `skills/diagnosing-bugs/SKILL.md` when the behavior to lock in is a bug.
