"""Tests for NHTSA MCP processor."""

from pathlib import Path

import pytest

from mcp_layer.nhtsa_processor import NhtsaProcessor
from osint_swarm.entities import Entity


def test_nhtsa_processor_source_id():
    proc = NhtsaProcessor()
    assert proc.source_id == "nhtsa"


def test_nhtsa_processor_returns_empty_without_make():
    """Entity with no name and no make identifier returns no evidence."""
    proc = NhtsaProcessor()
    entity = Entity(entity_id="x", name="", identifiers={})
    assert proc.get_evidence_for_entity(entity) == []


def test_nhtsa_processor_uses_cache(tmp_path: Path):
    """Processor uses cached JSON when present and returns Evidence."""
    raw_dir = tmp_path / "raw" / "nhtsa"
    raw_dir.mkdir(parents=True)
    cache_path = raw_dir / "recalls_make_TESLA.json"
    cache_path.write_text(
        '{"results": [{"report_received_date": "2024-06-01", "nhtsa_id": "24V123", "defect_summary": "Test recall", "subject": "Test", "manufacturer": "Tesla, Inc."}]}',
        encoding="utf-8",
    )
    proc = NhtsaProcessor(data_root=tmp_path)
    entity = Entity(
        entity_id="tesla_inc_cik_0001318605",
        name="Tesla, Inc.",
        identifiers={"make": "TESLA"},
    )
    evidence = proc.get_evidence_for_entity(entity)
    assert len(evidence) >= 1
    e = evidence[0]
    assert e.entity_id == "tesla_inc_cik_0001318605"
    assert e.source_type == "regulator_api"
    assert e.risk_category == "regulatory"
    assert "24V123" in e.evidence_id or "24v123" in e.evidence_id


def test_nhtsa_processor_derives_make_from_name(tmp_path: Path):
    """Make is derived from entity.name when identifiers.make is missing."""
    raw_dir = tmp_path / "raw" / "nhtsa"
    raw_dir.mkdir(parents=True)
    cache_path = raw_dir / "recalls_make_TESLA.json"
    cache_path.write_text(
        '{"results": [{"report_received_date": "2024-06-01", "nhtsa_id": "24V456", "defect_summary": "Recall", "subject": "R"}]}',
        encoding="utf-8",
    )
    proc = NhtsaProcessor(data_root=tmp_path)
    entity = Entity(entity_id="tesla_inc", name="Tesla, Inc.", identifiers={})
    evidence = proc.get_evidence_for_entity(entity)
    assert len(evidence) >= 1
