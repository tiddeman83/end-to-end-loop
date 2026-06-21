# End-to-End Loop

Private development repository for the `end-to-end-loop` Agent Skill.

The skill defines a disciplined software delivery loop:

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE -> TEST -> ITERATE -> DELIVER/DEPLOY -> REPORT
```

Its goal is to help coding agents keep working until a software task has real evidence: scoped plan, implementation through the required lane, observed verification, tests/security review, safe delivery, and an auditable report.

## Current status

- Repository visibility: private during development.
- Primary artifact: `SKILL.md`.
- Supporting references: `references/`.
- Research and rationale: `paper.md` and `research/`.
- DevBoss/Hermes handoff: `handoff/`.
- CI: `.github/workflows/validate.yml` runs the local skill validator.
- Public release: not yet; blocked until trigger/outcome evals, metrics, website readiness, and board approval are complete.
- Live deploy: not in scope without explicit approval.

## What makes this skill different

- **Evidence-first loop:** completion requires observed outputs, not agent confidence.
- **CAVEMAN hard gate:** code-producing phases must use the configured CAVEMAN/Cavekit execution lane or record an approved exception.
- **Deploy safety:** live deploy is opt-in and requires maturity, CI, rollback, credentials approval, smoke checks, and security review.
- **Portable core + adapters:** universal behavior lives in `SKILL.md`; tool-specific guidance lives in `references/adapters.md`.
- **Self-improving harness:** the loop improves its own instructions, memory, evals, and operating handoffs when evidence shows gaps.

## Repository layout

```text
.
├── SKILL.md                         # Production skill core
├── references/                      # Phase, safety, adapter, eval, report guidance
├── scripts/validate_skill.py        # Dependency-free validator
├── evals/trigger-cases.json         # Seed trigger evals
├── research/                        # Improvement and research notes
├── handoff/                         # Hermes/DevBoss setup briefs
├── agents/openai.yaml               # Codex UI metadata
├── AGENTS.md                        # Cross-agent repo instructions
├── .hermes.md                       # Hermes project context
├── development.md                   # Development log
├── memory.md                        # Durable decisions and preferences
└── paper.md                         # Research-paper draft
```

## Validate locally

If the checkout directory basename matches the skill name:

```bash
python3 scripts/validate_skill.py .
git diff --check
```

If the checkout directory basename does **not** match `SKILL.md`'s `name`, validate through a basename-matching temp copy:

```bash
TMP=/tmp/end-to-end-loop
rm -rf "$TMP"
mkdir -p "$TMP"
( cd /path/to/checkout && tar --exclude='.git' -cf - . ) | ( cd "$TMP" && tar -xf - )
python3 "$TMP/scripts/validate_skill.py" "$TMP"
git -C /path/to/checkout diff --check
```

## DevBoss operating notes

- Tijmen is Supervisory Board chair and final release/deploy approver.
- Board decisions route through Todoist and are mirrored back into repo notes.
- Repo changes must use worktrees; do not edit main directly.
- Each meaningful iteration should be committed and pushed.
- Firebase/dev-boss.nl work is prep-only until explicit deploy approval.

## Website readiness

Target domain: `dev-boss.nl`.

Current observed state: `https://tijmensassistant.web.app` is live for the TinTin assistant cockpit, while `https://dev-boss.nl` is not yet a valid public DevBoss site because TLS hostname validation fails. Before the site can be shown publicly, DevBoss needs a public info-site build, correct Firebase hosting/custom-domain setup, visitor-statistics plan, CI/deploy path, smoke/security checks, and explicit approval.
