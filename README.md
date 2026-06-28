# End-to-End Loop

**A portable Agent Skill that makes coding agents take work from intent to
*verified* delivery — and prove it with evidence.**

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE -> TEST -> DELIVER/DEPLOY -> REPORT
```

It runs in any Agent Skills-compatible coding tool: Codex, Claude Code, Cursor,
and AGENTS.md-compatible agents.

## Why this exists

Coding agents fail in predictable ways. They skip discovery, edit before they
reproduce a bug, claim "tests pass" without running them, and treat deploying to
production as the natural last step of any task. The result is confident-sounding
reports that nobody can audit.

`end-to-end-loop` turns those failure modes into explicit gates. The thesis is
simple: an agent should keep looping until the work is understood, implemented,
verified against pass/fail criteria, tested, security-reviewed where it matters,
delivered only inside the approved scope, and reported with real evidence —
command output, diffs, test results — not vibes.

## What it does

The skill gives an agent a disciplined delivery contract:

- **Discover** the real goal, inputs, and side effects before acting.
- **Plan** small slices with explicit pass/fail acceptance criteria and named
  verification layers (unit, integration, smoke, security, CI).
- **Execute** code changes through a defined execution lane (see *CAVEMAN* below).
- **Verify** every criterion with observed evidence, then **iterate** until green.
- **Test**: smoke-test critical paths and run a security review proportional to risk.
- **Deliver** within approved scope. Live deploy is opt-in, never automatic.
- **Report** what changed, the evidence, what failed or was skipped, and how to roll back.

## Core guarantees

- **Evidence required.** No "green" claim without command output, test results,
  diff review, manual verification, CI status, or a documented user approval.
- **Deploy is opt-in.** Live deploy only happens when the user asked for it, the
  project is mature enough, an applicable CI pipeline is green, and rollback and
  credentials are approved. Otherwise the skill stops at prepared delivery and
  reports what remains.
- **Side effects are gated.** Network writes, installs, remote state changes,
  destructive commands, secrets, and deploys need explicit permission.
- **Portable core.** Universal rules live in `SKILL.md`; tool-specific notes live
  in `references/adapters.md`.
- **Lean by default.** Scale ceremony to task risk; use the cheapest adequate
  model or a deterministic script per phase without weakening the gates.

## How to use it

### Install

For Agent Skills-compatible tools, install the full package:

```bash
bash scripts/install.sh
```

This copies `SKILL.md`, `VERSION`, `references/*.md`, the packaged subskills under
`skills/`, the eval artifacts, `agents/openai.yaml`, and the helper scripts into
`~/.agents/skills/end-to-end-loop/`. Reload your agent session afterward.

You can also place the skill folder under your tool's skills directory directly,
for example `.codex/skills/`, `~/.claude/skills/`, or `.cursor/skills/`. See
`references/adapters.md` for per-tool paths and notes.

### Invoke it

Once installed, the agent loads the skill automatically for build / fix /
refactor / debug / test / review / ship work (the trigger conditions are in the
`SKILL.md` description). You can also point an agent at `SKILL.md` explicitly.

### About the CAVEMAN execution lane

For code-producing phases the skill expects a **CAVEMAN** execution lane — a
convention for routing edits and review through dedicated code/orchestration
skills rather than ad-hoc editing. It maps to whatever code-edit and review
skills you have configured; acceptable mappings are listed in
`references/adapters.md`. **If no such lane is configured, the skill stops before
changing code and asks you to approve an explicit exception** — it does not
silently fall back to unstructured editing. CAVEMAN is a convention, not a
bundled dependency; configure it, or run with an approved exception.

## Packaged subskills

Focused techniques the loop reaches for at the right moment, under `skills/`:

| Subskill | When it fires |
|---|---|
| `grilling` | Stress-test a vague plan/design before building — one question at a time, each with a recommended answer, until scope and verification are crisp. |
| `handoff` | Compact the session into a redacted handoff document so another agent/session can continue, referencing existing artifacts instead of duplicating them. |
| `diagnosing-bugs` | Debug a crash, wrong output, flaky test, or regression — build a reproducible feedback loop *before* hypothesizing or fixing. |
| `tdd` | Add behavior or lock in a bug fix test-first (red-green-refactor, behavior over implementation, vertical slices). |

## Repository layout

```text
SKILL.md                          # production skill core
VERSION                           # current package version (presented at run start and in reports)
references/phase-checklists.md    # phase gates and summaries
references/test-and-security.md   # smoke/security/side-effect gates
references/deploy-readiness.md    # deploy-readiness rubric and hosting/custom-domain gates
references/adapters.md            # Codex/Claude Code/Cursor/AGENTS.md adapters + CAVEMAN mappings
references/evaluation.md          # trigger/output/release evaluation guidance
references/self-learning.md       # per-repo compact memory and result-log rules
references/report-template.md     # delivery report template
references/mission-mode.md        # optional helper-agent / model-routing layer
references/backlog-and-copilot.md # backlog sequencing + GitHub Copilot feedback
references/local-telemetry.md     # opt-in local-first telemetry schema and privacy contract
skills/grilling/SKILL.md          # subskill: one-question-at-a-time plan grilling
skills/handoff/SKILL.md           # subskill: redacted temp-dir continuation handoffs
skills/diagnosing-bugs/SKILL.md   # subskill: feedback-loop-first bug/regression diagnosis
skills/tdd/SKILL.md               # subskill: test-first red-green-refactor
scripts/validate_skill.py         # dependency-free repo validator
scripts/install.sh                # install the full package
scripts/telemetry_record.py       # opt-in local telemetry recorder
scripts/telemetry_aggregate.py    # local-first telemetry aggregator
scripts/test_telemetry_privacy.py # telemetry privacy self-test
agents/openai.yaml                # Codex/OpenAI UI metadata
.github/workflows/validate.yml    # CI validation
AGENTS.md                         # general coding-agent project instructions
CHANGELOG.md                      # release history
research/                         # design/research notes (not part of the installed skill)
evals/                            # trigger, outcome, and result-log eval artifacts
paper.md                          # rationale write-up
memory.md                         # durable product decisions and sanitized learnings
```

## Validate locally

```bash
python3 scripts/validate_skill.py .
git diff --check
```

The validator checks frontmatter, required files, reference links, subskill
shape, eval coverage, telemetry privacy artifacts, and whitespace hygiene. CI
runs the same validator via `.github/workflows/validate.yml`.

**Caveat:** the validator enforces that the skill's folder name matches the
frontmatter `name`. Run it from a checkout (or a copy) of the folder named
exactly `end-to-end-loop`; an ad-hoc worktree name will fail that check even when
the contents are valid.

## Self-learning memory

Inside a target repository the skill can keep compact per-repo memory under
`.end-to-end-loop/`: `memory.md` (sanitized, may be committed), `memory.local.md`
(private, not committed), and `results/*.json` (per-run logs). Memory uses a
terse label style (`FACT`, `CMD`, `BLOCK`, `PREF`, `RISK`, `FIX`, `AVOID`,
`NEXT`) and must exclude secrets, bulky transcripts, and unverified guesses. See
`references/self-learning.md`.

## Evaluation

Quality is tracked through `evals/`: trigger cases (should-fire vs near-miss),
outcome scenarios, a result-log schema, and sanitized example logs. The aim is to
measure whether the skill fires for delivery work, stays quiet on pure Q&A,
preserves the evidence and deploy gates, and produces honest reports. Performance
claims stay scoped to auditability and reviewability until backed by measured
results.

## Status & versioning

This is **v0.1.0-alpha.2** — an early, usable alpha. The loop, gates, subskills,
validator, and CI are in place; broader benchmarks and multi-tool evidence are
still being built. The version is recorded in `VERSION`, presented at the start
of each run, and tracked in `CHANGELOG.md`.

## Maintenance

This is a public-facing skill repository maintained by its owner, working through
coding agents (currently Claude Code). There is no separate agent fleet,
back-office, or approval board governing it — earlier docs that implied otherwise
have been removed. Work happens on branches with validation and CI; releases are
the owner's call.
