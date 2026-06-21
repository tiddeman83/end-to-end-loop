# TEST phase: smoke tests & security review

This is the second gate. Both halves must be green before DEPLOY. Anything found here
that must be fixed re-enters the iteration loop as a planned fix — never a hot-patch
around the process.

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

## Security review

Walk the high-impact, common issues. If a dedicated `security-review` skill (or
equivalent) is available, run it and fold its findings in here.

Checklist:
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

Record each item as pass / fail / N-A with a short note. The review is clean only when
there are no open must-fix findings. Lower-severity items can be logged as follow-ups
in the REPORT, but anything exploitable must be fixed and re-tested first.

---

## Routing issues back into the loop

For every must-fix item (smoke or security):
1. Add it to a focused mini-plan (PLAN).
2. Fix it via EXECUTE (CAVEMAN ULTRA / CAVEMAN CODE if available).
3. Re-VERIFY against acceptance criteria.
4. Re-run TEST (smoke + security) — including a check that the fix didn't regress
   anything else.

Only when a full re-run is green do you proceed to DEPLOY.
