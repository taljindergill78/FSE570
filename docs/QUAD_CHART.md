## Autonomous OSINT Investigation Swarm — Quad Chart (Status Update)

**Date**: 2026-02-28  
**Course/Team**: FSE570 Capstone — Autonomous OSINT Investigation Swarm  
**Goal**: Modular, multi-agent OSINT pipeline for **corporate/entity risk assessment** using **trusted, citable, reproducible** sources.

**Team roster (from Team Charter / Proposal)**:
- Taljinder Singh
- Aditya Pokharna
- Raj Kumar Mahto
- Arnab Mitra
- Jacob Kuriakose

**Working role leads (initial)**:
- **Data gathering & preprocessing**: Taljinder
- **Modeling & backend development**: Arnab, Raj
- **Frontend & visualization**: Aditya
- **Deployment & documentation**: Jacob

| **Latest accomplishments / KPIs** | **Next major tasks (RAIL) / Owners** |
|---|---|
| - **Defined multi-layer architecture**: `agents/`, `mcp_layer/`, `reflexion_layer/`, `knowledge_graph/`, `output_layer/` — all implemented in code.<br>- **Designed end-to-end flow**: natural-language query → Lead Agent → specialist agents → Reflexion → knowledge graph → risk dashboard + evidence report + audit trail.<br>- **Identified & integrated initial data sources**: SEC EDGAR (filings) + NHTSA recalls (DOT DataHub).<br>- **Evidence-first schema**: structured **Evidence** (citable claims) + **Entity** schema for audit-ready, reproducible reporting.<br>- **Pipeline runs end-to-end on stub data**: full flow works with a Flask web demo showing risk scores, gaps, evidence, and audit events (note: Legal + Social Graph are still stubs).<br>- **Unit test suite** across all major layers (`pytest tests/unit -v`).<br><br>**KPIs**:<br>- **2 sources integrated** (SEC + NHTSA)<br>- **~90 evidence rows** (Tesla test run; generated locally) | - **Replace stub agents with real data sources (highest priority)**:<br>  - Sanctions screening: integrate **OFAC SDN** + match logic — **Raj, Arnab**<br>  - Legal docs: **CourtListener/RECAP** integration + citations — **Jacob, Raj**<br>  - Beneficial ownership: **OpenCorporates** or curated dataset — **Arnab, Raj**<br>  - Adverse media: **GDELT** integration + cited evidence — **Taljinder, Aditya**<br><br>- **Multi-entity demo**: add +1–2 entities w/ identifiers (CIK/ticker) — **Taljinder, Raj**<br>- **Demo polish**: clearer labeling (real vs stub), error reporting, one-command run — **Aditya, Jacob** |
| **Major risks / barriers / obstacles** | **Remaining major activities / plan to complete** |
| - **Data access constraints**: SEC rate-limits; some sources are paywalled (PACER); social platforms have restrictive ToS.<br>  - **Mitigation**: use `.env` + caching; prioritize open, citable sources (SEC, NHTSA, CourtListener, OFAC, GDELT).<br>- **Coverage gaps**: Legal + Social Graph are stubs → thin AML results until replaced.<br>  - **Mitigation**: replace **sanctions + court docs** stubs first.<br>- **Entity resolution**: registry-based only (works for Tesla, limited generalization).<br>  - **Mitigation**: expand registry; add fuzzy matching + ID-based resolution.<br>- **Scoring interpretability**: mean confidence \(\neq\) severity/materiality.<br>  - **Mitigation**: add source reliability weighting + severity heuristics.<br>- **Reproducibility vs storage**: caching artifacts increases storage needs.<br>  - **Mitigation**: keep `data/` ignored; keep only `.gitkeep` placeholders.<br>- **Performance**: more sources/agents increases latency.<br>  - **Mitigation**: keep Flask runs bounded with caching. | - **Complete “proposal demo” loop**: AML prompt triggers corp structure, ownership, sanctions, transactions, adverse media (with at least sanctions + court docs on real data).<br>- **Reflexion pattern**: self-assessment → gap ID → retrieval → convergence; show gaps, follow-ups, and confidence changes.<br>- **Knowledge graph & outputs**: per-run artifacts (report + audit + graph), stable citations, and interactive drill-down.<br>- **Evaluation**: citations/claim, coverage by category, runtime, completeness vs manual workflow.<br><br>**Timeline**:<br>- Next 1–2 weeks: OFAC + CourtListener + multi-entity demo + KPIs<br>- Following 1–2 weeks: adverse media + structure mapping + scoring/UI improvements<br>- Final weeks: evaluation write-up + demo polish + deployment runbook |

**Presenter assignment (one quadrant each)**:
- Top-left (Accomplishments/KPIs): **Arnab Mitra**
- Top-right (Next tasks/RAIL): **Taljinder Singh**
- Bottom-left (Risks/Barriers): **Jacob Kuriakose**
- Bottom-right (Remaining plan/timeline): **Raj Kumar Mahto**

**Additional support role (non-quadrant, optional)**:
- **Metrics & demo operator / Q&A**: **Aditya Pokharna** (runs the demo live, captures KPIs, answers technical questions)

