"""Entity resolution: query string -> Entity candidates."""

from agents.lead_agent.entity_resolution.resolver import (
    ENTITY_REGISTRY,
    resolve,
    resolve_one,
)

__all__ = ["ENTITY_REGISTRY", "resolve", "resolve_one"]
