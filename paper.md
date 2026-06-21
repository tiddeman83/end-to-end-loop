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

Research sources will be added after the first web review.

## Findings

Pending.

## Design Implications

Pending.

## Limitations

Pending.
