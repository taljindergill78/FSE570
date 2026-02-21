"""Tests for knowledge graph."""

import pytest

from knowledge_graph import build_graph_from_evidence, Edge, Node
from osint_swarm.entities import Evidence


def test_build_graph_empty():
    nodes, edges = build_graph_from_evidence([])
    assert nodes == []
    assert edges == []


def test_build_graph_single_evidence():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "Summary", "https://sec.gov", confidence=0.9),
    ]
    nodes, edges = build_graph_from_evidence(findings)
    assert len(nodes) == 2  # entity + evidence
    node_ids = {n.id for n in nodes}
    assert "ent1" in node_ids
    assert "ev1" in node_ids
    assert any(n.node_type == "entity" for n in nodes)
    assert any(n.node_type == "evidence" for n in nodes)
    assert len(edges) >= 1
    assert any(e.source_id == "ent1" and e.target_id == "ev1" and e.relation_type == "has_evidence" for e in edges)


def test_build_graph_multiple_evidence_same_entity():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "A", "https://sec.gov", confidence=0.9),
        Evidence("ev2", "ent1", "2024-01-02", "regulator_api", "regulatory", "B", "https://nhtsa.gov", confidence=0.8),
    ]
    nodes, edges = build_graph_from_evidence(findings)
    assert len([n for n in nodes if n.node_type == "entity"]) == 1
    assert len([n for n in nodes if n.node_type == "evidence"]) == 2
    assert any(e.relation_type == "has_evidence" for e in edges)
    # same_source_type edges may link ev1-ev2 if they share source_type; here they don't, so only has_evidence
    assert len(edges) >= 2


def test_evidence_node_has_attributes():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "Summary", "https://sec.gov", confidence=0.85),
    ]
    nodes, _ = build_graph_from_evidence(findings)
    evidence_nodes = [n for n in nodes if n.node_type == "evidence"]
    assert len(evidence_nodes) == 1
    assert evidence_nodes[0].attributes.get("risk_category") == "governance"
    assert evidence_nodes[0].attributes.get("confidence") == 0.85
