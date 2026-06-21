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

## Questions To Revisit

- Define Hermes compatibility requirements from concrete Hermes conventions.
- Decide whether CAVEMAN-specific routing remains as an optional adapter or is
  removed from the universal core.
- Decide how strict the deploy gate should be for agents with limited permission
  models.
