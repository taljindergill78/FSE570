"""PACER Analyzer: court records (stub for Phase 4; PACER paywalled)."""

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
    """Stub: PACER/court data not integrated (paywalled). CourtListener optional later."""
    ev = Evidence(
        evidence_id=f"{entity.entity_id}_pacer_stub",
        entity_id=entity.entity_id,
        date="",
        source_type="court_record",
        risk_category="legal",
        summary="PACER/court record analysis not yet integrated (paywalled). CourtListener may be added later.",
        source_uri="",
        raw_location=None,
        confidence=0.0,
        attributes={"stub": True},
    )
    return [ev]
