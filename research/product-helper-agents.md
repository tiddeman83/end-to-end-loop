# Optional Public Helper Agents

`end-to-end-loop` is first a portable Agent Skill. Optional agents may add value, but they must remain functional, public-facing helpers — not an internal office/team simulation.

## Recommendation

Add optional helper agents only where they make the delivery loop easier to verify or adopt.

Do not add a general executor agent. Execution stays with the host coding agent and the required CAVEMAN/Cavekit lane.

## MVP candidates

### `loop-verifier`

Checks whether a completed task followed the loop.

Inputs:

- original request;
- plan / acceptance criteria;
- diff or artifact summary;
- commands and outputs;
- final report.

Output:

- pass/fail by phase;
- missing evidence;
- unsafe or overconfident claims;
- remediation checklist.

### `loop-reporter`

Turns messy evidence into a structured final report.

Guardrail: it must not mark anything green without observed evidence.

### `adapter-builder`

Produces target-specific installation/adaptation guidance for Codex, Hermes, Claude Code, Cursor, and AGENTS.md-style environments from `references/adapters.md`.

### `loop-reviewer`

Read-only review of a diff against scope, maintainability, safety, and the loop's evidence requirements.

### `loop-eval-runner`

Coordinates trigger/outcome evals and writes filled result logs from the existing eval templates.

### `deploy-readiness-checker`

Produces a readiness report for live deploy requests. It does not deploy by default.

## Non-goals

- No public character/persona team.
- No internal office governance.
- No release approval authority.
- No default deploy agent.
- No private task-routing or dashboard dependency.

## Packaging sketch

```text
agents/
  loop-verifier.md
  loop-reporter.md
  adapter-builder.md
  loop-reviewer.md
  loop-eval-runner.md
  deploy-readiness-checker.md
```

Each agent should include:

- trigger conditions;
- allowed inputs;
- read/write permissions;
- output schema;
- validation checks;
- explicit boundaries.

## Release posture

Treat public helper agents as a post-cleanup MVP track. First separate private office material from this repository, then add agents behind clear evals.
