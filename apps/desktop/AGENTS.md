# Desktop engineering and authority boundaries

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Electron/machine lifecycle: `electron/`. Renderer: `src/` and its local guide. Backend: root `tui_gateway/`. Visual/interaction contract: [DESIGN.md](DESIGN.md).

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Electron is authoritative for machine/runtime/filesystem facts; backend owns work/sessions/tools; renderer owns presentation and ephemeral UI. Model output never grants capability.
- Identity survives refresh/reconnect. Merge server truth, do not clobber optimistic state; reject stale async results and isolate the foreground session.
- Switching host/profile/session re-homes the appropriate state without rebooting unrelated work. Preserve caches and reference identity on no-ops.
- Credentials are one-use where the contract says so; connection checks exercise the real transport leg. Guest content cannot open links, files or execute actions by itself.
- Keep transport/framework boundaries thin; preserve compatibility without a second permanent control plane. Make feedback prompt and accurate; preserve onboarding and accessibility.
- Free-tier state is pulled from backend truth, not latched in renderer state. Reconnect and session changes must update entitlement consistently.

## Conditional reference
Authority/Identity/Server truth for state work; Switching context for host/profile navigation; Observable ladder for IPC/transport/auth; Guest content for opening/actions; Compatibility for upgrades; Onboarding/taste test for UX; Free tier for entitlement.

## Validation
Use the existing scripts/tests in `apps/desktop/package.json` for the affected layer; Python backend changes also use the root test runner. Read the reference validation/onboarding sections when that flow changes.
