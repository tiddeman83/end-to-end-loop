# Local Telemetry Research Plan

Date: 2026-06-28
Status: research candidate; implementation can be planned after review
Scope: new feature research for `end-to-end-loop`, focused on measuring performance on local machines without weakening privacy, portability, or CAVEMAN ULTRA discipline.

## CAVEMAN ULTRA packet

- MODE/OPTIONS: `research + backlog + standard`; implementation not started in this artifact.
- GOAL: define a local telemetry approach for measuring skill/run performance across developer machines.
- BACKLOG: telemetry research -> local JSONL recorder -> aggregation/reporting -> optional OpenTelemetry export.
- DEPS: existing eval result logs, privacy rules, validator schema, adapters for target tools, local filesystem write policy.
- INTERFERENCE: overlaps with self-learning memory, eval logs, token/model routing, CI logs, and release claims.
- LEVELS: research `level_1`; telemetry architecture/privacy `level_2`; public metrics claims `level_3` approval gate.
- ROUTES: deterministic Python/stdlib first; optional OpenTelemetry/psutil only as adapters.
- ACCEPTANCE: privacy-safe local metrics format, clear opt-in, cross-platform fallback, aggregation path, release-readiness boundaries.
- VERIFY/TEST: schema validation, fixture JSONL aggregation, no secrets, local smoke on Linux and at least one non-Linux target before public claims.
- NEXT: add feature backlog card; implement only after architecture/privacy slice is accepted.

## Research question

Can `end-to-end-loop` collect enough telemetry on local machines to support credible performance and reviewability claims, without creating privacy risk or requiring heavy infrastructure?

Short answer: yes, if telemetry is local-first, opt-in, sanitized, and separated from memory. OpenTelemetry can be a later export adapter, not the core storage format.

## Useful existing anchors in the repo

- `references/evaluation.md` already asks outcome evals to capture `timing/tokens if available`.
- `evals/result-log-template.json` already provides a machine-readable result-log pattern.
- `references/self-learning.md` and memory rules already distinguish durable learnings from bulky/private logs.
- Recent backlog/model-routing work already requires token/cost budget and CAVEMAN ULTRA compact state packets.

These make telemetry a natural extension rather than a separate product.

## External design anchor

OpenTelemetry is relevant because it is a vendor-neutral observability standard covering traces, metrics, logs, and OTLP exporters. For this skill, it should be treated as optional interoperability:

- core: local JSONL files that are easy to inspect, redact, and validate;
- optional adapter: OTLP/OpenTelemetry export for teams that already run collectors;
- no required network export for normal local users.

## What to measure locally

### Run-level metrics

- `run_id`, timestamp, skill commit/version, tool/agent name, OS/arch/Python version.
- Operating mode/options: `lean`, `standard`, `deep`, `backlog`, `github-copilot`, telemetry enabled.
- Complexity route per workstream: `level_0`..`level_3`, selected tool/model lane.
- Wall-clock duration per phase: DISCOVER, BACKLOG, PLAN, EXECUTE, VERIFY, TEST, REPORT.
- Command count, failed command count, retry count.
- Verification outcomes: acceptance pass/fail/blocked, tests pass/fail/blocked, CI status.
- Delivery classification: none, repo-only, prep-only, live-deploy.

### Machine/resource metrics

Use stdlib-safe metrics first:

- wall time via `time.monotonic()`;
- process/user/system CPU time via `resource.getrusage()` where available;
- peak RSS via `resource.getrusage().ru_maxrss` where available;
- command exit code and duration;
- git diff stats, changed-file count, line count deltas.

Optional/enhanced metrics if available:

- `psutil` for cross-platform CPU/memory/disk stats;
- OS-specific power/thermal metrics only as local adapter experiments;
- model/provider token/cost metrics only when tool exposes them.

### Agent-quality metrics

- evidence completeness score;
- unjustified success claims count;
- CAVEMAN compliance;
- Copilot feedback status and unresolved must-fix count;
- backlog dependency/interference completeness;
- prompt compression ratio when CAVEMAN ULTRA packet is available.

## Privacy and safety model

Telemetry must not become memory.

Rules:

1. Opt-in per repo or run; default can record only local development artifacts, not upload.
2. Local raw file path: `.end-to-end-loop/telemetry.local.jsonl`.
3. This file should usually be gitignored and treated as local-only.
4. Shareable aggregate path: `evals/results/*.json` or `evals/telemetry-summary.json`, containing redacted aggregates only.
5. Never store secrets, full prompts by default, raw stdout/stderr by default, environment variables, file contents, or private paths unless explicitly enabled.
6. Store command names and sanitized arguments carefully; for risky commands store command class plus hash instead of full text.
7. Machine identity should be coarse: OS, arch, CPU/RAM class, not hostname/user/home path.
8. Public claims require Tijmen/release approval and multiple-machine evidence.

## Proposed data model

Local JSONL event examples:

```json
{"event":"run_start","run_id":"2026-06-28T14-00Z-abc","skill_commit":"c5a30b5","tool":"hermes","os":"linux","arch":"x86_64","mode":"standard","options":["backlog"]}
{"event":"phase_end","run_id":"...","phase":"VERIFY","duration_ms":1532,"status":"pass"}
{"event":"command","run_id":"...","cmd_class":"validator","duration_ms":421,"exit_code":0,"stdout_sha256":"..."}
{"event":"resource_sample","run_id":"...","rss_peak_kb":123456,"user_cpu_s":1.2,"system_cpu_s":0.3}
{"event":"run_end","run_id":"...","duration_ms":38210,"outcome":"partial","blocked_reason":"Copilot unavailable"}
```

Aggregated public/shareable summary:

```json
{
  "schema_version": "telemetry-summary-v0",
  "skill_commit": "<commit>",
  "runs": 12,
  "machines": {"linux_x86_64": 8, "macos_arm64": 4},
  "median_duration_ms": 42000,
  "p90_duration_ms": 110000,
  "validation_pass_rate": 0.92,
  "caveman_compliance_rate": 1.0,
  "copilot_available_rate": 0.35,
  "notes": ["local raw logs not included", "small sample; not a reliability claim"]
}
```

## Implementation slices

### Slice 1 — telemetry spec and schema (`level_1`)

Deliverables:

- `references/local-telemetry.md` with schema, privacy rules, and examples.
- Validator additions for telemetry summaries/fixtures.
- Trigger/eval coverage for telemetry research and local-machine measurement.

Acceptance:

- docs explain opt-in/local-only behavior;
- schema validates fixture JSON;
- no implementation hooks yet.

### Slice 2 — local recorder script (`level_1` with privacy review `level_2`)

Deliverables:

- `scripts/telemetry_record.py` or equivalent stdlib helper;
- local JSONL append API;
- command wrapper for timing and exit status;
- no default network export.

Acceptance:

- can record a validation command locally;
- redaction tests pass;
- raw local file is gitignored or clearly local-only;
- validator confirms no generated telemetry is committed accidentally.

### Slice 3 — aggregation and release evidence (`level_2`)

Deliverables:

- aggregation script from JSONL -> shareable summary;
- release-readiness metric section;
- example telemetry summary from local fixture, not a broad claim.

Acceptance:

- fixture aggregation works deterministically;
- public report uses scoped language;
- release gate blocks overclaims from small samples.

### Slice 4 — optional OpenTelemetry adapter (`level_2`, maybe later)

Deliverables:

- optional adapter docs or script for OTLP export;
- disabled by default;
- requires explicit endpoint configuration.

Acceptance:

- local JSONL remains canonical;
- no network writes without explicit opt-in;
- exporter failure does not break local run recording.

## Go / no-go

Go for implementation planning because:

- existing eval/result-log machinery already needs timing/token capture;
- local telemetry supports the release evidence package without overclaiming;
- JSONL + aggregation can be implemented with Python stdlib and low risk;
- OpenTelemetry can be postponed as adapter, avoiding scope explosion.

No-go boundaries:

- do not add always-on background monitoring;
- do not collect full prompts/transcripts/secrets by default;
- do not claim performance improvements until multi-run/multi-machine evidence exists;
- do not require OpenTelemetry infrastructure for normal use.

## Recommended next action

Add a planned feature card to the release sprint:

1. `telemetry-spec` first;
2. `local-recorder` second;
3. `aggregation-summary` third;
4. `otel-adapter` as optional post-alpha or experimental adapter.
