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

Status: research complete; awaiting user decisions

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

Resolved / superseded decisions:
- First-class targets for now: Codex, Hermes, Claude Code, Cursor, and AGENTS.md.
- Architecture: canonical universal `SKILL.md` core plus adapter references.
- User approval: live deploy and high-impact side effects require explicit approval
  or the active tool's approval flow.
- CAVEMAN is mandatory for code-producing phases; adapters provide portability.

Research summary:
- Agent Skills is now an open folder format centered on `SKILL.md`, with required
  `name` and `description`, optional `scripts/`, `references/`, and `assets/`, and
  progressive disclosure as a core design constraint.
- Codex, Claude Code, and Cursor all support skills or similar rule formats, but
  they differ in discovery paths, frontmatter extensions, invocation control, and
  permission models.
- AGENTS.md is the broadest cross-agent repository instruction format, but it is
  less structured than a skill and is best treated as a compatibility adapter or
  short project-level bridge.
- Cursor distinguishes rules from skills: rules can be always-on, path-scoped,
  manual, or agent-selected; Cursor also supports the Agent Skills standard and
  loads from `.agents/skills`, `.cursor/skills`, and compatibility paths.
- Claude Code adds fields for invocation control, subagent execution, allowed tools,
  and skill visibility. It treats skills as prompt-based procedures and supports
  isolated evaluation workflows.
- Codex expects focused skills with concise descriptions, optional UI metadata, and
  repo/user/admin/system scopes. Its docs emphasize trigger precision and local
  authoring versus plugin distribution.
- Hermes Agent is relevant as a compatibility target because public material says it
  auto-generates skills, has persistent memory, isolated subagents, Python RPC
  scripts, and multiple sandbox backends. Its concrete skill file conventions need
  confirmation from the user or Hermes docs.

Safety implications:
- Recent research treats `SKILL.md` as operational text, not passive documentation.
  Natural-language descriptions can influence discovery, selection, and governance.
- A universal skill should avoid manipulative trigger phrasing, trust claims, and
  broad "always use me" language unless justified by explicit scope.
- The skill should classify side effects and require approval for privileged,
  destructive, external, networked, credentialed, or production-impacting actions.
- The current CAVEMAN execution contract needs adapters for portability, but remains
  part of the universal core because the user made it a hard requirement.
- The current deploy phase should be generalized to "deliver or hand off" with a
  stricter deployment approval gate.

Proposed five-iteration roadmap:

1. Research and architecture baseline
   - Capture sources, risks, and target compatibility requirements.
   - Decide whether the canonical artifact is a single skill or core-plus-adapters.
   - Output: this research log, paper draft, user questions.

2. Universal core rewrite
   - Rewrite `SKILL.md` to remove tool-specific assumptions from the core.
   - Define the loop as a portable behavioral contract with explicit scaling rules.
   - Output: universal `SKILL.md` v1 and updated phase checklists.

3. Safety and permissions model
   - Add side-effect taxonomy, approval gates, sandbox assumptions, rollback rules,
     and secret-handling requirements.
   - Output: revised `references/test-and-security.md` and safety acceptance checks.

4. Adapter strategy
   - Add concise adapters for Codex, Claude Code, Cursor, AGENTS.md, and Hermes.
   - Decide packaging layout and what belongs in the final distributable versus the
     development repository.
   - Output: adapter references or generated target files.

5. Evaluation and hardening
   - Create trigger evals, task evals, should-not-trigger cases, and regression
     checks for instruction bloat, conflicting instructions, and unsafe autonomy.
   - Output: eval specification and results, with revisions based on failures.

6. Paper and release candidate
   - Consolidate research claims, limitations, and design rationale.
   - Prepare a clean shareable package and a publication-ready `paper.md`.
   - Output: release candidate commit and final report.

Critical questions for the user before Iteration 2:
- Which surfaces are non-negotiable for v1: Codex, Hermes, Claude Code, Cursor,
  AGENTS.md, or another tool?
- How strict should future releases be when a tool lacks any CAVEMAN-compatible
  execution lane?
- Should "DEPLOY" mean actual deployment by the agent, or should the default be
  "prepare, verify, and ask for explicit approval before any live deploy"?
- Do you prefer a single canonical `SKILL.md` that is broadly compatible, or a
  canonical core plus generated/adapted files per agent ecosystem?
- For Hermes specifically, can you provide the expected skill/rules format if it has
  one, or should I infer compatibility from the public Hermes Agent capabilities?

Verification:
- GitHub repository created and initial commit pushed.
- Internet research complete for the first pass.
- Skill folder validates with the skill-creator `quick_validate.py` script after
  running it in a temporary venv with `PyYAML`.

## Sources Consulted

- Agent Skills overview: https://agentskills.io/home
- Agent Skills specification: https://agentskills.io/specification
- Agent Skills best practices: https://agentskills.io/skill-creation/best-practices
- Agent Skills description optimization: https://agentskills.io/skill-creation/optimizing-descriptions
- Agent Skills evaluation guidance: https://agentskills.io/skill-creation/evaluating-skills
- Agent Skills scripts guidance: https://agentskills.io/skill-creation/using-scripts
- OpenAI Codex Agent Skills: https://developers.openai.com/codex/skills
- OpenAI Codex sandboxing: https://developers.openai.com/codex/concepts/sandboxing
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code settings and permissions: https://code.claude.com/docs/en/settings
- Cursor rules: https://cursor.com/docs/rules.md
- Cursor skills: https://cursor.com/docs/skills.md
- Cursor agent security: https://cursor.com/docs/agent/security.md
- AGENTS.md open format: https://agents.md/
- Hermes Agent: https://hermes-agent.nousresearch.com/
- Saha et al., "Under the Hood of SKILL.md": https://arxiv.org/abs/2605.11418
- Ouyang et al., "SkCC": https://arxiv.org/abs/2605.03353
- dos Santos et al., "Configuration Smells in AGENTS.md Files":
  https://arxiv.org/abs/2606.15828

### Iteration 2 - Production Candidate and Hermes Handoff

Status: complete and pushed

User decisions:
- CAVEMAN is a hard requirement, not an optional preference.
- DEPLOY must be conditional per task. The user must explicitly opt in before live
  deploy can run.
- Live deploy also requires project maturity and an applicable CI pipeline.
- Skill architecture choice is delegated to the assistant. Decision: use a
  scalable core-plus-adapters model.
- Hermes target follows Nous Research Hermes Agent conventions; no extra private
  convention supplied.
- Repo must be ready for later Hermes handoff to a virtual office named DevBoss.

Design decisions:
- Rewrote `SKILL.md` as the universal production core.
- Moved tool-specific details into `references/adapters.md`.
- Added `references/evaluation.md` for trigger/outcome/release evals.
- Added `scripts/validate_skill.py`, a dependency-free validator for local and CI
  checks.
- Added GitHub Actions workflow `.github/workflows/validate.yml`.
- Added `AGENTS.md` and `.hermes.md` so Hermes and other coding agents get repo
  context without loading the whole skill into every prompt.
- Added Hermes handoff files under `handoff/`:
  - `hermes-devboss-brief.md`
  - `hermes-market-research-prompt.md`
- Added `research/improvement-plan.md` as the second-goal research/improvement plan.
- Added `evals/trigger-cases.json` as the first eval seed.
- Added `agents/openai.yaml` for Codex UI metadata.

Hermes research updates:
- Hermes docs state that skills live in `~/.hermes/skills/` and are compatible with
  the Agent Skills open standard.
- Hermes supports external skill directories via `skills.external_dirs`.
- Hermes supports `skills.write_approval`; this should be enabled before Hermes
  modifies this repo or installed skill copies.
- Hermes supports context files including `.hermes.md`, `AGENTS.md`, `CLAUDE.md`,
  and Cursor rule files, with `.hermes.md` highest priority.
- Hermes includes messaging gateways, persistent memory, scheduled automations,
  subagents, tool gateway, skills hub, and sandbox backends suitable for DevBoss.

Acceptance criteria for this iteration:
- [x] Universal core keeps CAVEMAN as a hard gate.
- [x] Live deploy requires user opt-in, project maturity, applicable CI, rollback,
      credentials approval, smoke tests, and security review.
- [x] CI validation exists in the repo.
- [x] Hermes handoff includes DevBoss office, named agents, Todoist routing, and
      Firebase website brief.
- [x] New improvement/research plan exists.
- [x] Market research prompt for Hermes exists.
- [x] Local validation passes.
- [x] Diff review passes.
- [x] Changes committed and pushed to GitHub.

Verification:
- `python3 scripts/validate_skill.py .` -> pass.
- `quick_validate.py` from `skill-creator` -> pass.
- YAML frontmatter / config parse -> pass.
- `python3 -m json.tool evals/trigger-cases.json` -> pass.
- `git diff --check` -> pass.
- Commit `38f63c4` pushed to `main`.
- GitHub Actions `Validate skill` run `27903436563` -> success.

Sources added:
- Hermes Agent docs: https://hermes-agent.nousresearch.com/docs
- Hermes Skills System:
  https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Hermes Context Files:
  https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- Hermes Security:
  https://hermes-agent.nousresearch.com/docs/user-guide/security

### Iteration 3 - DevBoss Todoist Routing and README Baseline

Status: in progress from Hermes handoff

User decisions captured from Todoist:
- `tiddeman83/end-to-end-loop` is the preferred source of truth above local copies.
- Development continues in the private repo for now.
- DevBoss work always uses worktrees.
- A strong `README.md` is required before broader release.
- Public release is later, after the skill is better supported by documentation,
  metrics, and release readiness.
- Firebase is a supporting website for the skill/product. The user will create the
  Firebase environment; Hermes should create a separate task for each credential or
  data item needed.
- DevBoss decisions should be routed through Todoist and mirrored through Telegram
  when possible.
- Use a dedicated Todoist project named `DevBoss` with sections by decision/work
  type.
- The currently shared fine-grained GitHub token works, but should later be replaced
  by `gh auth` or another durable access path.

Changes made in this iteration:
- Created `README.md` as a concise repo/product entry point.
- Updated `memory.md` with the newly settled decisions.
- Updated `.hermes.md` to watch `DevBoss ::` Todoist tasks and mirror decisions over
  Telegram where possible.
- Updated `handoff/hermes-devboss-brief.md` with the dedicated `DevBoss` Todoist
  project structure and `DevBoss ::` task prefix.
- Created Todoist project `DevBoss` with sections: `Board Decisions`,
  `Release Plans`, `Repo & CI`, `Firebase Website`, `Market Research`,
  `Agent Tasks`, and `Done / Archive`.
- Created Firebase prerequisite tasks in the `Firebase Website` section.
- Updated the local Hermes poller to run every 10 minutes and watch active and
  recently completed DevBoss tasks, including `DevBoss ::` tasks.

Acceptance criteria:
- [x] Todoist has a dedicated DevBoss project and decision/work sections.
- [x] Firebase prerequisite questions are individual Todoist tasks.
- [x] Polling cadence is 10 minutes.
- [x] Poller recognizes `DevBoss :: {description}` tasks.
- [x] Repo documents the new routing and private-release decisions.
- [x] README baseline exists.
- [x] Local validation passes.
- [x] Diff review passes.
- [ ] Changes committed and pushed.

Verification:
- `python3 scripts/validate_skill.py .` via basename-matching validation copy -> pass.
- `git diff --check` -> pass.
- Diff review -> pass; changes are docs/routing only.
- CI after push.

### Iteration 4 - DevBoss Overnight Sprint Kickoff

Date: 2026-06-21
Status: in progress on branch `devboss/todoist-routing-20260621203251`

DevBoss office was activated for an overnight improvement sprint. Initial agents/research streams:

- Research: agentic coding loops, verification ladders, SWE-bench-style metrics, ReAct/Reflexion/Self-Refine/SWE-agent patterns.
- Operations: safe virtual-office workflow with separated GM, architecture, implementation, CI, security, release governance, novice testing, research, and Firebase roles.
- Repo inspection: README, evaluation protocol, paper consistency, improvement backlog, and Hermes handoff maturity.

Changes made in this pass:

- Expanded README with purpose, validation caveat, and evaluation direction.
- Rewrote `references/evaluation.md` into a concrete scoring rubric and result-log schema.
- Expanded `evals/trigger-cases.json` with near-miss, ambiguous, deploy-block, and CAVEMAN-block scenarios.
- Added overnight priority order and non-safe-without-approval boundaries to `research/improvement-plan.md`.
- Fixed `paper.md` finding numbering, eval artifact naming, and Hermes/validation status language.
- Added first-day/overnight operating mode to `handoff/hermes-devboss-brief.md`.

Validation target:

- Validate from a folder named `end-to-end-loop` because the validator intentionally enforces folder-name equality.
- Run `git diff --check`.

Next expected output:

- Commit/push docs/eval improvement branch.
- Continue scheduled overnight DevBoss sprint every two hours.
- Report site progress in the hourly heartbeat; no live Firebase deploy without explicit approval.
