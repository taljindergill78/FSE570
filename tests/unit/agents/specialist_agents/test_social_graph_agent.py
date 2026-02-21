"""Tests for Social Graph Agent."""

import pytest

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner import SubTask
from agents.specialist_agents.social_graph_agent import SocialGraphAgent
from osint_swarm.entities import Entity


def test_social_graph_agent_agent_id():
    agent = SocialGraphAgent()
    assert agent.agent_id == "social_graph_agent"


def test_social_graph_agent_adverse_media_returns_stub():
    agent = SocialGraphAgent()
    entity = Entity(entity_id="e1", name="E", identifiers={})
    task = SubTask("adverse_media", "social_graph_agent", "Adverse media")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) == 1
    assert findings[0].risk_category == "network"
    assert findings[0].attributes.get("stub") is True


def test_social_graph_agent_network_analysis_returns_stub():
    agent = SocialGraphAgent()
    entity = Entity(entity_id="e1", name="E", identifiers={})
    task = SubTask("network_analysis", "social_graph_agent", "Network")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) == 1
    assert "gnn" in findings[0].summary.lower() or "stub" in findings[0].summary.lower()
