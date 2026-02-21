#!/usr/bin/env python3
"""Run the Lead Agent on a natural-language investigation query (Phase 3 demo)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agents.lead_agent import LeadAgent


def main() -> None:
    ap = argparse.ArgumentParser(description="Run Lead Agent: resolve entity, decompose tasks, collect evidence.")
    ap.add_argument("query", nargs="?", default="Investigate Tesla for money laundering", help="Investigation query")
    ap.add_argument("--data-root", type=Path, default=ROOT / "data", help="Data directory (raw/processed)")
    args = ap.parse_args()

    agent = LeadAgent(data_root=args.data_root)
    ctx = agent.run(args.query)

    print("Query:", ctx.get_query())
    entity = ctx.get_entity()
    if entity:
        print("Entity:", entity.entity_id, entity.name, entity.identifiers)
    else:
        print("Entity: (unresolved)")
    print("Tasks:", len(ctx.get_tasks()))
    for t in ctx.get_tasks():
        print("  -", t.task_type, "->", t.target_agent)
    findings = ctx.get_all_findings()
    print("Findings:", len(findings))
    for agent_id, results in ctx.results.items():
        print("  ", agent_id, ":", len(results), "evidence items")


if __name__ == "__main__":
    main()
