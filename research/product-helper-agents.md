# Mission Mode: Optional Public Helper Agents

`end-to-end-loop` is first a portable Agent Skill. A stronger product layer can be called **Mission Mode**: an optional agentic runtime pattern that assembles functional helper agents around a delivery mission.

Mission Mode is public/product-facing. It is not the private DevBoss office.

## Recommendation

Add optional helper agents where they make the delivery loop easier to execute, verify, or adopt. Keep the universal `SKILL.md` usable on its own.

Mission Mode should feel like:

```text
mission intent -> scoped agent team -> evidence gates -> final report
```

Do not add an unrestricted general executor agent. Execution still follows the host coding agent, CAVEMAN/Cavekit lane, and deploy/readiness gates.

## Reasoning levels

Mission Mode should assign agents by reasoning depth and risk, not by persona.

### Level 0 — Mechanical / cheap

Use for deterministic, low-risk tasks.

Examples:

- format result logs;
- check JSON/schema shape;
- list changed files;
- summarize command output;
- verify required sections exist.

Expected model class: fast/cheap/general model or local script.

### Level 1 — Standard implementation support

Use for bounded software delivery assistance.

Examples:

- draft plans from acceptance criteria;
- run loop compliance checks;
- prepare final report;
- inspect adapter docs;
- suggest verification commands.

Expected model class: strong general coding model.

### Level 2 — Deep review / safety / architecture

Use when consequences or ambiguity are higher.

Examples:

- review deploy readiness;
- evaluate security and privilege boundaries;
- assess cross-repo or multi-agent plans;
- judge whether evidence supports a release claim;
- decide whether public helper agents should be added to a product package.

Expected model class: high-reasoning model.

### Level 3 — Human approval gate

Use when the next step is irreversible, external, public, or privileged.

Examples:

- merge to protected/main branch;
- release/tag/public pre-release;
- production deploy;
- secret/admin/permission changes;
- publishing product claims.

Expected actor: maintainer/repository owner. Agents may prepare evidence, not approve.

## Mission Mode workflow

1. **Mission intake**
   - Classify task type, repo, risk, side effects, and desired delivery target.

2. **Agent assignment**
   - Pick helper agents and reasoning level per task.
   - Record why a higher/lower reasoning level is sufficient.

3. **Loop execution**
   - DISCOVER, PLAN, EXECUTE, VERIFY, TEST, DELIVER/DEPLOY, REPORT.
   - CAVEMAN/Cavekit remains mandatory for code-producing work.

4. **Evidence aggregation**
   - Gather commands, diffs, CI, smoke checks, risks, and blockers.

5. **Gate decision**
   - Agents can recommend pass/fail/readiness.
   - Human approval remains required for Level 3 actions.

## MVP public helper agents

### `mission-planner`

Creates the mission plan, assigns helper agents, and labels reasoning level per workstream.

Output:

- mission scope;
- acceptance criteria;
- agent assignments;
- reasoning-level choices;
- verification plan;
- approval gates.

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

Produces target-specific installation/adaptation guidance for Codex, Claude Code, Cursor, and AGENTS.md-style environments from `references/adapters.md`.

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
- No hidden autonomous office behind a user's repo.

## Packaging sketch

```text
agents/
  mission-planner.md
  loop-verifier.md
  loop-reporter.md
  adapter-builder.md
  loop-reviewer.md
  loop-eval-runner.md
  deploy-readiness-checker.md
references/
  mission-mode.md
```

Each agent should include:

- trigger conditions;
- allowed inputs;
- read/write permissions;
- output schema;
- validation checks;
- reasoning-level guidance;
- explicit boundaries.

## Product positioning

Mission Mode can be the more memorable product name for the agentic layer:

> Mission Mode turns the end-to-end loop into a scoped agent team: each helper gets the right reasoning depth for the job, every claim needs evidence, and high-impact actions still require human approval.

## Release posture

Treat Mission Mode as a post-cleanup MVP track. First separate private office material from this repository, then add Mission Mode behind clear evals and examples.
