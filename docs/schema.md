# Schema (v1)

The system operates over **structured Evidence records** (not raw web pages). Every claim must be citable.

## Entity

Minimum fields:
- `entity_id`: stable internal id (e.g., `tesla_inc_cik_0001318605`)
- `name`
- `entity_type`: `public_company | private_company | nonprofit | individual | unknown`
- `identifiers`: flexible map (e.g., `{"cik":"0001318605","ticker":"TSLA"}`)

## Evidence

Minimum fields:
- `evidence_id`: stable id (prefer deterministic generation)
- `entity_id`
- `date`: ISO `YYYY-MM-DD` (best-effort)
- `source_type`: where it came from (SEC filing, regulator API, court record, etc.)
- `risk_category`: `governance | regulatory | legal | network | other`
- `summary`: short claim text (human readable)
- `source_uri`: URL to primary source
- `raw_location`: file path under `data/raw/` (when applicable)
- `confidence`: 0..1
- `attributes`: JSON blob for additional structured fields (campaign numbers, forms, etc.)

