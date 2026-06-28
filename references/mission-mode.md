# Mission Mode Helper Agents

Mission Mode is the optional parallel layer for `end-to-end-loop`. Use it to reduce wall time, improve review quality, or compress context without weakening CAVEMAN, deploy, security, or approval gates.

## Reasoning and model levels

| Level | Route | Use | Approval |
|---|---|---|---|
| `level_0` | deterministic script or cheap/fast model | scans, summaries, formatting, schema checks, log parsing | none beyond normal tool policy |
| `level_1` | standard coding model + CAVEMAN | bounded implementation, tests, docs updates | repo-write approval as usual |
| `level_2` | high-reasoning model/specialist reviewer | architecture, security, deploy readiness, auth/data risk, repeated failure | explicit risk review |
| `level_3` | human approval | merge, release, live deploy, admin, secrets, destructive writes, public claims | human only |

Prefer the cheapest adequate route. Escalate only for ambiguity, risk, repeated failure, cross-cutting design, or irreversible side effects.

## Public helper-agent specs

| Helper | Scope | Input | Output | Suggested level |
|---|---|---|---|---|
| `mission-planner` | split a task into workstreams and ACs | prompt, repo map, constraints | compact plan, routes, risks | level_1; level_2 for architecture |
| `loop-investigator` | locate files, symbols, tests, prior patterns | search target, paths | path:line findings | level_0/1 |
| `loop-builder` | bounded 1-2 file implementation | exact files, ACs, verify hook | diff summary, verification | level_1 + CAVEMAN |
| `loop-reviewer` | diff/security/quality review | diff, ACs, risk class | findings by severity | level_1; level_2 for security/deploy |
| `loop-verifier` | run/interpret targeted checks | commands, expected behavior | pass/fail evidence | level_0/1 |
| `loop-eval-runner` | trigger/outcome eval checks | eval files, scenario | result-log-ready findings | level_0/1 |
| `loop-reporter` | compress final evidence | changed files, tests, blockers | compact report | level_0/1 |
| `deploy-readiness-checker` | readiness only, never deploy authority | target, CI, rollback, smoke path | gaps and go/no-go recommendation | level_2; deploy remains level_3 |

## Spawn policy

Always consider helper agents during PLAN. Use them when workstreams are independent, a specialist review is useful, or context compression helps. Do not spawn agents for one-line edits, when the needed context would exceed the expected saving, or to bypass approval gates.

## Boundaries

- Helpers are functional product tools, not private office personas.
- Helpers do not merge, release, deploy, administer repos, handle secrets, or approve public claims.
- Code-producing helper work still goes through CAVEMAN.
- Reports must include helpers considered/used and routing rationale.
