#!/usr/bin/env python3
"""Small, stdlib-only state and preflight kernel for end-to-end-loop runs.

This is deliberately a policy helper, not an agent runtime. It persists the
current phase, rejects impossible resumes, and tells a caller which focused
references are relevant before execution.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "loop-state-v2"
PREFLIGHT_SCHEMA_VERSION = "loop-preflight-v2"
INITIAL_PHASE = "DISCOVER"
TERMINAL_PHASE = "REPORT"
MODES = ("lean", "standard", "deep")
DELIVERY_CLASSIFICATIONS = ("none", "repo-only", "prep-only", "live-deploy")
CRITERION_STATUSES = ("pending", "pass", "fail", "blocked")
DEFAULT_BUDGETS = {
    "lean": {
        "max_iterations": 2,
        "max_retries_per_failure": 1,
        "max_tool_calls": 20,
        "max_elapsed_minutes": 30,
        "max_context_bytes": 65_536,
    },
    "standard": {
        "max_iterations": 4,
        "max_retries_per_failure": 2,
        "max_tool_calls": 60,
        "max_elapsed_minutes": 120,
        "max_context_bytes": 262_144,
    },
    "deep": {
        "max_iterations": 8,
        "max_retries_per_failure": 3,
        "max_tool_calls": 150,
        "max_elapsed_minutes": 480,
        "max_context_bytes": 1_048_576,
    },
}
PHASES = (
    "DISCOVER",
    "BACKLOG",
    "PLAN",
    "EXECUTE",
    "VERIFY",
    "ITERATE",
    "TEST",
    "DELIVER",
    "DEPLOY",
    "REPORT",
)
ALLOWED_TRANSITIONS = {
    "DISCOVER": {"BACKLOG", "PLAN", "REPORT"},
    "BACKLOG": {"PLAN", "REPORT"},
    "PLAN": {"EXECUTE", "REPORT"},
    "EXECUTE": {"VERIFY", "REPORT"},
    "VERIFY": {"ITERATE", "TEST", "REPORT"},
    "ITERATE": {"EXECUTE", "REPORT"},
    "TEST": {"ITERATE", "DELIVER", "REPORT"},
    "DELIVER": {"DEPLOY", "REPORT"},
    "DEPLOY": {"REPORT"},
    "REPORT": set(),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def initialize_state(
    run_id: str,
    *,
    goal: str = "",
    mode: str = "standard",
    delivery_classification: str = "repo-only",
    acceptance_criteria: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    if not run_id or len(run_id) > 120:
        raise ValueError("run_id must contain 1 to 120 characters")
    if mode not in MODES:
        raise ValueError(f"invalid mode: {mode}")
    if delivery_classification not in DELIVERY_CLASSIFICATIONS:
        raise ValueError(f"invalid delivery classification: {delivery_classification}")
    criteria = acceptance_criteria or []
    normalized_criteria = []
    for index, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict) or not criterion.get("criterion"):
            raise ValueError("each acceptance criterion requires non-empty criterion text")
        normalized_criteria.append(
            {
                "id": criterion.get("id") or f"criterion-{index}",
                "criterion": criterion["criterion"],
                "status": criterion.get("status", "pending"),
                "evidence": criterion.get("evidence", ""),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "goal": goal,
        "mode": mode,
        "delivery_classification": delivery_classification,
        "phase": INITIAL_PHASE,
        "status": "active",
        "transition_count": 0,
        "acceptance_criteria": normalized_criteria,
        "budgets": dict(DEFAULT_BUDGETS[mode]),
        "usage": {
            "iterations": 0,
            "tool_calls": 0,
            "elapsed_minutes": 0.0,
            "context_bytes": 0,
        },
        "retry_counts": {},
        "blockers": [],
        "termination_reason": None,
        "updated_at": utc_now(),
    }


def validate_state(state: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "run_id",
        "goal",
        "mode",
        "delivery_classification",
        "phase",
        "status",
        "transition_count",
        "acceptance_criteria",
        "budgets",
        "usage",
        "retry_counts",
        "blockers",
        "termination_reason",
        "updated_at",
    }
    missing = required - set(state)
    if missing:
        raise ValueError(f"state missing required fields: {sorted(missing)}")
    if state["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported state schema: {state['schema_version']}")
    if state["phase"] not in PHASES:
        raise ValueError(f"invalid phase: {state['phase']}")
    if state["mode"] not in MODES:
        raise ValueError(f"invalid mode: {state['mode']}")
    if state["delivery_classification"] not in DELIVERY_CLASSIFICATIONS:
        raise ValueError(f"invalid delivery classification: {state['delivery_classification']}")
    if state["status"] not in {"active", "complete", "blocked"}:
        raise ValueError(f"invalid state status: {state['status']}")
    if not isinstance(state["transition_count"], int) or state["transition_count"] < 0:
        raise ValueError("transition_count must be a non-negative integer")
    if state["phase"] == TERMINAL_PHASE and state["status"] == "active":
        raise ValueError("REPORT state must be complete or blocked")
    if not isinstance(state["acceptance_criteria"], list):
        raise ValueError("acceptance_criteria must be a list")
    for criterion in state["acceptance_criteria"]:
        if not isinstance(criterion, dict):
            raise ValueError("acceptance criteria must be objects")
        if not criterion.get("id") or not criterion.get("criterion"):
            raise ValueError("acceptance criteria require id and criterion")
        if criterion.get("status") not in CRITERION_STATUSES:
            raise ValueError(f"invalid criterion status: {criterion.get('status')}")
    expected_budget_keys = set(DEFAULT_BUDGETS[state["mode"]])
    if set(state["budgets"]) != expected_budget_keys:
        raise ValueError(f"budgets must contain exactly: {sorted(expected_budget_keys)}")
    for key, value in state["budgets"].items():
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"budget {key} must be a positive integer")
    expected_usage_keys = {"iterations", "tool_calls", "elapsed_minutes", "context_bytes"}
    if set(state["usage"]) != expected_usage_keys:
        raise ValueError(f"usage must contain exactly: {sorted(expected_usage_keys)}")
    for key, value in state["usage"].items():
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"usage {key} must be non-negative")
    if not isinstance(state["retry_counts"], dict):
        raise ValueError("retry_counts must be an object")
    if not isinstance(state["blockers"], list):
        raise ValueError("blockers must be a list")
    if state["termination_reason"] is not None and not isinstance(state["termination_reason"], str):
        raise ValueError("termination_reason must be a string or null")


def _budget_reason(state: dict[str, Any]) -> str | None:
    usage_to_budget = {
        "iterations": "max_iterations",
        "tool_calls": "max_tool_calls",
        "elapsed_minutes": "max_elapsed_minutes",
        "context_bytes": "max_context_bytes",
    }
    for usage_key, budget_key in usage_to_budget.items():
        if state["usage"][usage_key] >= state["budgets"][budget_key]:
            return f"budget_exhausted:{budget_key}"
    return None


def evaluate_termination(state: dict[str, Any]) -> str | None:
    validate_state(state)
    if state["status"] == "complete":
        return state["termination_reason"] or "completed"
    if state["blockers"]:
        return state["termination_reason"] or "hard_block"
    budget_reason = _budget_reason(state)
    if budget_reason:
        return budget_reason
    retry_limit = state["budgets"]["max_retries_per_failure"]
    if any(count > retry_limit for count in state["retry_counts"].values()):
        return "retry_ceiling"
    criteria = state["acceptance_criteria"]
    if criteria and all(item["status"] == "pass" for item in criteria):
        return "acceptance_criteria_passed"
    return None


def record_usage(
    state: dict[str, Any],
    *,
    iterations: int = 0,
    tool_calls: int = 0,
    elapsed_minutes: float = 0.0,
    context_bytes: int = 0,
) -> dict[str, Any]:
    validate_state(state)
    increments = {
        "iterations": iterations,
        "tool_calls": tool_calls,
        "elapsed_minutes": elapsed_minutes,
        "context_bytes": context_bytes,
    }
    for key in ("iterations", "tool_calls", "context_bytes"):
        if not isinstance(increments[key], int) or increments[key] < 0:
            raise ValueError(f"{key} increment must be a non-negative integer")
    if not isinstance(elapsed_minutes, (int, float)) or elapsed_minutes < 0:
        raise ValueError("elapsed_minutes increment must be a non-negative number")
    next_state = json.loads(json.dumps(state))
    for key, value in increments.items():
        next_state["usage"][key] += value
    reason = evaluate_termination(next_state)
    if reason and reason.startswith("budget_exhausted:"):
        next_state["status"] = "blocked"
        next_state["termination_reason"] = reason
    next_state["updated_at"] = utc_now()
    validate_state(next_state)
    return next_state


def record_retry(state: dict[str, Any], failure_key: str) -> dict[str, Any]:
    validate_state(state)
    if not failure_key or len(failure_key) > 120:
        raise ValueError("failure_key must contain 1 to 120 characters")
    next_state = json.loads(json.dumps(state))
    next_state["retry_counts"][failure_key] = next_state["retry_counts"].get(failure_key, 0) + 1
    if next_state["retry_counts"][failure_key] > next_state["budgets"]["max_retries_per_failure"]:
        next_state["status"] = "blocked"
        next_state["termination_reason"] = "retry_ceiling"
        next_state["blockers"].append(f"retry ceiling reached: {failure_key}")
    next_state["updated_at"] = utc_now()
    validate_state(next_state)
    return next_state


def record_criterion(
    state: dict[str, Any], criterion_id: str, status: str, evidence: str
) -> dict[str, Any]:
    validate_state(state)
    if status not in CRITERION_STATUSES:
        raise ValueError(f"invalid criterion status: {status}")
    next_state = json.loads(json.dumps(state))
    for criterion in next_state["acceptance_criteria"]:
        if criterion["id"] == criterion_id:
            criterion["status"] = status
            criterion["evidence"] = evidence
            break
    else:
        raise ValueError(f"unknown acceptance criterion: {criterion_id}")
    reason = evaluate_termination(next_state)
    if reason == "acceptance_criteria_passed":
        next_state["termination_reason"] = reason
    next_state["updated_at"] = utc_now()
    validate_state(next_state)
    return next_state


def transition(state: dict[str, Any], target: str, *, blocked: bool = False) -> dict[str, Any]:
    validate_state(state)
    if state["status"] != "active":
        raise ValueError(f"cannot transition state with status {state['status']}")
    termination = evaluate_termination(state)
    if termination and not (termination == "acceptance_criteria_passed" and target == TERMINAL_PHASE):
        raise ValueError(f"cannot transition terminated state: {termination}")
    if target not in PHASES:
        raise ValueError(f"invalid target phase: {target}")
    if target not in ALLOWED_TRANSITIONS[state["phase"]]:
        raise ValueError(f"transition {state['phase']} -> {target} is not allowed")
    next_state = dict(state)
    next_state["phase"] = target
    next_state["transition_count"] += 1
    next_state["updated_at"] = utc_now()
    next_state["status"] = "blocked" if blocked else ("complete" if target == TERMINAL_PHASE else "active")
    if blocked:
        next_state["termination_reason"] = "hard_block"
    elif target == TERMINAL_PHASE:
        next_state["termination_reason"] = next_state["termination_reason"] or "completed"
    validate_state(next_state)
    return next_state


def read_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read loop state: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("loop state must be a JSON object")
    validate_state(data)
    return data


def write_state(path: Path, state: dict[str, Any]) -> None:
    validate_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def build_preflight(
    *,
    code_change: bool,
    capabilities: set[str],
    network: bool,
    deploy: bool,
    github_copilot: bool,
    risks: set[str] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    risks = risks or set()
    references = ["references/phase-checklists.md"]
    blockers: list[str] = []
    if code_change and "caveman-code" not in capabilities:
        blockers.append("code change requires the caveman-code capability or an approved exception")
    if network or code_change or risks & {"auth", "dependencies", "secrets", "untrusted-input"}:
        references.append("references/test-and-security.md")
    if deploy:
        references.append("references/deploy-readiness.md")
    if github_copilot:
        references.append("references/backlog-and-copilot.md")
    if "evaluation" in risks:
        references.append("references/evaluation.md")
    if "memory" in risks:
        references.append("references/self-learning.md")
    references = list(dict.fromkeys(references))
    reference_bytes: dict[str, int] = {}
    if root:
        for reference in references:
            path = root / reference
            if path.is_file():
                reference_bytes[reference] = path.stat().st_size
    return {
        "schema_version": PREFLIGHT_SCHEMA_VERSION,
        "allowed": not blockers,
        "blockers": blockers,
        "references": references,
        "reference_bytes": reference_bytes,
        "selected_context_bytes": sum(reference_bytes.values()),
        "required_capabilities": ["caveman-code"] if code_change else [],
        "risks": sorted(risks),
    }


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Persist and validate end-to-end-loop phase state.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a new DISCOVER state file.")
    init.add_argument("--state", type=Path, default=Path(".end-to-end-loop/loop-state.json"))
    init.add_argument("--run-id", required=True)
    init.add_argument("--goal", default="")
    init.add_argument("--mode", choices=MODES, default="standard")
    init.add_argument("--delivery", choices=DELIVERY_CLASSIFICATIONS, default="repo-only")

    move = sub.add_parser("transition", help="Advance an existing state through an allowed phase transition.")
    move.add_argument("--state", type=Path, default=Path(".end-to-end-loop/loop-state.json"))
    move.add_argument("--to", required=True, choices=PHASES)
    move.add_argument("--blocked", action="store_true")

    preflight = sub.add_parser("preflight", help="Report focused references and required execution capabilities.")
    preflight.add_argument("--code-change", action="store_true")
    preflight.add_argument("--capability", action="append", default=[])
    preflight.add_argument("--network", action="store_true")
    preflight.add_argument("--deploy", action="store_true")
    preflight.add_argument("--github-copilot", action="store_true")
    preflight.add_argument("--risk", action="append", default=[])

    account = sub.add_parser("account", help="Add observed usage and stop when a budget is exhausted.")
    account.add_argument("--state", type=Path, default=Path(".end-to-end-loop/loop-state.json"))
    account.add_argument("--iterations", type=int, default=0)
    account.add_argument("--tool-calls", type=int, default=0)
    account.add_argument("--elapsed-minutes", type=float, default=0.0)
    account.add_argument("--context-bytes", type=int, default=0)

    retry = sub.add_parser("retry", help="Record a retry and enforce the per-failure ceiling.")
    retry.add_argument("--state", type=Path, default=Path(".end-to-end-loop/loop-state.json"))
    retry.add_argument("--failure-key", required=True)

    status = sub.add_parser("status", help="Validate state and report its termination condition.")
    status.add_argument("--state", type=Path, default=Path(".end-to-end-loop/loop-state.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            state = initialize_state(
                args.run_id,
                goal=args.goal,
                mode=args.mode,
                delivery_classification=args.delivery,
            )
            write_state(args.state, state)
            emit(state)
        elif args.command == "transition":
            state = transition(read_state(args.state), args.to, blocked=args.blocked)
            write_state(args.state, state)
            emit(state)
        elif args.command == "preflight":
            root = Path(__file__).resolve().parents[1]
            emit(
                build_preflight(
                    code_change=args.code_change,
                    capabilities=set(args.capability),
                    network=args.network,
                    deploy=args.deploy,
                    github_copilot=args.github_copilot,
                    risks=set(args.risk),
                    root=root,
                )
            )
        elif args.command == "account":
            state = record_usage(
                read_state(args.state),
                iterations=args.iterations,
                tool_calls=args.tool_calls,
                elapsed_minutes=args.elapsed_minutes,
                context_bytes=args.context_bytes,
            )
            write_state(args.state, state)
            emit(state)
        elif args.command == "retry":
            state = record_retry(read_state(args.state), args.failure_key)
            write_state(args.state, state)
            emit(state)
        else:
            state = read_state(args.state)
            emit({"state": state, "termination_reason": evaluate_termination(state)})
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
