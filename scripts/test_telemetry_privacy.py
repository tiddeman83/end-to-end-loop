#!/usr/bin/env python3
"""Privacy and aggregation smoke tests for local telemetry helpers.

This is intentionally stdlib-only and local-only. It verifies the feature's core
promise: raw/private fields are rejected and shareable output stays aggregate.
"""

from __future__ import annotations

import json
import sys
import tempfile
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import telemetry_aggregate  # noqa: E402
import telemetry_record  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_fixture_aggregation() -> None:
    fixture = REPO_ROOT / "evals/telemetry-events.fixture.jsonl"
    events = telemetry_aggregate.load_events(fixture)
    summary = telemetry_aggregate.aggregate(events, source="fixture", claim_scope="fixture-only")

    assert_true(summary["schema_version"] == "telemetry-summary-v0", "summary schema mismatch")
    assert_true(summary["runs"] == 1, "fixture should summarize one run")
    assert_true(summary["validation_pass_rate"] == 1.0, "validator pass rate mismatch")
    assert_true(summary["caveman_compliance_rate"] == 1.0, "CAVEMAN compliance rate mismatch")
    assert_true(summary["copilot_available_rate"] == 0.0, "Copilot blocked fixture should produce 0 availability")
    privacy = summary["privacy_review"]
    assert_true(privacy["raw_logs_included"] is False, "summary must not include raw logs")
    assert_true(privacy["contains_secrets"] is False, "summary must not contain secrets")


def test_aggregator_rejects_forbidden_raw_keys() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        for forbidden_key, forbidden_value in {
            "command": "python3 scripts/validate_skill.py .",
            "args": ["scripts/validate_skill.py", "."],
        }.items():
            bad_event = {
                "schema_version": "telemetry-event-v0",
                "event": "command",
                "run_id": "privacy-test",
                "timestamp": "2026-06-28T00:00:00Z",
                "cmd_class": "validator",
                "duration_ms": 1,
                "exit_code": 0,
                forbidden_key: forbidden_value,
            }
            path = Path(tmp) / f"bad-{forbidden_key}.jsonl"
            path.write_text(json.dumps(bad_event) + "\n", encoding="utf-8")
            try:
                with redirect_stderr(StringIO()):
                    telemetry_aggregate.load_events(path)
            except SystemExit as exc:
                assert_true(exc.code == 1, f"forbidden {forbidden_key} key should fail aggregation")
            else:  # pragma: no cover - failure path
                raise AssertionError(f"aggregator accepted forbidden {forbidden_key} key")


def test_recorder_rejects_forbidden_event_keys() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "events.jsonl"
        try:
            telemetry_record.append_event(
                path,
                {
                    "schema_version": "telemetry-event-v0",
                    "event": "command",
                    "run_id": "privacy-test",
                    "timestamp": "2026-06-28T00:00:00Z",
                    "stdout": "raw output must not be stored",
                },
            )
        except ValueError as exc:
            assert_true("forbidden telemetry keys" in str(exc), "unexpected recorder error")
        else:  # pragma: no cover - failure path
            raise AssertionError("recorder accepted forbidden stdout key")
        assert_true(not path.exists(), "recorder should not create a file for forbidden events")


def main() -> int:
    test_fixture_aggregation()
    test_aggregator_rejects_forbidden_raw_keys()
    test_recorder_rejects_forbidden_event_keys()
    print("telemetry privacy tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
