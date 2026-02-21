"""
MCP-style interface for data sources.

All agents and the Lead Agent should obtain evidence through this layer,
not by calling src/osint_swarm/data_sources directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

# Import from src; callers must have src on path or install osint_swarm
try:
    from osint_swarm.entities import Entity, Evidence
except ImportError:
    Entity = None  # type: ignore
    Evidence = None  # type: ignore


class DataSourceProcessor(ABC):
    """Contract for MCP-layer data source processors.

    Input: Entity (or entity identifiers).
    Output: List[Evidence] in the canonical schema.
    """

    @property
    @abstractmethod
    def source_id(self) -> str:
        """Short identifier for this source (e.g. 'sec_edgar', 'nhtsa')."""
        ...

    @abstractmethod
    def get_evidence_for_entity(self, entity: "Entity") -> List["Evidence"]:
        """Fetch and return all evidence for the given entity from this source.

        May use cache under data/raw/ or fetch live; either way returns
        structured Evidence instances.
        """
        ...
