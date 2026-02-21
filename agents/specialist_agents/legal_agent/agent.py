"""Legal Agent: sanctions screening + PACER; implements SpecialistAgent contract."""

from __future__ import annotations

from typing import List

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner.types import SubTask
from agents.specialist_agents.legal_agent.sanctions_screener.screener import run_stub as sanctions_run
from agents.specialist_agents.legal_agent.pacer_analyzer.analyzer import run_stub as pacer_run


class LegalAgent:
    """Legal and compliance agent: sanctions (stub), PACER (stub)."""

    AGENT_ID = "legal_agent"

    @property
    def agent_id(self) -> str:
        return self.AGENT_ID

    def run(
        self,
        entity: Entity,
        task: SubTask,
        context: InvestigationContext,
    ) -> List[Evidence]:
        """Dispatch to sanctions_screener or pacer_analyzer by task_type."""
        if task.task_type == "sanctions_screening":
            return sanctions_run(entity, task, context)
        if task.task_type in ("litigation", "regulatory_actions"):
            return pacer_run(entity, task, context)
        # Default: sanctions stub
        return sanctions_run(entity, task, context)
