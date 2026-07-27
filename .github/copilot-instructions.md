# Copilot review instructions

Review pull requests as an independent, evidence-focused reviewer.

- Read `AGENTS.md` and the changed skill/reference files before commenting.
- Prioritize correctness, unsafe state transitions, budget bypasses, privacy leaks,
  shell injection, overly broad GitHub permissions, and release-claim overreach.
- Treat `python3 scripts/validate_skill.py .`, kernel/package tests, telemetry
  privacy tests, and the installation smoke test as required evidence.
- Check that runtime files are declared in `runtime-package.json`; maintainer-only
  files must stay out of the installed runtime.
- Flag claims that Copilot review is an approval gate. Copilot comments are useful
  evidence but do not approve or block a merge.
- Keep findings specific, ranked, and actionable. Do not comment only on style.
