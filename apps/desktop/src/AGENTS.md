# Desktop renderer, slash palette and Bot Mode

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Routes/views: `app/`. Shared state: `store/`. Pure helpers: `lib/`. Bot Mode: `plugins/hermes-bots/`. Framework-independent RPC client: `../../shared/`. Also apply parent desktop/root guides.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Desktop has its own composer/transcript and attaches local sessions through `hermes gateway ensure --json`. Private one-use control tickets authenticate the transport; closing or switching the viewer never stops its gateway. Do not fall back to an independent local serve owner.
- Slash palette filters discovery; backend capability and command policies authorize execution. Preserve skill/quick-command discovery and explicit unsupported-command results on canonical transport.
- One bot equals one canonical forever-chat identified by name, not a stored session-id pin. Recency never wins; canonical Bot Chats stay hidden from normal recents and must not be duplicated on rename/refresh.
- Transport teardown/reconnect, stale async guards and profile re-homing obey the parent authority contract.
- Free-tier UI pulls profile-scoped backend state and preserves signed-in/guest/loading/error transitions; no latched entitlement or credentials in renderer state.

## Conditional reference
Desktop local execution for gateway ownership/tickets/transport; Slash commands for palette/dispatch; Bot Mode for canonical identity, rename, recents and lifecycle; Free-tier surfaces for auth/entitlement.

## Validation
Use the renderer tests/scripts from the desktop manifest; prove identity/refresh/rename behavior for Bot Mode changes.
