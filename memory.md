# Product Memory

Compact, sanitized learnings for the `end-to-end-loop` skill repository.

## Preferences

- PREF Keep the production skill portable across Codex, Hermes, Claude Code, Cursor, and AGENTS.md-compatible agents.
- PREF CAVEMAN remains mandatory for code-producing execution and iteration phases, and companion skills should be installed/update-checked before use.
- PREF Live deploy is opt-in per task; otherwise stop at prepared delivery or deploy-readiness reporting.
- PREF Keep private operations, office workflows, dashboard coordination, task-routing, and internal personas outside this product repo.

## Durable product facts

- FACT `SKILL.md` is the production skill core; `references/` contains supporting product references.
- FACT `scripts/validate_skill.py .` is the local validator, but the checkout folder must be named `end-to-end-loop` for the frontmatter/folder-name gate.
- FACT `references/adapters.md` is the home for tool-specific invocation and installation details.
- FACT `references/self-learning.md` defines compact memory and result-log rules.
- FACT Optional public helper agents, if added, should live under the Mission Mode product layer with functional names, narrow scopes, explicit reasoning levels, cheaper/standard/high-reasoning routing, and human approval gates for merge/release/deploy/admin/secrets/public claims.
- FACT The loop uses lean/standard/deep operating modes and level_0..level_3 complexity routing to minimize tokens, wall time, and model cost without weakening evidence or approval gates.
- FACT Repo-backed skill copies should check source freshness/self-update status before maintained repo work when feasible.
- FACT Local telemetry is opt-in local JSONL plus sanitized aggregation; recorder/aggregator must not store prompts, raw output, env, cwd, host/user/home identity, raw commands, or raw args by default.
- FACT `scripts/test_telemetry_privacy.py` is the local smoke test for telemetry helper privacy: fixture aggregation plus forbidden raw/private key rejection.
- FACT `skills/grilling/SKILL.md` is a packaged subskill for pre-build plan/design stress-testing, especially at agile feature/user-story level: ask one question at a time, provide a recommended answer, define precise verification layers, and inspect codebase instead of asking when repo evidence can answer.
- FACT When using Claude with a promptable Codex connector installed, code-producing work should include a Codex agentic reviewer as part of VERIFY/TEST evidence.

- FACT Every end-to-end-loop run should present the active skill version from `VERSION`; first target-project runs should discover production runtime and local development environments, then confirm them through grilling before build.

- FACT `skills/handoff/SKILL.md` is a packaged subskill for redacted continuation handoffs: write the handoff document to the OS temp directory, include suggested skills, and reference existing artifacts instead of duplicating them.

## Risks / avoid

- RISK Historical/private result logs can leak product-irrelevant operational context if committed as examples.
- AVOID Putting private office governance, dashboards, raw status feeds, secrets, raw chats, or private target repo details in this repo.
- AVOID Claiming green without observed command output, diff review, smoke evidence, or explicit approval.

## Next

- NEXT Decide whether to implement Mission Mode as packaged optional public helper agents: mission-planner, loop-verifier, loop-reporter, adapter-builder, loop-reviewer, loop-eval-runner, deploy-readiness-checker.
- NEXT Telemetry follow-up after aggregation: define release-readiness metric language and keep public performance claims behind human approval plus multi-run evidence.
- NEXT Telemetry follow-up: add release-readiness metric language only after local privacy tests stay green on real runs.
