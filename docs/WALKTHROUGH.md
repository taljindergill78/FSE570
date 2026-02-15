# Project Walkthrough: Autonomous OSINT Investigation Swarm

> **Author**: Taljinder Singh (Data Gathering & Preprocessing Lead)
> **Date**: February 15, 2026
> **Status**: Phase 1 complete (data infrastructure + Tesla vertical slice)

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [What Did We Build So Far?](#2-what-did-we-build-so-far)
3. [How the Data Pipeline Works (End-to-End Flow)](#3-how-the-data-pipeline-works-end-to-end-flow)
4. [Folder Structure: Every Folder and File Explained](#4-folder-structure-every-folder-and-file-explained)
5. [How We Got the Data](#5-how-we-got-the-data)
6. [What Is Hardcoded and Why](#6-what-is-hardcoded-and-why)
7. [Results So Far](#7-results-so-far)
8. [What Is Next](#8-what-is-next)
9. [How to Run Everything Yourself](#9-how-to-run-everything-yourself)
10. [FAQ](#10-faq)

---

## 1. What Is This Project?

We are building the **Autonomous OSINT Investigation Swarm** — a multi-agent AI system where a user can type a natural-language query like:

> "Investigate Tesla for any concerning patterns in executive turnover, regulatory issues, and unusual corporate structures"

...and the system autonomously:

1. Figures out what kind of entity "Tesla" is (public company, private LLC, individual, etc.)
2. Dispatches specialized AI agents — **Corporate Agent**, **Legal Agent**, **Social Graph Agent** — to investigate in parallel
3. Each agent pulls data from trusted public sources (SEC filings, NHTSA recalls, court records, news)
4. A **Reflexion layer** cross-checks findings across agents for consistency
5. The system produces a **risk-scored, court-ready report** with full source citations

### Team Roles (from the Charter)

| Role | Lead | What They Build |
|------|------|-----------------|
| Data Gathering & Preprocessing | **Taljinder** | Data source connectors, schemas, raw pipelines, curated ground-truth datasets |
| Modeling & Backend Development | Arnab, Raj | AI agents, orchestrator, reflexion/cross-validation logic, API layer |
| Frontend & Visualization | Aditya | Dashboard, knowledge graph UI, risk report templates |
| Deployment & Documentation | Jacob | CI/CD, cloud deployment, version control, docs |

### Why Data Infrastructure Comes First

The agents (Arnab/Raj's work) are the "brain" of the system — they decide *what* to search for and *how* to reason about findings. But they need "hands" to actually reach into SEC EDGAR, NHTSA databases, court records, etc. Those hands are the **data source connectors** and **schemas** that Taljinder builds.

Without this foundation:
- Agents wouldn't know how to call SEC or NHTSA APIs
- There would be no common format for evidence (each agent would output something different, and cross-referencing would be impossible)
- There would be no cached raw data for reproducibility or grading
- There would be no ground-truth dataset to test whether agents are finding the right things

---

## 2. What Did We Build So Far?

We completed **Phase 1: Data Infrastructure + Tesla Vertical Slice**. This means:

1. **A repo skeleton** that the whole team can build on top of (clear folder layout, dependency file, docs)
2. **Core data schemas** (`Entity` and `Evidence`) — the common language every agent, connector, and UI component will speak
3. **Two working data source connectors** (SEC EDGAR + NHTSA) — reusable Python modules that can pull data for *any* company, not just Tesla
4. **Three runnable scripts** that execute the full pull-and-transform pipeline
5. **A Tesla evidence dataset** — 91 real, citable evidence records from government sources, ready for agents to consume
6. **Documentation** — data sources blueprint + schema reference

---

## 3. How the Data Pipeline Works (End-to-End Flow)

Here is the flow from start to finish, step by step:

```
Step 1: PULL RAW DATA
   You run a script.
   It calls a government API over the internet.
   It downloads the full response as a JSON file.
   It saves that JSON file in data/raw/ (untouched, exactly as the API returned it).

Step 2: TRANSFORM INTO EVIDENCE
   You run the build script.
   It reads the raw JSON files from data/raw/.
   For each record (e.g., each NHTSA recall), it creates a standardized Evidence row
   with: ID, date, source type, risk category, summary, source URL, confidence score.
   It writes all rows into a single CSV file in data/processed/.

Step 3: AGENTS CONSUME THE EVIDENCE (future)
   Arnab/Raj's agents will read data/processed/tesla/evidence_tesla.csv.
   They will reason over these structured rows instead of scraping raw web pages.
   They will cross-reference, score risks, and generate reports.
```

Visually:

```
  [SEC EDGAR API]          [DOT DataHub / NHTSA]
        |                          |
        v                          v
  pull_sec_submissions.py    pull_nhtsa_recalls.py
        |                          |
        v                          v
  data/raw/sec/              data/raw/nhtsa/
  CIK0001318605.json         recalls_make_TESLA.json
        |                          |
        +----------+---------------+
                   |
                   v
         build_evidence_tesla.py
                   |
                   v
         data/processed/tesla/
         evidence_tesla.csv  (91 rows)
                   |
                   v
         [Future: Agents consume this]
```

---

## 4. Folder Structure: Every Folder and File Explained

```
Repo/
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/osint_swarm/               # Core library (reusable Python code)
│   ├── __init__.py
│   ├── entities.py
│   ├── data_sources/
│   │   ├── __init__.py
│   │   ├── sec_edgar.py
│   │   └── nhtsa.py
│   └── utils/
│       ├── __init__.py
│       └── io.py
│
├── scripts/                       # Runnable commands (execute these)
│   ├── pull_sec_submissions.py
│   ├── pull_nhtsa_recalls.py
│   └── build_evidence_tesla.py
│
├── data/                          # Generated data (not committed to git)
│   ├── raw/
│   │   ├── sec/
│   │   └── nhtsa/
│   └── processed/
│       └── tesla/
│
├── docs/                          # Documentation for the team
│   ├── schema.md
│   ├── data_sources.md
│   └── WALKTHROUGH.md             # This file
│
└── notebooks/                     # Reserved for Jupyter exploration
```

### Top-Level Files

#### `.gitignore`
Tells git which files/folders to **not** track. We exclude:
- `.venv/` — your local Python virtual environment (everyone creates their own)
- `__pycache__/` — Python's compiled bytecode cache (auto-generated)
- `data/raw/` and `data/processed/` — generated data files. These are outputs of the pipeline, not source code. Anyone can regenerate them by running the scripts.

#### `README.md`
The first thing a teammate (or professor) sees on GitHub. Contains: what the project is, how to set it up, and how to run the three scripts. Quick-start guide.

#### `requirements.txt`
Lists every Python package the project depends on. Right now it's just one:
- `requests` — the standard library for making HTTP calls to APIs

Anyone can install everything with: `pip install -r requirements.txt`

---

### `src/osint_swarm/` — The Core Library

This folder contains **reusable Python modules**. Nothing in here is run directly — instead, the scripts in `scripts/` import and use these modules. This separation means the same connector code can be used by scripts today and by agents tomorrow.

#### `__init__.py`
A one-line file that tells Python "this folder is a package you can import." Required boilerplate.

#### `entities.py` — The Data Contract

This is arguably the **most important file in the repo**. It defines two Python dataclasses:

**`Entity`** — represents the target of an investigation:
- `entity_id`: a stable internal ID (e.g., `tesla_inc_cik_0001318605`)
- `name`: human-readable name (e.g., "Tesla, Inc.")
- `entity_type`: what kind of entity — `public_company`, `private_company`, `nonprofit`, `individual`, or `unknown`
- `country`, `jurisdiction`: for future international support
- `identifiers`: a flexible dictionary for external IDs (CIK, ticker, OpenCorporates number, etc.)
- `aliases`: alternative names (e.g., "Tesla Motors Inc" is a former name for Tesla)

**`Evidence`** — represents a single citable claim about an entity:
- `evidence_id`: stable, unique ID for this piece of evidence
- `entity_id`: which entity this evidence is about (links back to an Entity)
- `date`: when this event happened (ISO format: `YYYY-MM-DD`)
- `source_type`: where this came from (`sec_filing`, `regulator_api`, `court_record`, `news_article`, etc.)
- `risk_category`: what kind of risk this represents (`governance`, `regulatory`, `legal`, `network`, `other`)
- `summary`: a short, human-readable description of the claim
- `source_uri`: a URL to the primary source (so anyone can verify it)
- `raw_location`: path to the cached raw file in `data/raw/` (for traceability)
- `confidence`: a score from 0 to 1 indicating how reliable this evidence is
- `attributes`: a flexible dictionary for any extra structured data (NHTSA campaign numbers, SEC form types, etc.)

**Why this matters**: Every agent, every connector, every UI component in the system will produce and consume `Evidence` records in this exact format. It's the common language. If you change this schema, you change the entire system.

#### `data_sources/sec_edgar.py` — SEC EDGAR Connector

Handles all communication with the SEC's EDGAR system. Key functions:

- `fetch_submissions(cik)`: Hits `https://data.sec.gov/submissions/CIK{cik}.json` and returns Tesla's full filing history (every 10-K, 8-K, 10-Q, DEF 14A, etc. they've ever filed). Requires a `SEC_USER_AGENT` environment variable (SEC's policy requires you to identify yourself).
- `extract_recent_filings(submissions, forms, start_date, end_date)`: Filters the raw filing list to only the form types and date range you care about.
- `filing_primary_doc_url(cik, accession, doc)`: Builds the URL to the actual filing document on SEC.gov.
- `cache_submissions_json(submissions, out_path)`: Saves the raw JSON to disk.

**This connector is generic** — pass any company's CIK and it works. It's not Tesla-specific.

#### `data_sources/nhtsa.py` — NHTSA Recalls Connector

Handles communication with NHTSA's recall database. Key functions:

- `fetch_recalls_by_make(make)`: Queries the DOT DataHub for all recall campaigns matching a manufacturer name (e.g., "TESLA"). Returns every recall Tesla has ever had — defect descriptions, consequences, remedies, affected vehicle counts, etc.
- `extract_recall_records(payload)`: Extracts the list of recall records from the API response.
- `cache_recalls_json(payload, out_path)`: Saves the raw JSON to disk.

**This connector is also generic** — pass any vehicle make ("FORD", "BMW", etc.) and it works.

#### `utils/__init__.py`
Package marker for the utils folder.

#### `utils/io.py` — File I/O Helpers

Small utility functions used by everything else:
- `write_json(path, obj)`: Write a Python object to a JSON file (creating parent directories if needed)
- `read_json(path)`: Read a JSON file back into a Python object
- `write_csv_dicts(path, rows, fieldnames)`: Write a list of dictionaries to a CSV file with a header row

---

### `scripts/` — Runnable Commands

These are the scripts you actually execute from the terminal. Each one does one specific job.

#### `pull_sec_submissions.py`

**What it does**: Fetches Tesla's complete SEC filing history and saves it locally.

**How to run**:
```bash
export SEC_USER_AGENT="Your Name your_email@example.com"
python scripts/pull_sec_submissions.py --cik 0001318605
```

**What it produces**: `data/raw/sec/CIK0001318605.json` — a large JSON file containing metadata for every SEC filing Tesla has ever made (form type, filing date, accession number, primary document name).

**Why it exists**: This raw filing index is the starting point for the Corporate Agent. It tells you *what* filings exist. (Actually reading their contents and extracting meaning is a future step.)

#### `pull_nhtsa_recalls.py`

**What it does**: Fetches every NHTSA recall campaign for Tesla and saves it locally.

**How to run**:
```bash
python scripts/pull_nhtsa_recalls.py --make TESLA
```

**What it produces**: `data/raw/nhtsa/recalls_make_TESLA.json` — a JSON file with ~90 recall records, each containing the defect description, consequence, remedy, number of affected vehicles, NHTSA campaign ID, and a link to the official recall page.

**Why it exists**: Recall data is a primary signal for the "regulatory" risk category. This gives us real, government-sourced evidence records.

#### `build_evidence_tesla.py`

**What it does**: Reads the raw files produced by the two pull scripts above, transforms each record into a standardized `Evidence` row, and writes the final CSV.

**How to run**:
```bash
python scripts/build_evidence_tesla.py
```

**What it produces**: `data/processed/tesla/evidence_tesla.csv` — 91 rows, each one a structured evidence record ready for agents to consume.

**Why it exists**: This is the "bridge" between raw API responses and the standardized format agents need. Raw JSON from SEC and NHTSA have completely different schemas. This script normalizes them both into the same `Evidence` format.

---

### `data/` — Generated Data

**This entire folder is in `.gitignore`** — it's not committed to git. Anyone can regenerate it by running the three scripts above.

#### `data/raw/` — Cached Raw Downloads

Contains the untouched JSON files exactly as the APIs returned them.

- `data/raw/sec/CIK0001318605.json` — Tesla's SEC filing history
- `data/raw/nhtsa/recalls_make_TESLA.json` — Tesla's NHTSA recall campaigns

**Why we keep raw files**: Traceability and reproducibility. If someone questions a claim in the evidence table, we can point to the exact raw record it came from. Also, caching means we don't hit the APIs repeatedly during development.

#### `data/processed/` — Normalized Evidence Tables

Contains the final output that agents consume.

- `data/processed/tesla/evidence_tesla.csv` — 91 evidence records in the standardized schema

---

### `docs/` — Documentation

#### `schema.md`
Reference document for the `Entity` and `Evidence` data models. Lists every field, its type, and valid values. Useful when building agents or UI components that need to produce/consume these records.

#### `data_sources.md`
Lists every data source we use (or plan to use), with exact API endpoints, access notes (rate limits, authentication requirements), and caching strategy. This is the "playbook" for adding new connectors.

#### `WALKTHROUGH.md`
This file. The comprehensive guide to everything we built so far.

### `notebooks/` — Reserved

Empty for now. This is where Jupyter notebooks for data exploration will go (e.g., "load the evidence CSV, plot recalls by year, check for gaps in coverage").

---

## 5. How We Got the Data

### SEC EDGAR (Filing Metadata)

- **Source**: The U.S. Securities and Exchange Commission's EDGAR system
- **Endpoint**: `https://data.sec.gov/submissions/CIK0001318605.json`
- **Access**: Free, public, no API key needed. SEC requires a valid `User-Agent` header with your name and email (their fair-use policy).
- **What it returns**: A JSON object containing Tesla's company info (name, CIK, ticker, SIC code, addresses) and a list of every filing they've made (form type, date, accession number, primary document).
- **How we use it**: We cache the raw JSON. Currently, we only use it as a filing index (what forms were filed and when). We don't yet download or parse the actual filing documents — that's a future step.

### NHTSA / DOT DataHub (Recall Campaigns)

- **Source**: The National Highway Traffic Safety Administration's Office of Defects Investigation
- **Endpoint**: `https://datahub.transportation.gov/resource/6axg-epim.json` (DOT DataHub, Socrata API)
- **Access**: Free, public, no API key needed.
- **What it returns**: A list of recall campaigns for Tesla, each containing: NHTSA campaign ID, report date, defect summary, consequence, corrective action, number of affected vehicles, and a link to the official recall page.
- **How we use it**: Each recall record becomes one `Evidence` row with `source_type="regulator_api"` and `risk_category="regulatory"`.

**Important note about the NHTSA endpoint**: The original plan assumed we'd use `https://api.nhtsa.gov/recalls/recallsByMake?make=TESLA`. This endpoint now returns HTTP 403 (it appears to have been retired or locked behind authentication). We switched to the DOT DataHub, which serves the exact same NHTSA recall dataset through a different, fully public portal. The data is identical — same fields, same source agency.

---

## 6. What Is Hardcoded and Why

There is **exactly one hardcoded thing** in the codebase:

### The SEC "CFO Transition" Evidence Row

In `scripts/build_evidence_tesla.py`, the function `build_sec_seed_evidence()` (lines 29–52) contains a **manually written** evidence record:

```
evidence_id: tesla_sec_cfo_2023_08_04
date: 2023-08-04
summary: "Tesla appointed Vaibhav Taneja as CFO to succeed Zachary Kirkhorn;
          Kirkhorn stepped down after a 13-year tenure."
source_uri: https://www.sec.gov/Archives/edgar/data/1318605/000095017023038779/tsla-20230804.htm
```

**Why it's hardcoded**:

The SEC connector (`pull_sec_submissions.py`) fetches Tesla's filing *index* — it tells you "on August 7, 2023, Tesla filed an 8-K." But it doesn't read the *contents* of that 8-K or extract meaning from it.

To automatically turn "8-K filed on 2023-08-04" into "CFO Kirkhorn stepped down" would require:
1. Downloading the actual HTML/PDF filing from SEC Archives
2. Parsing the document text
3. Running NLP or an LLM to extract the governance event

That extraction logic is the job of the **Corporate Agent** (Arnab/Raj's domain). We don't have agents yet.

So this one row is a **manually curated seed** — it gives the evidence table at least one governance-category record so it's not empty on that dimension. It's clearly marked in the code and will be replaced by automated extraction once agents are built.

**Everything else (all 90 NHTSA rows) is fully automated** — fetched from the DOT DataHub API and transformed programmatically. No hardcoding.

---

## 7. Results So Far

### What the Evidence Table Looks Like

`data/processed/tesla/evidence_tesla.csv` contains **91 rows**:

| Category | Count | Source |
|----------|-------|--------|
| Regulatory (recalls) | 90 | NHTSA via DOT DataHub (automated) |
| Governance (executive change) | 1 | SEC 8-K filing (manually seeded) |
| **Total** | **91** | |

Each row has:
- A unique `evidence_id` (e.g., `tesla_nhtsa_25v735000`)
- A link to `tesla_inc_cik_0001318605` (the entity)
- A date (e.g., `2025-10-28`)
- Source type (`regulator_api` or `sec_filing`)
- Risk category (`regulatory` or `governance`)
- A human-readable summary of what happened
- A clickable URL to the primary source on NHTSA.gov or SEC.gov
- A confidence score (0.8 for automated recalls, 0.95 for the verified SEC seed)
- An `attributes` JSON blob with extra structured data (NHTSA campaign ID, affected vehicle count, component, etc.)

### Example Rows

**Regulatory (automated from NHTSA)**:
> `tesla_nhtsa_25v092000` | 2025-02-14 | "Tesla is recalling certain 2023 Model 3 and Model Y vehicles. The printed circuit board for the electronic power steering assist may experience an overstress condition, causing a loss of power steering assist..." | 376,241 vehicles affected

**Governance (manually seeded from SEC)**:
> `tesla_sec_cfo_2023_08_04` | 2023-08-04 | "Tesla appointed Vaibhav Taneja as CFO to succeed Zachary Kirkhorn; Kirkhorn stepped down after a 13-year tenure." | Source: SEC 8-K

---

## 8. What Is Next

### Immediate Next Steps (Taljinder — Data)

1. **Add more SEC-based seed evidence rows** — Hand-curate rows for key governance events (DOJ subpoenas, Drew Baglino resignation, board departures) and legal events (range lawsuit, Autopilot investigation). This expands coverage across all risk categories, not just regulatory.

2. **SEC filing content extraction** — Right now we pull the filing *index* but don't read filing *contents*. Next: download specific 8-K and 10-K filings and extract governance signals (executive changes, disclosed investigations, risk factor disclosures). This can start as manual extraction and transition to automated once agents exist.

3. **Test with a second company** — Run the same pipeline for a different entity (e.g., Ford, Apple) to prove the connectors and schema are truly generic and not accidentally Tesla-specific.

4. **Add a CourtListener connector** — CourtListener/RECAP provides free access to federal court documents. This would fill the "legal" risk category with real lawsuit filings.

### Team Handoff Points

| Teammate | What they can start building now | What they need from the data layer |
|----------|----------------------------------|-----------------------------------|
| **Arnab, Raj** (Agents) | Lead Agent orchestrator, Corporate Agent that reads `evidence_tesla.csv`, Reflexion/cross-validation logic | Import `sec_edgar.py` and `nhtsa.py` connectors; use `Entity`/`Evidence` schemas from `entities.py` |
| **Aditya** (Frontend) | Risk dashboard, evidence table viewer, timeline visualization | Read `evidence_tesla.csv` as the data source; use `risk_category` for grouping, `date` for timelines, `confidence` for scoring |
| **Jacob** (DevOps) | GitHub repo setup, CI pipeline, deployment config | The repo skeleton is ready; add CI that runs the three scripts to verify the pipeline works |

---

## 9. How to Run Everything Yourself

### Prerequisites
- Python 3.9+ (check with `python --version`)
- `pip` (comes with Python)
- `git`

### Step 1: Clone the Repo

```bash
git clone <repo-url>
cd Repo
```

Replace `<repo-url>` with the actual GitHub URL (e.g., `https://github.com/your-org/your-repo.git`).

### Step 2: Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python.

```bash
python -m venv .venv
```

Then activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

You'll know it's active when your terminal prompt shows `(.venv)` at the beginning.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs two packages:
- `requests` — for making HTTP calls to SEC and NHTSA APIs
- `python-dotenv` — for auto-loading environment variables from the `.env` file

### Step 4: Set Up Your `.env` File

The repo includes a `.env.example` template. Copy it to create your own `.env`:

```bash
cp .env.example .env
```

Then open `.env` in any text editor and replace the placeholder with your real name and email:

```
SEC_USER_AGENT="Your Name your_email@example.com"
```

This is required by the SEC (their fair-use policy — they want to know who's calling their API). It's not a password or API key, just your identity. **Your `.env` file is gitignored and will never be pushed to GitHub.**

### Step 5: Run the Pipeline

Now you can run all three scripts. No manual `export` commands needed — the scripts auto-load your `.env` file.

```bash
# Pull SEC filing metadata for Tesla
python scripts/pull_sec_submissions.py --cik 0001318605

# Pull NHTSA recalls for Tesla
python scripts/pull_nhtsa_recalls.py --make TESLA

# Build the evidence table from the raw data above
python scripts/build_evidence_tesla.py
```

### Step 6: Verify the Output

After running all three scripts, you should see these files:

```
data/
├── raw/
│   ├── sec/
│   │   └── CIK0001318605.json          ← Tesla's SEC filing history
│   └── nhtsa/
│       └── recalls_make_TESLA.json      ← Tesla's NHTSA recall campaigns
└── processed/
    └── tesla/
        └── evidence_tesla.csv           ← 91 structured evidence rows
```

Open `evidence_tesla.csv` in any spreadsheet app or text editor to inspect the results.

### Running for a Different Company

The connectors are generic — they work for any company, not just Tesla. For example, to pull Ford's data:

```bash
# Ford's CIK is 0000037996
python scripts/pull_sec_submissions.py --cik 0000037996

# Ford's make name
python scripts/pull_nhtsa_recalls.py --make FORD
```

You can look up any company's CIK at [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany).

(You'd then need a `build_evidence_ford.py` script, or generalize `build_evidence_tesla.py` to accept a company parameter — that's a near-term improvement.)


---

## 10. FAQ

### Q: Why is `data/` not in git?

Because it's generated output, not source code. Anyone can reproduce it by running the three scripts. Committing large JSON files to git bloats the repo and creates merge conflicts. The scripts *are* in git, so the pipeline is fully reproducible.

### Q: Why did we use DOT DataHub instead of the NHTSA API?

The original NHTSA recalls API (`api.nhtsa.gov/recalls/recallsByMake`) started returning HTTP 403 errors (it appears to require an API key that isn't publicly documented, or has been retired). The DOT DataHub (`datahub.transportation.gov`) serves the exact same NHTSA recall dataset through a public Socrata endpoint. Same data, same source agency, no authentication needed.

### Q: Why is there only 1 governance row and 90 regulatory rows?

Because the NHTSA connector automatically converts every recall into an evidence row, but the SEC connector currently only pulls the filing *index* (list of forms filed), not the filing *contents*. Extracting governance events from filing text requires either manual curation or NLP/LLM extraction. We seeded one manually; more will be added.

### Q: Can I add evidence rows manually?

Yes, and you should. The `build_sec_seed_evidence()` function in `build_evidence_tesla.py` is the place to add hand-curated rows. Just create a new `Evidence(...)` object following the same pattern. Make sure every row has a real `source_uri` pointing to a primary source.

### Q: What's a CIK?

CIK (Central Index Key) is the SEC's unique identifier for every company that files with them. Tesla's is `0001318605`. You can look up any company's CIK at [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany).

### Q: What does `confidence` mean?

It's a number from 0 to 1 representing how reliable we consider this evidence:
- **0.95**: Directly verified from a primary government source (e.g., an SEC filing we manually read and confirmed)
- **0.80**: Automatically extracted from a reliable API (e.g., NHTSA recall records — the data is authoritative but we haven't manually verified every field)
- **0.50**: Default / unverified
- Lower values would be used for less reliable sources (social media, unverified news, etc.)

### Q: How do agents use this data?

Agents will import the connectors from `src/osint_swarm/data_sources/` to pull raw data, and they'll read the evidence CSV (or call the build functions directly) to get structured evidence. The `Evidence` schema ensures every agent outputs data in the same format, which makes cross-referencing possible in the Reflexion layer.

---

*Questions? Reach out to Taljinder or post in the team channel.*
