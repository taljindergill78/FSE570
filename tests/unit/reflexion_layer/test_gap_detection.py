"""Tests for reflexion gap detection."""

import pytest

from agents.lead_agent.context_manager import InvestigationContext
from agents.lead_agent.task_planner import SubTask
from reflexion_layer.gap_detection import Gap, detect_gaps
from osint_swarm.entities import Entity, Evidence


def test_detect_gaps_no_entity_returns_entity_resolution_gap():
    ctx = InvestigationContext()
    ctx.set_query("Investigate XYZ")
    gaps = detect_gaps(ctx)
    assert len(gaps) >= 1
    assert any(g.area == "entity_resolution" for g in gaps)


def test_detect_gaps_legal_stub_returns_sanctions_gap():
    ctx = InvestigationContext()
    ctx.set_entity(Entity(entity_id="e1", name="E", identifiers={}))
    stub_ev = Evidence(
        "e1_sanctions_stub", "e1", "", "other", "legal",
        "Sanctions not integrated", "", None, 0.0, {"stub": True},
    )
    ctx.add_agent_results("legal_agent", [stub_ev])
    gaps = detect_gaps(ctx)
    assert any("Sanctions" in g.area or "legal" in g.description.lower() for g in gaps)


def test_detect_gaps_social_stub_returns_gap():
    ctx = InvestigationContext()
    ctx.set_entity(Entity(entity_id="e1", name="E", identifiers={}))
    stub_ev = Evidence(
        "e1_gnn_stub", "e1", "", "other", "network",
        "GNN not integrated", "", None, 0.0, {"stub": True},
    )
    ctx.add_agent_results("social_graph_agent", [stub_ev])
    gaps = detect_gaps(ctx)
    assert any("Adverse" in g.area or "network" in g.description.lower() or "Social" in g.area for g in gaps)


def test_detect_gaps_structure_mapper_stub_returns_beneficial_ownership_gap():
    ctx = InvestigationContext()
    ctx.set_entity(Entity(entity_id="e1", name="E", identifiers={}))
    stub_ev = Evidence(
        "e1_structure_mapper_stub", "e1", "", "other", "governance",
        "Structure Mapper not integrated", "", None, 0.0, {"stub": True},
    )
    ctx.add_agent_results("corporate_agent", [stub_ev])
    gaps = detect_gaps(ctx)
    assert any(g.area == "beneficial_ownership" for g in gaps)


def test_detect_gaps_legal_empty_returns_gap():
    ctx = InvestigationContext()
    ctx.set_entity(Entity(entity_id="e1", name="E", identifiers={}))
    # No legal results at all
    gaps = detect_gaps(ctx)
    assert any("legal" in g.area.lower() or "Sanctions" in g.area for g in gaps)
