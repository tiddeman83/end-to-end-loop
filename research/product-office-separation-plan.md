# Product Cleanup Plan

Goal: keep `end-to-end-loop` focused on the public delivery-loop tool/skill and move private office operations to the private operations repository.

## Boundary

- Product repo: skill core, generic adapters, validation, eval assets, deploy-readiness rubric, self-learning memory design, optional public helper agents.
- Operations repo: internal agents, task routing, private shift logs, governance, operational memory, public-team support briefs.

## Cleanup checklist

- [x] README maintenance model rewritten as generic maintainer/product language.
- [x] `.hermes.md` reduced to minimal product repo context.
- [x] `AGENTS.md` product-boundary note added.
- [x] `SKILL.md` reference routing made generic for hosting/custom domains.
- [x] Handoff files removed from the product package.
- [x] Product helper-agent strategy added.
- [x] Sanitize `development.md`, `memory.md`, `paper.md`, eval scenarios, and result logs.
- [x] Replace private target repo names with fictional/generic sample targets or move logs to the private operations repo.
- [x] Update validator if it encodes office-specific scenario expectations.
- [ ] Create PR and run CI.

## Acceptance criteria for final cleanup PR

Searches over product-facing files should show no unintended private office terms:

- internal office names/personas;
- private target names;
- task-routing platform specifics;
- custom domain or dashboard internals except generic hosting/deploy examples.

Any private migration links should remain outside the product package once the private operations repository is reachable.
