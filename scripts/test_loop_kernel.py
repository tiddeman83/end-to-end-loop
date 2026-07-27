#!/usr/bin/env python3
"""Public-behavior tests for the end-to-end-loop executable kernel."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import loop_kernel  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_state_can_resume_only_through_allowed_transitions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "loop-state.json"
        state = loop_kernel.initialize_state(
            "kernel-test",
            goal="verify deterministic resume",
            acceptance_criteria=[{"criterion": "Resume at the persisted phase"}],
        )
        loop_kernel.write_state(path, state)

        planned = loop_kernel.transition(loop_kernel.read_state(path), "PLAN")
        loop_kernel.write_state(path, planned)
        resumed = loop_kernel.read_state(path)

        assert_true(resumed["phase"] == "PLAN", "persisted state should resume at PLAN")
        assert_true(resumed["transition_count"] == 1, "transition count should be persisted")

        try:
            loop_kernel.transition(resumed, "DEPLOY")
        except ValueError as exc:
            assert_true("not allowed" in str(exc), "invalid transition should fail deterministically")
        else:
            raise AssertionError("invalid PLAN -> DEPLOY transition was accepted")


def test_preflight_routes_only_required_references_and_blocks_missing_code_lane() -> None:
    preflight = loop_kernel.build_preflight(
        code_change=True,
        capabilities=set(),
        network=True,
        deploy=False,
        github_copilot=True,
        risks={"evaluation"},
        root=REPO_ROOT,
    )

    assert_true(preflight["allowed"] is False, "code change without execution lane must be blocked")
    assert_true("references/test-and-security.md" in preflight["references"], "network risk needs safety reference")
    assert_true("references/backlog-and-copilot.md" in preflight["references"], "Copilot work needs its reference")
    assert_true("references/deploy-readiness.md" not in preflight["references"], "non-deploy work should not load deploy reference")
    assert_true("references/evaluation.md" in preflight["references"], "evaluation risk needs its focused reference")
    assert_true(preflight["selected_context_bytes"] > 0, "preflight should measure selected context")


def test_budget_exhaustion_blocks_more_work() -> None:
    state = loop_kernel.initialize_state("budget-test", mode="lean")
    exhausted = loop_kernel.record_usage(
        state,
        tool_calls=state["budgets"]["max_tool_calls"],
    )
    assert_true(exhausted["status"] == "blocked", "budget boundary must block the run")
    assert_true(
        exhausted["termination_reason"] == "budget_exhausted:max_tool_calls",
        "budget termination reason should name the exhausted budget",
    )
    try:
        loop_kernel.transition(exhausted, "PLAN")
    except ValueError as exc:
        assert_true("status blocked" in str(exc), "blocked run must reject further transitions")
    else:
        raise AssertionError("blocked run accepted another transition")


def test_retry_ceiling_is_bounded() -> None:
    state = loop_kernel.initialize_state("retry-test", mode="lean")
    retrying = loop_kernel.record_retry(state, "same-failure")
    assert_true(retrying["status"] == "active", "one configured retry should remain allowed")
    stopped = loop_kernel.record_retry(retrying, "same-failure")
    assert_true(stopped["status"] == "blocked", "lean retry ceiling must stop repeated failure")
    assert_true(stopped["termination_reason"] == "retry_ceiling", "retry stop reason missing")


def test_acceptance_evidence_can_close_the_loop() -> None:
    state = loop_kernel.initialize_state(
        "criteria-test",
        acceptance_criteria=[{"id": "tests", "criterion": "Automated tests pass"}],
    )
    updated = loop_kernel.record_criterion(state, "tests", "pass", "tests: 12 passed")
    assert_true(
        loop_kernel.evaluate_termination(updated) == "acceptance_criteria_passed",
        "passing all criteria should produce a deterministic stop signal",
    )
    try:
        loop_kernel.transition(updated, "PLAN")
    except ValueError as exc:
        assert_true("acceptance_criteria_passed" in str(exc), "passed run should only move to REPORT")
    else:
        raise AssertionError("passed acceptance criteria allowed more implementation work")
    reported = loop_kernel.transition(updated, "REPORT")
    assert_true(reported["status"] == "complete", "passed run should be able to close through REPORT")


def test_state_json_is_machine_readable() -> None:
    state = loop_kernel.initialize_state("json-test")
    encoded = json.dumps(state)
    assert_true(json.loads(encoded)["schema_version"] == loop_kernel.SCHEMA_VERSION, "schema version missing")


def main() -> int:
    test_state_can_resume_only_through_allowed_transitions()
    test_preflight_routes_only_required_references_and_blocks_missing_code_lane()
    test_budget_exhaustion_blocks_more_work()
    test_retry_ceiling_is_bounded()
    test_acceptance_evidence_can_close_the_loop()
    test_state_json_is_machine_readable()
    print("loop kernel tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
