"""Context manager: holds investigation state (entity, query, tasks, results per agent)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from osint_swarm.entities import Entity, Evidence

from agents.lead_agent.task_planner.types import SubTask


@dataclass
class InvestigationContext:
    """
    Holds the current investigation context for the Lead Agent and specialists.

    - entity: resolved investigation target (or None if unresolved)
    - query: original natural-language query
    - tasks: list of sub-tasks from the task planner
    - results: findings per agent (agent_id -> list of Evidence)
    """

    entity: Optional[Entity] = None
    query: str = ""
    tasks: List[SubTask] = field(default_factory=list)
    results: Dict[str, List[Evidence]] = field(default_factory=dict)

    def set_entity(self, entity: Optional[Entity]) -> None:
        self.entity = entity

    def get_entity(self) -> Optional[Entity]:
        return self.entity

    def set_query(self, query: str) -> None:
        self.query = query

    def get_query(self) -> str:
        return self.query

    def set_tasks(self, tasks: List[SubTask]) -> None:
        self.tasks = tasks

    def get_tasks(self) -> List[SubTask]:
        return self.tasks.copy()

    def add_agent_results(self, agent_id: str, findings: List[Evidence]) -> None:
        if agent_id not in self.results:
            self.results[agent_id] = []
        self.results[agent_id].extend(findings)

    def get_agent_results(self, agent_id: str) -> List[Evidence]:
        return self.results.get(agent_id, []).copy()

    def get_all_findings(self) -> List[Evidence]:
        out: List[Evidence] = []
        for findings in self.results.values():
            out.extend(findings)
        return out
