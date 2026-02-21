"""Types for confidence module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ConfidenceScores:
    """Aggregate confidence: overall and by dimension (e.g. risk_category)."""

    overall: float
    by_risk_category: Dict[str, float]
    by_source_type: Dict[str, float]
