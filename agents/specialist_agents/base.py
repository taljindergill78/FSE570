"""Specialist agent contract: all specialist agents implement this interface."""

from __future__ import annotations

from typing import List, Protocol

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner.types import SubTask


class SpecialistAgent(Protocol):
    """
    Contract for specialist agents.

    Lead Agent calls run(entity, task, context) for each allocated task.
    Agents may use context to read query/entity and to inspect other agents' results.
    """

    @property
    def agent_id(self) -> str:
        """Identifier for this agent (e.g. 'corporate_agent')."""
        ...

    def run(
        self,
        entity: Entity,
        task: SubTask,
        context: InvestigationContext,
    ) -> List[Evidence]:
        """
        Execute the task for the entity; return list of Evidence (findings).

        May use MCP layer or context.get_all_findings() to obtain input evidence.
        """
        ...
