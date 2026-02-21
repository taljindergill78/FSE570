"""Social Graph Agent: GNN Analyzer + Influence Mapper (stubs); implements SpecialistAgent contract."""

from __future__ import annotations

from typing import List

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner.types import SubTask
from agents.specialist_agents.social_graph_agent.gnn_analyzer.analyzer import run_stub as gnn_run
from agents.specialist_agents.social_graph_agent.influence_mapper.mapper import run_stub as influence_run


class SocialGraphAgent:
    """Social network analysis agent: GNN and influence mapping (stubs)."""

    AGENT_ID = "social_graph_agent"

    @property
    def agent_id(self) -> str:
        return self.AGENT_ID

    def run(
        self,
        entity: Entity,
        task: SubTask,
        context: InvestigationContext,
    ) -> List[Evidence]:
        """Dispatch to GNN analyzer or influence mapper by task_type."""
        if task.task_type == "network_analysis":
            return gnn_run(entity, task, context)
        if task.task_type == "adverse_media":
            # Adverse media also uses stub for now (no news/social data)
            return gnn_run(entity, task, context)
        return influence_run(entity, task, context)
