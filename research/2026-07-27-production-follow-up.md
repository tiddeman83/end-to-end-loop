# Production Research Follow-up

Date: 2026-07-27

Scope: agentic control, cost, recovery, GitHub CI/CD, automatic pull requests, and
GitHub Copilot review.

## Decision

The framework should remain an assurance/control layer, not become another agent
runtime. Current runtimes already provide tool execution, sessions, persistence,
interrupts, tracing, and handoffs. This release makes the portable policy
machine-readable and leaves runtime transport to those systems.

`v0.1.0-alpha.3` is materially stronger but still not production-proven. The
highest-value shipped slice is deterministic state + budgets + focused context +
repeatable packaging + repository automation. Multi-agent expansion stays
deferred until comparative evaluations show a benefit.

## Fresh primary-source findings

### Durable agent execution

- [OpenAI Agents SDK human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)
  serializes `RunState`, pending approvals, usage, nested resumptions, and trace
  metadata. Sensitive context must be treated as persisted data.
- [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/)
  records model generations, tool calls, handoffs, guardrails, and custom spans,
  with controls for sensitive data.
- [LangGraph interrupts](https://langchain-ai.github.io/langgraph/concepts/breakpoints/)
  checkpoint graph state before interruption and resume through a stable thread
  identifier.

Implication: a production control layer needs versioned persisted state,
validated resume, explicit approvals, and privacy rules. A prose phase diagram is
not enough.

### GitHub Copilot review

- [GitHub Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review)
  can review pull requests automatically, optionally on every push. Reviews use
  AI credits and may also use Actions minutes.
- [Using Copilot code review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)
  supports `gh pr create --reviewer @copilot` and REST reviewer
  `copilot-pull-request-reviewer[bot]`.
- [Automatic review configuration](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-automatic-review)
  is a repository/organization ruleset option.

Implication: request Copilot after deterministic local gates. Automatic
`review_on_push` improves coverage but costs more. Copilot always comments; it
does not approve or block merge, so CI and maintainer judgment remain mandatory.

### GitHub automation and supply chain

- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
  supports timezone-aware schedules, concurrency, and default-branch scheduled
  execution.
- [Workflow token permissions](https://docs.github.com/en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)
  default to restricted access in newer repositories; workflows need explicit
  write permission for releases or PR creation.
- [Secure use of GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use)
  recommends limiting permissions and monitoring action dependencies.
- [GitHub Agentic Workflows](https://docs.github.com/en/copilot/how-tos/github-agentic-workflows)
  can safely expose bounded outputs such as pull-request creation, but remains in
  public preview.

Implication: keep ordinary validation deterministic and cheap. Use a scheduled
Codex maintenance task for research and scoped implementation now; evaluate
GitHub Agentic Workflows later rather than making a preview feature the only
maintenance path.

## Implemented improvements

1. `loop-state-v2`: atomic persistence, validated resume, deterministic
   transitions, acceptance evidence, budgets, retries, blockers, stop reasons.
2. `loop-preflight-v2`: capability/risk routing and selected reference byte count.
3. `runtime-package-v1`: explicit production files, 250 KB ceiling, reproducible
   ZIP, maintainer/eval exclusions.
4. CI: least-privilege pinned actions, kernel/package/privacy/validator/install
   gates, concurrency and timeouts.
5. CD: tag/VERSION match, full release gates, deterministic runtime artifact,
   SHA-256 checksums, GitHub Release publication.
6. Review: Copilot instructions and review skill; repository ruleset requested
   for automatic reviews on new pushes.
7. Maintenance: weekly task researches sources, applies only evidenced bounded
   changes, opens a PR, waits for CI, and requests Copilot review.

## Remaining production gates

- Baseline/current repeated task runs across at least two supported tools.
- Cost per verified success, not only package/context byte proxies.
- Crash/restart and corrupted-state tests against real tool side effects.
- Idempotency keys or side-effect receipts for remote writes.
- Independent adjudication of Copilot and agent-authored findings.
- Green remote CI and release rehearsal for this pull request.
- Authenticated provenance/attestation beyond archive SHA-256.
