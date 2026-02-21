"""Confidence module: aggregate and optionally adjust confidence from evidence."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from osint_swarm.entities import Evidence

from reflexion_layer.confidence_module.types import ConfidenceScores

# Source reliability weights (optional adjustment)
SOURCE_RELIABILITY: Dict[str, float] = {
    "sec_filing": 0.95,
    "sec_submissions": 0.9,
    "regulator_api": 0.85,
    "regulator_report": 0.85,
    "court_record": 0.8,
    "news_article": 0.6,
    "other": 0.5,
}


def aggregate_confidence(findings: List[Evidence]) -> ConfidenceScores:
    """
    Aggregate confidence across findings: overall mean and by risk_category / source_type.
    """
    if not findings:
        return ConfidenceScores(overall=0.0, by_risk_category={}, by_source_type={})

    by_risk: Dict[str, List[float]] = defaultdict(list)
    by_source: Dict[str, List[float]] = defaultdict(list)
    for e in findings:
        by_risk[e.risk_category].append(e.confidence)
        by_source[e.source_type].append(e.confidence)

    overall = sum(e.confidence for e in findings) / len(findings)
    by_risk_category = {k: sum(v) / len(v) for k, v in by_risk.items() if v}
    by_source_type = {k: sum(v) / len(v) for k, v in by_source.items() if v}

    return ConfidenceScores(
        overall=round(overall, 4),
        by_risk_category=by_risk_category,
        by_source_type=by_source_type,
    )


def adjusted_confidence(findings: List[Evidence]) -> List[Tuple[Evidence, float]]:
    """
    Return each finding with an adjusted confidence (evidence.confidence * source_reliability).
    """
    out: List[Tuple[Evidence, float]] = []
    for e in findings:
        weight = SOURCE_RELIABILITY.get(e.source_type, SOURCE_RELIABILITY["other"])
        adj = min(1.0, e.confidence * weight)
        out.append((e, round(adj, 4)))
    return out
