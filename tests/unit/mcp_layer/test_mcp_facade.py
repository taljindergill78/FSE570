"""Tests for MCP layer facade (get_processor, get_evidence_for_entity)."""

from pathlib import Path

import pytest

from mcp_layer import (
    get_evidence_for_entity,
    get_processor,
    load_evidence_for_entity,
)
from osint_swarm.entities import Entity


def test_get_processor_sec_edgar():
    proc = get_processor("sec_edgar")
    assert proc is not None
    assert proc.source_id == "sec_edgar"


def test_get_processor_nhtsa():
    proc = get_processor("nhtsa")
    assert proc is not None
    assert proc.source_id == "nhtsa"


def test_get_processor_unknown_returns_none():
    assert get_processor("unknown_source") is None


def test_get_evidence_for_entity_aggregates_sources(tmp_path: Path):
    """get_evidence_for_entity returns evidence from requested sources (using cache)."""
    import json

    # SEC cache
    sec_dir = tmp_path / "raw" / "sec"
    sec_dir.mkdir(parents=True)
    sec_dir.joinpath("CIK0001318605.json").write_text(
        json.dumps({
            "filings": {
                "recent": {
                    "form": ["8-K"],
                    "filingDate": ["2024-01-10"],
                    "accessionNumber": ["0000950170-24-000099"],
                    "primaryDocument": ["doc.htm"],
                }
            }
        }),
        encoding="utf-8",
    )
    # NHTSA cache
    nhtsa_dir = tmp_path / "raw" / "nhtsa"
    nhtsa_dir.mkdir(parents=True)
    nhtsa_dir.joinpath("recalls_make_TESLA.json").write_text(
        '{"results": [{"report_received_date": "2024-06-01", "nhtsa_id": "24V1", "defect_summary": "Recall", "subject": "S"}]}',
        encoding="utf-8",
    )

    entity = Entity(
        entity_id="tesla_inc_cik_0001318605",
        name="Tesla, Inc.",
        identifiers={"cik": "0001318605", "make": "TESLA"},
    )
    evidence = get_evidence_for_entity(
        entity,
        sources=["sec_edgar", "nhtsa"],
        data_root=tmp_path,
    )
    assert len(evidence) >= 2
    source_types = {e.source_type for e in evidence}
    assert "sec_filing" in source_types
    assert "regulator_api" in source_types


def test_load_evidence_for_entity_facade(tmp_path: Path):
    """load_evidence_for_entity (from mcp_layer) delegates to evidence_loader."""
    subdir = tmp_path / "tesla"
    subdir.mkdir()
    subdir.joinpath("evidence_tesla.csv").write_text(
        "evidence_id,entity_id,date,source_type,risk_category,summary,source_uri,raw_location,confidence,attributes\n"
        'e1,tesla_inc_cik_0001318605,2024-01-01,other,other,S,https://x,,0.5,{}\n',
        encoding="utf-8",
    )
    out = load_evidence_for_entity(tmp_path, "tesla_inc_cik_0001318605")
    assert len(out) == 1
    assert out[0].evidence_id == "e1"
