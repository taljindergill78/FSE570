"""Tests for risk dashboard."""

import pytest

from output_layer.risk_dashboard import RiskDashboardScores, compute_risk_scores, format_dashboard_cli
from osint_swarm.entities import Evidence


def test_compute_risk_scores_empty():
    out = compute_risk_scores([])
    assert out.overall == 0.0
    assert out.finding_count == 0
    assert out.by_risk_category == {}


def test_compute_risk_scores_single():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "X", "https://sec.gov", confidence=0.9),
    ]
    out = compute_risk_scores(findings)
    assert out.finding_count == 1
    assert out.overall == 0.9
    assert out.by_risk_category.get("governance") == 0.9


def test_compute_risk_scores_multiple_categories():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "X", "https://sec.gov", confidence=0.9),
        Evidence("ev2", "ent1", "2024-01-02", "regulator_api", "regulatory", "Y", "https://nhtsa.gov", confidence=0.7),
    ]
    out = compute_risk_scores(findings)
    assert out.finding_count == 2
    assert out.overall == 0.8
    assert out.by_risk_category["governance"] == 0.9
    assert out.by_risk_category["regulatory"] == 0.7


def test_format_dashboard_cli():
    scores = RiskDashboardScores(by_risk_category={"governance": 0.85, "regulatory": 0.7}, overall=0.775, finding_count=10)
    out = format_dashboard_cli(scores)
    assert "Risk Dashboard" in out
    assert "0.78" in out or "0.775" in out
    assert "governance" in out
    assert "regulatory" in out
    assert "10" in out
