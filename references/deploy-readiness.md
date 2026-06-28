# Deploy readiness rubric

Use this reference whenever a task asks for deployment, site publication, release readiness, hosting work, or production/staging changes. It turns the `live-deploy` policy in `SKILL.md` into an auditable pass/fail checklist.

A deployment is **ready** only when every required item below is green or has an explicit user-approved waiver recorded in the final report. If any required item is red and not waived, do not deploy; deliver a readiness report instead.

## 1. Classification gate

| Question | Ready answer |
| --- | --- |
| What is the delivery target? | `none`, `repo-only`, `prep-only`, or `live-deploy` is named. |
| Did the user explicitly request live deploy for this task? | Yes, in the current task or an unambiguous standing instruction. |
| What will change externally? | Domain, hosting target, data, API, or service impact is listed. |
| What is out of scope? | Destructive operations, data deletion, public release, auth/rules changes, and secret exposure are excluded unless separately approved. |

If the user did not opt into live deploy, stop at `repo-only` or `prep-only` even when all technical checks pass.

## 2. Environment maturity

| Item | Pass condition | Evidence to record |
| --- | --- | --- |
| Target environment | Project/site/environment name is known. | Hosting target, URL, cloud project, or service name. |
| Ownership | Human owner or approving role is known. | User, release owner, or named maintainer. |
| Configuration | Required env vars/config are known and not printed. | Names only, source location, or confirmation they are present. |
| Rollback path | A concrete rollback is possible. | Previous commit/tag, hosting version, PR revert, or restore command. |
| Monitoring/smoke endpoint | There is a way to confirm the deployed target works. | URL, health endpoint, CLI smoke command, or manual page path. |

## 3. CI and local validation

| Check | Required for live deploy? | Ready answer |
| --- | --- | --- |
| Local validation | Yes | Project validator/build/test command passed locally. |
| Diff hygiene | Yes | `git diff --check` passed. |
| JSON/YAML/config validation | When changed | Parser/validator passed for changed structured files. |
| CI pipeline exists | Yes unless explicitly waived | Applicable workflow/check exists for this repo/path. |
| CI status | Yes unless explicitly waived | Latest branch/PR run is green, or named gap is waived. |

If CI does not exist and deploy is requested, prefer adding minimal CI when it is in scope. Otherwise block live deploy and report the CI gap.

## 4. Smoke and security review

Before live deploy, run the closest realistic smoke path and review security. Minimum evidence:

- Smoke: target builds/starts or the static site renders; critical URL/entry point returns success after deploy.
- Secrets: no tokens, API keys, private keys, or credential values are committed or printed in logs.
- Auth/rules: no authentication, authorization, CORS, database rules, or permission broadening unless explicitly approved for this task.
- Injection/shell: no untrusted input flows into commands, templates, queries, or generated config without validation/escaping.
- External writes: each remote write is named and approved by scope.
- Rollback: rollback command/path is still valid after the final diff.

## 5. Generic hosting/custom-domain addendum

For static hosting or custom-domain work:

1. Confirm the repository contains the site source or identify the external source of truth before changing copy or layout.
2. Validate static assets/build output locally.
3. Confirm provider project/site/target and active account without printing credentials.
4. Check the approved custom domain, not only provider default URLs.
5. Record the hosting version or commit used for rollback.
6. Do not change provider rules, auth providers, billing, or data stores in the same run unless separately approved.

## 6. Readiness report format

When deployment is blocked or deliberately deferred, report:

```markdown
Deployment classification: live-deploy requested | prep-only | repo-only
Live deploy result: blocked | deferred | not in scope
Blocking gaps:
- [ ] <gap, required owner/action>
Ready checks:
- [x] <check and evidence>
Rollback/recovery plan:
- <what to revert/restore if a future deploy fails>
Next action:
- <single highest-leverage step>
```

A readiness report is a successful delivery when the safe outcome is to avoid an unsafe deploy.
