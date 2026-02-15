# Data Sources Blueprint (v1)

This capstone needs sources that are **trusted, citable, and reproducible**.

## Core sources (should always work)

### SEC EDGAR (US public companies)
- **What we use**: company submissions JSON (filing metadata)
- **Endpoint**: `https://data.sec.gov/submissions/CIK{CIK10}.json`
- **Notes**:
  - Use a valid `User-Agent` (set `SEC_USER_AGENT`)
  - Cache raw JSON to `data/raw/sec/`

### NHTSA Recalls API (US vehicle safety recalls)
- **What we use**: recall campaigns by manufacturer (starting with Tesla)
- **Endpoint (v1)** (public DOT DataHub tabular view):
  - `https://datahub.transportation.gov/resource/6axg-epim.json?...`
- **Why**:
  - In some environments (including many school networks), the legacy endpoints under `api.nhtsa.gov/recalls/...` can return 403.
- **Notes**:
  - Cache raw JSON to `data/raw/nhtsa/`
  - Later enrichment: link campaigns to Part 573 PDFs on `static.nhtsa.gov`

### CourtListener / RECAP (free court documents)
- **What we use**: PDFs of filings (complaints, orders) when available
- **Notes**:
  - Store PDFs under `data/raw/courtlistener/` and emit `Evidence` rows with citations

## Extension sources (optional / may be rate-limited or paywalled)
- GDELT (news/event coverage at scale)
- State registries / OpenCorporates (private companies, international)
- Social platforms (LinkedIn/Twitter) — likely not reliable for automated ingestion in capstone constraints

