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
- execute code-producing work only through a CAVEMAN-compatible lane that is installed and update-checked;
- route work by complexity to cheaper/faster models or scripts where safe;
- consider helper agents for parallelizable discovery, build, review, tests, and reporting;
- verify with observed evidence, not confidence;
- run smoke tests and security review;
- deliver or deploy only inside the approved scope;
- report outcome, evidence, CI/test state, limitations, and rollback notes.

## Non-negotiables

- **CAVEMAN is mandatory** for code-producing execution and iteration.
- **No live deploy by default.** Live deploy requires explicit user opt-in, project maturity, applicable green CI, rollback, credentials approval, smoke tests, and security review.
- **Observed evidence required.** No “green” claims without command output, test results, diff review, manual verification, CI status, or documented approval.
- **Portable core.** Tool-specific behavior lives in `references/adapters.md`.
- **Lean by default.** Minimize context, tool calls, wall time, and model cost without weakening gates.

## Repository layout

```text
SKILL.md                         # production skill core
references/phase-checklists.md   # phase gates and summaries
references/test-and-security.md  # smoke/security/side-effect gates
references/deploy-readiness.md   # deploy-readiness rubric and hosting/custom-domain gates
references/adapters.md           # Codex/Hermes/Claude/Cursor/AGENTS adapters
references/evaluation.md         # trigger/release/eval guidance
references/self-learning.md      # per-repo compact memory/result-log rules
references/report-template.md    # delivery report template
references/mission-mode.md       # optional helper-agent/model-routing layer
scripts/validate_skill.py        # dependency-free repo validator
.github/workflows/validate.yml   # CI validation
AGENTS.md                        # general coding-agent project instructions
.hermes.md                       # minimal Hermes adapter context for this product repo
research/                        # improvement/research plans
evals/                           # trigger, outcome, and result-log eval artifacts
paper.md                         # shareable rationale/research draft
memory.md                        # product decisions and sanitized learnings
```

## Validate locally

```bash
git fetch origin --prune          # when a remote/upstream is configured
python3 scripts/validate_skill.py .
git diff --check
```

If validating from a worktree whose directory name differs from `end-to-end-loop`,
copy or archive the tree into a temporary folder named `end-to-end-loop` first.

CI runs the same validator through `.github/workflows/validate.yml`.

## Install

For generic Agent Skills-compatible tools, install the full package with:

```bash
bash scripts/install.sh
```

The script installs `SKILL.md`, `references/*.md`, and `agents/openai.yaml` under `~/.agents/skills/end-to-end-loop/`.

For a local Hermes profile, copy this repository or the skill folder under:

```text
~/.hermes/skills/software-development/end-to-end-loop/
```

Install/update the companion CAVEMAN skills in the same active profile before use:

- `caveman-ultra`
- `caveman-code`
- a reviewer/delegation lane such as `cavecrew` or configured equivalent

For repo-backed installs, fetch and compare against the upstream branch, validate
from a folder named `end-to-end-loop`, then sync the installed copy:

```bash
git fetch origin --prune
tmp=$(mktemp -d)
cp -a /path/to/end-to-end-loop "$tmp/end-to-end-loop"
rm -rf "$tmp/end-to-end-loop/.git"
python3 "$tmp/end-to-end-loop/scripts/validate_skill.py" "$tmp/end-to-end-loop"
```

After validation, copy/sync into the active Hermes profile only, then start a
fresh Hermes session or reload skills. Use `skills_list()`/`skill_view()` to
verify `end-to-end-loop`, `caveman-ultra`, `caveman-code`, and `cavecrew` or a
configured reviewer lane. In this project, the repo itself is the source of truth;
installed local copies should be refreshed from GitHub after validation.

## Maintenance model

This repository is maintained as a public-facing product/tool repository:

- repo work uses worktrees, branches, commits, validation, and CI;
- release decisions require explicit maintainer/repository-owner approval;
- website or hosting work is support/marketing infrastructure, not the core skill;
- the repo remains private until the skill is sufficiently justified by docs, metrics, evals, install examples, and release readiness.

Private operational automation, office workflows, dashboard coordination, and task-routing runbooks belong outside this product package.

## Why this matters

Modern coding agents are powerful but often fail in predictable ways: they skip discovery, edit before reproducing, claim tests passed without evidence, or treat deployment as a normal final step. `end-to-end-loop` turns those failure modes into explicit gates.

The skill's thesis is simple: an agent should keep looping until the requested code or application work is understood, implemented, verified, tested, security-reviewed when relevant, delivered inside approved scope, and reported with real evidence.

## Self-learning memory

When used inside a target repository, the skill may maintain compact per-repo memory under `.end-to-end-loop/`:

- `memory.md` for sanitized durable repo learnings;
- `memory.local.md` for private/local-only facts;
- `results/*.json` for per-run result logs.

Memory uses CAVEMAN ULTRA compact style: `FACT`, `CMD`, `BLOCK`, `PREF`, `RISK`, `FIX`, `AVOID`, and `NEXT`. It must exclude secrets, bulky transcripts, unverified guesses, and non-durable noise. See `references/self-learning.md`.

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
- `evals/outcome-scenarios.md` defines eight manual outcome scenarios covering bugfix, feature, release, deploy, CAVEMAN, planning-only, and scheduled unattended maintenance paths.
- `evals/result-log-template.json` provides a structured template for recording scenario results with evidence, acceptance criteria, delivery classification, CI, security, CAVEMAN, and deploy-policy status.
- `evals/results/` contains filled scenario-result logs and sanitized examples for release-readiness evaluation.
- `references/evaluation.md` defines the scoring rubric and result-log schema.
- `references/self-learning.md` defines per-repo compact memory, result logs, privacy controls, and learning promotion rules.
- `research/traction-plan.md` defines the pre-release traction strategy, benchmark assets, launch sequence, and Tijmen review gate.
- `scripts/validate_skill.py` now enforces baseline eval quality: trigger case count/balance/coverage, outcome scenario count/coverage, result-log template shape, telemetry artifacts, Mission Mode coverage, install assets, and at least one non-placeholder filled result log.
- Local validation passes when the repository is checked out or copied under a folder named exactly `end-to-end-loop`.
- `v0.1.0-alpha.1` release readiness is gated on the release-candidate branch being merged to `main`, exact-SHA CI success, no existing tag/release, and prerelease notes that call out remaining beta gaps.

## Current release posture

Alpha/private prerelease readiness. First prerelease requires:

- exact-SHA validator and CI success on `main`;
- release notes that distinguish included alpha capabilities from unmerged future work;
- no unresolved secret/privacy findings;
- Tijmen's explicit release approval before any public-facing or externally distributed tag.

Public/stable release remains later, after:

- stronger README/docs;
- evaluation metrics;
- market/research findings;
- website support material;
- maintainer-approved release plan;
- explicit repository-owner review and approval before any first public pre-release tag.

## Deploy-readiness discipline

Live deploys are treated as a separate readiness decision, not as the natural end
of every repo task. Use `references/deploy-readiness.md` to classify the delivery
target, confirm explicit deploy opt-in, check environment maturity, verify CI/local
validation, review smoke/security evidence, and produce a readiness report when a
deploy is blocked or deferred. For hosted docs or marketing sites, the approved custom domain must be checked directly after any hosting deployment.
