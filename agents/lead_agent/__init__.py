"""Lead Agent: orchestrator for the OSINT Investigation Swarm."""

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.entity_resolution import resolve, resolve_one
from agents.lead_agent.orchestrator import LeadAgent
from agents.lead_agent.task_planner import SubTask, decompose

__all__ = [
    "LeadAgent",
    "InvestigationContext",
    "SubTask",
    "decompose",
    "resolve",
    "resolve_one",
]
