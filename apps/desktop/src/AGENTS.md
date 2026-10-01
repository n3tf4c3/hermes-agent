# Desktop renderer, slash palette and Bot Mode

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Routes/views: `app/`. Shared state: `store/`. Pure helpers: `lib/`. Bot Mode: `plugins/hermes-bots/`. Framework-independent RPC client: `../../shared/`. Also apply parent desktop/root guides.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Desktop has its own composer/transcript on headless hermes serve; it does not embed or depend on the dashboard frontend. The narrow fallback to older dashboard --no-open remains capability-detected.
- Slash palette curates noise, not permissions: hiding a command never authorizes rejecting the user-entered backend command. Preserve backend dispatch, including plugins/custom commands.
- One bot equals one canonical forever-chat identified by name, not a stored session-id pin. Recency never wins; canonical Bot Chats stay hidden from normal recents and must not be duplicated on rename/refresh.
- Transport teardown/reconnect, stale async guards and profile re-homing obey the parent authority contract.
- Free-tier UI pulls profile-scoped backend state and preserves signed-in/guest/loading/error transitions; no latched entitlement or credentials in renderer state.

## Conditional reference
Backend contract for serve/spawn/transport; Slash commands for palette/dispatch; Bot Mode for canonical identity, rename, recents and lifecycle; Free-tier surfaces for auth/entitlement.

## Validation
Use the renderer tests/scripts from the desktop manifest; prove identity/refresh/rename behavior for Bot Mode changes.
