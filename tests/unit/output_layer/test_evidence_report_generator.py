"""Tests for evidence report generator."""

from pathlib import Path

import pytest

from output_layer.evidence_report_generator import generate_html_report, generate_markdown_report, write_markdown_report
from osint_swarm.entities import Evidence


def test_generate_markdown_report_empty():
    out = generate_markdown_report([], entity_id="e1", query="Investigate X")
    assert "Investigation Evidence Report" in out
    assert "Total findings" in out and "0" in out
    assert "e1" in out
    assert "Investigate X" in out


def test_generate_markdown_report_with_findings():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "CFO appointed", "https://sec.gov", confidence=0.9),
        Evidence("ev2", "ent1", "2024-01-02", "regulator_api", "regulatory", "Recall issued", "https://nhtsa.gov", confidence=0.8),
    ]
    out = generate_markdown_report(findings, entity_id="ent1")
    assert "Total findings" in out and "2" in out
    assert "Governance" in out
    assert "Regulatory" in out
    assert "CFO appointed" in out
    assert "Recall issued" in out
    assert "https://sec.gov" in out
    assert "0.90" in out or "0.9" in out


def test_generate_markdown_report_with_graph():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "Summary", "https://sec.gov", confidence=0.9),
    ]
    from knowledge_graph import build_graph_from_evidence
    nodes, edges = build_graph_from_evidence(findings)
    out = generate_markdown_report(findings, entity_id="ent1", graph=(nodes, edges))
    assert "Knowledge Graph Summary" in out
    assert "Nodes:" in out
    assert "Edges:" in out


def test_write_markdown_report(tmp_path: Path):
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "Summary", "https://sec.gov", confidence=0.9),
    ]
    path = tmp_path / "report.md"
    write_markdown_report(path, findings, entity_id="ent1")
    assert path.exists()
    assert "Investigation Evidence Report" in path.read_text()


def test_generate_html_report():
    findings = [
        Evidence("ev1", "ent1", "2024-01-01", "sec_filing", "governance", "Summary", "https://sec.gov", confidence=0.9),
    ]
    out = generate_html_report(findings, entity_id="ent1")
    assert "<!DOCTYPE html>" in out
    assert "<h1>" in out
    assert "ent1" in out
    assert "Summary" in out
    assert "Source</a>" in out
