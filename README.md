# Autonomous OSINT Investigation Swarm (Capstone)

This repository is the implementation for **Autonomous OSINT Investigation Swarm** — a modular, multi-agent system for corporate/entity risk assessment.

## Architecture

![Autonomous OSINT Investigation Swarm architecture](Architecture Diagram.jpeg)

## Quickstart

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd Repo

# 2. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your .env (one time)
cp .env.example .env
# Open .env and replace the placeholder with your name/email

# 5. Run the pipeline (Tesla vertical slice)
python scripts/pull_sec_submissions.py --cik 0001318605
python scripts/pull_nhtsa_recalls.py --make TESLA
python scripts/build_evidence_tesla.py
```

**Output**: `data/processed/tesla/evidence_tesla.csv` (91 structured evidence rows from SEC + NHTSA).

For the full walkthrough, see [`docs/WALKTHROUGH.md`](docs/WALKTHROUGH.md).

## Repo layout

- `src/osint_swarm/`: core library (schemas + connectors)
- `scripts/`: runnable ingestion/build scripts
- `data/raw/`: cached raw source files (traceability)
- `data/processed/`: normalized evidence tables used by agents
- `docs/`: data sources blueprint + schemas

## Notes

- The v1 pipeline uses **authoritative, open sources**: SEC EDGAR + NHTSA (plus optional CourtListener artifacts).
- NHTSA recall ingestion uses the DOT **DataHub** tabular dataset (public), since the legacy `api.nhtsa.gov/recalls/...` endpoints may return 403.
- Paywalled sources (PACER/Reuters/etc.) are treated as future extensions.

