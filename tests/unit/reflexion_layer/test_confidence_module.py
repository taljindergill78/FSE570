"""Tests for reflexion confidence module."""

import pytest

from reflexion_layer.confidence_module import (
    ConfidenceScores,
    aggregate_confidence,
    adjusted_confidence,
)
from osint_swarm.entities import Evidence


def test_aggregate_confidence_empty():
    out = aggregate_confidence([])
    assert out.overall == 0.0
    assert out.by_risk_category == {}
    assert out.by_source_type == {}


def test_aggregate_confidence_single():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "X", "https://sec.gov", confidence=0.9),
    ]
    out = aggregate_confidence(findings)
    assert out.overall == 0.9
    assert out.by_risk_category.get("governance") == 0.9
    assert out.by_source_type.get("sec_filing") == 0.9


def test_aggregate_confidence_multiple_categories():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "X", "https://sec.gov", confidence=0.9),
        Evidence("e2", "ent1", "2024-01-02", "regulator_api", "regulatory", "Y", "https://nhtsa.gov", confidence=0.8),
    ]
    out = aggregate_confidence(findings)
    assert out.overall == 0.85
    assert out.by_risk_category["governance"] == 0.9
    assert out.by_risk_category["regulatory"] == 0.8
    assert out.by_source_type["sec_filing"] == 0.9
    assert out.by_source_type["regulator_api"] == 0.8


def test_adjusted_confidence_applies_source_weight():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "X", "https://sec.gov", confidence=1.0),
    ]
    out = adjusted_confidence(findings)
    assert len(out) == 1
    ev, adj = out[0]
    assert ev.evidence_id == "e1"
    assert adj <= 1.0
    assert adj >= 0.9  # sec_filing weight 0.95


def test_adjusted_confidence_other_source_lower():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "other", "other", "X", "https://x.com", confidence=1.0),
    ]
    out = adjusted_confidence(findings)
    assert len(out) == 1
    _, adj = out[0]
    assert adj == 0.5  # other weight 0.5
