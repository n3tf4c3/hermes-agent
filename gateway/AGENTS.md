# Messaging gateway, adapters and delivery

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
`run.py` is the facade; inspect `run_*.py` by phase. Sessions: `session*.py`. Adapters: `platforms/`. Authorization: `authz_mixin.py`. Slash dispatch: `slash_commands_*.py` and `run_busy.py`.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Both inbound guards (base adapter and busy gateway) must bypass approval/control commands; never fix just one.
- Preserve stream-is-the-message delivery: no duplicate final send, and no background completion attributed to a different conversation/profile.
- The gateway has its own raw YAML loader. Resolve configuration at the actual consumer; do not assume CLI DEFAULT_CONFIG covers gateway settings.
- Messaging gateway survives desktop exit; lifecycle, locks and remote-profile scope are distinct. Paired off-turn login remains authorization-gated.
- Every adapter/turn/callback/child environment binds the owning profile. Under multiplex, unscoped reads fail closed and adapter YAML never leaks into process-global env.

## Conditional reference
The TWO message guards for inbound control; Streaming delivery for message output; Background notifications for completion; /login for auth; Lifecycle for process ownership; Profile scope for any config/identity/secrets change.

## Validation
`scripts/run_tests.sh tests/gateway/` from the root. Profile changes also exercise real A→B→A scope.
