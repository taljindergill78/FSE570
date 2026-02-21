"""Tests for evidence loader (canonical agent input)."""

import json
import tempfile
from pathlib import Path

import pytest

from mcp_layer.evidence_loader import load_evidence_for_entity, load_evidence_from_csv
from osint_swarm.entities import Evidence


def test_load_evidence_from_csv_empty_path():
    """Non-existent path returns empty list."""
    assert load_evidence_from_csv(Path("/nonexistent/evidence.csv")) == []


def test_load_evidence_from_csv_single_row(tmp_path: Path):
    """Load one Evidence row from CSV."""
    csv_path = tmp_path / "evidence.csv"
    csv_path.write_text(
        "evidence_id,entity_id,date,source_type,risk_category,summary,source_uri,raw_location,confidence,attributes\n"
        'ev1,ent1,2024-01-15,sec_filing,governance,"Summary here",https://sec.gov,,0.9,"{""form"": ""8-K""}"\n',
        encoding="utf-8",
    )
    out = load_evidence_from_csv(csv_path)
    assert len(out) == 1
    assert out[0].evidence_id == "ev1"
    assert out[0].entity_id == "ent1"
    assert out[0].date == "2024-01-15"
    assert out[0].source_type == "sec_filing"
    assert out[0].risk_category == "governance"
    assert out[0].confidence == 0.9
    assert out[0].attributes.get("form") == "8-K"


def test_load_evidence_for_entity_from_processed_dir(tmp_path: Path):
    """load_evidence_for_entity finds CSV by entity_id."""
    subdir = tmp_path / "tesla"
    subdir.mkdir()
    csv_path = subdir / "evidence_tesla.csv"
    csv_path.write_text(
        "evidence_id,entity_id,date,source_type,risk_category,summary,source_uri,raw_location,confidence,attributes\n"
        'e1,tesla_inc_cik_0001318605,2024-01-01,regulator_api,regulatory,Recall,https://nhtsa.gov,,0.8,{}\n',
        encoding="utf-8",
    )
    out = load_evidence_for_entity(tmp_path, "tesla_inc_cik_0001318605")
    assert len(out) == 1
    assert out[0].entity_id == "tesla_inc_cik_0001318605"

    out_other = load_evidence_for_entity(tmp_path, "other_entity")
    assert len(out_other) == 0


def test_load_evidence_for_entity_nonexistent_dir():
    """Non-existent processed_dir returns empty list."""
    assert load_evidence_for_entity(Path("/nonexistent/processed"), "any_id") == []
