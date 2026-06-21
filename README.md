# End-to-End Loop

A portable Agent Skill for taking software work from intent to verified delivery:

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE -> TEST -> DELIVER/DEPLOY -> REPORT
```

The skill is designed for Codex, Hermes Agent, Claude Code, Cursor, and AGENTS.md-compatible coding agents.

## What it does

`end-to-end-loop` gives agents a disciplined delivery contract:

- discover the real goal and side effects before acting;
- plan with pass/fail acceptance criteria;
- execute code-producing work only through a CAVEMAN-compatible lane;
- verify with observed evidence, not confidence;
- run smoke tests and security review;
- deliver or deploy only inside the approved scope;
- report outcome, evidence, CI/test state, limitations, and rollback notes.

## Non-negotiables

- **CAVEMAN is mandatory** for code-producing execution and iteration.
- **No live deploy by default.** Live deploy requires explicit user opt-in, project maturity, applicable green CI, rollback, credentials approval, smoke tests, and security review.
- **Observed evidence required.** No “green” claims without command output, test results, diff review, manual verification, CI status, or documented approval.
- **Portable core.** Tool-specific behavior lives in `references/adapters.md`.

## Repository layout

```text
SKILL.md                         # production skill core
references/phase-checklists.md   # phase gates and summaries
references/test-and-security.md  # smoke/security/side-effect gates
references/adapters.md           # Codex/Hermes/Claude/Cursor/AGENTS adapters
references/evaluation.md         # trigger/release/eval guidance
references/report-template.md    # delivery report template
scripts/validate_skill.py        # dependency-free repo validator
.github/workflows/validate.yml   # CI validation
AGENTS.md                        # general coding-agent project instructions
.hermes.md                       # Hermes-specific operating context
handoff/                         # DevBoss/Hermes handoff prompts
research/                        # improvement/research plans
paper.md                         # shareable rationale/research draft
memory.md                        # settled decisions
```

## Validate locally

```bash
python3 scripts/validate_skill.py .
git diff --check
```

CI runs the same validator through `.github/workflows/validate.yml`.

## Install in Hermes

For a local Hermes profile, copy this repository or the skill folder under:

```text
~/.hermes/skills/software-development/end-to-end-loop/
```

Then start a fresh Hermes session or reload skills. In this project, the repo itself is the source of truth; installed local copies should be refreshed from GitHub after validation.

## DevBoss maintenance model

This repository is maintained through a virtual office called **DevBoss**:

- Tijmen is Supervisory Board chair and approves releases.
- Board/release decisions route through Todoist and Telegram where possible.
- Repo work uses worktrees, branches, commits, validation, and CI.
- Firebase website work is support/marketing infrastructure, not the core skill.
- The repo remains private until the skill is sufficiently justified by docs, metrics, evals, and release readiness.

See `handoff/hermes-devboss-brief.md` for the full operating model.

## Current release posture

Private development. Public release later, after:

- stronger README/docs;
- evaluation metrics;
- market/research findings;
- website support material;
- board-approved release plan.
