"""Corporate Agent: SEC Analyzer + Structure Mapper; implements SpecialistAgent contract."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner.types import SubTask
from agents.specialist_agents.corporate_agent.sec_analyzer.analyzer import summarize_governance_red_flags
from agents.specialist_agents.corporate_agent.structure_mapper.mapper import run_stub as structure_mapper_run


class CorporateAgent:
    """Corporate intelligence agent: SEC filings, structure mapping (stub)."""

    AGENT_ID = "corporate_agent"

    def __init__(self, data_root: Optional[Path] = None):
        self.data_root = Path(data_root) if data_root else Path("data")

    @property
    def agent_id(self) -> str:
        return self.AGENT_ID

    def run(
        self,
        entity: Entity,
        task: SubTask,
        context: InvestigationContext,
    ) -> List[Evidence]:
        """
        For corporate_structure, sec_filings, transaction_patterns: fetch evidence via MCP,
        add governance summary. For beneficial_ownership: Structure Mapper (stub).
        """
        if task.task_type == "beneficial_ownership":
            return structure_mapper_run(entity, task, context)

        # Fetch evidence from MCP (SEC + NHTSA)
        try:
            from mcp_layer import get_evidence_for_entity
            evidence = get_evidence_for_entity(
                entity,
                sources=("sec_edgar", "nhtsa"),
                data_root=self.data_root,
            )
        except Exception:
            evidence = []

        # Add one summary Evidence for governance/regulatory red flags
        summary_evidence = summarize_governance_red_flags(evidence, entity.entity_id)
        return evidence + summary_evidence
