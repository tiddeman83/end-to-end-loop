# Toward a Universal End-to-End Loop Skill for Coding Agents

## Abstract

This paper-in-progress investigates how to turn a phase-based coding-agent workflow
into a portable, safe, and testable skill that can operate across multiple agent and
coding-tool ecosystems. The initial artifact is the `end-to-end-loop` skill: a
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE -> TEST -> ITERATE -> DEPLOY ->
REPORT loop for taking software work from request to verified delivery.

## Research Questions

1. What common design patterns exist across agent skills, rule files, coding-agent
   instructions, and repository guidance systems?
2. Which parts of an end-to-end delivery loop should be universal, and which should
   be adapter-specific?
3. How can a skill enforce safety without becoming so ceremonial that agents skip it
   or users disable it?
4. What validation artifacts prove that the skill improves outcomes across realistic
   coding tasks?
5. How should deployment and external side effects be handled for agents with
   different permission models?

## Initial Hypothesis

A universal coding-agent skill should separate:

- Core behavioral contract: phases, gates, safety requirements, reporting.
- Tool adapters: Codex skills, Claude skills, Cursor rules, AGENTS.md, Hermes, and
  other agent-specific activation formats.
- Evidence artifacts: task plans, verification logs, test results, security review,
  and deployment records.

This separation should improve portability while preserving rigor.

## Method

- Review documentation and examples from comparable agent-instruction systems.
- Extract common primitives: trigger, scope, permissions, execution loop,
  validation, side-effect policy, memory, and reporting.
- Iterate on the skill in at least five GitHub-pushed revisions.
- In later iterations, forward-test the skill on realistic coding tasks with fresh
  agent context where feasible.

## Sources

- Agent Skills overview and specification: https://agentskills.io/home and
  https://agentskills.io/specification
- Agent Skills creator guidance: https://agentskills.io/skill-creation/best-practices,
  https://agentskills.io/skill-creation/optimizing-descriptions,
  https://agentskills.io/skill-creation/evaluating-skills, and
  https://agentskills.io/skill-creation/using-scripts
- OpenAI Codex skills and sandboxing:
  https://developers.openai.com/codex/skills and
  https://developers.openai.com/codex/concepts/sandboxing
- Claude Code skills and permissions:
  https://code.claude.com/docs/en/skills and
  https://code.claude.com/docs/en/settings
- Cursor rules, skills, and agent security:
  https://cursor.com/docs/rules.md,
  https://cursor.com/docs/skills.md, and
  https://cursor.com/docs/agent/security.md
- AGENTS.md open repository instruction format: https://agents.md/
- Hermes Agent public overview: https://hermes-agent.nousresearch.com/
- Saha, Faghih, and Feizi (2026), "Under the Hood of SKILL.md":
  https://arxiv.org/abs/2605.11418
- Ouyang, Xiao, Gu, and Zhang (2026), "SkCC: Portable and Secure Skill
  Compilation for Cross-Framework LLM Agents": https://arxiv.org/abs/2605.03353
- dos Santos et al. (2026), "Configuration Smells in AGENTS.md Files":
  https://arxiv.org/abs/2606.15828

## Findings

### Finding 1: The ecosystem is converging on progressive disclosure

Codex, Claude Code, Cursor, and the Agent Skills specification all describe skills
as folders centered on `SKILL.md`, with optional scripts, references, and assets.
The shared pattern is progressive disclosure: agents see lightweight metadata first,
then load the main instructions and optional resources only when needed.

Implication: the end-to-end-loop skill should keep `SKILL.md` lean and move detailed
phase checklists, security checks, adapter notes, and eval guidance into referenced
files.

### Finding 2: Trigger text is a safety boundary

The `description` field controls when a skill is surfaced and selected. Best-practice
guides recommend realistic should-trigger and should-not-trigger tests; recent
research shows that small changes to SKILL.md text can manipulate discovery,
selection, and governance.

Implication: the skill description must be specific, non-manipulative, and tested
against near misses. It should not claim universal superiority, trustworthiness, or
security without evidence.

### Finding 3: Cross-tool portability needs a core-plus-adapters model

The Agent Skills standard defines the common denominator, while Codex, Claude Code,
Cursor, AGENTS.md, and Hermes expose different trigger, permission, memory, subagent,
and sandbox mechanics. A single Markdown file can be broadly useful, but target
adapters are needed for high-fidelity behavior.

Implication: the project should define a canonical universal core, then add adapters
for tool-specific packaging and invocation behavior.

### Finding 4: Safety must classify side effects, not just tests

Codex, Claude Code, Cursor, and Hermes all describe some combination of sandboxing,
permissions, approvals, or isolated execution. The common principle is that agents
can operate autonomously within known boundaries and must ask before crossing them.

Implication: the loop should include a side-effect taxonomy and approval gate for
network access, external writes, credentials, production deploys, destructive file
operations, dependency changes, and irreversible actions.

### Finding 5: Evaluation must test both activation and outcomes

Skill evaluation guidance separates trigger accuracy from output quality. It also
recommends baseline comparisons, fresh contexts, realistic prompts, edge cases, and
recorded timing/token costs.

Implication: this skill needs evals for should-trigger prompts, should-not-trigger
prompts, full task outcomes, safety behavior, and instruction-smell regressions.

## Design Implications

- Remove mandatory CAVEMAN routing from the universal core. Keep it only as an
  optional Codex/local adapter if the user wants it.
- Reframe "DEPLOY" as "DELIVER" in the core, with live deployment as a conditional
  high-risk subcase requiring explicit user approval.
- Preserve the existing phase loop, but make it adaptive by task risk and size.
- Add a formal side-effect gate before commands that touch network, credentials,
  production systems, package registries, remote state, or destructive operations.
- Split reference material by concern: phase loop, safety, adapters, evals, and
  report template.
- Add trigger and outcome evals before declaring the skill mature.

## Limitations

- Hermes compatibility is not yet grounded in concrete Hermes skill-file
  conventions. Public material confirms relevant capabilities but not the exact
  packaging standard.
- Research sources are current as of 2026-06-21, but these agent ecosystems are
  changing quickly.
- The first iteration has not yet forward-tested the skill in independent agent
  contexts.
- The existing skill has not yet been rewritten; this paper currently supports a
  plan, not a validated final artifact.

## Proposed Artifact Architecture

```text
end-to-end-loop/
├── SKILL.md                         # Universal core
├── references/
│   ├── phase-checklists.md          # Core loop gates
│   ├── test-and-security.md         # Safety and verification checks
│   ├── adapters.md                  # Tool-specific packaging notes
│   ├── evals.md                     # Trigger and outcome evaluation plan
│   └── report-template.md           # Final report shape
├── evals/
│   └── evals.json                   # Future realistic eval cases
├── development.md                   # Development log, not packaged by default
├── memory.md                        # Discussion memory, not packaged by default
└── paper.md                         # Research paper draft, not packaged by default
```
