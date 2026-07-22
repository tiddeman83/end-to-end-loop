# Competitive Research and Production Assessment

Date: 2026-07-22

Assessed version: `0.1.0-alpha.2` (`ece3d94`)

Mode: `standard + review-improve`, research and planning only

## Executive decision

The skill is a credible **alpha delivery policy**, but it is **not yet proven for
production work** and should not be promoted as production-ready in the next
release. Its strongest assets are explicit evidence, safety, and deployment
gates. Its weakest areas are runtime agency, enforceable state, measured
comparative outcomes, portability evidence, and cost controls that an agent can
execute rather than merely read.

The next release should remain an alpha and concentrate on a small executable
kernel: a run-state artifact, deterministic policy checks, budget-aware context
packets, bounded recovery, and baseline-versus-skill evaluations on real tasks.
Do not build a large named-agent fleet first. That would add coordination cost
before the single-agent loop is measurable.

## Research method and limitation

The review combined:

1. a repository inventory of the production skill, adapters, subskills,
   validator, installer, telemetry, evaluation corpus, and existing result logs;
2. local execution of the validator, privacy self-test, Python compilation, an
   installation smoke test, JSON parsing, and diff hygiene;
3. a comparison framework derived from the primary projects and standards below.

Live web retrieval was attempted on 2026-07-22 through both the configured web
research tool and direct HTTPS. The web tool returned `401 Unauthorized`; direct
HTTPS returned `403 Forbidden` from the environment tunnel. Therefore this is a
**source-indexed research pass, not a claim that every upstream page was freshly
re-read**. URLs and time-sensitive project details must be refreshed in a
network-enabled release pass. No pricing or current-version claim is made.

## Comparable approaches

The products are not exact substitutes. They occupy three useful comparison
layers: orchestration runtimes, coding-agent harnesses, and assurance standards.

| Approach | Primary source | Useful pattern | Gap it exposes here |
|---|---|---|---|
| Anthropic effective-agent patterns | [Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Prefer the simplest workflow that works; distinguish workflows from agents; use evaluator/optimizer and parallelization selectively. | The skill says “use helpers only when useful,” but has no executable decision rule or measured break-even point. |
| OpenAI Agents SDK | [Agents SDK documentation](https://openai.github.io/openai-agents-python/) | Small primitives for agents, handoffs, guardrails, sessions, and tracing. | The skill is prose-first: it has no resumable session state, typed handoff contract, or trace that reconstructs control flow. |
| LangGraph | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Durable execution, persistence, interrupts, memory, and human-in-the-loop around a graph/state model. | The phase diagram is not an executable state machine and cannot resume deterministically after interruption. |
| Microsoft AutoGen / AgentChat | [AgentChat guide](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html) | Explicit teams, termination conditions, state, and logging for multi-agent applications. | “Mission Mode” proposes roles, but termination, message budgets, shared state, and conflict resolution are underspecified. |
| Google Agent Development Kit | [Multi-agent systems](https://google.github.io/adk-docs/agents/multi-agents/) | Compose specialist agents and deterministic workflow agents; use evaluation and callbacks around execution. | Subskills are referenced, not dispatched through a common input/output protocol with lifecycle hooks. |
| SWE-agent | [SWE-agent repository](https://github.com/SWE-agent/SWE-agent) and [paper](https://arxiv.org/abs/2405.15793) | The agent-computer interface and constrained tools materially affect coding outcomes. | The skill constrains policy but does not provide a minimal tool interface or quantify how its instructions change outcomes. |
| SWE-bench | [SWE-bench paper](https://arxiv.org/abs/2310.06770) | Evaluate repository-level issue resolution with executable tests and contamination-aware task sets. | Current scenarios are mostly specifications and self-authored result logs; there is no held-out comparative task suite. |
| Agent Skills specification | [Agent Skills specification](https://agentskills.io/specification) | Progressive disclosure and a conventional skill package improve portability and context efficiency. | The root skill is long and eagerly carries multiple optional policies; routing/reference loading needs token measurements. |
| Model Context Protocol | [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | Standardize discovery and invocation of tools/data instead of baking provider behavior into prompts. | Adapters describe tool differences, but the loop has no capability manifest or machine-readable preflight. |
| NIST SSDF | [SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | Organize secure development practices around preparation, protection, production, and vulnerability response. | Security review is required proportionally, but release evidence is not mapped to a small auditable control set. |
| SLSA | [SLSA specification](https://slsa.dev/spec/) | Provenance and build integrity claims require verifiable evidence, not process language alone. | The release path does not emit provenance or tie a delivered artifact to source, builder, and verification evidence. |
| OpenSSF Scorecard | [OpenSSF Scorecard](https://scorecard.dev/) | Automate repository security-health checks and surface objective gaps. | The repo has validation CI but no dependency, branch-protection, signed-release, or broader supply-chain evidence in this checkout. |

### Market position

The defensible position is **an assurance and delivery-policy layer for coding
agents**, not a replacement for an agent runtime. Runtimes already own tool
calling, sessions, persistence, tracing, and multi-agent transport. Coding
harnesses own the shell/editor interface. `end-to-end-loop` can add value by
providing portable acceptance, evidence, cost, security, and delivery gates over
those runtimes.

Trying to become another general orchestration framework would increase scope,
tokens, and maintenance cost while weakening portability. Instead, define a
small machine-readable protocol that runtimes can implement.

## Current production-readiness assessment

Scores use `0 = absent`, `1 = stated`, `2 = partially implemented`,
`3 = locally evidenced`, and `4 = production evidenced across tools`. They are
an assessment aid, not a benchmark result.

| Dimension | Score | Evidence and finding |
|---|---:|---|
| Safety and deployment control | 3/4 | Strong explicit opt-in, CI, rollback, smoke, credential, and security gates; scenario coverage exists. No external deployment exercise or provenance evidence was available. |
| Verification discipline | 3/4 | Static validator, privacy self-test, acceptance language, and result schema all run locally. Most outcome evidence is produced by this same repo rather than an independent evaluator. |
| Runtime agency | 1/4 | Phases and loops are prose. There is no persistent run state, policy engine, event-driven transition, bounded retry controller, or deterministic resume. |
| Cost and token efficiency | 1/4 | Lean/standard/deep and complexity routing are documented, but no hard budgets, context accounting, early-stop policy, or baseline cost comparison is enforced. |
| Reliability and recovery | 1/4 | Iteration is required, but retry ceilings, failure taxonomy, checkpoint/resume, idempotency, and escalation rules are not executable. |
| Portability | 2/4 | Package and adapters cover several tools conceptually; this pass only smoke-tested local installation, not activation and behavior in each named tool. |
| Observability | 2/4 | Privacy-aware telemetry helpers exist, but they use fixture/local examples and do not reconstruct phase transitions, decisions, retries, or budget use from a real run. |
| Security and supply chain | 2/4 | Security guidance and local privacy rejection tests are useful. No dependency/supply-chain scan, provenance, signed artifact, or mapped release-control evidence was observed. |
| Evaluation maturity | 1/4 | There are 43 trigger cases, 11 written outcome scenarios, and 6 result logs, but no baseline comparison, held-out set, multi-tool matrix, repeated trials, or measured quality/cost confidence interval. |
| Release operations | 1/4 | Version/changelog/CI exist, but this checkout has no configured Git remote or upstream, so freshness, push, remote CI, tag, and release checks cannot be completed. |

**Total: 17/40.** This supports “usable alpha,” not “production-ready.” A
reasonable production-candidate threshold is at least `30/40`, with no score
below `2`, plus all mandatory release gates below.

## What local testing actually proved

- `python3 scripts/validate_skill.py .` passed the repository's static contract.
- `python3 scripts/test_telemetry_privacy.py` passed fixture aggregation and
  forbidden-key rejection.
- `python3 -m py_compile scripts/*.py` passed syntax compilation.
- A temporary-home install completed and included the documented package files.
- All six committed result logs parsed as JSON; the trigger corpus contains 43
  cases (28 positive, 15 negative).
- `git diff --check` passed before this documentation iteration.

These checks prove package consistency and a narrow privacy property. They do
**not** prove that the skill improves task success, lowers cost, operates across
tools, survives interruption, or is safe for production deployment.

The installer smoke test also exposed a cost/packaging concern: it installs
repository-maintenance files such as `AGENTS.md`, `.github/workflows/validate.yml`,
`.gitignore`, all historical eval results, and every helper. The next release
should measure and define a minimal runtime package rather than assume the full
repository is the cheapest useful context or install surface.

## Highest-value product changes

### 1. Make the loop stateful before making it multi-agent

Add a small versioned run manifest, for example
`.end-to-end-loop/run.json`, containing phase, mode, goal, acceptance criteria,
capabilities, side-effect approvals, budgets, evidence references, retry counts,
delivery class, and blockers. Define allowed transitions and resumability. Keep
large command output outside the manifest; store references and digests.

This makes the tool more agentic because the agent can decide the next allowed
action from state and observed results, rather than reread a long policy and
improvise.

### 2. Replace blanket ceremony with risk-triggered gates

Retain non-negotiable evidence and deploy rules, but load optional references
only when a capability/risk trigger fires. Examples: load security controls for
auth/dependencies/secrets, deploy readiness only for `prep-only` or
`live-deploy`, and helper-team rules only when independent work exceeds the
coordination threshold.

### 3. Add explicit budgets and termination

Each run should declare maximum iterations, approximate token/tool/time budgets,
and escalation conditions. Stop when acceptance criteria pass, a hard gate
blocks, the retry ceiling is reached, or further work has negative expected
value. Report budget use as available rather than fabricating unavailable model
metrics.

### 4. Use bounded specialists, not a standing “agent fleet”

Create one common specialist contract first: input state slice, allowed tools,
deliverable schema, evidence, confidence, budget, and termination reason. Spawn a
specialist only for independent parallel work, context isolation, or materially
different expertise. The coordinator alone owns state transitions and final
claims.

### 5. Prove value with comparative evals

For each held-out repository task, run baseline and skill variants in fresh
contexts, ideally with repeated trials. Measure task success, regression rate,
unsafe side effects, evidence completeness, wall time, tool calls, model tokens
where exposed, retries, and human interventions. Report medians and raw sample
counts. Do not optimize prompt length alone; optimize cost per verified success.

## Mandatory gates for a production candidate

1. **Comparative evidence:** at least three task classes, two supported tools,
   baseline/current comparisons, and repeated runs with raw sanitized results.
2. **State and recovery:** versioned run state, deterministic transition checks,
   interruption/resume test, retry ceiling, and idempotent side-effect handling.
3. **Cost:** measured context/package size, tool calls and tokens where available,
   plus a regression budget for cost per verified success.
4. **Portability:** install, trigger, execute/block, verify, and report scenarios
   exercised in every tool claimed in public documentation.
5. **Security:** threat model, secret/privacy negative tests, dependency and
   supply-chain checks, and artifact/source traceability for release assets.
6. **Release integrity:** configured remote/upstream, reviewed diff, green remote
   CI, signed or otherwise authenticated tag/release according to maintainer
   policy, rollback instructions, and release notes.
7. **Independent review:** an evaluator or reviewer that did not author the
   change adjudicates a representative sample and unresolved findings.

## Recommended next release scope

Ship `0.1.0-alpha.3`, not `0.2.0` or `1.0.0`, after implementing and evaluating
only the following vertical slice:

- machine-readable run manifest and transition schema;
- deterministic preflight/transition validator;
- context packet with risk-triggered reference routing;
- retry, budget, and termination fields;
- two baseline-versus-current task pairs recorded in sanitized result logs;
- lean runtime-package manifest and install-size/context-size report;
- refreshed primary-source research when network access is available.

Defer a named multi-agent product, live deployment, broad runtime framework,
public production claims, and major-version release until the gates above pass.
