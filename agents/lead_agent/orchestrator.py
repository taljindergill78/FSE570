"""Lead Agent: orchestrate query -> entity resolution -> task decomposition -> agent dispatch -> context."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Optional

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.entity_resolution import resolve_one
from agents.lead_agent.task_planner import SubTask, decompose


AgentStub = Callable[[Entity, SubTask, InvestigationContext], List[Evidence]]


def _default_agent_stubs(data_root: Optional[Path] = None) -> Dict[str, AgentStub]:
    """Build stub callables from Phase 4 specialist agents."""
    data_root = data_root or Path("data")
    from agents.specialist_agents import CorporateAgent, LegalAgent, SocialGraphAgent
    corporate = CorporateAgent(data_root=data_root)
    legal = LegalAgent()
    social = SocialGraphAgent()
    return {
        "corporate_agent": lambda e, t, c: corporate.run(e, t, c),
        "legal_agent": lambda e, t, c: legal.run(e, t, c),
        "social_graph_agent": lambda e, t, c: social.run(e, t, c),
    }


class LeadAgent:
    """
    Lead Agent: accepts a natural-language investigation query, resolves the entity,
    decomposes into sub-tasks, dispatches to specialist agents (stubs), and
    collects results into an InvestigationContext.
    """

    def __init__(
        self,
        data_root: Optional[Path] = None,
        agent_stubs: Optional[Dict[str, AgentStub]] = None,
    ):
        self.data_root = Path(data_root) if data_root else Path("data")
        self._stubs = agent_stubs if agent_stubs is not None else _default_agent_stubs(self.data_root)

    def run(self, query: str) -> InvestigationContext:
        """
        Execute the investigation pipeline: resolve entity -> decompose -> dispatch -> collect.

        Returns the InvestigationContext with entity, tasks, and results per agent.
        """
        context = InvestigationContext()
        context.set_query(query)

        entity = resolve_one(query)
        if not entity:
            return context
        context.set_entity(entity)

        tasks = decompose(query, entity=entity)
        context.set_tasks(tasks)

        for task in tasks:
            stub = self._stubs.get(task.target_agent)
            if stub:
                findings = stub(entity, task, context)
                context.add_agent_results(task.target_agent, findings)

        return context
