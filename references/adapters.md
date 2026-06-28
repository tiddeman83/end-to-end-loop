# Agent and Tool Adapters

The universal core lives in `SKILL.md`. Use this file only for product-specific
installation and behavior notes.

## Common package

Recommended scalable layout. `scripts/validate_skill.py` (`check_required_files`)
is the authoritative list of files an installed package must contain; keep this
tree in sync with it.

```text
end-to-end-loop/
├── SKILL.md
├── references/
│   ├── phase-checklists.md
│   ├── test-and-security.md
│   ├── deploy-readiness.md
│   ├── adapters.md
│   ├── evaluation.md
│   ├── self-learning.md
│   ├── report-template.md
│   ├── mission-mode.md
│   ├── backlog-and-copilot.md
│   └── local-telemetry.md
├── scripts/
│   ├── validate_skill.py
│   ├── install.sh
│   ├── telemetry_record.py
│   ├── telemetry_aggregate.py
│   └── test_telemetry_privacy.py
└── agents/
    └── openai.yaml
```

Development files (`development.md`, `memory.md`, `paper.md`, `.github/`,
`.hermes.md`, `AGENTS.md`) belong in the repo, not
necessarily in a minimal installed skill package. Installed copies should record
or preserve their source repo and commit when possible so agents can run a
freshness check before relying on stale instructions.

## Codex

- Install as a skill folder under `.codex/skills/end-to-end-loop/`,
  `~/.codex/skills/end-to-end-loop/`, or a plugin `skills/` directory.
- Keep only `name` and `description` in `SKILL.md` frontmatter for maximum
  compatibility.
- Use `agents/openai.yaml` for Codex UI metadata.
- Before code-producing work, run a repo freshness check when a remote exists:
  `git fetch origin --prune` then compare `HEAD` with the intended upstream.
- Run `python3 scripts/validate_skill.py .` before committing changes.
- Install or update CAVEMAN ULTRA/CODE/REVIEW companion skills before EXECUTE and
  ITERATE when Codex skill install/update is available. If install/update is
  blocked, stop before code changes and ask for a user-approved exception.

## Hermes Agent

Hermes supports the Agent Skills standard and uses `~/.hermes/skills/` as the
primary skill directory. It can also scan external skill directories configured in
`~/.hermes/config.yaml`.

Recommended setup:

```yaml
skills:
  write_approval: true
  external_dirs:
    - ~/.agents/skills
    - /path/to/end-to-end-loop-parent
```

Notes:

- Hermes loads skills progressively with `skills_list()`, `skill_view(name)`, and
  `skill_view(name, path)`.
- Hermes supports `SKILL.md` frontmatter fields beyond the open standard, including
  `version`, `platforms`, `metadata.hermes`, required env vars, and toolset
  conditions. Do not require those fields in the universal core.
- For this repo, give Hermes project context through `.hermes.md` and `AGENTS.md`.
- Turn on `skills.write_approval` before allowing Hermes to modify this skill.
- Install/update `end-to-end-loop` and companion CAVEMAN skills under the active
  profile only, normally `~/.hermes/skills/software-development/`. Do not edit
  another profile's skills unless explicitly directed.
- Before use, load `end-to-end-loop`, `caveman-ultra`, `caveman-code`, and a
  reviewer/Cavecrew skill when available. If missing, use Hermes skill management
  or the configured source repo to install/update them; otherwise report
  `missing-blocked` before code changes.
- For repo-backed installs, check freshness with `git fetch origin --prune` and a
  compare against the configured upstream branch. Validate in a temporary folder
  named exactly `end-to-end-loop`, sync the installed copy only after validation,
  then start a fresh session or reload skills.
- Keep Hermes-specific product context in `.hermes.md` and generic project
  instructions in `AGENTS.md`; private operations workflows should live outside
  this public-facing product package.
- Hermes persistent memory may complement repo memory, but repo memory should stay
  explicit, reviewable, compact, and privacy-safe. Prefer
  `.end-to-end-loop/memory.md` for sanitized repo facts and
  `.end-to-end-loop/memory.local.md` for private local facts.

## Claude Code

- Install under `~/.claude/skills/end-to-end-loop/` or
  `.claude/skills/end-to-end-loop/`.
- Claude-specific fields such as `disable-model-invocation`, `allowed-tools`,
  `context`, and `agent` can be added in a wrapper copy, but should not be required
  by the universal core.
- For high-risk repo changes, use permission rules to ask/deny tools rather than
  embedding broad autonomy in the skill.
- Evaluate in fresh sessions and compare with-skill versus without-skill behavior.

## Cursor

- Cursor can load Agent Skills from `.agents/skills/`, `.cursor/skills/`,
  `~/.agents/skills/`, `~/.cursor/skills/`, and compatibility paths for Claude and
  Codex skills.
- Prefer the skill format for reusable procedures. Use `.cursor/rules/*.mdc` only
  for always-on or path-scoped project rules.
- Keep `AGENTS.md` as the project-level bridge for simple repository instructions.

## AGENTS.md-only agents

If an agent does not support Agent Skills:

1. Put a short `AGENTS.md` in the repo root.
2. Reference this skill folder and instruct the agent to read `SKILL.md` when the
   task involves build/fix/refactor/test/release work.
3. Do not paste the full skill into `AGENTS.md`; that creates context bloat.
4. Keep CAVEMAN and deploy gates visible in the short project instructions.
5. If `.end-to-end-loop/memory.md` exists, read it before planning and update it
   only when the task scope allows documentation writes.

## GitHub Copilot / PR review

When pushing to GitHub, include Copilot findings when possible:

- If an authenticated Copilot/gh-copilot review path exists, run it before or after
  push according to tool capability.
- Treat Copilot output as review input, not proof. Verify any suggested change
  through the loop.
- Include findings in result logs under `copilot_findings`.
- If unavailable, record the reason (`not installed`, `not authenticated`,
  `unsupported for local branch`, or `permission denied`) instead of inventing a
  review.

## Concrete install/update preflight

Use these templates when the tool/profile supports local skill files. Adapt paths to
the active profile only.

### Repo freshness check

```bash
git fetch origin --prune
git rev-parse --short HEAD
git rev-parse --short @{u} 2>/dev/null || true
git status --short --branch
```

If `@{u}` is unavailable, compare against the configured source branch explicitly,
for example `origin/main`. Treat network/auth failure as `not_checked` or
`outdated-blocked`, not as proof that the skill is current.

### Validate before sync

```bash
tmp=$(mktemp -d)
cp -a /path/to/end-to-end-loop "$tmp/end-to-end-loop"
rm -rf "$tmp/end-to-end-loop/.git"
python3 "$tmp/end-to-end-loop/scripts/validate_skill.py" "$tmp/end-to-end-loop"
```

### Hermes active-profile sync

```bash
install_root="$HOME/.hermes/skills/software-development"
mkdir -p "$install_root"
# after validation only:
rsync -a --delete --exclude .git /path/to/end-to-end-loop/ "$install_root/end-to-end-loop/"
```

If `rsync` is missing, use a small Python `shutil.copytree(..., dirs_exist_ok=True)`
after deleting the old installed copy. Then start a fresh Hermes session or reload
skills. Use `skills_list()`/`skill_view()` to verify `end-to-end-loop`,
`caveman-ultra`, `caveman-code`, and `cavecrew` or a configured reviewer lane.

### CAVEMAN companion check

Required names or equivalents before code-producing phases:

- `caveman-ultra` for orchestration/compression.
- `caveman-code` for code edits.
- `cavecrew`, `caveman-review`, or configured reviewer for review/delegation.

If a companion is missing and no approved source/install mechanism is available,
record `missing-blocked` and stop before repo writes unless the user approves a
CAVEMAN exception.

## Skill freshness and install/update statuses

Use these status labels in reports:

- `installed-current`: required skill is present and source/upstream is current.
- `installed-updated`: missing/outdated skill was installed or updated and reloaded.
- `missing-installed`: missing skill was installed successfully.
- `missing-blocked`: missing skill could not be installed because permissions,
  network, approval, or source configuration was unavailable.
- `outdated-blocked`: update was available but blocked.
- `exception-approved`: user approved proceeding without a current CAVEMAN lane.

Skill lifecycle actions are side effects. Network fetches, local skill writes,
and reload/restart steps must be planned and reported.

## CAVEMAN adapters

CAVEMAN is a required execution lane, but different tools may expose it under
different names. Acceptable mappings:

| Required role | Preferred name | Adapter examples |
| --- | --- | --- |
| Execution orchestration | CAVEMAN ULTRA | caveman-ultra, cavecrew-builder, configured Hermes engineering agent |
| Code modification | CAVEMAN CODE | caveman-code, code-focused CAVEMAN agent, configured Hermes implementation agent |
| Review compression | CAVEMAN REVIEW | caveman-review, code-review with caveman output style |

If no mapping exists, the run is blocked before code changes unless the user grants
an explicit exception.
