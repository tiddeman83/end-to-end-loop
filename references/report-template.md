# REPORT template

The final deliverable to the user. Keep it skimmable: short sections and prose, not a
wall of bullets. Adapt section depth to the size of the task.

```markdown
# <Task name> — delivery report

## What was built
<One short paragraph: what now exists that didn't before, in plain language.>

## Goal & how it was met
<Restate the original goal. Map the result to each acceptance criterion: met / not met,
with a word on why. This closes the loop back to DISCOVER/PLAN.>

## Key decisions
<The handful of choices that shaped the result — tech, approach, trade-offs — and why.>

## Testing
- Smoke tests: <what was exercised, result — pass/fail>
- Security review: <what was checked, result — clean / fixed items / open follow-ups>

## Deployment
<Where it was deployed, how it was verified in the target, and how to roll back.>

## How to use it
<Concise usage: commands, endpoints, entry points, config the user needs.>

## Known limitations & follow-ups
<Anything out of scope, deferred, or worth doing next. Be honest.>
```

Guidance:
- Lead with the outcome, not the process — the user followed along; don't re-narrate
  every step.
- If acceptance criteria weren't fully met, say so plainly and explain the gap.
- Surface security follow-ups even if they were below the must-fix bar, so nothing is
  silently dropped.
