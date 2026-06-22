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
references/deploy-readiness.md   # deploy-readiness rubric and Firebase addendum
references/adapters.md           # Codex/Hermes/Claude/Cursor/AGENTS adapters
references/evaluation.md         # trigger/release/eval guidance
references/report-template.md    # delivery report template
scripts/validate_skill.py        # dependency-free repo validator
.github/workflows/validate.yml   # CI validation
AGENTS.md                        # general coding-agent project instructions
.hermes.md                       # Hermes-specific operating context
handoff/                         # DevBoss/Hermes handoff prompts
research/                        # improvement/research plans
evals/                           # trigger, outcome, and result-log eval artifacts
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

## Why this matters

Modern coding agents are powerful but often fail in predictable ways: they skip discovery, edit before reproducing, claim tests passed without evidence, or treat deployment as a normal final step. `end-to-end-loop` turns those failure modes into explicit gates.

The skill's thesis is simple: an agent should keep looping until the requested code or application work is understood, implemented, verified, tested, security-reviewed when relevant, delivered inside approved scope, and reported with real evidence.

## Validation caveat

The validator intentionally checks that `SKILL.md` frontmatter name matches the folder name. Run validation from a checkout or copied skill folder named exactly `end-to-end-loop`; ad-hoc worktree names such as `end-to-end-loop-todoist-routing` will fail that folder-name check even when the skill contents are valid.

## Evaluation direction

Release readiness depends on more than local validation. The next release train tracks:

- trigger accuracy on should-trigger and near-miss prompts;
- loop compliance across DISCOVER, PLAN, EXECUTE, VERIFY, TEST, DELIVER/DEPLOY, REPORT;
- CAVEMAN compliance for code-producing phases;
- deploy safety under missing-CI, no-approval, and green-CI scenarios;
- evidence quality in final reports;
- reproducible outcome scenarios inspired by SWE-bench-style task resolution.

## Baseline status

Current branch baseline:

- `evals/trigger-cases.json` contains 20 seed trigger cases.
- `evals/outcome-scenarios.md` defines eight manual outcome scenarios covering bugfix, feature, release, deploy, CAVEMAN, planning-only, and DevBoss cron paths.
- `evals/result-log-template.json` provides a structured template for recording scenario results with evidence, acceptance criteria, delivery classification, CI, security, CAVEMAN, and deploy-policy status.
- `evals/results/` contains filled scenario-result logs; the first seed log records a DevBoss cron-maintenance run against Scenario 8.
- `references/evaluation.md` defines the scoring rubric and result-log schema.
- `scripts/validate_skill.py` now enforces baseline eval quality: trigger case count/balance/coverage, outcome scenario count/coverage, result-log template shape, and at least one non-placeholder filled result log.
- Local validation passes when the repository is checked out or copied under a folder named exactly `end-to-end-loop`.
- Public release is still blocked on running the evals, recording results, and polishing install docs/examples.

## Current release posture

Private development. Public release later, after:

- stronger README/docs;
- evaluation metrics;
- market/research findings;
- website support material;
- board-approved release plan.

## Deploy-readiness discipline

Live deploys are treated as a separate readiness decision, not as the natural end
of every repo task. Use `references/deploy-readiness.md` to classify the delivery
target, confirm explicit deploy opt-in, check environment maturity, verify CI/local
validation, review smoke/security evidence, and produce a readiness report when a
deploy is blocked or deferred. For `dev-boss.nl`, the custom domain must be checked
directly after any Firebase Hosting deployment.
