#!/usr/bin/env python3
"""Validate the end-to-end-loop skill repository without third-party deps."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, cast


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"`?(references/[A-Za-z0-9_.\-/]+|handoff/[A-Za-z0-9_.\-/]+|scripts/[A-Za-z0-9_.\-/]+)`?")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md must start with YAML frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail("SKILL.md frontmatter must end with ---")

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            fail(f"Unsupported frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, "\n".join(lines[end + 1 :])


def check_frontmatter(root: Path, text: str) -> None:
    data, body = parse_frontmatter(text)
    allowed = {"name", "description"}
    extras = set(data) - allowed
    if extras:
        fail(f"Only name and description are allowed in SKILL.md frontmatter: {sorted(extras)}")
    name = data.get("name", "")
    description = data.get("description", "")
    if not NAME_RE.fullmatch(name):
        fail(f"Invalid skill name: {name!r}")
    if name != root.name:
        fail(f"Skill name {name!r} must match folder name {root.name!r}")
    if not description:
        fail("description is required")
    if len(description) > 1024:
        fail(f"description is too long: {len(description)} > 1024")
    if len(body.splitlines()) > 500:
        fail("SKILL.md body should stay under 500 lines")


def check_required_files(root: Path) -> None:
    required = [
        "SKILL.md",
        "references/phase-checklists.md",
        "references/test-and-security.md",
        "references/adapters.md",
        "references/evaluation.md",
        "references/self-learning.md",
        "references/report-template.md",
        "references/local-telemetry.md",
        "evals/telemetry-events.fixture.jsonl",
        "evals/telemetry-summary.example.json",
        "scripts/telemetry_record.py",
        "scripts/validate_skill.py",
        "handoff/hermes-devboss-brief.md",
        "handoff/hermes-market-research-prompt.md",
        "AGENTS.md",
        ".hermes.md",
        ".github/workflows/validate.yml",
    ]
    for rel in required:
        if not (root / rel).is_file():
            fail(f"Missing required file: {rel}")


def check_references(root: Path, text: str) -> None:
    missing: list[str] = []
    for match in REF_RE.findall(text):
        if not (root / match).exists():
            missing.append(match)
    if missing:
        fail(f"Referenced files missing: {sorted(set(missing))}")


def check_policy_terms(root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    safety = (root / "references/test-and-security.md").read_text(encoding="utf-8")
    phase = (root / "references/phase-checklists.md").read_text(encoding="utf-8")
    adapters = (root / "references/adapters.md").read_text(encoding="utf-8")
    self_learning = (root / "references/self-learning.md").read_text(encoding="utf-8")
    local_telemetry = (root / "references/local-telemetry.md").read_text(encoding="utf-8")
    combined = "\n".join([skill, safety, phase, adapters, self_learning, local_telemetry])
    required_terms = [
        "CAVEMAN",
        "live deploy",
        "explicit",
        "CI",
        "rollback",
        "Hermes",
        "AGENTS.md",
        "self-learning",
        "memory",
        "privacy",
        "result log",
        "backlog",
        "Copilot",
        "model routing",
        "telemetry",
        "local-first",
    ]
    for term in required_terms:
        if term not in combined:
            fail(f"Required policy term missing: {term}")


def check_json_files(root: Path) -> None:
    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {path.relative_to(root)}: {exc}")


def check_trigger_cases(root: Path) -> None:
    path = root / "evals/trigger-cases.json"
    if not path.is_file():
        fail("Missing trigger evals: evals/trigger-cases.json")

    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in evals/trigger-cases.json: {exc}")

    if not isinstance(cases, list):
        fail("evals/trigger-cases.json must contain a JSON array")
    if len(cases) < 20:
        fail(f"At least 20 trigger cases are required; found {len(cases)}")

    positives = 0
    negatives = 0
    near_miss_negatives = 0
    deploy_cases = 0
    caveman_cases = 0
    backlog_cases = 0
    copilot_cases = 0
    telemetry_cases = 0

    for idx, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"Trigger case {idx} must be an object")

        query = case.get("query")
        should_trigger = case.get("should_trigger")
        reason = case.get("reason")

        if not isinstance(query, str) or not query.strip():
            fail(f"Trigger case {idx} must include a non-empty query")
        if not isinstance(should_trigger, bool):
            fail(f"Trigger case {idx} must include boolean should_trigger")
        if not isinstance(reason, str) or not reason.strip():
            fail(f"Trigger case {idx} must include a non-empty reason")

        text = f"{query} {reason}".lower()
        if should_trigger:
            positives += 1
        else:
            negatives += 1
            near_miss_terms = (
                "explain",
                "brainstorm",
                "summarize",
                "plan",
                "report",
                "no code",
            )
            if any(term in text for term in near_miss_terms):
                near_miss_negatives += 1
        if "deploy" in text:
            deploy_cases += 1
        if "caveman" in text:
            caveman_cases += 1
        if "backlog" in text:
            backlog_cases += 1
        if "copilot" in text:
            copilot_cases += 1
        if "telemetry" in text or "measurement" in text or "performance" in text:
            telemetry_cases += 1

    if positives < 8:
        fail(f"Trigger evals need at least 8 should-trigger positives; found {positives}")
    if negatives < 8:
        fail(f"Trigger evals need at least 8 should-not-trigger negatives; found {negatives}")
    if near_miss_negatives < 5:
        fail(f"Trigger evals need at least 5 near-miss negatives; found {near_miss_negatives}")
    if deploy_cases < 3:
        fail(f"Trigger evals need at least 3 deploy-policy cases; found {deploy_cases}")
    if caveman_cases < 2:
        fail(f"Trigger evals need at least 2 CAVEMAN cases; found {caveman_cases}")
    if backlog_cases < 2:
        fail(f"Trigger evals need at least 2 backlog-option cases; found {backlog_cases}")
    if copilot_cases < 2:
        fail(f"Trigger evals need at least 2 Copilot-option cases; found {copilot_cases}")
    if telemetry_cases < 2:
        fail(f"Trigger evals need at least 2 telemetry/measurement cases; found {telemetry_cases}")


def check_outcome_scenarios(root: Path) -> None:
    path = root / "evals/outcome-scenarios.md"
    if not path.is_file():
        fail("Missing outcome scenarios: evals/outcome-scenarios.md")

    text = path.read_text(encoding="utf-8")
    scenario_count = len(re.findall(r"^## Scenario \d+:", text, flags=re.MULTILINE))
    if scenario_count < 8:
        fail(f"At least 8 outcome scenarios are required; found {scenario_count}")

    required_terms = {
        "CAVEMAN": "CAVEMAN compliance coverage",
        "live-deploy": "live-deploy policy coverage",
        "repo-only": "repo-only delivery coverage",
        "prep-only": "prep-only delivery coverage",
        "dev-boss.nl": "DevBoss/Firebase site coverage",
        "git diff --check": "diff hygiene verification coverage",
        "JSON validation": "structured-data validation coverage",
    }
    for term, label in required_terms.items():
        if term not in text:
            fail(f"Outcome scenarios missing {label}: {term}")


def check_eval_result_template(root: Path) -> None:
    path = root / "evals/result-log-template.json"
    if not path.is_file():
        fail("Missing eval result template: evals/result-log-template.json")

    try:
        template = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in evals/result-log-template.json: {exc}")

    if not isinstance(template, dict):
        fail("evals/result-log-template.json must contain a JSON object")

    required_keys = {
        "date",
        "agent_or_tool",
        "skill_version_or_commit",
        "scenario_id",
        "prompt",
        "expected_trigger",
        "actual_trigger",
        "outcome",
        "commands_or_evidence",
        "acceptance_criteria",
        "caveman_behavior",
        "deploy_policy_behavior",
        "security_review",
        "delivery_classification",
        "ci_status",
        "memory_read",
        "memory_update",
        "learning_candidates",
        "privacy_review",
        "copilot_findings",
        "notes",
    }
    missing = sorted(required_keys - set(template))
    if missing:
        fail(f"Eval result template missing required keys: {missing}")

    if not isinstance(template.get("commands_or_evidence"), list) or not template["commands_or_evidence"]:
        fail("Eval result template needs a non-empty commands_or_evidence list")
    criteria = template.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria:
        fail("Eval result template needs a non-empty acceptance_criteria list")
    first_criterion = criteria[0]
    if not isinstance(first_criterion, dict):
        fail("Eval result template acceptance_criteria entries must be objects")
    for key in ("criterion", "status", "evidence"):
        if key not in first_criterion:
            fail(f"Eval result template acceptance_criteria entry missing key: {key}")


EVAL_RESULT_REQUIRED_KEYS = {
    "date",
    "agent_or_tool",
    "skill_version_or_commit",
    "scenario_id",
    "prompt",
    "expected_trigger",
    "actual_trigger",
    "outcome",
    "commands_or_evidence",
    "acceptance_criteria",
    "caveman_behavior",
    "deploy_policy_behavior",
    "security_review",
    "delivery_classification",
    "ci_status",
    "memory_read",
    "memory_update",
    "learning_candidates",
    "privacy_review",
    "copilot_findings",
    "notes",
}

EVAL_RESULT_ENUMS = {
    "agent_or_tool": {"codex", "hermes", "claude-code", "cursor", "agents-md", "copilot", "other"},
    "expected_trigger": {True, False, "planning_only"},
    "actual_trigger": {True, False, "planning_only"},
    "outcome": {"passed", "failed", "blocked", "partial"},
    "caveman_behavior": {"compliant", "blocked", "exception_approved", "not_applicable"},
    "deploy_policy_behavior": {"compliant", "violation", "not_applicable"},
    "security_review": {"pass", "fail", "blocked", "not_applicable"},
    "delivery_classification": {"none", "repo-only", "prep-only", "live-deploy"},
    "ci_status": {"green", "red", "missing", "not_checked", "not_applicable"},
    "memory_read": {"yes", "no", "not_present", "not_applicable"},
    "memory_update": {"updated", "none", "local_only", "blocked", "not_applicable"},
}


def check_eval_result_logs(root: Path) -> None:
    results_dir = root / "evals/results"
    if not results_dir.is_dir():
        fail("Missing eval result logs directory: evals/results")

    logs = sorted(results_dir.glob("*.json"))
    if not logs:
        fail("At least one eval result log is required in evals/results/*.json")

    allowed_statuses = {"pass", "fail", "blocked"}
    placeholder_markers = ("<", "YYYY", "|", "prompt here")

    for path in logs:
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {path.relative_to(root)}: {exc}")
        if not isinstance(result, dict):
            fail(f"{path.relative_to(root)} must contain a JSON object")

        missing = sorted(EVAL_RESULT_REQUIRED_KEYS - set(result))
        if missing:
            fail(f"{path.relative_to(root)} missing required keys: {missing}")

        for key in ("date", "agent_or_tool", "scenario_id", "prompt", "outcome", "notes"):
            value = result.get(key)
            if not isinstance(value, str) or not value.strip():
                fail(f"{path.relative_to(root)} field {key!r} must be a non-empty string")
            if any(marker in value for marker in placeholder_markers):
                fail(f"{path.relative_to(root)} field {key!r} still looks like a placeholder")

        date = result.get("date")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            fail(f"{path.relative_to(root)} field 'date' must use YYYY-MM-DD")

        scenario_id = result.get("scenario_id")
        if not re.fullmatch(r"scenario-\d+", scenario_id):
            fail(f"{path.relative_to(root)} field 'scenario_id' must look like scenario-N")

        for key, allowed in EVAL_RESULT_ENUMS.items():
            value = result.get(key)
            if value not in allowed:
                fail(
                    f"{path.relative_to(root)} field {key!r} has invalid value "
                    f"{value!r}; expected one of {sorted(map(str, allowed))}"
                )

        evidence = result.get("commands_or_evidence")
        if not isinstance(evidence, list) or not evidence:
            fail(f"{path.relative_to(root)} needs non-empty commands_or_evidence")
        if not all(isinstance(item, str) and item.strip() for item in evidence):
            fail(f"{path.relative_to(root)} commands_or_evidence entries must be non-empty strings")

        criteria = result.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria:
            fail(f"{path.relative_to(root)} needs non-empty acceptance_criteria")
        for idx, criterion in enumerate(criteria, start=1):
            if not isinstance(criterion, dict):
                fail(f"{path.relative_to(root)} acceptance criterion {idx} must be an object")
            for key in ("criterion", "status", "evidence"):
                if key not in criterion:
                    fail(f"{path.relative_to(root)} acceptance criterion {idx} missing {key!r}")
            if criterion["status"] not in allowed_statuses:
                fail(
                    f"{path.relative_to(root)} acceptance criterion {idx} has invalid status "
                    f"{criterion['status']!r}"
                )

        learning_types = {"FACT", "CMD", "BLOCK", "PREF", "RISK", "FIX", "AVOID", "NEXT"}
        candidates = result.get("learning_candidates")
        if not isinstance(candidates, list):
            fail(f"{path.relative_to(root)} learning_candidates must be a list")
        for idx, item in enumerate(candidates, start=1):
            if not isinstance(item, dict):
                fail(f"{path.relative_to(root)} learning candidate {idx} must be an object")
            if item.get("type") not in learning_types:
                fail(f"{path.relative_to(root)} learning candidate {idx} has invalid type")
            text = item.get("text")
            if not isinstance(text, str) or not text.strip() or len(text) > 220:
                fail(f"{path.relative_to(root)} learning candidate {idx} needs compact text <= 220 chars")
            if not isinstance(item.get("promote"), bool):
                fail(f"{path.relative_to(root)} learning candidate {idx} promote must be boolean")

        privacy = result.get("privacy_review")
        if not isinstance(privacy, dict):
            fail(f"{path.relative_to(root)} privacy_review must be an object")
        for key in ("contains_secrets", "commit_safe", "redactions"):
            if key not in privacy:
                fail(f"{path.relative_to(root)} privacy_review missing {key!r}")
        if not isinstance(privacy["contains_secrets"], bool) or not isinstance(privacy["commit_safe"], bool):
            fail(f"{path.relative_to(root)} privacy_review booleans must be true/false")
        if not isinstance(privacy["redactions"], list):
            fail(f"{path.relative_to(root)} privacy_review.redactions must be a list")

        copilot = result.get("copilot_findings")
        if not isinstance(copilot, dict) or "available" not in copilot or "summary" not in copilot or "items" not in copilot:
            fail(f"{path.relative_to(root)} copilot_findings must include available, summary, and items")
        if not isinstance(copilot["available"], bool) or not isinstance(copilot["items"], list):
            fail(f"{path.relative_to(root)} copilot_findings has invalid types")


def check_telemetry_artifacts(root: Path) -> None:
    reference = root / "references/local-telemetry.md"
    fixture = root / "evals/telemetry-events.fixture.jsonl"
    summary_path = root / "evals/telemetry-summary.example.json"
    recorder = root / "scripts/telemetry_record.py"
    gitignore = root / ".gitignore"

    text = reference.read_text(encoding="utf-8")
    required_terms = [
        "opt-in",
        "local-first",
        "telemetry.local.jsonl",
        "no default network writes",
        "OpenTelemetry/OTLP export is an optional adapter",
        "Never store full prompts",
        "raw stdout/stderr",
        "privacy_review",
        "telemetry-summary-v0",
        "telemetry-event-v0",
    ]
    for term in required_terms:
        if term not in text:
            fail(f"Telemetry reference missing required privacy/schema term: {term}")

    recorder_text = recorder.read_text(encoding="utf-8")
    required_recorder_terms = [
        "DEFAULT_PATH = Path(\".end-to-end-loop/telemetry.local.jsonl\")",
        "subprocess.run",
        "cmd_class",
        "duration_ms",
        "exit_code",
        "FORBIDDEN_EVENT_KEYS",
        "raw command text",
    ]
    for term in required_recorder_terms:
        if term not in recorder_text:
            fail(f"Telemetry recorder missing required privacy/recording term: {term}")

    if ".end-to-end-loop/telemetry.local.jsonl" not in gitignore.read_text(encoding="utf-8"):
        fail(".gitignore must exclude .end-to-end-loop/telemetry.local.jsonl")

    event_allowed = {"run_start", "phase_end", "command", "resource_sample", "quality_gate", "run_end"}
    phase_allowed = {"DISCOVER", "BACKLOG", "PLAN", "EXECUTE", "VERIFY", "ITERATE", "TEST", "DELIVER", "DEPLOY", "REPORT"}
    status_allowed = {"pass", "fail", "blocked", "skipped"}
    outcome_allowed = {"passed", "failed", "blocked", "partial"}
    cmd_allowed = {
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

    lines = [line for line in fixture.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 3:
        fail("Telemetry JSONL fixture must include at least 3 events")
    seen_events: set[str] = set()
    for idx, line in enumerate(lines, start=1):
        parsed_event: Any = None
        try:
            parsed_event = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSONL telemetry fixture line {idx}: {exc}")
        event: dict[str, Any] = cast(dict[str, Any], parsed_event) if isinstance(parsed_event, dict) else {}
        if not event:
            fail(f"Telemetry fixture line {idx} must be a JSON object")
        for key in ("schema_version", "event", "run_id", "timestamp"):
            if not isinstance(event.get(key), str) or not event[key].strip():
                fail(f"Telemetry fixture line {idx} missing non-empty {key!r}")
        if event["schema_version"] != "telemetry-event-v0":
            fail(f"Telemetry fixture line {idx} has wrong schema_version")
        if event["event"] not in event_allowed:
            fail(f"Telemetry fixture line {idx} has invalid event {event['event']!r}")
        seen_events.add(event["event"])
        if event["event"] == "phase_end":
            if event.get("phase") not in phase_allowed or event.get("status") not in status_allowed:
                fail(f"Telemetry phase_end line {idx} has invalid phase/status")
        if event["event"] == "command":
            if event.get("cmd_class") not in cmd_allowed:
                fail(f"Telemetry command line {idx} has invalid cmd_class")
            if not isinstance(event.get("exit_code"), int):
                fail(f"Telemetry command line {idx} needs integer exit_code")
        if event["event"] == "run_end" and event.get("outcome") not in outcome_allowed:
            fail(f"Telemetry run_end line {idx} has invalid outcome")

        forbidden_keys = {"prompt", "stdout", "stderr", "env", "hostname", "username", "home_path", "cwd"}
        present_forbidden = forbidden_keys & set(event)
        if present_forbidden:
            fail(f"Telemetry fixture line {idx} contains forbidden raw/private keys: {sorted(present_forbidden)}")

    for required_event in ("run_start", "command", "run_end"):
        if required_event not in seen_events:
            fail(f"Telemetry fixture missing required event: {required_event}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    required_summary_keys = {
        "schema_version",
        "generated_at",
        "source",
        "runs",
        "machines",
        "median_duration_ms",
        "p90_duration_ms",
        "validation_pass_rate",
        "caveman_compliance_rate",
        "copilot_available_rate",
        "privacy_review",
        "claim_scope",
    }
    missing = sorted(required_summary_keys - set(summary))
    if missing:
        fail(f"Telemetry summary missing required keys: {missing}")
    if summary.get("schema_version") != "telemetry-summary-v0":
        fail("Telemetry summary has wrong schema_version")
    if not isinstance(summary.get("runs"), int) or summary["runs"] < 1:
        fail("Telemetry summary runs must be a positive integer")
    if not isinstance(summary.get("machines"), dict) or not summary["machines"]:
        fail("Telemetry summary machines must be a non-empty object")
    privacy = summary.get("privacy_review")
    if not isinstance(privacy, dict):
        fail("Telemetry summary privacy_review must be an object")
    if privacy.get("raw_logs_included") is not False or privacy.get("contains_secrets") is not False:
        fail("Telemetry summary must exclude raw logs and secrets")
    if summary.get("claim_scope") == "public-claim-approved":
        fail("Telemetry example must not claim public approval")


def check_line_hygiene(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json"} and path.name not in {"SKILL.md", "AGENTS.md", ".hermes.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                fail(f"Trailing whitespace in {path.relative_to(root)}:{idx}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Skill repository root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        fail("SKILL.md not found")
    text = skill_path.read_text(encoding="utf-8")
    check_frontmatter(root, text)
    check_required_files(root)
    check_references(root, text)
    check_policy_terms(root)
    check_json_files(root)
    check_trigger_cases(root)
    check_outcome_scenarios(root)
    check_eval_result_template(root)
    check_eval_result_logs(root)
    check_telemetry_artifacts(root)
    check_line_hygiene(root)
    print("end-to-end-loop skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
