"""Types for the knowledge graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Node:
    """A node in the graph (entity or evidence/document)."""

    id: str
    node_type: str  # "entity" | "evidence"
    label: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """A directed edge between two nodes."""

    source_id: str
    target_id: str
    relation_type: str  # e.g. "has_evidence", "same_source", "same_date"
    attributes: Dict[str, Any] = field(default_factory=dict)
