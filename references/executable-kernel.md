# Executable Control Kernel

Use `scripts/loop_kernel.py` as a machine-readable control plane for multi-step,
interrupted, budget-sensitive, or release work. It supplements policy; it does
not execute tools, grant permissions, or make remote side effects idempotent.

## Run contract

1. Initialize `.end-to-end-loop/loop-state.json` with run id, goal, mode,
   delivery class, budgets, and acceptance criteria.
2. Run `preflight` with observed capabilities and risks. Load only returned
   references. Record `selected_context_bytes` as a context-cost proxy.
3. Use `transition` only for allowed phase changes.
4. Use `account` to add observed iterations, tool calls, elapsed minutes, and
   context bytes. Never invent unavailable token or cost data.
5. Use `retry` for repeated failures.
6. Stop on a hard blocker, retry ceiling, budget ceiling, completed REPORT, or
   fully passed acceptance set.
7. Persist state atomically. On resume, validate before taking another action.

Lean/standard/deep defaults are ceilings, not spending targets. Stop as soon as
acceptance criteria pass.

## Commands

```bash
python3 scripts/loop_kernel.py init \
  --run-id task-123 \
  --goal "Deliver verified change" \
  --mode standard \
  --delivery repo-only

python3 scripts/loop_kernel.py preflight \
  --code-change \
  --capability caveman-code \
  --risk dependencies

python3 scripts/loop_kernel.py transition --to PLAN
python3 scripts/loop_kernel.py account --tool-calls 4 --context-bytes 12000
python3 scripts/loop_kernel.py retry --failure-key failing-integration-test
python3 scripts/loop_kernel.py status
```

The caller owns acceptance-criterion insertion and evidence capture through the
Python API in alpha.3. CLI coverage can expand after comparative usage shows the
smallest useful interface.
