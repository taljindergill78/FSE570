# Evidence as Canonical Agent Input

All agents (Lead Agent and Specialist Agents) must consume **structured Evidence** (and optionally **Entity**), not raw JSON or HTML.

## Where evidence comes from

1. **MCP layer** — When an agent requests fresh data, it calls the MCP layer (e.g. `get_evidence_for_entity(entity, sources=["sec_edgar", "nhtsa"])`). The MCP layer uses the existing connectors and returns `List[Evidence]`.
2. **Evidence loader** — To use already-processed evidence (e.g. from a prior pipeline run), use `load_evidence_for_entity(processed_dir, entity_id)` from `mcp_layer`. This reads CSV files under `data/processed/<slug>/evidence_*.csv` and returns only rows whose `entity_id` matches.

## Contract

- **Input to agents:** `Entity` (with `entity_id`, `identifiers`, etc.) and/or `List[Evidence]`.
- **Output from agents:** Findings should be expressed as `Evidence` (or a type that maps 1:1 to Evidence) so that the Reflexion layer and output layer can consume them uniformly.
- Do **not** call `osint_swarm.data_sources` directly from agent code; use the MCP layer so that caching, auth, and future sources stay centralized.
