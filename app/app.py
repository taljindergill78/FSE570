"""Flask demo app: run investigation from a web form and display results."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for p in (ROOT, SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from flask import Flask, render_template, request

from app.pipeline import run_investigation

app = Flask(__name__, template_folder=Path(__file__).resolve().parent / "templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    query = (request.form.get("query") or "").strip()
    if not query:
        return render_template("index.html", error="Please enter an investigation query.")
    data_root = ROOT / "data"
    result = run_investigation(query, data_root=data_root)
    # Extract body fragment for embedding (report_html is full document)
    if result.get("report_html"):
        html = result["report_html"]
        if "<body>" in html and "</body>" in html:
            start = html.index("<body>") + len("<body>")
            end = html.index("</body>")
            result["report_body"] = html[start:end].strip()
        else:
            result["report_body"] = html
    else:
        result["report_body"] = ""
    return render_template("results.html", result=result)


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
