from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from osint_swarm.data_sources.sec_edgar import cache_submissions_json, fetch_submissions, normalize_cik


def main() -> None:
    ap = argparse.ArgumentParser(description="Pull SEC submissions JSON for a CIK (cached to data/raw/sec/).")
    ap.add_argument("--cik", required=True, help="Company CIK (digits). Example: 0001318605")
    args = ap.parse_args()

    cik10 = normalize_cik(args.cik)
    submissions = fetch_submissions(cik10)

    out_path = Path("data/raw/sec") / f"CIK{cik10}.json"
    cache_submissions_json(submissions, out_path=out_path)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

