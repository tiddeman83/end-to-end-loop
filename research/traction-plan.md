# Traction and Pre-Release Strategy

Goal: build credible traction for `end-to-end-loop` after the repo goes live, without overclaiming reliability before evidence exists.

## Positioning

`end-to-end-loop` is not another agent framework. It is a portable discipline layer for coding agents: discover, plan, execute, verify, test, deploy-gate, and report with evidence.

Tagline candidates:

- A portable quality loop for coding agents.
- Make coding agents produce evidence, not just patches.
- The missing review gate between autonomous coding and production.

Primary audiences:

- agent power users using Codex, Claude Code, Cursor, Aider, Cline, Continue, OpenCode, or similar tools;
- AI researchers studying verifiable software-engineering agents;
- engineering teams experimenting with agentic development;
- open-source maintainers who want more reviewable agent PRs.

## Credibility anchors

Use these as public research analogies, not as claims of equivalence:

- SWE-bench: real-world task evaluation matters more than polished demos.
- SWE-agent: scaffold and interface design can materially change coding-agent outcomes.
- OpenAI Evals: capability claims should ship with repeatable tasks and transparent scoring.
- Aider leaderboards: developers like benchmark results that are readable and reproducible.
- Claude/Cursor/Cline/Aider communities: adoption follows practical examples and copyable workflow snippets.

## Launch evidence package

Minimum viable package before public pre-release:

1. README with visual loop diagram and one-minute quickstart.
2. One before/after example: vague agent report vs evidence-backed end-to-end-loop report.
3. Three examples:
   - successful bugfix with tests;
   - failed verification where the agent says “not done” honestly;
   - deploy gate blocked because readiness is insufficient.
4. Compatibility matrix:
   - tested;
   - expected;
   - planned;
   - not supported.
5. Small benchmark note:
   - task set;
   - agents/tools tested;
   - scoring rubric;
   - raw result logs;
   - limitations.
6. Issue templates for compatibility reports, benchmark submissions, skill improvements, and evidence examples.

## Metrics to report

Avoid unsupported “agent reliability improved X%” claims until measured rigorously.

Better metrics:

- evidence completeness score;
- verification honesty: passed/failed/not-run claims match evidence;
- unjustified success-claim count;
- deploy-gate correctness;
- human reviewability score;
- task success rate where objectively measurable;
- regression preservation where tests exist.

## Private review gate

Tijmen review is mandatory before first pre-release.

Do not tag a public pre-release until:

- README explains the project in the first 100 words;
- at least 3 real or realistic run transcripts exist;
- at least one example shows failed verification or blocked deploy;
- install/use instructions work from scratch in one target environment;
- claims are scoped to auditability/reviewability unless benchmarked;
- 3 external reviewers can explain the project correctly;
- 2 users can try it without hand-holding;
- 1 skeptical reviewer says the claims are appropriately scoped;
- Tijmen has reviewed the repo and explicitly approves `v0.1.0-alpha` or equivalent.

## Suggested launch sequence

### Week -2: private review

- Finish README, examples, evidence report sample, compatibility matrix.
- Ask 5–10 targeted reviewers for launch-blocking critique.
- Fix unsupported claims and confusing install paths.

### Week -1: evidence package

- Run 10–20 small tasks with and without the skill when feasible.
- Publish raw logs or compact result logs.
- Create a short demo video/GIF showing the loop and final evidence report.
- Seed GitHub issues and labels.

### Launch day

- Tag `v0.1.0-alpha` or `v0.1.0-pre.1`, not stable.
- Post a concise launch thread with honest claims.
- Share in high-signal agent/dev communities before broad channels.

### First 72 hours

- Respond to substantive GitHub issues.
- Convert feedback into labeled work.
- Publish “early feedback and roadmap.”
- Add compatibility reports from real users.

## Community channels

Prioritize practical developer communities:

- GitHub repo and Discussions/Issues;
- X/Twitter developer/AI audience;
- LinkedIn for professional delivery framing;
- Aider, Cline, Continue, Cursor, Claude Code and Hermes/Nous communities where allowed;
- Hacker News Show HN only after README/demo/evidence are strong;
- Reddit only with practical examples, not hype.

## Launch post draft

> Coding agents often say “done” without showing enough evidence.
>
> `end-to-end-loop` is a portable Agent Skill that makes agents follow a disciplined loop:
>
> discover → plan → execute → verify → test → deploy gate → report
>
> It focuses on evidence: files changed, commands run, test results, unresolved risks, and deployment recommendations.
>
> Looking for early reviewers before the first pre-release.

## Risks and mitigations

- Too abstract → lead with examples and actual reports.
- Seen as prompt fluff → ship eval cases, raw logs, and benchmark notes.
- Overclaiming → say “auditability/reviewability” until stronger data exists.
- Compatibility confusion → separate tested from expected/planned.
- No contribution path → seed benchmark and compatibility issues before launch.
