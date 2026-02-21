"""Influence Mapper: influence and centrality (stub for Phase 4)."""

from __future__ import annotations

from typing import List

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner.types import SubTask


def run_stub(
    entity: Entity,
    task: SubTask,
    context: InvestigationContext,
) -> List[Evidence]:
    """Stub: no influence mapping data yet."""
    ev = Evidence(
        evidence_id=f"{entity.entity_id}_influence_stub",
        entity_id=entity.entity_id,
        date="",
        source_type="other",
        risk_category="network",
        summary="Influence mapping not yet integrated (social graph data required).",
        source_uri="",
        raw_location=None,
        confidence=0.0,
        attributes={"stub": True},
    )
    return [ev]
