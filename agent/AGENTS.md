# Agent loop, prompts and compression

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Entry facade: `../run_agent.py`. Turn loop: `conversation_loop.py` and `turn_*.py`. Startup: `agent_init.py`. Prompt/context: `prompt_builder.py`. Compression: `compression_facade.py` and topic siblings. Providers: resolution/auth modules in this directory.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Preserve the cached prefix, strict message-role alternation, startup-only context loading and session turn lease. No synthetic user injection or silent toolset/prompt change.
- Agent-level tools are intercepted before generic tool dispatch. Preserve that path when changing tool execution.
- Profile secrets/config must resolve under the owning session scope; no real-home state in fixtures.
- Compression retains message validity, tool call/result pairing and the resume contract. Provider resolution and fallback must preserve the configured provider/auth boundary.

## Conditional reference
Shape/Agent loop for construction and turn phases; Message-flow invariants for prompt/history/tool changes; Compression for compaction; Model and provider resolution for routing; Memory/context engines/curator for memory.

## Validation
Python validation: `scripts/run_tests.sh tests/agent/` from the repository root.
