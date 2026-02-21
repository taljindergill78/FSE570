"""Task planner: decompose investigation query into sub-tasks for specialist agents."""

from __future__ import annotations

from typing import List, Optional

from osint_swarm.entities import Entity

from agents.lead_agent.task_planner.types import SubTask


# Keywords that trigger task types (for rule-based decomposition).
MONEY_LAUNDERING_KEYWORDS = [
    "money laundering",
    "money-laundering",
    "laundering",
    "aml",
    "anti-money",
    "proceeds of crime",
    "shell company",
    "beneficial owner",
    "beneficial ownership",
    "sanctions",
    "ofac",
    "transaction pattern",
    "adverse media",
    "pep",
    "politically exposed",
]

CORPORATE_TASK_TYPES = [
    ("corporate_structure", "corporate_agent", "Analyze corporate structure and subsidiaries"),
    ("beneficial_ownership", "corporate_agent", "Map beneficial ownership and control"),
    ("sec_filings", "corporate_agent", "Review SEC filings for governance and risk disclosures"),
    ("transaction_patterns", "corporate_agent", "Identify unusual transaction or revenue patterns"),
]

LEGAL_TASK_TYPES = [
    ("sanctions_screening", "legal_agent", "Screen entity and related parties against sanctions lists"),
    ("regulatory_actions", "legal_agent", "Check regulatory and enforcement history"),
    ("litigation", "legal_agent", "Review litigation and court records"),
]

SOCIAL_TASK_TYPES = [
    ("adverse_media", "social_graph_agent", "Monitor adverse media and public sentiment"),
    ("network_analysis", "social_graph_agent", "Analyze executive and entity network connections"),
]


def _query_lower(query: str) -> str:
    return (query or "").strip().lower()


def _suggests_money_laundering(query: str) -> bool:
    q = _query_lower(query)
    return any(kw in q for kw in MONEY_LAUNDERING_KEYWORDS)


def decompose(
    query: str,
    entity: Optional[Entity] = None,
) -> List[SubTask]:
    """
    Decompose an investigation query into sub-tasks (task_type, target_agent, description).

    For money-laundering-style queries we emit: corporate structure, beneficial ownership,
    sanctions, transaction patterns, adverse media. Otherwise we emit a default set
    of corporate + legal + social tasks.
    """
    tasks: List[SubTask] = []
    q = _query_lower(query)

    if _suggests_money_laundering(query):
        tasks.append(SubTask("corporate_structure", "corporate_agent", "Analyze corporate structure and subsidiaries for red flags"))
        tasks.append(SubTask("beneficial_ownership", "corporate_agent", "Map beneficial ownership and undisclosed interests"))
        tasks.append(SubTask("sanctions_screening", "legal_agent", "Screen against OFAC and sanctions lists"))
        tasks.append(SubTask("transaction_patterns", "corporate_agent", "Identify unusual transaction or revenue patterns"))
        tasks.append(SubTask("adverse_media", "social_graph_agent", "Review adverse media and public records"))
        return tasks

    # Default: generic investigation
    tasks.append(SubTask("sec_filings", "corporate_agent", "Review SEC filings and governance"))
    tasks.append(SubTask("sanctions_screening", "legal_agent", "Screen against sanctions lists"))
    tasks.append(SubTask("adverse_media", "social_graph_agent", "Check adverse media"))
    return tasks
