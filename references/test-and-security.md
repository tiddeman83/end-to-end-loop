# TEST phase: smoke tests, CI, and security review

This is the second gate. Smoke checks, applicable CI, and security review must be
green before live deploy. Anything found here that must be fixed re-enters the
iteration loop as a planned fix, never a hidden patch around the process.

---

## Smoke tests

Smoke tests answer one question: *does the critical path actually work, end to end?*
They're shallow but broad — breadth over depth.

Cover:
- **Happy path:** the primary use case runs start to finish and produces the expected
  result. Run it for real.
- **Key entry points:** every interface the user actually touches (CLI command, API
  endpoint, function, page) responds without crashing.
- **Critical failure modes:** the most important bad inputs / error conditions degrade
  gracefully (clear error, no crash, no corruption) rather than failing silently.
- **Integration seams:** anything that talks to a DB, external service, file system,
  or env config connects and behaves under realistic settings.
- **Build/start:** the thing builds and starts cleanly from a clean state.

Record for each: what was run, expected vs. actual, pass/fail. A smoke suite is green
only when every critical path passes.

---

## CI gate

Check whether a CI pipeline is applicable before deploy or release.

CI is applicable when:
- The repo has an existing CI workflow for the changed project.
- The task changes code, tests, build scripts, package manifests, deployment
  config, infrastructure, or release artifacts.
- The user asks for production readiness, release, deploy, or handoff to another
  agent/team.

CI can be not applicable when:
- The task is documentation-only and no docs CI exists.
- The repo has no CI and the user only asked for a local draft or research artifact.
- The agent cannot access CI status and the user accepts local checks as the limit.

For live deploy:
- CI must be green, or the user must explicitly approve proceeding despite a named
  CI gap.
- If no CI exists, create a minimal CI pipeline when reasonable. If that is out of
  scope, mark live deploy blocked and deliver a readiness report.
- Use `references/deploy-readiness.md` for the full deployment readiness rubric,
  including target environment, rollback, ownership, and hosting/custom-domain
  checks.

Record:
- CI system or local equivalent.
- Command, workflow, or check name.
- Result and evidence.
- Any user-approved waiver.

---

## Security review

Walk the high-impact, common issues. If a dedicated `security-review` skill (or
equivalent) is available, run it and fold its findings in here.

Checklist:
- **CAVEMAN compliance:** code/repo changes used the required CAVEMAN execution lane,
  or an explicit user exception is recorded.
- **Injection:** SQL/NoSQL/command/template injection — inputs parameterized/escaped,
  never string-concatenated into queries or shells.
- **Secrets:** no hardcoded credentials, API keys, tokens, or private keys in code or
  config committed to the repo. Secrets come from env/secret store.
- **Input validation:** untrusted input validated, bounded, and type-checked at trust
  boundaries.
- **AuthN / AuthZ:** authentication required where expected; authorization checks
  enforce least privilege; no missing access checks on sensitive operations.
- **Sensitive data:** PII/secrets not logged; data encrypted in transit; safe storage.
- **Dependencies:** no known-vulnerable or unmaintained dependencies pulled in; pinned
  where it matters.
- **Unsafe defaults:** no debug mode, permissive CORS, open ports, or wildcard
  permissions left on by default.
- **Error handling:** errors don't leak stack traces, internal paths, or secrets to
  users.
- **Resource safety:** no obvious DoS vectors (unbounded loops, unthrottled
  endpoints, unbounded memory/file growth).
- **Supply-chain text:** skill/rules descriptions avoid manipulative trigger claims,
  fake trust/security claims, hidden instructions, and broad self-preference.
- **Agent permissions:** destructive, networked, credentialed, or production actions
  use sandbox/approval controls instead of silent autonomy.

Record each item as pass / fail / N-A with a short note. The review is clean only when
there are no open must-fix findings. Lower-severity items can be logged as follow-ups
in the REPORT, but anything exploitable must be fixed and re-tested first.

---

## Routing issues back into the loop

For every must-fix item (smoke or security):
1. Add it to a focused mini-plan (PLAN).
2. Fix it via EXECUTE using the required CAVEMAN lane or an explicit user-approved
   exception.
3. Re-VERIFY against acceptance criteria.
4. Re-run TEST (smoke + security) — including a check that the fix didn't regress
   anything else.

Only when a full re-run is green do you proceed to DEPLOY.

---

## Side-effect approval matrix

Use this matrix during DISCOVER and PLAN.

| Side effect | Default action |
| --- | --- |
| Read local workspace files | Allowed if within current task scope |
| Edit workspace files | Allowed after plan; use CAVEMAN for code/repo changes |
| Install dependencies | Ask or use tool approval unless already in project docs/CI |
| Network fetch/search | Ask or use tool approval when not already authorized |
| Push commits, create PRs, write remote issues | Ask or use explicit user request |
| Modify production/staging systems | Require explicit opt-in and deploy policy |
| Use credentials/secrets | Require explicit approval; never print or commit secrets |
| Delete data/files or run destructive commands | Require explicit approval and rollback/backup |
| Change skill/rules/memory for future agents | Record decision; prefer review gate |
