# CLI, config, profiles and updates

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
`../cli.py` is the facade; start at `cli_*_mixin.py` or the topic sibling. Slash registry: `commands.py`. Config: `config.py`, `config_defaults.py` and `cli_config_load.py`. Updates: `update_*.py`. Skins: `skin_engine.py`.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Slash aliases dispatch on the literal entered name; preserve one canonical registry/handler table and the shared goal-command lifecycle.
- Behavioral config belongs in DEFAULT_CONFIG/config.yaml; secrets only in .env. Bump config version only for an actual persisted migration. Respect each CLI/gateway/cron/TUI loader.
- Updates keep plan → snapshot → apply → restart by installation kind → verify → receipt. Never execute pulled code in the old interpreter or replace a failed branch guard with an unverified fallback.
- Profiles remain independent. Switching profile rebinds home/secrets/runtime; no mid-session prompt rebuild or inherited mutable config that couples profiles.
- Process identity uses canonical parsers/matchers, never substring heuristics; preserve fleet-wide restart, managed-install and Windows launcher contracts.
- Free-tier credentials and entitlement remain profile-scoped. Public launchers must not log or export secrets into unrelated sessions.

## Conditional reference
CLI architecture for mixin bindings; Slash registry for commands; Config system for any option/env/default change; Skin engine for rendering; Update pipeline for updater/process changes; Profiles for home/multiplex; Free tier for login/entitlement.

## Validation
`scripts/run_tests.sh tests/hermes_cli/` from the root. Windows process-topology changes follow the root contribution contract and native CI lane.
