"""
Evidence loader: load structured Evidence from data/processed/ (canonical agent input).

All agents should consume Evidence via the MCP layer or this loader,
not raw JSON or ad-hoc CSV reads.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from osint_swarm.entities import Evidence


EVIDENCE_CSV_FIELDS = [
    "evidence_id",
    "entity_id",
    "date",
    "source_type",
    "risk_category",
    "summary",
    "source_uri",
    "raw_location",
    "confidence",
    "attributes",
]


def load_evidence_from_csv(csv_path: Path) -> List[Evidence]:
    """Load Evidence list from a single CSV (same schema as build_evidence_tesla output)."""
    if not csv_path.exists():
        return []
    out: List[Evidence] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            attrs = row.get("attributes", "{}")
            if isinstance(attrs, str):
                try:
                    attrs = json.loads(attrs) if attrs else {}
                except json.JSONDecodeError:
                    attrs = {}
            conf = row.get("confidence", "0.5")
            try:
                confidence = float(conf)
            except (TypeError, ValueError):
                confidence = 0.5
            out.append(
                Evidence(
                    evidence_id=row.get("evidence_id", ""),
                    entity_id=row.get("entity_id", ""),
                    date=row.get("date", ""),
                    source_type=row.get("source_type", "other"),
                    risk_category=row.get("risk_category", "other"),
                    summary=row.get("summary", ""),
                    source_uri=row.get("source_uri", ""),
                    raw_location=row.get("raw_location") or None,
                    confidence=confidence,
                    attributes=attrs if isinstance(attrs, dict) else {},
                )
            )
    return out


def load_evidence_for_entity(processed_dir: Path, entity_id: str) -> List[Evidence]:
    """
    Load all Evidence for an entity from data/processed/.

    Scans processed_dir for subdirs containing evidence_*.csv and returns
    rows where entity_id matches. Convention: data/processed/<slug>/evidence_*.csv.
    """
    processed_dir = Path(processed_dir)
    if not processed_dir.exists():
        return []
    out: List[Evidence] = []
    for subdir in processed_dir.iterdir():
        if not subdir.is_dir():
            continue
        for csv_path in subdir.glob("evidence_*.csv"):
            for e in load_evidence_from_csv(csv_path):
                if e.entity_id == entity_id:
                    out.append(e)
    return out
