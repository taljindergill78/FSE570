from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from osint_swarm.entities import Evidence
from osint_swarm.utils.io import read_json, write_csv_dicts


TESLA_ENTITY_ID = "tesla_inc_cik_0001318605"


def _safe_get(d: Dict[str, Any], *keys: str) -> Any:
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def build_sec_seed_evidence() -> List[Evidence]:
    # Seed 1 governance event with primary SEC source (8-K).
    # This provides an immediately usable, fully citable row.
    return [
        Evidence(
            evidence_id="tesla_sec_cfo_2023_08_04",
            entity_id=TESLA_ENTITY_ID,
            date="2023-08-04",
            source_type="sec_filing",
            risk_category="governance",
            summary=(
                "Tesla appointed Vaibhav Taneja as CFO to succeed Zachary Kirkhorn; "
                "Kirkhorn stepped down after a 13-year tenure."
            ),
            source_uri="https://www.sec.gov/Archives/edgar/data/1318605/000095017023038779/tsla-20230804.htm",
            raw_location=None,
            confidence=0.95,
            attributes={
                "form": "8-K",
                "accession": "0000950170-23-038779",
                "item": "5.02",
            },
        )
    ]


def build_nhtsa_evidence(raw_path: Path) -> List[Evidence]:
    payload = read_json(raw_path)
    records = payload.get("results") or payload.get("Results") or []
    out: List[Evidence] = []

    for r in records:
        if not isinstance(r, dict):
            continue

        # DOT DataHub schema (2026): `nhtsa_id`, `report_received_date`, `defect_summary`, etc.
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
            # Skip records without a date; evidence requires a sortable date.
            continue

        source_uri = recall_url or "https://www.nhtsa.gov/recalls"
        ev_id = f"tesla_nhtsa_{(nhtsa_id or mfr_campaign_number or report_date)}".lower().replace(" ", "_")
        out.append(
            Evidence(
                evidence_id=ev_id,
                entity_id=TESLA_ENTITY_ID,
                date=str(report_date)[:10],
                source_type="regulator_api",
                risk_category="regulatory",
                summary=(defect_summary or subject or "").strip()[:5000],
                source_uri=source_uri,
                raw_location=str(raw_path),
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


def main() -> None:
    raw_nhtsa = Path("data/raw/nhtsa/recalls_make_TESLA.json")
    if not raw_nhtsa.exists():
        raise SystemExit(
            "Missing NHTSA raw file. Run: python scripts/pull_nhtsa_recalls.py --make TESLA"
        )

    evidence: List[Evidence] = []
    evidence.extend(build_sec_seed_evidence())
    evidence.extend(build_nhtsa_evidence(raw_nhtsa))

    rows = [e.to_dict() for e in evidence]
    # Flatten attributes as JSON string for CSV portability.
    for row in rows:
        row["attributes"] = json.dumps(row.get("attributes") or {}, ensure_ascii=False)

    out_path = Path("data/processed/tesla/evidence_tesla.csv")
    fieldnames = [
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
    write_csv_dicts(out_path, rows, fieldnames=fieldnames)
    print(f"Wrote: {out_path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

