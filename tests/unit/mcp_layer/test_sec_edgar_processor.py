"""Tests for SEC EDGAR MCP processor."""

from pathlib import Path

import pytest

from mcp_layer.sec_edgar_processor import SecEdgarProcessor
from osint_swarm.entities import Entity


MINIMAL_SUBMISSIONS = {
    "filings": {
        "recent": {
            "form": ["10-K", "8-K"],
            "filingDate": ["2024-02-01", "2024-01-15"],
            "accessionNumber": ["0000950170-24-000001", "0000950170-24-000002"],
            "primaryDocument": ["tsla-10k.htm", "tsla-8k.htm"],
        }
    }
}


def test_sec_edgar_processor_source_id():
    proc = SecEdgarProcessor()
    assert proc.source_id == "sec_edgar"


def test_sec_edgar_processor_returns_empty_without_cik():
    """Entity without cik identifier returns no evidence."""
    proc = SecEdgarProcessor()
    entity = Entity(entity_id="x", name="Y", identifiers={})
    assert proc.get_evidence_for_entity(entity) == []


def test_sec_edgar_processor_uses_cache(tmp_path: Path):
    """Processor uses cached submissions JSON and returns Evidence."""
    import json

    raw_dir = tmp_path / "raw" / "sec"
    raw_dir.mkdir(parents=True)
    cache_path = raw_dir / "CIK0001318605.json"
    cache_path.write_text(json.dumps(MINIMAL_SUBMISSIONS), encoding="utf-8")

    proc = SecEdgarProcessor(data_root=tmp_path)
    entity = Entity(
        entity_id="tesla_inc_cik_0001318605",
        name="Tesla, Inc.",
        identifiers={"cik": "0001318605"},
    )
    evidence = proc.get_evidence_for_entity(entity)
    assert len(evidence) == 2
    forms = {e.attributes.get("form") for e in evidence}
    assert "10-K" in forms and "8-K" in forms
    for e in evidence:
        assert e.entity_id == "tesla_inc_cik_0001318605"
        assert e.source_type == "sec_filing"
        assert e.date in ("2024-02-01", "2024-01-15")
        assert "sec.gov" in e.source_uri
