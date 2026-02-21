"""SEC EDGAR processor: fetches/caches submissions and returns Evidence."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Set

from osint_swarm.data_sources import sec_edgar
from osint_swarm.entities import Evidence
from osint_swarm.utils.io import read_json, write_json

from mcp_layer.base import DataSourceProcessor

if TYPE_CHECKING:
    from osint_swarm.entities import Entity


ARCHIVES_BASE = "https://www.sec.gov/Archives"


def _submissions_to_evidence(
    submissions: dict,
    entity_id: str,
    cik: str,
    raw_location: Optional[str] = None,
    *,
    forms: Optional[Set[str]] = None,
    max_filings: int = 500,
) -> List[Evidence]:
    """Convert SEC submissions JSON to Evidence list."""
    from osint_swarm.data_sources.sec_edgar import (
        extract_recent_filings,
        filing_primary_doc_url,
    )

    filings = extract_recent_filings(submissions, forms=forms)[:max_filings]
    out: List[Evidence] = []
    for f in filings:
        form = f.get("form") or "FILING"
        filing_date = f.get("filingDate") or ""
        accession = f.get("accessionNumber") or ""
        primary_doc = f.get("primaryDocument") or ""
        if not filing_date or not accession:
            continue
        accession_nodash = accession.replace("-", "")
        ev_id = f"{entity_id}_sec_{accession_nodash}".lower().replace(" ", "_")
        source_uri = filing_primary_doc_url(cik, accession, primary_doc) if primary_doc else f"{ARCHIVES_BASE}/edgar/data/{cik}/{accession_nodash}/"
        summary = f"SEC filing: {form} filed on {filing_date}"
        risk = "governance" if form in ("8-K", "4", "DEF 14A") else "regulatory"
        out.append(
            Evidence(
                evidence_id=ev_id,
                entity_id=entity_id,
                date=filing_date[:10] if len(filing_date) >= 10 else filing_date,
                source_type="sec_filing",
                risk_category=risk,
                summary=summary,
                source_uri=source_uri,
                raw_location=raw_location,
                confidence=0.85,
                attributes={
                    "form": form,
                    "accessionNumber": accession,
                    "primaryDocument": primary_doc,
                },
            )
        )
    return out


class SecEdgarProcessor(DataSourceProcessor):
    """MCP processor for SEC EDGAR; uses osint_swarm.data_sources.sec_edgar."""

    def __init__(self, data_root: Optional[Path] = None):
        self.data_root = Path(data_root) if data_root else Path("data")
        self._raw_dir = self.data_root / "raw" / "sec"

    @property
    def source_id(self) -> str:
        return "sec_edgar"

    def get_evidence_for_entity(self, entity: "Entity") -> List[Evidence]:
        cik = entity.identifiers.get("cik") if entity.identifiers else None
        if not cik:
            return []
        cik10 = sec_edgar.normalize_cik(cik)
        entity_id = entity.entity_id

        cache_path = self._raw_dir / f"CIK{cik10}.json"
        if cache_path.exists():
            submissions = read_json(cache_path)
            raw_location = str(cache_path)
        else:
            submissions = sec_edgar.fetch_submissions(cik10)
            self._raw_dir.mkdir(parents=True, exist_ok=True)
            write_json(cache_path, submissions)
            raw_location = str(cache_path)

        return _submissions_to_evidence(
            submissions, entity_id, cik10, raw_location=raw_location
        )
