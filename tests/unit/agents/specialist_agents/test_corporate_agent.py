"""Tests for Corporate Agent."""

from pathlib import Path

import pytest

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner import SubTask
from agents.specialist_agents.corporate_agent import CorporateAgent
from agents.specialist_agents.corporate_agent.sec_analyzer import summarize_governance_red_flags
from osint_swarm.entities import Entity, Evidence


def test_corporate_agent_agent_id():
    agent = CorporateAgent()
    assert agent.agent_id == "corporate_agent"


def test_corporate_agent_beneficial_ownership_returns_stub_evidence():
    agent = CorporateAgent()
    entity = Entity(entity_id="e1", name="E", identifiers={})
    task = SubTask("beneficial_ownership", "corporate_agent", "Map ownership")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) == 1
    assert "structure" in findings[0].summary.lower() or "stub" in findings[0].summary.lower()
    assert findings[0].attributes.get("stub") is True


def test_corporate_agent_sec_task_uses_mcp_when_cache_exists():
    data_root = Path("data")
    if not (data_root / "raw" / "sec").exists():
        pytest.skip("no SEC cache")
    agent = CorporateAgent(data_root=data_root)
    entity = Entity(
        entity_id="tesla_inc_cik_0001318605",
        name="Tesla, Inc.",
        identifiers={"cik": "0001318605", "make": "TESLA"},
    )
    task = SubTask("corporate_structure", "corporate_agent", "Analyze structure")
    ctx = InvestigationContext()
    findings = agent.run(entity, task, ctx)
    assert len(findings) >= 1
    # Should include raw evidence + one summary
    summary_ev = [f for f in findings if "summary" in f.evidence_id or "corporate_summary" in f.evidence_id]
    assert len(summary_ev) >= 1
    assert "SEC" in summary_ev[0].summary or "filing" in summary_ev[0].summary.lower()


def test_summarize_governance_red_flags_empty_returns_empty():
    assert summarize_governance_red_flags([], "e1") == []


def test_summarize_governance_red_flags_adds_summary():
    evidence = [
        Evidence("ev1", "e1", "2024-01-01", "sec_filing", "governance", "8-K", "https://sec.gov", confidence=0.9, attributes={"form": "8-K"}),
        Evidence("ev2", "e1", "2024-01-02", "regulator_api", "regulatory", "Recall", "https://nhtsa.gov", confidence=0.8, attributes={}),
    ]
    out = summarize_governance_red_flags(evidence, "e1")
    assert len(out) == 1
    assert out[0].evidence_id == "e1_corporate_summary"
    assert out[0].attributes.get("sec_count") == 1
    assert out[0].attributes.get("reg_count") == 1
    assert out[0].attributes.get("eight_k_count") == 1
