"""Types for cross-check results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Conflict:
    """A detected inconsistency between findings."""

    dimension: str  # e.g. "date_consistency", "entity_consistency"
    evidence_ids: tuple[str, ...]
    description: str
