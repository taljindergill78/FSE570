"""NHTSA processor: fetches/caches recalls by make and returns Evidence."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from osint_swarm.data_sources import nhtsa
from osint_swarm.entities import Evidence
from osint_swarm.utils.io import read_json, write_json

from mcp_layer.base import DataSourceProcessor

if TYPE_CHECKING:
    from osint_swarm.entities import Entity


def _records_to_evidence(
    records: List[Dict[str, Any]],
    entity_id: str,
    raw_location: Optional[str] = None,
) -> List[Evidence]:
    """Convert NHTSA recall records to Evidence list (same logic as build_evidence_tesla)."""
    out: List[Evidence] = []
    for r in records:
        if not isinstance(r, dict):
            continue
        nhtsa_id = r.get("nhtsa_id") or r.get("NHTSA_ID")
        report_date = r.get("report_received_date") or r.get("ReportReceivedDate")
        subject = r.get("subject") or r.get("Subject") or ""
        component = r.get("component") or r.get("Component") or ""
        defect_summary = r.get("defect_summary") or r.get("Summary") or ""
        consequence = r.get("consequence_summary") or r.get("Consequence") or ""
        corrective_action = r.get("corrective_action") or r.get("Remedy") or ""
        recall_type = r.get("recall_type") or ""
        potentially_affected = r.get("potentially_affected") or ""
        mfr_campaign_number = r.get("mfr_campaign_number") or ""
        manufacturer = r.get("manufacturer") or ""
        recall_link = r.get("recall_link") if isinstance(r.get("recall_link"), dict) else {}
        recall_url = (recall_link or {}).get("url") or ""

        if not report_date:
            continue

        source_uri = recall_url or "https://www.nhtsa.gov/recalls"
        ev_id = f"{entity_id}_nhtsa_{(nhtsa_id or mfr_campaign_number or report_date)}".lower().replace(" ", "_")
        out.append(
            Evidence(
                evidence_id=ev_id,
                entity_id=entity_id,
                date=str(report_date)[:10],
                source_type="regulator_api",
                risk_category="regulatory",
                summary=(defect_summary or subject or "").strip()[:5000],
                source_uri=source_uri,
                raw_location=raw_location,
                confidence=0.8,
                attributes={
                    "nhtsa_id": nhtsa_id,
                    "manufacturer": manufacturer,
                    "subject": subject,
                    "component": component,
                    "recall_type": recall_type,
                    "potentially_affected": potentially_affected,
                    "mfr_campaign_number": mfr_campaign_number,
                    "consequence_summary": (consequence or "").strip()[:5000],
                    "corrective_action": (corrective_action or "").strip()[:5000],
                },
            )
        )
    return out


class NhtsaProcessor(DataSourceProcessor):
    """MCP processor for NHTSA recalls; uses osint_swarm.data_sources.nhtsa."""

    def __init__(self, data_root: Optional[Path] = None):
        self.data_root = Path(data_root) if data_root else Path("data")
        self._raw_dir = self.data_root / "raw" / "nhtsa"

    @property
    def source_id(self) -> str:
        return "nhtsa"

    def _make_for_entity(self, entity: "Entity") -> Optional[str]:
        """Derive NHTSA 'make' from entity (identifiers or name)."""
        if entity.identifiers and entity.identifiers.get("make"):
            return entity.identifiers.get("make")
        if entity.name:
            # e.g. "Tesla, Inc." -> "TESLA"
            return entity.name.split(",")[0].strip().upper()
        return None

    def get_evidence_for_entity(self, entity: "Entity") -> List[Evidence]:
        make = self._make_for_entity(entity)
        if not make:
            return []
        entity_id = entity.entity_id

        cache_path = self._raw_dir / f"recalls_make_{make.upper()}.json"
        if cache_path.exists():
            payload = read_json(cache_path)
            raw_location = str(cache_path)
        else:
            payload = nhtsa.fetch_recalls_by_make(make)
            self._raw_dir.mkdir(parents=True, exist_ok=True)
            write_json(cache_path, payload)
            raw_location = str(cache_path)

        records = nhtsa.extract_recall_records(payload)
        return _records_to_evidence(records, entity_id, raw_location=raw_location)
