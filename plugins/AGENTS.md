# Plugin contracts, discovery and catalog

Root project rules apply. CLAUDE.md imports this local guide; detailed contracts live in [reference](AGENT_REFERENCE.md).

## Start here
Start at the plugin kind directory and its ABC/context/discovery surface. Authoring and canonical compatibility contract: `../website/docs/developer-guide/plugins/index.md`. Catalog assets: `../plugin-catalog/`.

Use scoped rg searches; expand only when the dependency/contract requires it. Read the sections listed below before changing the related behavior.

## Invariants
- Plugins operate inside their own directory/ABCs/hooks/ctx and never modify core files. Add a generic framework capability only for a concrete consumer.
- New memory backends and third-party-product integrations ship as standalone plugins, not new in-tree vendor providers. Existing providers may receive scoped fixes.
- Preserve plugin discovery ordering and lifecycle under the owning profile; importing the wrong facade is not proof that discovery has run.
- Do not remove/rename PluginContext methods; new params have optional defaults. Persisted/wire contracts require compatibility handling and tests with frozen plugins through real discovery.
- Internal code must not consume external compat shims. The old dated decomposition window is historical; inspect current code before removing compatibility.

## Conditional reference
Policy before adding an integration; Plugin kinds/discovery for loaders; Catalog for listing changes; Native compatibility for public contracts; Decomposition window only when investigating legacy support.

## Validation
Use `scripts/run_tests.sh` with the affected plugin/discovery tests from the root; exercise real discovery for compatibility changes.
