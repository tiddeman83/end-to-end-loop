# End-to-End Loop Skill Development Log

This file records decisions, trade-offs, iteration goals, and verification outcomes
for the development of the end-to-end-loop skill.

Repository: https://github.com/tiddeman83/end-to-end-loop
Visibility: private during development
Started: 2026-06-21

## Operating Rules

- Keep every iteration committed and pushed to GitHub.
- Treat this file, `memory.md`, and `paper.md` as development artifacts. They may be
  excluded from a final distributable skill package if the target agent expects a
  minimal skill folder.
- Design the skill to be portable across agent/coding tools, including Codex,
  Claude-style skills, Cursor-style rules, AGENTS.md workflows, and Hermes.
- Prefer explicit gates, safety checks, and validation artifacts over implicit
  confidence.
- Record user decisions before encoding them into the skill.

## Iteration Log

### Iteration 1 - Repository, Research Frame, and Direction

Status: in progress

Goals:
- Create the private GitHub repository and connect this workspace to it.
- Add development documentation for decisions, memory, and research output.
- Research comparable agent-skill and coding-agent instruction systems.
- Produce a first improvement plan and critical questions for the user.

Initial observations:
- The existing skill has a strong phase-based delivery loop.
- The current wording is still Codex- and CAVEMAN-specific in places.
- The safety model is present but can become more explicit, portable, and testable.
- The current "DEPLOY" phase needs a clearer cross-tool definition because many
  agents cannot deploy directly or should not deploy without user approval.

Open decisions:
- What exact agent surfaces must be first-class targets besides Codex and Hermes?
- Should the skill be one universal markdown document, or a canonical core plus
  adapters for different agent systems?
- What level of mandatory user approval is required before external writes, deploys,
  package installs, or destructive operations?

Verification:
- Pending internet research.
- Pending first commit and push.
