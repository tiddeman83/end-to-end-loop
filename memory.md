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
- 2026-06-21: DevBoss work always uses git worktrees.
- 2026-06-21: The repository remains private for now; public release comes later
  after documentation, metrics, research support, and release readiness improve.
- 2026-06-21: A good `README.md` is required before broader release.
- 2026-06-21: Todoist routing should also be mirrored through Telegram where
  possible so the user can flexibly follow up.
- 2026-06-21: Use a dedicated Todoist project named `DevBoss` with decision-type
  sections for board decisions, release plans, repo/CI, Firebase website, market
  research, and agent tasks.
- 2026-06-21: Firebase is a supporting website for the product/skill, not the
  core product; create separate Todoist tasks for each required credential or
  detail.
- 2026-06-21: The fine-grained GitHub token supplied in chat works for now, but a
  later `gh auth` or other durable access path should replace it.
- 2026-06-23: Self-learning is core skill behavior: target repos may keep compact
  `.end-to-end-loop/` memory/result logs, CAVEMAN ULTRA style, privacy-safe only.
- 2026-06-23: First public pre-release requires Tijmen's explicit repo review and
  approval before tagging.
- 2026-06-23: GitHub pushes should include Copilot findings when an authenticated
  Copilot/gh-copilot path exists; otherwise log the unavailability honestly.

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
- 2026-06-23: Static-site dry-run evals can exercise the loop safely with Python
  HTMLParser checks for parseability, duplicate IDs, anchor targets, forms,
  scripts, external links, and embedded assets before any implementation/deploy.
- 2026-06-23: WordPress scaffold dry-runs without PHP/WordPress access should
  combine JS syntax checks, HTML/asset integrity, local HTTP smoke, refined
  credential scans, and explicit PHP-lint blocker reporting.
- 2026-06-23: Broad secret scans can flag safe documentation references to tokens;
  refine credential-like patterns before classifying findings as real secrets.
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
