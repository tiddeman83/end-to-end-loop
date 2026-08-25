# Product Memory

Compact, sanitized learnings for the `end-to-end-loop` skill repository.

## Preferences

- PREF Keep the production skill portable across Codex, Claude Code, Cursor, and AGENTS.md-compatible agents.
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
- FACT Deep documentation or skill audit requests should use the `review-improve` option: inventory surfaces, compare cross-document claims, rank evidence-backed findings, make scoped edits, and report deferred follow-ups.
- FACT Remote `origin` is configured (`github.com/tiddeman83/end-to-end-loop`);
  push, remote CI, and release publication work. Supersedes the earlier
  no-remote blocker.
- FACT Remote tags before v0.1.0-alpha.3 were `v0.1.0-alpha.1` and
  `v0.1.0-alpha.2.dev`; alpha.2 was never tagged cleanly.

## Risks / avoid

- RISK Historical/private result logs can leak product-irrelevant operational context if committed as examples.
- AVOID Putting private office governance, dashboards, raw status feeds, secrets, raw chats, or private target repo details in this repo.
- AVOID Claiming green without observed command output, diff review, smoke evidence, or explicit approval.

## State-graph direction (2026-08-25)

- FACT The loop is already a finite state machine written as prose; the gap is
  materialization, not concept. Phases are nodes, `Exit:` lines are edges,
  ITERATE paths are cycles, `level_3` is an interrupt-before list.
- FACT Adopt the state-machine directives without a framework dependency: typed
  run state, per-key reducers (evidence append-only/immutable, counters
  increment-only), routers separated from phases, iteration ceilings with a named
  ESCALATE fallback, checkpoint/resume, one interrupt-before list.
- FACT `SKILL.md` body is 499 lines against the validator's 500-line body cap
  (503 lines with frontmatter); the cap counts body only. Core changes must be
  effectively net-zero on body lines: tables replace prose, detail to references.
- PREF A graph operating mode stays optional and later: it must inherit phase
  gates per node, must not duplicate work-graph orchestration skills
  (`graph-engineer` owns zones/PRDs/workers; this owns state/cycles/gates), and
  must prove itself against the linear loop before any claim that it helps.
- AVOID Turning the skill into an orchestration runtime or taking a framework
  dependency; the defensible role is the policy layer above runtimes.

## Next

- FACT The 2026-07-22 production assessment classifies the package as usable
  alpha, not production-ready (`17/40` evidence rubric); comparative multi-tool
  runs, recovery/state, and measured cost remain release blockers. Still true at
  v0.1.0-alpha.3, which changed documentation only.
- FACT The product should remain an assurance/delivery-policy layer over agent
  runtimes; prioritize executable run state, deterministic transitions,
  risk-triggered context, and budgets before a broad helper-agent fleet.
- NEXT Refresh `research/competitive-production-assessment.md` primary sources in
  a network-enabled environment; the 2026-07-22 pass's web tool returned 401 and
  direct HTTPS returned 403. The same caveat applies to the framework claims in
  `research/state-graph-adoption-plan.md`, which came from user-supplied
  secondary research.
- NEXT Build the `v0.1.0-alpha.4` kernel in order: run-state schema + reducers,
  then the transition table and `scripts/run_state.py`, then routers, budgets,
  failure taxonomy, checkpoint/resume/interrupts.
- NEXT Answer the four open decisions in `research/state-graph-adoption-plan.md`
  section 3.8: home of graph mode, JSON vs YAML, preset naming, and whether bare
  `graph` requires confirmation.
- NEXT Decide whether to implement Mission Mode as packaged optional public helper agents: mission-planner, loop-verifier, loop-reporter, adapter-builder, loop-reviewer, loop-eval-runner, deploy-readiness-checker.
- NEXT Telemetry follow-up after aggregation: define release-readiness metric language and keep public performance claims behind human approval plus multi-run evidence.
- NEXT Telemetry follow-up: add release-readiness metric language only after local privacy tests stay green on real runs.
