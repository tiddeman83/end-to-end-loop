#!/usr/bin/env python3
"""Local-first telemetry recorder for end-to-end-loop.

The recorder is intentionally stdlib-only and privacy conservative:
- opt-in CLI invocation only;
- writes local JSONL only;
- stores command class, duration, exit code, and optional hashes supplied by caller;
- never stores raw command text, stdout, stderr, env vars, cwd, host, user, or paths.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import secrets
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:  # Unix-only but harmlessly optional.
    import resource
except ImportError:  # pragma: no cover - Windows fallback
    resource = None  # type: ignore[assignment]

SCHEMA_VERSION = "telemetry-event-v0"
DEFAULT_PATH = Path(".end-to-end-loop/telemetry.local.jsonl")
PHASES = {"DISCOVER", "BACKLOG", "PLAN", "EXECUTE", "VERIFY", "ITERATE", "TEST", "DELIVER", "DEPLOY", "REPORT"}
STATUSES = {"pass", "fail", "blocked", "skipped"}
OUTCOMES = {"passed", "failed", "blocked", "partial"}
CMD_CLASSES = {
    "validator",
    "json-validation",
    "git",
    "test",
    "lint",
    "build",
    "smoke",
    "security-review",
    "ci-check",
    "copilot-check",
    "other",
}
FORBIDDEN_EVENT_KEYS = {"prompt", "stdout", "stderr", "env", "hostname", "username", "home_path", "cwd", "command", "args"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{secrets.token_hex(3)}"


def append_event(path: Path, event: dict[str, Any]) -> None:
    forbidden = FORBIDDEN_EVENT_KEYS & set(event)
    if forbidden:
        raise ValueError(f"refusing to write forbidden telemetry keys: {sorted(forbidden)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")


def base_event(kind: str, run_id: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "event": kind,
        "run_id": run_id,
        "timestamp": utc_now(),
    }


def record_run_start(args: argparse.Namespace) -> int:
    event = base_event("run_start", args.run_id)
    event.update(
        {
            "tool": args.tool,
            "os": platform.system().lower() or "unknown",
            "arch": platform.machine() or "unknown",
            "mode": args.mode,
            "options": args.option,
            "telemetry_mode": args.telemetry_mode,
        }
    )
    if args.skill_commit:
        event["skill_commit"] = args.skill_commit
    if args.python_version:
        event["python_version"] = platform.python_version()
    append_event(args.telemetry_path, event)
    return 0


def record_phase_end(args: argparse.Namespace) -> int:
    if args.phase not in PHASES:
        raise ValueError(f"invalid phase: {args.phase}")
    if args.status not in STATUSES:
        raise ValueError(f"invalid status: {args.status}")
    event = base_event("phase_end", args.run_id)
    event.update({"phase": args.phase, "duration_ms": args.duration_ms, "status": args.status})
    append_event(args.telemetry_path, event)
    return 0


def record_run_end(args: argparse.Namespace) -> int:
    if args.outcome not in OUTCOMES:
        raise ValueError(f"invalid outcome: {args.outcome}")
    event = base_event("run_end", args.run_id)
    event.update({"duration_ms": args.duration_ms, "outcome": args.outcome})
    if args.delivery_classification:
        event["delivery_classification"] = args.delivery_classification
    if args.blocked_reason:
        event["blocked_reason"] = args.blocked_reason[:160]
    append_event(args.telemetry_path, event)
    return 0


def resource_event(run_id: str) -> dict[str, Any] | None:
    if resource is None:
        return None
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    event = base_event("resource_sample", run_id)
    event.update(
        {
            "rss_peak_kb": int(usage.ru_maxrss),
            "user_cpu_s": round(float(usage.ru_utime), 6),
            "system_cpu_s": round(float(usage.ru_stime), 6),
            "source": "stdlib-resource",
        }
    )
    return event


def wrap_command(args: argparse.Namespace) -> int:
    if args.cmd_class not in CMD_CLASSES:
        raise ValueError(f"invalid cmd_class: {args.cmd_class}")
    if not args.command:
        raise ValueError("wrap requires a command after --")
    start = time.monotonic()
    completed = subprocess.run(args.command, check=False)  # noqa: S603 - explicit opt-in wrapper; command text not persisted.
    duration_ms = int((time.monotonic() - start) * 1000)

    event = base_event("command", args.run_id)
    event.update({"cmd_class": args.cmd_class, "duration_ms": duration_ms, "exit_code": int(completed.returncode)})
    if args.retry_index is not None:
        event["retry_index"] = args.retry_index
    append_event(args.telemetry_path, event)

    sample = resource_event(args.run_id)
    if sample is not None:
        append_event(args.telemetry_path, sample)
    return int(completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append privacy-safe local telemetry JSONL events.")
    parser.add_argument("--telemetry-path", type=Path, default=Path(os.environ.get("E2E_LOOP_TELEMETRY_PATH", DEFAULT_PATH)))
    parser.add_argument("--run-id", default=os.environ.get("E2E_LOOP_RUN_ID") or default_run_id())
    sub = parser.add_subparsers(dest="command_name", required=True)

    start = sub.add_parser("run-start", help="Append a run_start event.")
    start.add_argument("--tool", default="hermes")
    start.add_argument("--mode", default="standard")
    start.add_argument("--option", action="append", default=[])
    start.add_argument("--telemetry-mode", choices=["local-jsonl", "aggregate-only", "off"], default="local-jsonl")
    start.add_argument("--skill-commit")
    start.add_argument("--python-version", action="store_true")
    start.set_defaults(func=record_run_start)

    phase = sub.add_parser("phase-end", help="Append a phase_end event.")
    phase.add_argument("--phase", required=True, choices=sorted(PHASES))
    phase.add_argument("--duration-ms", required=True, type=int)
    phase.add_argument("--status", required=True, choices=sorted(STATUSES))
    phase.set_defaults(func=record_phase_end)

    end = sub.add_parser("run-end", help="Append a run_end event.")
    end.add_argument("--duration-ms", required=True, type=int)
    end.add_argument("--outcome", required=True, choices=sorted(OUTCOMES))
    end.add_argument("--delivery-classification", choices=["none", "repo-only", "prep-only", "live-deploy"])
    end.add_argument("--blocked-reason")
    end.set_defaults(func=record_run_end)

    wrap = sub.add_parser("wrap", help="Run a command and append command/resource telemetry without raw output capture.")
    wrap.add_argument("--cmd-class", required=True, choices=sorted(CMD_CLASSES))
    wrap.add_argument("--retry-index", type=int)
    wrap.add_argument("command", nargs=argparse.REMAINDER)
    wrap.set_defaults(func=wrap_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", None) and args.command[0:1] == ["--"]:
        args.command = args.command[1:]
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
