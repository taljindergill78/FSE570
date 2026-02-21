"""Build an in-memory knowledge graph from evidence (verified findings)."""

from __future__ import annotations

from collections import defaultdict
from typing import List, Set

from osint_swarm.entities import Evidence

from knowledge_graph.types import Edge, Node


def build_graph_from_evidence(findings: List[Evidence]) -> tuple[List[Node], List[Edge]]:
    """
    Build nodes and edges from evidence.
    - Nodes: one per entity_id, one per evidence_id (evidence as document).
    - Edges: entity --[has_evidence]--> evidence; optional evidence--[same_source]-->evidence for same source_type.
    """
    nodes: List[Node] = []
    edges: List[Edge] = []
    entity_ids: Set[str] = set()
    evidence_ids: Set[str] = set()

    for e in findings:
        if e.entity_id and e.entity_id not in entity_ids:
            entity_ids.add(e.entity_id)
            nodes.append(Node(id=e.entity_id, node_type="entity", label=e.entity_id, attributes={}))
        if e.evidence_id and e.evidence_id not in evidence_ids:
            evidence_ids.add(e.evidence_id)
            nodes.append(
                Node(
                    id=e.evidence_id,
                    node_type="evidence",
                    label=e.summary[:80] + "..." if len(e.summary) > 80 else e.summary,
                    attributes={
                        "date": e.date,
                        "source_type": e.source_type,
                        "risk_category": e.risk_category,
                        "confidence": e.confidence,
                    },
                )
            )
        if e.entity_id and e.evidence_id:
            edges.append(
                Edge(source_id=e.entity_id, target_id=e.evidence_id, relation_type="has_evidence", attributes={})
            )

    # Optional: link evidence that share the same source_type (e.g. same filing family)
    by_source: dict[str, List[str]] = defaultdict(list)
    for e in findings:
        if e.source_type:
            by_source[e.source_type].append(e.evidence_id)
    for ev_ids in by_source.values():
        if len(ev_ids) > 1:
            for i in range(len(ev_ids) - 1):
                edges.append(
                    Edge(
                        source_id=ev_ids[i],
                        target_id=ev_ids[i + 1],
                        relation_type="same_source_type",
                        attributes={},
                    )
                )

    return nodes, edges
