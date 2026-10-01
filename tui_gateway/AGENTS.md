# TUI transport, RPC and session state

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Python entry: `server.py`; RPC handlers: `methods_*.py`. Wire contracts: `contracts/`. Ink frontend: `../ui-tui/`; shared transport: `../apps/shared/`. Backend has TUI, desktop and dashboard consumers.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Python owns sessions/tools/model/slash behavior; TypeScript owns rendering. Do not move agent behavior into the renderer.
- Preserve newline JSON-RPC, correlated server requests and events. Approval/clarify/sudo/secret/vault requests must retain response correlation, deadlines and cancellation.
- Wire contracts are declared in Python and generated for TypeScript; update both via the documented generator, not hand-edited divergent schemas.
- RPC handlers bind the complete profile runtime scope. Setting only a home override is insufficient for config/secrets/provider/process state.
- Shared subagent snapshots preserve canonical identity and ownership; slash commands keep the backend dispatch contract and consumer ordering.

## Conditional reference
Transport for wire/request changes; Profile scope for any handler that reads config or creates runtime state; Key surfaces for features; Shared snapshots for children; Slash flow for commands; Dev commands for frontend validation.

## Validation
Python: `scripts/run_tests.sh tests/tui_gateway/` from the root. Frontend checks/tests run in `ui-tui/` using that package manifest.
