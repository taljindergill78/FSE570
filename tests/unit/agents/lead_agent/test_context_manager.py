"""Tests for context manager."""

import pytest

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner import SubTask
from osint_swarm.entities import Entity, Evidence


def test_context_starts_empty():
    ctx = InvestigationContext()
    assert ctx.get_entity() is None
    assert ctx.get_query() == ""
    assert ctx.get_tasks() == []
    assert ctx.get_all_findings() == []


def test_context_set_get_entity():
    ctx = InvestigationContext()
    entity = Entity(entity_id="e1", name="Test")
    ctx.set_entity(entity)
    assert ctx.get_entity() is entity


def test_context_set_get_query():
    ctx = InvestigationContext()
    ctx.set_query("Investigate X")
    assert ctx.get_query() == "Investigate X"


def test_context_set_get_tasks():
    ctx = InvestigationContext()
    tasks = [SubTask("corporate_structure", "corporate_agent", "Analyze structure")]
    ctx.set_tasks(tasks)
    assert len(ctx.get_tasks()) == 1
    assert ctx.get_tasks()[0].task_type == "corporate_structure"


def test_context_add_and_get_agent_results():
    ctx = InvestigationContext()
    ev = Evidence(
        evidence_id="ev1",
        entity_id="e1",
        date="2024-01-01",
        source_type="sec_filing",
        risk_category="governance",
        summary="Test",
        source_uri="https://sec.gov",
        confidence=0.9,
    )
    ctx.add_agent_results("corporate_agent", [ev])
    assert len(ctx.get_agent_results("corporate_agent")) == 1
    assert ctx.get_agent_results("corporate_agent")[0].evidence_id == "ev1"
    assert len(ctx.get_all_findings()) == 1


def test_context_get_agent_results_returns_copy():
    ctx = InvestigationContext()
    ctx.add_agent_results("legal_agent", [])
    r1 = ctx.get_agent_results("legal_agent")
    r2 = ctx.get_agent_results("legal_agent")
    assert r1 is not r2
