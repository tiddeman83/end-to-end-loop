# Local telemetry

Use this reference when a task asks to measure `end-to-end-loop` performance, run quality, phase timing, command timing, CAVEMAN compliance, Copilot status, backlog completeness, model/token/cost usage, or local-machine telemetry.

Telemetry is a research and evidence feature, not memory. Keep raw telemetry local by default. Produce only sanitized aggregates for shared release evidence. The core design is local-first: local JSONL and local aggregation before any optional adapter.

## Feature card

| Field | Value |
|---|---|
| owner | end-to-end-loop maintainer |
| lane | New feature: telemetry research and measurement |
| output | Local-first telemetry schema, fixtures, validation, and future recorder/aggregation plan |
| acceptance | Opt-in/local-only rules documented; fixture and summary validate; raw local logs excluded from commits; no default network writes |
| verification | `python3 scripts/validate_skill.py <root>`, JSON/JSONL parsing, `git diff --check`, security review |
| approval status | Implementation slices allowed only when privacy-safe local spec is clear; public metrics claims remain human-gated |

## CAVEMAN ULTRA state packet fields

When telemetry is enabled or planned, include these compact fields in the run packet:

```text
TELEMETRY: off | local-jsonl | aggregate-only | otlp-adapter
TELEMETRY_PATH: .end-to-end-loop/telemetry.local.jsonl | <local override>
TELEMETRY_PRIVACY: no prompts, secrets, env vars, raw stdout/stderr, private paths, or hostnames by default
TELEMETRY_CLAIMS: local evidence only | release aggregate | blocked pending approval
```

Do not replace the normal packet fields. This only adds telemetry-specific state.

## Privacy contract

1. Telemetry is opt-in per repo or run.
2. Raw telemetry stays local at `.end-to-end-loop/telemetry.local.jsonl` unless the user explicitly chooses another local path.
3. Raw telemetry files must not be committed by default.
4. Shareable artifacts contain aggregates only, for example `evals/telemetry-summary.example.json` or a release-specific `evals/results/*.json` entry.
5. Never store full prompts, transcripts, secrets, tokens, cookies, environment variables, raw stdout/stderr, file contents, private paths, hostnames, usernames, home directories, or credential-helper output by default.
6. Store command data as a `cmd_class` and optional redacted/summarized arguments. For risky commands, store a class plus hash only.
7. Machine identity is coarse: OS family, architecture, and optional resource class. No host or user identity.
8. Public performance or reliability claims need owner/release approval plus multi-run and ideally multi-machine evidence.
9. OpenTelemetry/OTLP export is an optional adapter only. It must never create a default network write.

## Local JSONL event schema v0

Each line is one JSON object. Unknown fields are allowed only if they follow the privacy contract.

Common required fields for every event:

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | Must be `telemetry-event-v0` for this schema. |
| `event` | string | One of `run_start`, `phase_end`, `command`, `resource_sample`, `quality_gate`, `run_end`. |
| `run_id` | string | Local run identifier; no private path or username. |
| `timestamp` | string | ISO-like timestamp; timezone or `Z` recommended. |

Event-specific fields:

| Event | Required fields | Optional safe fields |
|---|---|---|
| `run_start` | `tool`, `os`, `arch`, `mode`, `options`, `telemetry_mode` | `skill_commit`, `python_version`, `machine_class` |
| `phase_end` | `phase`, `duration_ms`, `status` | `notes_count` |
| `command` | `cmd_class`, `duration_ms`, `exit_code` | `stdout_sha256`, `stderr_sha256`, `retry_index` |
| `resource_sample` | one of `rss_peak_kb`, `user_cpu_s`, `system_cpu_s` | `source`, `sample_phase` |
| `quality_gate` | `gate`, `status` | `unresolved_must_fix_count`, `evidence_count` |
| `run_end` | `duration_ms`, `outcome` | `blocked_reason`, `delivery_classification` |

Enums:

- `phase`: `DISCOVER`, `BACKLOG`, `PLAN`, `EXECUTE`, `VERIFY`, `ITERATE`, `TEST`, `DELIVER`, `DEPLOY`, `REPORT`.
- `status`: `pass`, `fail`, `blocked`, `skipped`.
- `outcome`: `passed`, `failed`, `blocked`, `partial`.
- `telemetry_mode`: `local-jsonl`, `aggregate-only`, `off`.
- `cmd_class`: `validator`, `json-validation`, `git`, `test`, `lint`, `build`, `smoke`, `security-review`, `ci-check`, `copilot-check`, `other`.

Example:

```json
{"schema_version":"telemetry-event-v0","event":"run_start","run_id":"2026-06-28T14-00Z-a1","timestamp":"2026-06-28T14:00:00Z","tool":"claude-code","os":"linux","arch":"x86_64","mode":"standard","options":["backlog","github-copilot"],"telemetry_mode":"local-jsonl","skill_commit":"13214f2"}
{"schema_version":"telemetry-event-v0","event":"phase_end","run_id":"2026-06-28T14-00Z-a1","timestamp":"2026-06-28T14:02:00Z","phase":"VERIFY","duration_ms":1532,"status":"pass"}
{"schema_version":"telemetry-event-v0","event":"command","run_id":"2026-06-28T14-00Z-a1","timestamp":"2026-06-28T14:02:04Z","cmd_class":"validator","duration_ms":421,"exit_code":0,"stdout_sha256":"e3b0c44298fc1c149afbf4c8996fb924"}
```

## Local recorder helper

`scripts/telemetry_record.py` is the opt-in stdlib helper for local machines.
It appends JSONL events to `.end-to-end-loop/telemetry.local.jsonl` by default
or to `E2E_LOOP_TELEMETRY_PATH` / `--telemetry-path` when explicitly supplied.
It never stores raw command text, stdout, stderr, environment variables, current
working directory, hostnames, usernames, home paths, prompts, transcripts, or
private file contents.

Useful commands:

```bash
python3 scripts/telemetry_record.py --run-id local-a run-start \
  --tool claude-code --mode standard --option backlog --option github-copilot
python3 scripts/telemetry_record.py --run-id local-a wrap --cmd-class validator -- \
  python3 scripts/validate_skill.py .
python3 scripts/telemetry_record.py --run-id local-a run-end \
  --duration-ms 120000 --outcome passed --delivery-classification repo-only
```

`wrap` lets the child process inherit stdout/stderr for the operator, but only
records `cmd_class`, `duration_ms`, `exit_code`, and stdlib resource samples.
Use the narrowest safe `cmd_class` instead of storing shell commands. Generated
local telemetry files remain ignored by default and should not be committed.

## Shareable telemetry summary schema v0

Use this for release evidence or public-safe reports. It must not include raw event lines.
`scripts/telemetry_aggregate.py` is the opt-in stdlib helper for this slice: it reads an explicitly supplied local JSONL file, refuses forbidden raw/private keys, emits aggregate JSON only, and performs no default network writes.

Example:

```bash
python3 scripts/telemetry_aggregate.py evals/telemetry-events.fixture.jsonl \
  --source fixture --claim-scope fixture-only
python3 scripts/test_telemetry_privacy.py
```

Required fields:

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | Must be `telemetry-summary-v0`. |
| `generated_at` | string | Timestamp. |
| `source` | string | `fixture`, `local-aggregate`, `ci-aggregate`, or `release-evidence`. |
| `runs` | integer | Number of summarized runs. |
| `machines` | object | Coarse machine bucket counts, e.g. `linux_x86_64`. |
| `median_duration_ms` | integer/null | Null when sample is too small or unavailable. |
| `p90_duration_ms` | integer/null | Null when sample is too small or unavailable. |
| `validation_pass_rate` | number/null | 0..1. |
| `caveman_compliance_rate` | number/null | 0..1. |
| `copilot_available_rate` | number/null | 0..1. |
| `privacy_review` | object | Must include `raw_logs_included`, `contains_secrets`, and `notes`. |
| `claim_scope` | string | `fixture-only`, `local-only`, `internal-release-evidence`, or `public-claim-approved`. |

Rules:

- `raw_logs_included` must be `false` for a shareable summary.
- `claim_scope: public-claim-approved` requires explicit human approval outside the telemetry artifact.
- Small samples must say so in `notes`.

## Backlog slices

| Order | Slice | Outcome | Dependencies | Interference | Complexity | Route | Acceptance |
|---:|---|---|---|---|---|---|---|
| 1 | `telemetry-spec` | Privacy-safe local schema and docs | Research plan, existing eval/result-log format | Self-learning memory, eval logs, release claims | `level_1`; privacy review `level_2` | CAVEMAN CODE + deterministic validator | Docs + fixtures validate; no hooks or network writes |
| 2 | `local-recorder` | Stdlib helper appends local JSONL and wraps command timing | Slice 1 schema, gitignore | Shell safety, raw output leakage | `level_1`; privacy review `level_2` | CAVEMAN CODE + focused tests | Records local validation command without raw stdout/stderr |
| 3 | `aggregation-summary` | JSONL -> sanitized summary | Slices 1-2 fixtures | Public overclaims, small sample ambiguity | `level_2` | high-reasoning review + deterministic Python | Fixture aggregation deterministic; scoped claims |
| 4 | `otlp-adapter` | Optional OpenTelemetry export docs/script | Slices 1-3, explicit endpoint config | Network writes, dependency scope | `level_2`; endpoint approval `level_3` | adapter-only implementation after approval | Disabled by default; no network without opt-in |

## Verification checklist

- [ ] `.gitignore` excludes `.end-to-end-loop/telemetry.local.jsonl` and local/private result logs.
- [ ] `scripts/validate_skill.py` validates telemetry fixtures and summaries.
- [ ] `scripts/telemetry_aggregate.py` deterministically converts the fixture JSONL into the shareable summary shape.
- [ ] `scripts/test_telemetry_privacy.py` passes, including forbidden raw/private key rejection for recorder and aggregator helpers.
- [ ] JSONL fixture parses one JSON object per line.
- [ ] Summary fixture has `raw_logs_included: false` and no private path/host/user fields.
- [ ] Security review confirms no prompts, secrets, env vars, stdout/stderr, or private paths are collected by default.
- [ ] Copilot status is represented as availability/rate/blocked evidence, not fabricated findings.
