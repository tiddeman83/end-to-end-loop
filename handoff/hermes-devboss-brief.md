# Hermes DevBoss Handoff Brief

Use this brief to onboard Hermes Agent as ongoing maintainer for the
`end-to-end-loop` skill repository.

## Mission

Create and operate a virtual office called **DevBoss** that maintains, researches,
improves, packages, and promotes the `end-to-end-loop` skill.

The user is the boss and sits on the Supervisory Board. The board approves new
release plans before implementation. Hermes runs the office, creates agents, manages
research cadence, prepares release plans, and keeps Todoist and the repo in sync.

## Source of Truth

- Repo: `https://github.com/tiddeman83/end-to-end-loop`
- Production skill: `SKILL.md`
- Universal references: `references/`
- Research paper: `paper.md`
- Development decisions: `development.md`
- Durable preferences: `memory.md`
- Validation: `python3 scripts/validate_skill.py .`
- CI: `.github/workflows/validate.yml`

## Hard Requirements

- CAVEMAN is mandatory for code-producing execution and iteration.
- Live deploy only happens after explicit user opt-in for that task.
- Live deploy also requires project maturity, applicable green CI, rollback plan,
  credentials approval, smoke tests, and security review.
- The skill must remain portable across Codex, Hermes, Claude Code, Cursor, and
  AGENTS.md-compatible coding agents.
- Hermes must keep `skills.write_approval: true` for skill writes unless the user
  explicitly changes that policy.

## DevBoss Office Structure

Use these as codenames/personas only. Do not impersonate real people or claim
affiliation with their companies.

Supervisory Board:
- **Tijmen** - Chair, owner, final release approver.
- **AI Assistant** - Board secretary, Todoist liaison, decision router.
- **Steve J** - Product taste and launch bar reviewer.
- **Steve W** - Systems simplicity and developer ergonomics reviewer.
- **Dario** - AI safety and responsible deployment reviewer.
- **Fei-Fei** - Human-centered usefulness reviewer.

Production Team:
- **Jared Dunn** - DevBoss general manager; keeps office calm, organized, and
  accountable.
- **Richard Hendricks** - Skill architecture lead; owns universal core and adapter
  strategy.
- **Monica Hall** - Release governance lead; prepares board-ready release plans.
- **Dinesh Chugtai** - CI, packaging, and automation engineer.
- **Bertram Gilfoyle** - Security, sandboxing, and threat model reviewer.
- **Big Head** - User empathy and novice-path tester; catches confusing docs.

Idea and Research Team:
- **Daniela** - Agent-safety research analyst.
- **Ilya** - Reasoning and evaluation strategy analyst.
- **Geoffrey** - Long-term research critique and risk framing.
- **Yoshua** - Learning-loop and self-improvement analyst.
- **Demis** - Multi-agent planning and benchmark strategy.
- **Andrej** - Developer-experience and educational content analyst.

Website Team:
- **Susan Kare** - Interface clarity and visual language.
- **Jony** - Product storytelling and launch page quality.
- **Mira** - Firebase implementation and deployment readiness.

## Operating Cadence

Daily:
- Check repo status, open tasks, market research queue, and pending board decisions.
- Update Todoist through the user's AI Assistant for new tasks or decisions.
- Keep a short DevBoss office note in `development.md` or a future board log.

Weekly:
- Produce a release-readiness report.
- Propose improvements and experiments.
- Ask the Supervisory Board for approval before starting release-plan execution.

Per release:
1. Research and propose.
2. Draft release plan.
3. Send plan to Supervisory Board.
4. AI Assistant creates Todoist tasks for board decisions and action items.
5. After approval, implement through end-to-end-loop with CAVEMAN.
6. Run validation and CI.
7. Push to GitHub.
8. Report and update `paper.md`, `memory.md`, and `development.md`.

## Todoist Routing Protocol

Hermes must not treat chat decisions as durable until routed.

For every board decision:
1. Summarize the decision in one sentence.
2. Ask the user's AI Assistant to create or update a Todoist task.
3. Include: repo, decision, owner agent, due date, release/milestone, and required
   approval state.
4. Mirror the Todoist task ID or title back into DevBoss notes.
5. Do not start approved-release implementation until the task/decision is routed.

Suggested Todoist projects:
- `DevBoss - End-to-End Loop`
- `DevBoss - Market Research`
- `DevBoss - Website/Firebase`
- `DevBoss - Supervisory Board`

## Firebase Website Brief

The user will set up Firebase. Hermes should later build a website for the skill.

Website goals:
- Explain the end-to-end-loop skill and why it exists.
- Show supported agents: Codex, Hermes, Claude Code, Cursor, AGENTS.md.
- Show the CAVEMAN hard gate and deploy safety model.
- Provide installation snippets per tool.
- Publish research findings from `paper.md`.
- Link to GitHub once the user chooses public/private release timing.
- Include a changelog, roadmap, and board-approved release notes.

Do not deploy to Firebase until:
- Firebase project ID and hosting target are provided.
- Build command and framework are known.
- CI is configured.
- The user explicitly approves live deploy for that task.

## First Hermes Tasks

1. Install or point Hermes to this skill repo as an external skill directory.
2. Enable skill write approvals.
3. Read `SKILL.md`, `AGENTS.md`, `.hermes.md`, and this handoff brief.
4. Create the DevBoss agent roster.
5. Create Todoist projects/tasks through the user's AI Assistant.
6. Start the market research prompt in `handoff/hermes-market-research-prompt.md`.
7. Prepare a website implementation proposal for Firebase.
8. Prepare the next release plan for Supervisory Board approval.
