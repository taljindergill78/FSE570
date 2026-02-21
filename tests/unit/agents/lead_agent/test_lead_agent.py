"""Tests for Lead Agent orchestration."""

from pathlib import Path

import pytest

from agents.lead_agent import LeadAgent
from osint_swarm.entities import Entity, Evidence


def test_lead_agent_run_unknown_entity_returns_context_with_no_entity():
    agent = LeadAgent()
    ctx = agent.run("Unknown Company XYZ 12345")
    assert ctx.get_entity() is None
    assert ctx.get_query() == "Unknown Company XYZ 12345"
    assert ctx.get_tasks() == []
    assert ctx.get_all_findings() == []


def test_lead_agent_run_tesla_resolves_entity_and_has_tasks():
    agent = LeadAgent()
    ctx = agent.run("Investigate Tesla for money laundering")
    assert ctx.get_entity() is not None
    assert ctx.get_entity().entity_id == "tesla_inc_cik_0001318605"
    assert len(ctx.get_tasks()) == 5
    assert ctx.get_query() == "Investigate Tesla for money laundering"


def test_lead_agent_run_tesla_gets_corporate_evidence_with_mcp(tmp_path: Path):
    """With cached SEC/NHTSA data, corporate_agent stub returns evidence."""
    # Use project data dir if it has cache; else use tmp_path (empty -> no evidence)
    data_root = Path("data")
    if (data_root / "raw" / "sec").exists() and (data_root / "raw" / "nhtsa").exists():
        agent = LeadAgent(data_root=data_root)
        ctx = agent.run("Investigate Tesla")
        findings = ctx.get_all_findings()
        # Corporate stub should have returned evidence from MCP
        assert len(findings) >= 1
        assert any(f.source_type == "sec_filing" or f.source_type == "regulator_api" for f in findings)
    else:
        agent = LeadAgent(data_root=tmp_path)
        ctx = agent.run("Investigate Tesla")
        # No cache -> corporate stub may return [] or minimal
        assert ctx.get_entity() is not None


def test_lead_agent_accepts_custom_stubs():
    """Custom agent stubs are used when provided (entity, task, context)."""
    collected = []

    def stub(_entity: Entity, task, _context):
        collected.append(task.task_type)
        return []

    agent = LeadAgent(agent_stubs={
        "corporate_agent": stub,
        "legal_agent": stub,
        "social_graph_agent": stub,
    })
    ctx = agent.run("Investigate Tesla for money laundering")
    assert len(collected) == 5
    assert "corporate_structure" in collected
    assert "sanctions_screening" in collected
