"""Types for risk dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RiskDashboardScores:
    """Composite risk scores by dimension and overall."""

    by_risk_category: Dict[str, float]  # governance, regulatory, legal, network, other
    overall: float
    finding_count: int
