# Backlog and GitHub Copilot options

Use this reference when `backlog` or `github-copilot` is selected, or when a long
prompt evolves into multi-feature planning plus CI/CD feedback handling.

## CAVEMAN ULTRA state packet

Keep this packet current at every phase transition:

```text
MODE/OPTIONS: <lean|standard|deep> + <backlog?> + <github-copilot?>
GOAL: <observable outcome>
BACKLOG: <ordered slice ids or none>
DEPS: <known prerequisites/blockers>
INTERFERENCE: <cross-feature conflicts>
LEVELS: <slice -> level_0..level_3>
ROUTES: <slice -> tool/model lane>
ACCEPTANCE: <pass/fail checks>
VERIFY/TEST: <commands, CI, smoke, security, Copilot>
BLOCKERS: <open blockers + owner>
NEXT: <single next action>
```

If the user adds scope mid-run, update only the delta and re-emit this packet before
continuing. Do not carry forward a full transcript when this packet is enough.

## Backlog analysis template

For each backlog item:

| Field | Meaning |
|---|---|
| `id` | Stable short name |
| `outcome` | User-visible result |
| `current_feature_fit` | How it relates to existing features/architecture |
| `dependencies` | Prerequisites, shared files, data/API/schema, auth, CI/deploy |
| `interference` | Conflicts or coupling with other backlog items |
| `slice` | Smallest independently verifiable implementation unit |
| `acceptance` | Pass/fail done checks |
| `complexity` | `level_0`..`level_3` |
| `route` | Deterministic tool, cheap model, standard coding model, high-reasoning model, human gate |
| `order_reason` | Why this slice should be before/after others |

Required backlog gates:

1. No implementation before dependencies and interference are explicit.
2. No large vague backlog item enters EXECUTE; split it first.
3. No hidden reordering; explain dependency, risk, or value reason.
4. No model overuse by default; route cheap first, escalate on evidence.
5. No context bloat; keep CAVEMAN ULTRA packet as the handoff artifact.

## Copilot feedback template

Record Copilot status in VERIFY/TEST and final REPORT:

```text
COPILOT_STATUS: collected | unavailable | waived
SOURCE: PR review | gh copilot | gh-copilot | GitHub API | CI annotation | other
AUTH/TOOLING: <observed command/API status>
FINDINGS:
- id: <copilot-1>
  severity: must-fix | should-fix | false-positive | note
  summary: <finding>
  action: fixed | planned | rejected-with-rationale | blocked
BLOCKERS: <if unavailable>
```

Rules:

- Use real Copilot/GitHub output only. Never invent findings.
- Do not install Copilot tooling unless installation is explicitly in scope.
- Unresolved must-fix Copilot findings block PR/CI/CD readiness like failing tests.
- False positives need a short rationale.
- If unavailable, name the blocker and keep normal review/security gates active.

## Model routing hints

- `level_0`: shell/Python scripts, linters, validators, GitHub API reads, cheap summarizer.
- `level_1`: standard coding model + CAVEMAN CODE for bounded implementation slices.
- `level_2`: high-reasoning planning/review for architecture, dependency graph,
  backlog interference, security, deploy, or Copilot conflict triage.
- `level_3`: human decision for merge/release/deploy/admin/secrets/destructive actions
  or accepting unresolved must-fix findings.

Always state the selected route and why it is the cheapest adequate option.
