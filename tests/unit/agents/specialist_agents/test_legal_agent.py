"""Tests for Legal Agent."""

import pytest

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner import SubTask
from agents.specialist_agents.legal_agent import LegalAgent
from osint_swarm.entities import Entity


def test_legal_agent_agent_id():
    agent = LegalAgent()
    assert agent.agent_id == "legal_agent"


def test_legal_agent_sanctions_returns_stub():
    agent = LegalAgent()
    entity = Entity(entity_id="e1", name="E", identifiers={})
    task = SubTask("sanctions_screening", "legal_agent", "Screen sanctions")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) == 1
    assert "sanctions" in findings[0].summary.lower() or "stub" in findings[0].summary.lower()
    assert findings[0].risk_category == "legal"
    assert findings[0].attributes.get("stub") is True


def test_legal_agent_litigation_returns_pacer_stub():
    agent = LegalAgent()
    entity = Entity(entity_id="e1", name="E", identifiers={})
    task = SubTask("litigation", "legal_agent", "Court records")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) == 1
    assert "pacer" in findings[0].summary.lower() or "court" in findings[0].summary.lower()

