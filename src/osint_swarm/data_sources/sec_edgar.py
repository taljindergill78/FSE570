from __future__ import annotations

import os
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

import requests

from osint_swarm.utils.io import write_json


SEC_BASE = "https://data.sec.gov"
ARCHIVES_BASE = "https://www.sec.gov/Archives"


class SecEdgarError(RuntimeError):
    pass


def _sec_headers() -> Dict[str, str]:
    ua = os.environ.get("SEC_USER_AGENT") or os.environ.get("SEC_UA")
    if not ua:
        raise SecEdgarError(
            "Missing SEC user agent. Set environment variable SEC_USER_AGENT "
            'to something like: "Your Name your_email@example.com"'
        )
    return {
        "User-Agent": ua,
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov",
    }


def normalize_cik(cik: str) -> str:
    cik = cik.strip()
    if cik.isdigit():
        return cik.zfill(10)
    raise ValueError(f"CIK must be digits only, got: {cik!r}")


def fetch_submissions(cik: str, *, sleep_s: float = 0.2) -> Dict[str, Any]:
    """Fetch SEC company submissions JSON for a CIK."""
    cik10 = normalize_cik(cik)
    url = f"{SEC_BASE}/submissions/CIK{cik10}.json"
    resp = requests.get(url, headers=_sec_headers(), timeout=30)
    if resp.status_code != 200:
        raise SecEdgarError(f"SEC submissions request failed ({resp.status_code}): {url}")
    time.sleep(sleep_s)
    return resp.json()


def extract_recent_filings(
    submissions: Dict[str, Any],
    *,
    forms: Optional[Set[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Extract a normalized list of recent filings from submissions JSON."""
    recent = submissions.get("filings", {}).get("recent", {})
    form_list: Sequence[str] = recent.get("form", []) or []
    date_list: Sequence[str] = recent.get("filingDate", []) or []
    accession_list: Sequence[str] = recent.get("accessionNumber", []) or []
    primary_doc_list: Sequence[str] = recent.get("primaryDocument", []) or []

    out: List[Dict[str, Any]] = []
    for form, filing_date, accession, primary_doc in zip(
        form_list, date_list, accession_list, primary_doc_list
    ):
        if forms and form not in forms:
            continue
        if start_date and filing_date < start_date:
            continue
        if end_date and filing_date > end_date:
            continue
        out.append(
            {
                "form": form,
                "filingDate": filing_date,
                "accessionNumber": accession,
                "primaryDocument": primary_doc,
            }
        )
    return out


def accession_to_archives_path(cik: str, accession_number: str) -> str:
    """Build SEC Archives path from accession (with dashes)."""
    cik_no_pad = str(int(cik))  # remove left padding for Archives path
    accession_nodash = accession_number.replace("-", "")
    return f"/edgar/data/{cik_no_pad}/{accession_nodash}/"


def filing_primary_doc_url(cik: str, accession_number: str, primary_document: str) -> str:
    return (
        f"{ARCHIVES_BASE}{accession_to_archives_path(cik, accession_number)}{primary_document}"
    )


def cache_submissions_json(submissions: Dict[str, Any], *, out_path: Path) -> None:
    write_json(out_path, submissions)

