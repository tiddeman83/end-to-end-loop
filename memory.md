# End-to-End Loop Skill Memory

This file captures durable learnings from the discussion and research so future
iterations do not re-litigate settled points.

## User Intent

- The user wants the existing end-to-end-loop skill developed into a safe, mature,
  shareable skill.
- The user wants at least five iterations, with the assistant leading research and
  planning.
- Each iteration must be committed and pushed to GitHub.
- The repository must remain private for now.
- The skill must work beyond Codex, including Hermes and other agent/coding tools.
- The assistant should ask critical questions and request proposals from the user at
  each iteration.

## Working Assumptions

- The canonical skill should be written in English to maximize portability and future
  sharing.
- Development artifacts can live in the repository, but the final packaged skill may
  need to exclude non-operational documents depending on the target ecosystem.
- Safety should be modeled as explicit permission, scope, verification, and rollback
  gates instead of relying on agent judgment alone.

## Decisions

- 2026-06-21: Repository name chosen as `tiddeman83/end-to-end-loop`.
- 2026-06-21: Repository created as private.
- 2026-06-21: Initial repository state pushed to GitHub.
- 2026-06-21: CAVEMAN is a hard requirement for code-producing phases.
- 2026-06-21: Live deploy is conditional per task and requires explicit user opt-in,
  project maturity, applicable green CI, rollback, credentials approval, smoke
  tests, and security review.
- 2026-06-21: Architecture decision: use a universal `SKILL.md` core plus
  adapter/reference files for Codex, Hermes, Claude Code, Cursor, and AGENTS.md.
- 2026-06-21: Hermes handoff should use Nous Research Hermes Agent conventions,
  including skills, context files, external dirs, write approval, subagents,
  scheduled automation, and sandbox backends.
- 2026-06-21: DevBoss virtual office is the intended Hermes operating model.
- 2026-06-21: The user sits on the Supervisory Board and approves new release plans.
- 2026-06-21: Board decisions should route through the user's AI Assistant into
  Todoist and then back into DevBoss notes.

## Questions To Revisit

- Define Hermes compatibility requirements from concrete Hermes conventions.
- Define exact CAVEMAN-compatible adapters for each target tool.
- Decide how strict the deploy gate should be for agents with limited permission
  models.

## Research Learnings

- Agent Skills use progressive disclosure: metadata first, full `SKILL.md` only
  when activated, references/scripts/assets only as needed.
- The `description` field is operational because it controls trigger behavior. It
  must be precise enough to avoid both false negatives and false positives.
- Cursor, Claude Code, and Codex increasingly converge on `SKILL.md`, but each adds
  tool-specific fields. The universal core should avoid depending on those fields.
- AGENTS.md is useful as broad compatibility glue for repository-level instructions,
  but it is not a full skill format and lacks structured invocation controls.
- Public Hermes Agent material confirms relevant capabilities but not enough file
  format detail. Treat Hermes as a first-class target after user confirmation.
- Research on SKILL.md attacks and AGENTS.md smells supports a conservative design:
  avoid context bloat, conflicting instructions, broad triggers, manipulative
  trust/security claims, and unsafe state-changing behavior.
- A portable delivery loop should distinguish "deliverable prepared" from "live
  deployment executed" and require explicit approval for high-impact side effects.
- Hermes supports Agent Skills, `~/.hermes/skills/`, external skill directories,
  context files, write approval for skills, subagents, scheduled automation,
  messaging gateways, and hardened sandbox backends.
- Hermes should receive both a project context file and a handoff prompt so it can
  run long-lived maintenance without needing this conversation.

## DevBoss Naming Constraints

- Agent names can use Silicon Valley characters, Apple-related codenames, Anthropic
  and AI researcher-inspired codenames, but must be treated as codenames/personas.
- Agents must not impersonate real people or claim affiliation with their companies.

## DevBoss Website / Firebase Decisions

- 2026-06-21: The support website should be a public information site for the skill,
  not a private cockpit.
- 2026-06-21: Desired public domain is `dev-boss.nl`.
- 2026-06-21: The site should explain the skill's purpose and operation to AI
  researchers and AI users seeking efficient work methods.
- 2026-06-21: Positioning phrase to preserve: the skill is a self-learning for-loop
  that keeps running until a code component or application is completed safely and
  tested.
- 2026-06-21: Visitor statistics are wanted, but backend/admin access should be
  restricted to `tijmenbaas83@gmail.com`.
- 2026-06-21: Firebase deployment is preferred later, but no deploy is approved in
  the current overnight sprint.
- 2026-06-21: Observed status: `https://tijmensassistant.web.app` is live for TinTin,
  while `https://dev-boss.nl` has a certificate hostname mismatch and is not yet a
  showable DevBoss URL.

## DevBoss Metrics To Track

- Loop completion rate against acceptance criteria.
- Validation pass rate: local validator, `git diff --check`, CI, and task-specific
  checks.
- Iteration count before VERIFY/TEST green.
- Safety gate hits for deploy, credentials, destructive actions, network writes, and
  external state changes.
- CAVEMAN compliance for code-producing phases.
- Context freshness: Todoist/repo/project context read before edits.
- PR readiness: branch pushed, PR created or manual PR URL supplied, CI observed.
