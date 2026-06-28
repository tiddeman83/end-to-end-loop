#!/usr/bin/env python3
"""Aggregate local end-to-end-loop telemetry JSONL into a shareable summary.

Privacy model:
- reads local JSONL event files only when explicitly invoked;
- writes aggregate JSON only;
- refuses forbidden raw/private keys such as prompts, stdout/stderr, env, cwd,
  hostnames, usernames, home paths, raw commands, or raw args;
- never performs network writes.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUMMARY_SCHEMA = "telemetry-summary-v0"
EVENT_SCHEMA = "telemetry-event-v0"
FORBIDDEN_EVENT_KEYS = {"prompt", "stdout", "stderr", "env", "hostname", "username", "home_path", "cwd", "command", "args"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parsed: Any
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL line {idx}: {exc}")
        if not isinstance(parsed, dict):
            fail(f"line {idx} must be a JSON object")
        forbidden = FORBIDDEN_EVENT_KEYS & set(parsed)
        if forbidden:
            fail(f"line {idx} contains forbidden raw/private keys: {sorted(forbidden)}")
        if parsed.get("schema_version") != EVENT_SCHEMA:
            fail(f"line {idx} has unsupported schema_version")
        events.append(parsed)
    if not events:
        fail("telemetry input contains no events")
    return events


def rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)


def median(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return int(round((ordered[mid - 1] + ordered[mid]) / 2))


def percentile(values: list[int], pct: float) -> int | None:
    if len(values) < 2:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((pct / 100) * len(ordered)) - 1))
    return ordered[index]


def aggregate(events: list[dict[str, Any]], *, source: str, claim_scope: str) -> dict[str, Any]:
    run_ids: set[str] = {str(event.get("run_id")) for event in events if event.get("run_id")}
    starts = [event for event in events if event.get("event") == "run_start"]
    ends = [event for event in events if event.get("event") == "run_end"]
    commands = [event for event in events if event.get("event") == "command"]
    gates = [event for event in events if event.get("event") == "quality_gate"]

    machines: Counter[str] = Counter()
    for event in starts:
        os_name = str(event.get("os") or "unknown").lower()
        arch = str(event.get("arch") or "unknown").lower()
        machines[f"{os_name}_{arch}"] += 1
    if not machines:
        machines["unknown_unknown"] = len(run_ids) or 1

    durations = [int(event["duration_ms"]) for event in ends if isinstance(event.get("duration_ms"), int)]

    validator_commands = [event for event in commands if event.get("cmd_class") == "validator"]
    validator_passes = sum(1 for event in validator_commands if event.get("exit_code") == 0)

    gate_statuses: dict[str, list[str]] = defaultdict(list)
    for event in gates:
        gate = event.get("gate")
        status = event.get("status")
        if isinstance(gate, str) and isinstance(status, str):
            gate_statuses[gate].append(status)

    caveman_statuses = gate_statuses.get("caveman-compliance", [])
    caveman_passes = sum(1 for status in caveman_statuses if status == "pass")

    copilot_statuses = gate_statuses.get("copilot-feedback", [])
    copilot_available = sum(1 for status in copilot_statuses if status == "pass")

    notes = ["raw local telemetry is not included"]
    if source == "fixture":
        notes.append("fixture-only sample")
    if len(run_ids) < 3:
        notes.append("small sample; not a public performance claim")

    return {
        "schema_version": SUMMARY_SCHEMA,
        "generated_at": utc_now(),
        "source": source,
        "runs": len(run_ids) or 1,
        "machines": dict(sorted(machines.items())),
        "median_duration_ms": median(durations),
        "p90_duration_ms": percentile(durations, 90),
        "validation_pass_rate": rate(validator_passes, len(validator_commands)),
        "caveman_compliance_rate": rate(caveman_passes, len(caveman_statuses)),
        "copilot_available_rate": rate(copilot_available, len(copilot_statuses)),
        "privacy_review": {
            "raw_logs_included": False,
            "contains_secrets": False,
            "notes": notes,
        },
        "claim_scope": claim_scope,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Aggregate local telemetry JSONL into privacy-safe summary JSON.")
    parser.add_argument("input", type=Path, help="Local telemetry JSONL file")
    parser.add_argument("--output", type=Path, help="Write summary JSON to this path instead of stdout")
    parser.add_argument("--source", choices=["fixture", "local-aggregate", "ci-aggregate", "release-evidence"], default="local-aggregate")
    parser.add_argument(
        "--claim-scope",
        choices=["fixture-only", "local-only", "internal-release-evidence", "public-claim-approved"],
        default="local-only",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.claim_scope == "public-claim-approved":
        fail("public-claim-approved requires human approval; do not generate it from this helper")
    summary = aggregate(load_events(args.input), source=args.source, claim_scope=args.claim_scope)
    output = json.dumps(summary, indent=2, sort_keys=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
