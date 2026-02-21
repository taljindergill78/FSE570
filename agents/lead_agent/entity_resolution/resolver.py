"""Entity resolution: map query text (e.g. 'Tesla', 'Company X') to Entity or candidates."""

from __future__ import annotations

from typing import List, Optional

from osint_swarm.entities import Entity


# Lookup table: normalized name/alias -> Entity.
# Expand with more entities as needed.
ENTITY_REGISTRY: List[Entity] = [
    Entity(
        entity_id="tesla_inc_cik_0001318605",
        name="Tesla, Inc.",
        entity_type="public_company",
        identifiers={"cik": "0001318605", "ticker": "TSLA", "make": "TESLA"},
        aliases=["Tesla", "Tesla Inc", "Tesla Motors", "TSLA"],
    ),
]


def _normalize(s: str) -> str:
    return s.strip().lower() if s else ""


def resolve(query: str) -> List[Entity]:
    """
    Resolve a query string (e.g. 'Tesla', 'Investigate Tesla for money laundering') to candidates.

    Uses a registry and alias match. Returns all entities whose name or any alias
    appears in the query (case-insensitive), or when the query equals the name/alias.
    """
    if not query or not query.strip():
        return []
    norm = _normalize(query)
    if not norm:
        return []
    candidates: List[Entity] = []
    for entity in ENTITY_REGISTRY:
        name_norm = _normalize(entity.name)
        if norm == name_norm or name_norm in norm or norm in name_norm:
            candidates.append(entity)
            continue
        for alias in entity.aliases:
            alias_norm = _normalize(alias)
            if norm == alias_norm or alias_norm in norm or norm in alias_norm:
                candidates.append(entity)
                break
    return candidates


def resolve_one(query: str) -> Optional[Entity]:
    """Return the first resolved entity, or None if no match."""
    candidates = resolve(query)
    return candidates[0] if candidates else None
