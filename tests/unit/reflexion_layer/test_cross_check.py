"""Tests for reflexion cross-check."""

import pytest

from reflexion_layer.cross_check import Conflict, cross_check_findings
from osint_swarm.entities import Evidence


def test_cross_check_empty_returns_empty():
    assert cross_check_findings([]) == []


def test_cross_check_single_finding_no_conflict():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "CFO appointed", "https://sec.gov", confidence=0.9),
    ]
    assert cross_check_findings(findings) == []


def test_cross_check_same_entity_date_different_summary_flags_conflict():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "CFO appointed: Alice", "https://sec.gov", confidence=0.9),
        Evidence("e2", "ent1", "2024-01-01", "regulator_api", "regulatory", "CFO appointed: Bob", "https://nhtsa.gov", confidence=0.8),
    ]
    conflicts = cross_check_findings(findings)
    assert len(conflicts) == 1
    assert conflicts[0].dimension == "summary_consistency"
    assert "ent1" in conflicts[0].description
    assert "2024-01-01" in conflicts[0].description


def test_cross_check_same_entity_date_same_summary_no_conflict():
    findings = [
        Evidence("e1", "ent1", "2024-01-01", "sec_filing", "governance", "CFO appointed", "https://sec.gov", confidence=0.9),
        Evidence("e2", "ent1", "2024-01-01", "regulator_api", "regulatory", "CFO appointed", "https://nhtsa.gov", confidence=0.8),
    ]
    assert len(cross_check_findings(findings)) == 0


def test_cross_check_no_date_skipped():
    findings = [
        Evidence("e1", "ent1", "", "other", "other", "No date", "https://x.com", confidence=0.5),
    ]
    assert cross_check_findings(findings) == []
