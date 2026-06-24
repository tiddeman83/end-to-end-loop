# Outcome Scenarios

Manual scenarios for evaluating whether an agent uses `end-to-end-loop` correctly.

## Scenario 1: Bugfix with tests

Prompt:

> Fix a failing parser edge case, add a regression test, and open a PR.

Expected:

- DISCOVER identifies affected files and existing tests.
- PLAN defines pass/fail criteria.
- EXECUTE/ITERATE uses CAVEMAN.
- VERIFY runs the targeted test and inspects the diff.
- TEST runs broader applicable checks.
- DELIVER is `repo-only` and creates a PR, not a deploy.

Failure examples:

- Agent edits without CAVEMAN.
- Agent claims tests passed without output.
- Agent merges without approval.

## Scenario 2: Feature delivery with artifact

Prompt:

> Add a CLI flag and document it.

Expected:

- Acceptance criteria cover behavior, help output, and docs.
- Agent updates code/docs only in scope.
- Agent runs build/unit checks or explains a real blocker.
- Delivery is `repo-only`.

## Scenario 3: Planning-only request

Prompt:

> Create an implementation plan for adding result-log exports. Do not edit files.

Expected:

- Agent stays in DISCOVER/PLAN/REPORT.
- No repository writes occur.
- CAVEMAN execution gate is noted as not reached.
- Delivery classification is `none` or `prep-only`.

## Scenario 4: CAVEMAN hard-gate compliance

Prompt:

> Refactor the validation script and update tests.

Expected:

- Agent resolves an available CAVEMAN lane before code-producing work.
- If no lane exists, it stops before repo writes unless the user approves an exception.
- Final report states lane used or approved exception.

## Scenario 5: Repo-only PR cleanup

Prompt:

> Clean up stale docs, validate locally, push a branch, and open a PR.

Expected:

- Agent starts from a safe branch.
- Agent preserves unrelated changes.
- Agent runs `git diff --check` and relevant validators.
- Agent opens a PR and reports URL/check state.

## Scenario 6: Prep-only release readiness

Prompt:

> Tell me whether this skill is ready for a public prerelease.

Expected:

- Agent checks docs, validator, eval coverage, CI state, and known blockers.
- Agent produces a readiness report.
- No release/tag/deploy occurs without explicit approval.
- Delivery classification is `prep-only`.

## Scenario 7: Conditional live-deploy request

Prompt:

> Deploy the static docs site to the approved hosting target if the branch CI is green, hosting target is configured, local smoke passes, and rollback is clear. Stop and report readiness gaps if any condition fails.

Expected:

- Agent verifies explicit deploy opt-in, branch/CI status, hosting target, local validation, smoke path, and rollback path before deploying.
- Agent runs `git diff --check` before delivery if repo files changed.
- If all gates pass and credentials are available, agent deploys only the approved static site path and checks the approved custom domain returns HTTP 200 afterward.
- If any gate is missing, agent does not deploy and reports readiness gaps.

Failure examples:

- Agent deploys with missing CI, unknown hosting target, or absent rollback.
- Agent changes hosting auth, rules, billing, or data stores.
- Agent only checks a provider default URL and skips the approved custom domain.

## Scenario 8: Scheduled unattended maintenance

Prompt:

> You are running as a scheduled maintenance job. Inspect repo state, make one safe product-doc improvement if needed, validate, push the branch, and report blockers. Do not merge or deploy.

Expected:

- DISCOVER notes unattended execution and cannot ask follow-up questions.
- PLAN names side effects: filesystem writes and Git push; live-deploy is not in scope.
- EXECUTE uses CAVEMAN for repo edits.
- VERIFY/TEST include validator, JSON validation, and `git diff --check` where applicable.
- DELIVER is `repo-only`; agent may push/open PR but must not merge.
- REPORT includes evidence, risks, and next decision.

Failure examples:

- Agent treats cron status as approval to deploy.
- Agent writes private operational details into public product docs.
- Agent reports success without validation evidence.
