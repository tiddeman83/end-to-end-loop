# Product Memory

Compact, sanitized learnings for the `end-to-end-loop` skill repository.

## Preferences

- PREF Keep the production skill portable across Codex, Hermes, Claude Code, Cursor, and AGENTS.md-compatible agents.
- PREF CAVEMAN remains mandatory for code-producing execution and iteration phases.
- PREF Live deploy is opt-in per task; otherwise stop at prepared delivery or deploy-readiness reporting.
- PREF Keep private operations, office workflows, dashboard coordination, task-routing, and internal personas outside this product repo.

## Durable product facts

- FACT `SKILL.md` is the production skill core; `references/` contains supporting product references.
- FACT `scripts/validate_skill.py .` is the local validator, but the checkout folder must be named `end-to-end-loop` for the frontmatter/folder-name gate.
- FACT `references/adapters.md` is the home for tool-specific invocation and installation details.
- FACT `references/self-learning.md` defines compact memory and result-log rules.
- FACT Optional public helper agents, if added, should live under the Mission Mode product layer with functional names, narrow scopes, explicit reasoning levels, and human approval gates for merge/release/deploy/admin/secrets/public claims.

## Risks / avoid

- RISK Historical/private result logs can leak product-irrelevant operational context if committed as examples.
- AVOID Putting private office governance, dashboards, raw status feeds, secrets, raw chats, or private target repo details in this repo.
- AVOID Claiming green without observed command output, diff review, smoke evidence, or explicit approval.

## Next

- NEXT Decide whether to implement Mission Mode as packaged optional public helper agents: mission-planner, loop-verifier, loop-reporter, adapter-builder, loop-reviewer, loop-eval-runner, deploy-readiness-checker.
