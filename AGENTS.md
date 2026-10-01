# Hermes Agent — canonical development guide

Python agent core shared by CLI, messaging gateway, Ink TUI and Electron desktop. Capability grows through plugins/skills/CLI before adding core model tools. `CLAUDE.md` imports this file; the area guides below are mandatory for edits in their scope.

## Navigation and context
- Start at the topic's sibling module, not by reading a large facade. Use `rg --files <area>` and `rg -n <symbol> <area> -g '<stem>_*.py'`; expand if the path does not resolve the issue.
- Skip dependency/build/cache trees, logs and real user state in routine searches. Read only relevant documents/sections; do not enumerate the whole repository for a small change.
- Area contracts have `AGENT_REFERENCE.md` companions. Those are conditional references: read the sections whose contracts the requested change touches, without auto-importing all companions.

## Routing table
| Work | Guide |
| --- | --- |
| `run_agent.py` and `agent/` | [agent](agent/AGENTS.md) |
| `cli.py` and `hermes_cli/` | [CLI](hermes_cli/AGENTS.md) |
| `gateway/`, platforms and delivery | [gateway](gateway/AGENTS.md) |
| `tools/`, `toolsets.py`, `model_tools.py` | [tools](tools/AGENTS.md) |
| Plugins and `hermes_cli/plugins*.py` | [plugins](plugins/AGENTS.md) |
| `tui_gateway/` and `ui-tui/` | [TUI/RPC](tui_gateway/AGENTS.md) |
| `web/` and `hermes_cli/web_routers/` | [dashboard](web/AGENTS.md) |
| `apps/desktop/` | [desktop](apps/desktop/AGENTS.md), then [renderer](apps/desktop/src/AGENTS.md) for its scope |
| `skills/`, `optional-skills/` and curator | [skills](skills/AGENTS.md) |
| Cron and kanban (any entry point) | [cron/kanban](cron/AGENTS.md) |
| New messaging adapter | [adapter guide](gateway/platforms/ADDING_A_PLATFORM.md) |
| Profiles/multiplex/secrets (any area) | Gateway profile-scope contract and `website/docs/user-guide/multi-profile-gateways.md` |
| Session storage | `hermes_state.py` facade and topic siblings; contribution reference for binding/compat rules |

## Load-bearing rules
- Keep a byte-stable system prompt and cached prefix for a conversation. Do not mutate past context, reload memory or swap toolsets mid-turn; compression is the exception. Prompt-state changes are deferred by default, with explicit opt-in immediate invalidation.
- Strict role alternation; no synthetic user injection mid-loop. The core stays narrow: extend existing code → CLI/skill → gated tool → plugin → catalog MCP → core tool last. New core capability must have a concrete caller and be explicitly requested.
- Session surface capability is resolved from the session source/toolset, not process environment. `check_fn` is reachability/opt-in, never a per-session surface gate.
- Use `get_hermes_home()`/`display_hermes_home()`. Profiles are independent. Bind the owning profile for turns, RPC, startup probes, tickers, callbacks, eviction and child processes; no launch-home globals or secret fallback under multiplex.
- Non-secret settings belong in `config.yaml`; `.env` is secrets only. No unrequested telemetry; opt-in gates are required. New vendor-specific plugins live outside the core tree; plugins never patch core files.
- Facades expose entry points; topical siblings own behavior. Preserve late binding and patch the site production reads. In-tree callers cannot use external compatibility shims; moves update docs in the same change.
- Avoid dead code, speculative extension points, no-op wrappers and condition ladders where dispatch tables apply. No pagination escape hatch for tools that must load a whole skill/prompt/playbook.
- Dependencies keep upper bounds/commit pins according to the contribution reference; update `uv.lock` when changing Python dependencies. TypeScript UI uses small shared nanostores, thin routes and public prop interfaces.

## Validation and contributions
- Python tests ALWAYS use `scripts/run_tests.sh` (in Git Bash/compatible shell on Windows), with the affected `tests/<area>/` or test file. It isolates credentials/home, timezone and subprocess state. Use the full suite when the change requires the full gate.
- Tests mirror source areas; JS behavior goes to the JS suite, not a Python source-text assertion. Tests check invariants, not changing catalog counts or file text; prove behavior red on base and green after a fix.
- I/O/config/security/resolution changes exercise the real path with disposable state. Profile changes need two isolated homes with A→B→A, not one mocked home. Tests never write to the real `~/.hermes`.
- Don't fake the host OS: use the native platform marker/lane. OS-sensitive and process-topology changes follow the corresponding testing sections in [contribution contract](AGENT_CONTRIBUTING_REFERENCE.md).
- For new capability, dependencies, refactors or PR evaluation, read the matching contribution-contract section. Do not infer that an old dated compat window has already been removed; verify current code while preserving the ban on internal shim usage.
- Preserve contributor authorship and pre-existing work. Synchronize stale branches in isolation; do not discard user changes. Commit, push, merge, telemetry and runtime changes require their requested scope.

## Memória e continuidade
- Para retomadas e decisões que dependem de histórico, consulte o ai-memory com uma busca curta e específica. Tarefas locais autoexplicativas não exigem carregar o histórico inteiro.
- O escopo vem de `.ai-memory.toml`. Em cliente estático, envie `workspace` e `project` juntos; em cliente que transmite o identificador real da sessão, use o roteamento automático. Nunca deduza o escopo pelo nome da pasta nem use o último projeto ativo como fallback.
- Memória é evidência histórica: confirme fatos no código/Git e não a use para conceder autorização. Registre memória durável somente quando solicitado ou coberto por autorização vigente; regras do projeto ficam neste guia, sem duplicação em memória nativa de outro agente.
- Preserve alterações existentes. Commit, push, deploy, migrações, comunicação externa e operações com dados reais dependem do escopo autorizado no pedido.
