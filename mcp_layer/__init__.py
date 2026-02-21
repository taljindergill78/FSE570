"""
MCP Layer: unified data access for the OSINT Investigation Swarm.

Agents and the Lead Agent should obtain evidence through this layer,
not by calling src/osint_swarm/data_sources directly.

Usage:
  from mcp_layer import get_evidence_for_entity, load_evidence_for_entity
  from osint_swarm.entities import Entity

  entity = Entity(entity_id="tesla_inc_cik_0001318605", name="Tesla, Inc.", identifiers={"cik": "0001318605", "make": "TESLA"})
  evidence = get_evidence_for_entity(entity, sources=["sec_edgar", "nhtsa"])
  # Or load from existing processed CSV:
  evidence = load_evidence_for_entity(Path("data/processed"), entity.entity_id)
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence

from osint_swarm.entities import Entity, Evidence

from mcp_layer.base import DataSourceProcessor
from mcp_layer.evidence_loader import load_evidence_for_entity as load_evidence_for_entity_from_dir
from mcp_layer.sec_edgar_processor import SecEdgarProcessor
from mcp_layer.nhtsa_processor import NhtsaProcessor


def get_processor(source_id: str, data_root: Optional[Path] = None) -> Optional[DataSourceProcessor]:
    """Return the processor for the given source_id, or None."""
    root = Path(data_root) if data_root else Path("data")
    if source_id == "sec_edgar":
        return SecEdgarProcessor(data_root=root)
    if source_id == "nhtsa":
        return NhtsaProcessor(data_root=root)
    return None


def get_evidence_for_entity(
    entity: Entity,
    sources: Sequence[str] = ("sec_edgar", "nhtsa"),
    data_root: Optional[Path] = None,
) -> List[Evidence]:
    """
    Fetch evidence for an entity from the requested MCP sources.

    sources: e.g. ["sec_edgar", "nhtsa"]. Uses cache under data/raw/ when available.
    """
    out: List[Evidence] = []
    for sid in sources:
        proc = get_processor(sid, data_root=data_root)
        if proc:
            out.extend(proc.get_evidence_for_entity(entity))
    return out


def load_evidence_for_entity(processed_dir: Path, entity_id: str) -> List[Evidence]:
    """Load all Evidence for entity_id from data/processed/ (canonical agent input)."""
    return load_evidence_for_entity_from_dir(Path(processed_dir), entity_id)


__all__ = [
    "DataSourceProcessor",
    "SecEdgarProcessor",
    "NhtsaProcessor",
    "get_processor",
    "get_evidence_for_entity",
    "load_evidence_for_entity",
]
