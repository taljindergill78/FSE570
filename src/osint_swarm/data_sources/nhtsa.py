from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from osint_swarm.utils.io import write_json


DOT_DATAHUB_BASE = "https://datahub.transportation.gov"
ODI_RECALLS_VIEW_ID = "6axg-epim"  # tabular view powering "NHTSA Recalls by Manufacturer"


class NhtsaError(RuntimeError):
    pass


def fetch_recalls_by_make(make: str) -> Dict[str, Any]:
    """Fetch recall campaigns for a make/manufacturer (e.g., TESLA).

    NOTE: As of 2026, the old `api.nhtsa.gov/recalls/...` endpoints may return 403.
    This function uses the DOT DataHub (Socrata) tabular view instead.

    Returns a dict with a single `results` list for consistency with earlier code.
    """
    make_norm = make.strip().upper()

    # SoQL: match manufacturer name containing the make string (e.g., "Tesla, Inc.")
    where = f"upper(manufacturer) like '%{make_norm}%'"
    url = f"{DOT_DATAHUB_BASE}/resource/{ODI_RECALLS_VIEW_ID}.json"

    all_rows: List[Dict[str, Any]] = []
    limit = 5000
    offset = 0
    while True:
        resp = requests.get(
            url,
            params={
                "$limit": limit,
                "$offset": offset,
                "$where": where,
            },
            headers={"Accept": "application/json", "User-Agent": "capstone-osint-swarm/0.1"},
            timeout=30,
        )
        if resp.status_code != 200:
            raise NhtsaError(f"DOT DataHub request failed ({resp.status_code}): {resp.url}")
        batch = resp.json()
        if not isinstance(batch, list) or not batch:
            break
        all_rows.extend([r for r in batch if isinstance(r, dict)])
        if len(batch) < limit:
            break
        offset += limit

    return {"results": all_rows, "source": url, "where": where}


def extract_recall_records(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return normalized recall records list."""
    results = payload.get("results") or payload.get("Results") or []
    if not isinstance(results, list):
        return []
    # Keep records as-is, but ensure dict type.
    return [r for r in results if isinstance(r, dict)]


def cache_recalls_json(payload: Dict[str, Any], *, out_path: Path) -> None:
    write_json(out_path, payload)

