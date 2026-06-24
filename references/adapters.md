# Agent and Tool Adapters

The universal core lives in `SKILL.md`. Use this file only for product-specific
installation and behavior notes.

## Common package

Recommended scalable layout:

```text
end-to-end-loop/
├── SKILL.md
├── references/
│   ├── phase-checklists.md
│   ├── test-and-security.md
│   ├── adapters.md
│   ├── evaluation.md
│   ├── self-learning.md
│   └── report-template.md
├── scripts/
│   └── validate_skill.py
└── agents/
    └── openai.yaml
```

Development files (`development.md`, `memory.md`, `paper.md`, `.github/`,
`.hermes.md`, `AGENTS.md`) belong in the repo, not
necessarily in a minimal installed skill package.

## Codex

- Install as a skill folder under `.codex/skills/end-to-end-loop/`,
  `~/.codex/skills/end-to-end-loop/`, or a plugin `skills/` directory.
- Keep only `name` and `description` in `SKILL.md` frontmatter for maximum
  compatibility.
- Use `agents/openai.yaml` for Codex UI metadata.
- Run `python3 scripts/validate_skill.py .` before committing changes.
- If CAVEMAN ULTRA/CODE skills are installed, use them for EXECUTE and ITERATE.
  If not installed, stop before code changes and ask for a user-approved exception.

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
