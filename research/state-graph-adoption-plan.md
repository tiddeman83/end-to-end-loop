# State-Graph Adoption Plan

Date: 2026-08-25

Assessed version: `0.1.0-alpha.2` (`99f256d`)

Mode: `standard + review-improve`, research and planning only. No production
skill files were changed by this pass.

Input: a user-supplied research report on graph-based state machines and looping
control flow for agentic systems (LangGraph, LlamaIndex Workflows, AutoGen,
CrewAI Flows; ReAct, evaluator-optimizer, self-healing repair loops; reducers,
checkpointing, recursion limits, human-in-the-loop interrupts).

Source status: the report is **user-supplied secondary material**. Its framework
claims match what `research/competitive-production-assessment.md` already
recorded for LangGraph and AutoGen, but the per-framework details below were not
re-verified against upstream documentation in this pass. Any public claim about
another framework's behavior must be refreshed against primary sources first.

---

## 0. What the research actually says that matters here

Stripped of vendor detail, the report makes five design directives:

1. **Schema first.** A typed, centralized state object is the contract; nodes
   return updates to it, they do not pass prose forward.
2. **Reducers are explicit.** For every accumulating key, say how a new value
   merges with the old one (append vs overwrite). Otherwise history is silently
   destroyed.
3. **Routing is decoupled from work.** Nodes do one focused thing; conditional
   edges — pure functions over state — decide what runs next.
4. **Every cycle is bounded.** Global transition cap plus a state-level iteration
   counter, and a deterministic fallback route when the counter trips. An
   unbounded loop is the default failure mode of cyclic agents.
5. **Persist at trust boundaries.** Checkpoint at node boundaries so runs resume
   after interruption, and pause *before* high-risk nodes for human approval.

None of this requires adopting a framework. All five are expressible as a small
JSON state file plus a transition table, which is what this repo can carry
without giving up portability.

## 1. Where end-to-end-loop already stands

`end-to-end-loop` is **already a finite state machine written as prose**. The
phases are nodes, the `Exit:` lines are edge conditions, ITERATE→VERIFY and
ITERATE→TEST are cycles, and `level_3` is an interrupt-before list in disguise.

The gap is not conceptual, it is that none of it is *materialized*:

| Research directive | Current state in this repo | Gap |
|---|---|---|
| Typed state schema | Phase/mode/plan live in the agent's context and the report | No run artifact; nothing survives a lost context window |
| Reducers | `references/self-learning.md` memory labels are append-ish by convention | No key-level merge rule; a later phase can silently overwrite earlier evidence |
| Routing decoupled from work | Each phase ends with prose `Exit:` conditions | Routing is embedded in node text and judged by the model; not inspectable, not testable |
| Bounded cycles | "Change approach if repeated attempts do not make progress" | No counter, no ceiling, no named fallback route; the two ITERATE loops can run forever |
| Checkpoint / resume | None | An interrupted run restarts from prose re-reading |
| Interrupt before high-risk | `level_3` human approval, deploy policy | Real, but expressed per-phase rather than as one machine-readable node list |

This is the same finding as `research/competitive-production-assessment.md`
("Runtime agency 1/4 — the phase diagram is not an executable state machine and
cannot resume deterministically"), scored 17/40 overall. The research report does
not open a new track; it **sharpens the existing alpha.3 backlog** (slices 1-3:
run-state schema, risk-triggered router, budget/termination contract) and adds
four things that backlog did not name: reducers, router/node separation, a
failure taxonomy for the repair cycle, and interrupt-before as a list.

### What we should *not* copy

- **Do not become a runtime.** The defensible position recorded in the
  competitive assessment is an assurance and delivery-policy layer *over*
  runtimes. Depending on LangGraph, or reimplementing its executor, would break
  portability across Codex / Claude Code / Cursor / AGENTS.md-only agents, which
  is Non-Negotiable 6.
- **Do not add a Python runtime dependency.** Everything below is plain JSON plus
  dependency-free scripts, matching the existing `scripts/*.py` style.
- **Do not import framework vocabulary wholesale.** Users of this skill get
  `phase`, `route`, `cap`, `evidence` — not `StateGraph`, `add_conditional_edges`.

---

## 2. Plan 1 — adjust the current end-to-end-loop

Goal: make the existing linear loop an explicit, resumable, bounded state
machine, without adding ceremony to small tasks and without weakening any gate.

Target release: `0.1.0-alpha.3` (replaces and sharpens the slice list in
`research/improvement-plan.md`).

### Hard constraint discovered in this pass

`SKILL.md` is **503 lines**; `scripts/validate_skill.py` fails the body over 500
lines. The core is at its budget. Therefore every slice below is **net-zero or
net-negative on `SKILL.md` lines**: tables replace prose, and detail moves into
references. If a slice cannot pay for itself in lines, it ships as a reference
plus a one-line routing entry.

### Slice A1 — Run-state schema with explicit reducers `level_2`

Add `references/run-state.md` and `schemas/run-state.schema.json`; write the
artifact to `.end-to-end-loop/run.json` in the target repo.

```json
{
  "schema_version": "1.0",
  "run_id": "2026-08-25-1410-auth-fix",
  "skill_version": "0.1.0-alpha.3",
  "goal": "…",
  "phase": "VERIFY",
  "mode": ["standard", "github-copilot"],
  "delivery_class": "repo-only",
  "acceptance": [{"id": "ac1", "text": "…", "status": "pass|fail|blocked", "evidence_ref": "ev3"}],
  "evidence": [{"id": "ev3", "kind": "command", "cmd": "pytest -q", "exit": 0, "digest": "sha256:…", "path": ".end-to-end-loop/logs/ev3.txt"}],
  "counters": {"verify_iterations": 1, "test_iterations": 0, "transitions": 7},
  "budget": {"max_verify_iterations": 3, "max_test_iterations": 3, "max_transitions": 40},
  "approvals": [{"action": "push", "granted": true, "at": "…"}],
  "blockers": [],
  "termination": null
}
```

Reducer table (the part the research adds that the old backlog missed) — one row
per key, enforced by the transition script and stated in the reference:

| Key | Reducer | Rationale |
|---|---|---|
| `evidence` | append-only, immutable entries | Non-Negotiable 3 becomes mechanically checkable: nothing can quietly erase the proof |
| `acceptance[].status` | replace by `id` | Latest verdict wins, history lives in `evidence` |
| `blockers` | append, resolve by id (never delete) | Preserves the failure lineage for the report |
| `counters.*` | increment only | A loop cannot reset its own budget |
| `approvals` | append-only | An approval is a fact, not a mutable flag |
| `phase`, `goal`, `delivery_class` | replace, transition-checked | Single-writer keys |

Large command output stays **out** of the manifest: store a path plus a digest
(this rule already exists in the competitive assessment; make it schema-level).

Acceptance: an interrupted run resumes at the recorded phase with acceptance,
evidence, counters and approvals intact; a manifest that drops a prior evidence
entry fails validation.

### Slice A2 — Transition table and deterministic gate checks `level_2`

Move the per-phase `Exit:` prose into one table (net-negative on `SKILL.md`
lines) and add `scripts/run_state.py` (`init` / `show` / `transition` /
`check`), dependency-free like the telemetry scripts.

| From | Allowed to | Required state before the transition |
|---|---|---|
| DISCOVER | BACKLOG, PLAN | goal set, side effects listed, options chosen |
| BACKLOG | PLAN | ordered slices, dependency + interference notes |
| PLAN | EXECUTE | acceptance criteria non-empty, delivery_class set, lane resolved |
| EXECUTE | VERIFY | diff or artifact recorded, lane recorded |
| VERIFY | ITERATE_V, TEST, ESCALATE | every acceptance criterion has a status + evidence_ref |
| ITERATE_V | EXECUTE, ESCALATE | at least one failing criterion converted to a mini-plan |
| TEST | ITERATE_T, DELIVER, ESCALATE | tests, smoke and security review each pass/blocked with evidence |
| ITERATE_T | EXECUTE, ESCALATE | must-fix item planned |
| DELIVER | REPORT, ESCALATE | delivery verified (branch pushed / PR exists / URL responds) |
| ESCALATE | REPORT | termination reason recorded |

Anything not in this table is an invalid transition and fails deterministically —
that is what kills "EXECUTE → DELIVER, tests probably fine".

Acceptance: `run_state.py transition --to DELIVER` exits non-zero when the TEST
row's requirements are unmet, with the missing key named.

### Slice A3 — Routers as named functions over state `level_2`

Today routing is embedded in phase prose. Split it: nodes do work, routers decide.
Each router is a short deterministic rule list, with model judgment only as the
last rule.

```text
route_after_verify(state) ->
  all acceptance pass, no must-fix open        -> test
  verify_iterations >= max_verify_iterations   -> escalate(budget)
  any blocker with severity=blocking           -> escalate(blocked)
  otherwise                                    -> iterate_v
```

Routers to define: `route_after_discover`, `route_after_plan`,
`route_after_verify`, `route_after_test`, `route_after_deliver`, and
`route_failure` (below). They live in `references/run-state.md`; `SKILL.md` gets
one table of router names and their route sets.

Acceptance: every route name in the table resolves to a phase in the transition
table; each router's rules are ordered deterministic-first.

### Slice A4 — Budget, ceilings and a named fallback for every cycle `level_2`

The research's recursion-limit rule, translated: a global `max_transitions`
plus a per-loop iteration counter, and **no cycle without a fallback edge**.

- Defaults: `max_verify_iterations: 3`, `max_test_iterations: 3`,
  `max_transitions: 40` (`lean`: 2/2/20; `deep`: 5/5/80). Overridable per run,
  recorded in state.
- Fallback target is always `ESCALATE`: stop, write `termination.reason`, report
  what is still failing and what is needed — never a silent extra lap.
- `termination.reason` enum: `acceptance_met`, `hard_gate_blocked`,
  `retry_ceiling`, `budget_ceiling`, `user_stop`, `unsafe_action_refused`.
- Report the remaining budget in REPORT, alongside the existing evidence.

Acceptance: a task engineered to never pass VERIFY stops at the third iteration
with `retry_ceiling` and reports the failing criterion instead of looping.

### Slice A5 — Checkpoint, resume, and interrupt-before `level_2`

- **Checkpoint** on every node exit (write `run.json` before routing).
- **Resume**: DISCOVER first checks for an unfinished `run.json`; if found, it
  summarizes phase, acceptance status and blockers and offers resume-or-restart
  instead of re-deriving context. This makes the existing `handoff` subskill
  generate its document *from state* rather than from prose recall.
- **Interrupt-before list**, machine-readable, replacing scattered per-phase
  wording: `["live_deploy", "merge", "release_tag", "publish", "secret_write",
  "destructive_command", "external_write"]`. Hitting one of these writes state,
  pauses, and requires explicit approval recorded in `approvals[]`.

This is the strongest fit between the research and this repo's existing rules:
`level_3` and the deploy policy already describe interrupts; the change is to
make them one list an agent can check, not prose it must remember.

Acceptance: a run that hits a deploy node without a recorded approval pauses and
records `hard_gate_blocked`; resuming after approval continues from the same
state.

### Slice A6 — Failure taxonomy for the repair cycle `level_1`

The report's "self-healing repair loop" needs a classifier, otherwise ITERATE is
one undifferentiated blob. Add `route_failure(state)`:

| Failure class | Route | Subskill / reference |
|---|---|---|
| `test_fail` | ITERATE_V with the failing test as the loop | `skills/tdd`, `skills/diagnosing-bugs` |
| `bug_or_regression` | ITERATE_V, reproduce first | `skills/diagnosing-bugs` |
| `lint_or_type_fail` | EXECUTE, mechanical, `level_0/1` | — |
| `ci_fail` | ITERATE_T | `references/test-and-security.md` |
| `security_finding` | ITERATE_T, `level_2` | `references/test-and-security.md` |
| `copilot_must_fix` | ITERATE_T | `references/backlog-and-copilot.md` |
| `merge_conflict` | EXECUTE | repo convention |
| `env_or_tooling_error` | ESCALATE after one retry | `references/adapters.md` |
| `ambiguous_requirement` | ESCALATE / `grilling` | `skills/grilling` |

Each class carries a structured payload (command, exit code, evidence ref) into
the repair node — the research's "route the stack trace to the repair node",
which is exactly what `diagnosing-bugs` already demands informally.

Acceptance: each class routes to a named target; no class falls through to
"try again".

### Slice A7 — Wire state into what already exists `level_1`

- **Telemetry**: `scripts/telemetry_record.py` already records phase events;
  emit them from the same transition call so there is one clock, not two.
- **Result logs**: add `run_state_ref`, `counters`, `termination_reason` to the
  eval result schema and `evals/result-log-template.json`.
- **Report template**: add budget used, termination reason, and resume history to
  `references/report-template.md` and the REPORT phase list.
- **Memory**: `NEXT:` lines can be generated from unresolved blockers.

### Slice A8 — Docs, validator, evals, release `level_1` / `level_3`

- `scripts/validate_skill.py`: require `references/run-state.md` and
  `schemas/run-state.schema.json`; validate example manifests against the schema;
  keep the 500-line body check (it is the forcing function).
- `evals/trigger-cases.json`: no new triggers needed for Part 1.
- `evals/outcome-scenarios.md`: add scenarios for invalid transition, retry
  ceiling, interrupted resume, interrupt-before-deploy.
- `CHANGELOG.md`, `VERSION` → `0.1.0-alpha.3`; `development.md` decision entry;
  `memory.md` durable decisions; `paper.md` rationale.
- Release remains `level_3` (maintainer approval).

### Sequencing and cost

| Order | Slice | Depends on | Route |
|---:|---|---|---|
| 1 | A1 schema + reducers | — | `level_2` design, CAVEMAN CODE |
| 2 | A2 transitions + script | A1 | `level_2` |
| 3 | A3 routers | A2 | `level_2` |
| 4 | A4 budgets + fallback | A1 | `level_2` |
| 5 | A6 failure taxonomy | A3 | `level_1` |
| 6 | A5 checkpoint/resume/interrupts | A1, A2 | `level_2` |
| 7 | A7 wiring | A1-A6 | `level_1` |
| 8 | A8 docs/validator/evals/release | all | `level_1`, release `level_3` |

First batch: A1 + A2. They are the kernel; A3-A6 are cheap once state exists.

### What Part 1 deliberately does not do

- No new mode, no new syntax, no graph authoring. The linear loop stays the
  default and gets *cheaper* to run, not heavier.
- No enforcement runtime: in tools that cannot run scripts, `run.json` is still
  written and the tables are still followed by the agent; the script is the
  determinism upgrade where it is available.
- No claim that this improves task success until the comparative evals in the
  competitive assessment's gate 1 measure it.

---

## 3. Plan 2 — a graph-based mode for end-to-end-loop

### 3.1 Why a mode is needed at all

Part 1 makes the *fixed* topology explicit. Graph mode is for work whose topology
is not fixed at plan time: multiple candidate solutions scored against a rubric,
fan-out over independent slices with a join, event-driven repair against CI,
runs that must pause for a human and resume days later.

Forcing that into DISCOVER→…→REPORT either flattens it (losing the parallelism)
or smuggles it into ITERATE (losing the visibility). That is the honest case for
a mode.

### 3.2 Boundary with the `graph-engineer` skill

A sibling skill, `graph-engineer`, is installed in this environment and already
covers **the work graph**: division of labour, PRDs, exclusive file zones, model
tiering, parallel workers, two human gates, merge/verify. Graph mode must not
re-implement it.

The split, stated once and enforced in both directions:

| | `graph-engineer` | `end-to-end-loop: graph` |
|---|---|---|
| Answers | *Who does which part, in isolation from whom* | *What happens next, given the current state* |
| Primitive | Node = worker with a zone and a PRD | Node = phase-typed step with a state contract |
| Shape | Fan-out then join (mostly acyclic) | Cycles, conditional routes, interrupts |
| Owns | Zones, tiers, cost estimate, PRD roast | State, reducers, budgets, checkpoints, gates |
| Human gates | Gate A (goal/PRD), Gate B (graph/cost) | Interrupt-before list, `level_3` |

**Composition rule:** a graph-mode node may declare `dispatch: graph-engineer` to
run a fan-out; `end-to-end-loop` keeps ownership of state, evidence, and gates,
and treats the fan-out's merged result as one node output. Graph mode does not
grow its own zone/worker/PRD machinery.

Recommendation: keep graph mode in this repo (it is the state layer these gates
already live in) and add a one-paragraph pointer in both skills so neither claims
the other's job.

### 3.3 When graph mode fires — and when it must refuse

Use graph mode only if **at least one** holds:

1. **≥2 distinct cyclic loops** with different exit criteria (e.g. refine-until-
   rubric *and* repair-until-CI-green).
2. **Fan-out ≥3 independent slices** that need a join gate before VERIFY.
3. **The run must survive interruption** — a human approval wait, an overnight
   CI run, a session boundary.
4. **Routing depends on runtime signals** (evaluator score, CI status, tool
   output) rather than on a plan written up front.

Otherwise: say in one line that a graph adds nothing here and run the linear loop
with Part 1's state kernel. Refusing to build a graph is a correct outcome —
same posture `graph-engineer` takes at its `<3 subtasks` threshold.

### 3.4 Use cases (the presets)

Presets matter more than authoring: most users should never write a graph file.
Six use cases, each shipping as a named preset with fixed nodes, cycles, caps and
evidence.

**UC1 `graph:repair` — self-healing CI/test repair.** *Highest immediate value;
it is the workflow this repo already lives in (PR babysitting).*
Nodes: `run_checks → classify_failure → repair → run_checks`.
Router: `route_failure` from Slice A6. Cap: 2 repairs per failure class, then
ESCALATE with the diagnosis and a proposed patch. Evidence: command + exit code
per lap. Refuses to disable or skip a test to go green (existing rule).

**UC2 `graph:refine` — evaluator-optimizer.**
Nodes: `draft → evaluate → (revise → evaluate)*`. Router: rubric threshold.
Cap: 3 revisions, then deliver best-so-far *and say it is best-so-far*.
Use for: docs and README rewrites, skill/prompt authoring, API surface design,
report quality. Requires an explicit rubric in state — a critic without a rubric
is an opinion loop, and must be refused.

**UC3 `graph:fanout` — backlog slices in parallel with a join.**
Nodes: `slice_plan → [worker₁..workerₙ] → join_verify → integration_test`.
Delegates the worker layer to `graph-engineer` when installed; otherwise runs
sequentially in fresh contexts and labels the verifier `SELF-REVIEW`. Zones must
be disjoint or the split is wrong. Join gate is a single VERIFY over the merged
result, never per-worker self-certification.

**UC4 `graph:react` — bounded investigation.**
Nodes: `search → read → hypothesize → (more?)`. For unfamiliar codebases and
"why is this happening" questions. Cap: transitions, not confidence. Exit: the
DISCOVER questions have answers with `path:line` evidence, or budget hits and it
reports what is still unknown. This is the loop that most often runs away today.

**UC5 `graph:release` — release with human interrupts.**
Nodes: `readiness → INTERRUPT(approve) → deploy → smoke → (rollback | report)`.
The deploy policy is unchanged; the graph adds durable pause/resume across the
approval wait and an explicit rollback edge on smoke failure. This is the case
where checkpointing actually pays for itself.

**UC6 `graph:longrun` — multi-session delivery.**
Not a topology so much as a posture: any preset above plus checkpoint/resume and
a `handoff` document generated from state at each session boundary.

### 3.5 Syntax

Two layers, deliberately: an invocation layer everyone uses, and an authoring
layer few will.

**Layer 1 — invocation (user-facing, no files).** Extend the existing options
table with one row: `graph`. Presets are selected with a colon:

```text
end-to-end-loop: graph:repair + github-copilot
end-to-end-loop: graph:refine + deep            # rubric required
end-to-end-loop: graph:fanout + backlog
end-to-end-loop: graph                          # agent proposes a topology, human confirms
```

Bare `graph` triggers a proposal: the agent renders the topology it intends to
run (mermaid + caps) and asks for confirmation before the first node. That
confirmation is the graph-mode equivalent of Gate B, and is the only new
human gate.

**Layer 2 — authoring (`.end-to-end-loop/graph.json`).** JSON, not YAML, so the
existing dependency-free validator can read it without a parser. A commented
example (fields, not literal comments):

```json
{
  "schema_version": "1.0",
  "name": "ci-repair",
  "entry": "run_checks",
  "state": {
    "findings":  {"type": "list", "reducer": "append_unique", "key": "id"},
    "evidence":  {"type": "list", "reducer": "append", "immutable": true},
    "draft":     {"type": "string", "reducer": "replace"},
    "iterations":{"type": "map<string,int>", "reducer": "increment"}
  },
  "budget": {"max_transitions": 30, "max_iterations": {"repair": 2}},
  "nodes": {
    "run_checks": {"phase": "TEST",    "level": "level_0", "produces": ["evidence"]},
    "classify":   {"phase": "VERIFY",  "level": "level_1", "produces": ["findings"]},
    "repair":     {"phase": "EXECUTE", "level": "level_1", "lane": "caveman-code",
                   "writes": ["src/**", "tests/**"], "produces": ["evidence"]}
  },
  "edges": [
    {"from": "run_checks", "to": "classify"},
    {"from": "classify", "router": "route_failure",
     "when": {"green": "END", "test_fail": "repair", "security_finding": "repair",
              "env_or_tooling_error": "ESCALATE"}},
    {"from": "repair", "to": "run_checks"}
  ],
  "routers": {
    "route_failure": {
      "inputs": ["findings", "iterations", "budget"],
      "rules": [
        {"if": "findings.empty", "then": "green"},
        {"if": "iterations.repair >= budget.max_iterations.repair", "then": "ESCALATE"},
        {"else": "findings[0].class"}
      ]
    }
  },
  "interrupts": {"before": ["deploy", "merge", "publish"]},
  "fallback": "ESCALATE",
  "checkpoint": {"path": ".end-to-end-loop/run.json", "on": "node_exit"}
}
```

Design decisions embedded in that shape:

- **`phase:` on every node** — a graph node inherits the gates of the loop phase
  it is typed as. A graph can *add* nodes; it can never remove a gate. This is
  the single most important rule: it keeps Non-Negotiables 1-5 intact under an
  arbitrary topology.
- **`lane:`** — any node that produces code declares its CAVEMAN lane, so the
  hard gate survives graph mode.
- **`level:`** — reuses `level_0..level_3`, so model routing and human approval
  are the existing ones, not a parallel system.
- **`writes:`** — zones, borrowed from `graph-engineer`, only meaningful for
  parallel branches; must be disjoint.
- **`END` and `ESCALATE`** — reserved node names, always present.
- **Reserved routes** in every router: `green`, `blocked`, `budget_exhausted`.

**Layer 3 — the chat fallback.** Tools that cannot write files use a fenced
` ```loop-graph ` block with the same JSON. Reports render the graph as mermaid
so a reviewer sees the topology and which edges actually fired.

**Static checks** (`scripts/graph_validate.py`, dependency-free):

1. every node reachable from `entry`;
2. every cycle has at least one edge that can leave it;
3. every router mapping is total — every route name resolves to a node,
   `END`, or `ESCALATE`;
4. `fallback` present, and any cycle has an iteration cap;
5. code-producing nodes declare a `lane`;
6. parallel branches have disjoint `writes`;
7. every node with a `level_3` effect appears in `interrupts.before`;
8. every node has a `phase`, and no node claims a phase gate it does not satisfy;
9. reducers declared for every accumulating key.

Failing any check refuses to run the graph. Determinism first, model judgment
after — the same posture as Slice A3.

### 3.6 Delivery phases

Graph mode must not be built before the state kernel exists. Schema first is the
research's own directive and this repo's ordering constraint.

| Phase | Release | Content | Acceptance |
|---|---|---|---|
| B0 | `alpha.3` | Nothing. Part 1 only. | State kernel green |
| B1 | `alpha.4` | `references/graph-mode.md` + `skills/graph-mode/SKILL.md`; presets `graph:repair` and `graph:refine` as prose topologies running on the Part-1 kernel; no authoring, no new scripts | Two presets run end to end with caps and evidence; 4 outcome scenarios; trigger cases for graph vs linear vs `graph-engineer` |
| B2 | `alpha.5` | `graph.json` authoring + `scripts/graph_validate.py` + mermaid render in the report | All 9 static checks enforced; a graph with an unbounded cycle is refused |
| B3 | `0.2.0` | `graph:fanout` with `graph-engineer` delegation; `graph:react`, `graph:release`, `graph:longrun` | Delegation boundary tested in both skills; resume-across-session test |
| B4 | gate | Comparative evals: linear vs `graph:repair` on repair tasks, linear vs `graph:refine` on doc tasks | Task success, laps, wall time, tool calls, interventions recorded before any claim that graph mode helps |

### 3.7 Risks

- **Duplication with `graph-engineer`.** Mitigation: the boundary table in 3.2,
  a pointer in both skills, and no worker/PRD/zone machinery here beyond `writes`.
- **Ceremony creep.** Mitigation: the four-condition threshold in 3.3, presets
  over authoring, and refusal as a valid outcome.
- **`SKILL.md` line budget.** Graph mode gets one options-table row and one
  reference-routing line in the core; everything else lives in the subskill.
- **False determinism.** In prose-only tools, routers are still evaluated by a
  model. Reports must say which checks were script-enforced and which were
  agent-judged — the same honesty rule `graph-engineer` applies with
  `SELF-REVIEW`.
- **Token cost.** A graph that never cycles costs more than the linear loop for
  nothing. B4's comparative evals exist to catch that, and a negative result
  should shrink the mode, not be explained away.

### 3.8 Decisions needed from the maintainer

1. **Home of graph mode** — this repo as a packaged subskill (recommended: the
   gates and state live here), or a companion to `graph-engineer`?
2. **`graph.json` vs `graph.yaml`** — recommendation JSON, because
   `validate_skill.py` and `graph_validate.py` stay dependency-free.
3. **Preset naming** — `graph:repair` colon syntax (recommended, composes with
   the existing `+` option syntax) or separate mode names (`repair-loop`)?
4. **Does bare `graph` require confirmation before the first node?**
   Recommendation yes; it is cheap and it is where being wrong is cheapest.

---

## 4. Summary

Part 1 is not a new direction: it is the existing `alpha.3` backlog, made
sharper by four things the research names and the backlog did not — reducers,
node/router separation, a failure taxonomy, and interrupt-before as a list. It
should ship first and alone.

Part 2 is genuinely new surface. It is worth building only for the four
conditions in 3.3, only after the state kernel exists, and only if the
comparative evals in B4 show it beats the linear loop on the tasks it claims.
