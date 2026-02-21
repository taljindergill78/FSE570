# OSINT Investigation Swarm — Flask Demo

Web UI to run the full investigation pipeline: enter a query (e.g. "Investigate Tesla for money laundering"), run the pipeline, and view results (entity, tasks, findings, risk dashboard, gaps, report, audit trail).

## Run the app

From the **project root** (FSE570):

```bash
# Activate venv and install deps if needed
source .venv/bin/activate   # or: .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Start the Flask server
python app/app.py
```

Then open **http://127.0.0.1:5000** in your browser. Enter an investigation query and click **Run investigation**.

## Alternative

```bash
cd /path/to/FSE570
FLASK_APP=app/app.py flask run --host=0.0.0.0 --port=5000
```

## What runs

1. **Lead Agent** — Resolves entity (e.g. "Tesla" → Tesla, Inc.), decomposes the query into tasks, and dispatches to specialist agents.
2. **Specialist agents** — Corporate (SEC + NHTSA via MCP), Legal (stubs), Social Graph (stubs).
3. **Reflexion** — Cross-check (conflicts), gap detection, confidence scores.
4. **Knowledge graph** — Built from evidence (nodes/edges summary).
5. **Output** — Evidence report (by risk category), risk dashboard, audit trail.

Results are shown on one page: query & entity, tasks & finding counts, risk dashboard, gaps, conflicts (if any), full evidence report, and audit events.
