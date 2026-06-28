# Self-Learning and Per-Repo Memory

`end-to-end-loop` should improve across repeated runs without turning memory into a transcript dump. The goal is compact, durable, privacy-safe repo memory: enough to avoid repeating discovery, failed approaches, and known blockers, small enough that the next agent actually reads it.

## Memory locations

Inside a target repository using the skill:

```text
.end-to-end-loop/memory.md              # sanitized durable repo memory; may be committed when safe
.end-to-end-loop/memory.local.md        # private/local-only memory; do not commit by default
.end-to-end-loop/results/*.json         # per-run result logs
```

Inside this skill repository:

```text
memory.md                              # settled decisions about this skill itself
development.md                         # longer iteration log
evals/results/*.json                   # evaluation result logs for the skill
```

## CAVEMAN ULTRA memory style

Use terse line labels. No prose unless needed. One durable fact per line.

Allowed labels:

- `FACT:` durable repo fact.
- `CMD:` verified command and compact result.
- `BLOCK:` known blocker likely to recur.
- `PREF:` user/repo preference.
- `RISK:` recurring risk.
- `FIX:` successful fix pattern.
- `AVOID:` failed or unsafe approach.
- `NEXT:` likely next action.
- `STALE?:` item that needs re-check.

Template:

```text
# End-to-End Loop Repo Memory

Updated: YYYY-MM-DD
Scope: <repo-name>
Privacy: sanitized|local-only|mixed

FACT: <durable repo fact>
CMD: `<verified command>` -> <compact result>
BLOCK: <known blocker>
PREF: <repo/user preference>
RISK: <recurring risk>
FIX: <successful pattern>
AVOID: <failed/unsafe approach>
NEXT: <likely next action>
STALE?: <needs re-check>
```

Example:

```text
FACT: Validator requires checkout folder basename `end-to-end-loop`.
CMD: `python3 scripts/validate_skill.py .` -> pass in exact-name temp copy.
BLOCK: GitHub PR/Actions read may fail when token lacks metadata/actions scopes.
PREF: No live deploy unless explicit opt-in + CI/waiver + rollback + smoke.
FIX: For validation, copy worktree to `/tmp/.../end-to-end-loop` before running validator.
NEXT: Run trigger/outcome evals before first pre-release.
```

## Run result log schema

Write one JSON object per meaningful run when repo writes are in scope.

```json
{
  "schema_version": "1.0",
  "date": "YYYY-MM-DD",
  "run_id": "YYYY-MM-DD-HHMM-slug",
  "agent_or_tool": "codex|claude-code|cursor|agents-md|copilot|other",
  "skill_version_or_commit": "<commit-or-version>",
  "repo": {
    "name": "<repo>",
    "branch": "<branch>",
    "commit_before": "<sha-or-null>",
    "commit_after": "<sha-or-null>"
  },
  "prompt_summary": "<sanitized short prompt>",
  "delivery_classification": "none|repo-only|prep-only|live-deploy",
  "side_effects": ["filesystem", "git", "network", "deploy", "credentials"],
  "outcome": "passed|failed|blocked|partial",
  "commands_or_evidence": ["<compact observed result>"],
  "acceptance_criteria": [
    {"criterion": "<pass/fail statement>", "status": "pass|fail|blocked", "evidence": "<observed evidence>"}
  ],
  "caveman_behavior": "compliant|blocked|exception_approved|not_applicable",
  "deploy_policy_behavior": "compliant|violation|not_applicable",
  "security_review": "pass|fail|blocked|not_applicable",
  "ci_status": "green|red|missing|not_checked|not_applicable",
  "memory_read": "yes|no|not_present|not_applicable",
  "memory_update": "updated|none|local_only|blocked|not_applicable",
  "learning_candidates": [
    {"type": "FACT|CMD|BLOCK|PREF|RISK|FIX|AVOID|NEXT", "text": "<compact sanitized learning>", "promote": true, "reason": "<durability/privacy rationale>"}
  ],
  "privacy_review": {"contains_secrets": false, "commit_safe": true, "redactions": []},
  "copilot_findings": {"available": false, "summary": "not checked", "items": []},
  "notes": "<short notes>"
}
```

## Learning update rules

Read at DISCOVER:

1. If present, read `.end-to-end-loop/memory.md`.
2. If present and allowed by local privacy policy, read `.end-to-end-loop/memory.local.md`.
3. Treat memory as context, not proof. Re-verify safety/correctness facts before relying on them.

Write at REPORT:

1. Write a result log when file writes are in scope and the run changed state or produced a material decision.
2. Extract learning candidates from observed evidence.
3. Promote only compact, durable, safe items to memory.
4. Merge duplicates; replace stale facts only when the new fact is verified.
5. If unsure whether an item is safe to commit, put it in `memory.local.md` or ask the user.

Promote only when all are true:

- durable across future runs;
- verified by command, diff, CI, user instruction, or observed repo state;
- repo-specific or durable user preference;
- short enough to scan quickly;
- privacy-safe.

Do not promote:

- secrets, tokens, private keys, env var values, cookies, auth headers;
- full prompts, full transcripts, bulky logs, or stack traces;
- one-off transient failures unless likely to recur;
- speculative conclusions;
- personal data unrelated to repo work;
- absolute paths when a relative path is enough.

## Size controls

Suggested limits:

- `memory.md`: max 120 lines or 8 KB.
- `memory.local.md`: max 200 lines or 16 KB.
- one result log: max 16 KB unless the user asks for full trace archival.
- keep last 50 result logs by default.
- summarize/archive older logs before `.end-to-end-loop/` exceeds 1 MB.

## Privacy and gitignore

Recommended target-repo `.gitignore` snippet:

```gitignore
# end-to-end-loop local/private memory
.end-to-end-loop/memory.local.md
.end-to-end-loop/results/*.local.json
```

A result log with `privacy_review.commit_safe: false` must not be committed.

## Evaluation requirement

Self-learning is part of release quality. Evaluation should check that the agent:

- reads prior repo memory when present;
- writes a compact result log when appropriate;
- proposes learning candidates;
- promotes only durable/privacy-safe items;
- avoids memory bloat;
- never lets memory override current user instructions or live evidence.
