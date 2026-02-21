"""Structure Mapper: map corporate networks, beneficial ownership (stub for Phase 4)."""

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
    """
    Stub: no OpenCorporates or structure data yet.
    Returns a single Evidence row indicating no data.
    """
    ev = Evidence(
        evidence_id=f"{entity.entity_id}_structure_mapper_stub",
        entity_id=entity.entity_id,
        date="",
        source_type="other",
        risk_category="governance",
        summary="Structure Mapper: beneficial ownership and corporate network data not yet integrated (OpenCorporates planned).",
        source_uri="",
        raw_location=None,
        confidence=0.0,
        attributes={"stub": True},
    )
    return [ev]
