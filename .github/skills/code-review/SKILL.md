---
name: code-review
description: Review end-to-end-loop pull requests for correctness, safety, cost regressions, and unsupported release claims.
---

# End-to-End Loop Code Review

Inspect the diff, `AGENTS.md`, affected tests, and CI evidence.

Report only actionable findings. Rank correctness and safety above style.

Check:

- state transitions, resume behavior, retry ceilings, and budget boundaries;
- runtime-package membership and byte-limit regressions;
- telemetry privacy and accidental raw prompt, command, environment, or identity data;
- GitHub Actions permissions, untrusted input use, and immutable action pins;
- production-readiness or cost claims that exceed measured evidence;
- missing tests for changed public behavior.

Copilot review supplements deterministic CI and human judgment. Never represent a
Copilot comment as an approval.
