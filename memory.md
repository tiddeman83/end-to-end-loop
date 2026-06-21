# End-to-End Loop Skill Memory

This file captures durable learnings from the discussion and research so future
iterations do not re-litigate settled points.

## User Intent

- The user wants the existing end-to-end-loop skill developed into a safe, mature,
  shareable skill.
- The user wants at least five iterations, with the assistant leading research and
  planning.
- Each iteration must be committed and pushed to GitHub.
- The repository must remain private for now.
- The skill must work beyond Codex, including Hermes and other agent/coding tools.
- The assistant should ask critical questions and request proposals from the user at
  each iteration.

## Working Assumptions

- The canonical skill should be written in English to maximize portability and future
  sharing.
- Development artifacts can live in the repository, but the final packaged skill may
  need to exclude non-operational documents depending on the target ecosystem.
- Safety should be modeled as explicit permission, scope, verification, and rollback
  gates instead of relying on agent judgment alone.

## Decisions

- 2026-06-21: Repository name chosen as `tiddeman83/end-to-end-loop`.
- 2026-06-21: Repository created as private.
- 2026-06-21: Initial repository state pushed to GitHub.

## Questions To Revisit

- Define Hermes compatibility requirements from concrete Hermes conventions.
- Decide whether CAVEMAN-specific routing remains as an optional adapter or is
  removed from the universal core.
- Decide how strict the deploy gate should be for agents with limited permission
  models.

## Research Learnings

- Agent Skills use progressive disclosure: metadata first, full `SKILL.md` only
  when activated, references/scripts/assets only as needed.
- The `description` field is operational because it controls trigger behavior. It
  must be precise enough to avoid both false negatives and false positives.
- Cursor, Claude Code, and Codex increasingly converge on `SKILL.md`, but each adds
  tool-specific fields. The universal core should avoid depending on those fields.
- AGENTS.md is useful as broad compatibility glue for repository-level instructions,
  but it is not a full skill format and lacks structured invocation controls.
- Public Hermes Agent material confirms relevant capabilities but not enough file
  format detail. Treat Hermes as a first-class target after user confirmation.
- Research on SKILL.md attacks and AGENTS.md smells supports a conservative design:
  avoid context bloat, conflicting instructions, broad triggers, manipulative
  trust/security claims, and unsafe state-changing behavior.
- A portable delivery loop should distinguish "deliverable prepared" from "live
  deployment executed" and require explicit approval for high-impact side effects.
