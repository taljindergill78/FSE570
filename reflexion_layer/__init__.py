"""Reflexion layer: cross-check, gap detection, confidence (Phase 5)."""

from reflexion_layer.confidence_module import (
    ConfidenceScores,
    aggregate_confidence,
    adjusted_confidence,
)
from reflexion_layer.cross_check import Conflict, cross_check_findings
from reflexion_layer.gap_detection import Gap, detect_gaps

__all__ = [
    "Conflict",
    "cross_check_findings",
    "Gap",
    "detect_gaps",
    "ConfidenceScores",
    "aggregate_confidence",
    "adjusted_confidence",
]
