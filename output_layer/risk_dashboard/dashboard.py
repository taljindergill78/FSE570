"""Risk dashboard: composite risk score by dimension (governance, regulatory, legal, network)."""

from __future__ import annotations

from collections import defaultdict
from typing import List

from osint_swarm.entities import Evidence

from output_layer.risk_dashboard.types import RiskDashboardScores

RISK_CATEGORIES = ("governance", "regulatory", "legal", "network", "other")


def compute_risk_scores(findings: List[Evidence]) -> RiskDashboardScores:
    """
    Compute composite risk score per risk_category (mean confidence of findings in that category)
    and overall. Higher confidence in risk findings = higher score for that dimension.
    """
    if not findings:
        return RiskDashboardScores(by_risk_category={}, overall=0.0, finding_count=0)

    by_category: dict[str, List[float]] = defaultdict(list)
    for e in findings:
        by_category[e.risk_category].append(e.confidence)

    by_risk_category = {
        cat: round(sum(by_category[cat]) / len(by_category[cat]), 4)
        for cat in RISK_CATEGORIES
        if by_category[cat]
    }
    overall = sum(e.confidence for e in findings) / len(findings)
    return RiskDashboardScores(
        by_risk_category=by_risk_category,
        overall=round(overall, 4),
        finding_count=len(findings),
    )


def format_dashboard_cli(scores: RiskDashboardScores) -> str:
    """Format dashboard scores for CLI (e.g. print to console)."""
    lines = ["Risk Dashboard", "---------------", f"Overall score: {scores.overall:.2f}", f"Finding count: {scores.finding_count}", ""]
    for cat in RISK_CATEGORIES:
        if cat in scores.by_risk_category:
            lines.append(f"  {cat}: {scores.by_risk_category[cat]:.2f}")
    return "\n".join(lines)
