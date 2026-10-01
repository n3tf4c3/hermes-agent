# Tools, registry, toolsets and backends

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Registry/discovery: `registry.py` and `../model_tools.py`. Toolsets: `../toolsets.py`. Terminal backends: `environments/`. Delegation: `delegate_tool.py`. Start with the relevant tool and its topical siblings.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Settle the root footprint ladder before adding a core tool. Local/custom integrations use plugins; new core surface requires an explicitly requested contribution.
- Handlers return JSON strings. Registration is auto-discovered; package tools use their tool.py entry and required __init__.py.
- Tool schema descriptions cannot name tools from another toolset or expose machine-specific home paths. check_fn is reachability/opt-in, never session surface.
- Preserve agent-level tool interception, child-local tool-name sets, provider/profile scope and bounded subprocess environments.
- Native vision content is history, not a one-shot payload. Subprocess spawning uses the common environment builder; teardown signals the parent first.
- Delegated work preserves ownership, result delivery and capability limits. Do not add offset/limit truncation to instructional tools.

## Conditional reference
Registry/discovery for registration; Adding a core tool for approved core contributions; Toolsets for capability schema; Backends/providers for process/env/vision; Delegation for child lifecycle.

## Validation
`scripts/run_tests.sh tests/tools/` from the root, plus the specific integration path affected.
