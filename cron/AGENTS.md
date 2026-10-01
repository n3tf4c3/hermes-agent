# Cron, scheduling and kanban ownership

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Store: `jobs.py`. Tick loop: `scheduler.py` and `scheduler_*.py`. Kanban: `../hermes_cli/kanban*.py`, `../tools/kanban_tools.py` and `../plugins/kanban/`.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Preserve inactivity/script timeouts, catch-up/grace, error reporting and overlap/claim guards. A live but active job must not be killed as idle.
- The ticker binds each owning profile for the whole tick, including pre-loop config/probes. Cron ownership is not gated by the messaging multiplex flag.
- Release claims under the key they were registered with, reclaim ticked-home state and stand down when that profile has its own gateway.
- Work that must survive process restarts uses persisted cron/kanban ownership; process-local background delegation is not durable scheduling.
- Kanban delivery/notifications use the owning profile. Prompt injection is gated on task ownership, not merely tool visibility; preserve the descendant-path fence.

## Conditional reference
Cron for schedule fields, watchdogs and every ticker/profile change; Kanban for board storage, dispatch, claims, prompt injection or notifications; Tests for the matching ownership regression.

## Validation
Use `scripts/run_tests.sh` with the affected cron/kanban test files from the root; validate profile alternation for ownership changes.
