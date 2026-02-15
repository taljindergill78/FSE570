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

from osint_swarm.data_sources.nhtsa import cache_recalls_json, fetch_recalls_by_make


def main() -> None:
    ap = argparse.ArgumentParser(description="Pull NHTSA recalls for a vehicle make (cached to data/raw/nhtsa/).")
    ap.add_argument("--make", required=True, help="Vehicle make. Example: TESLA")
    args = ap.parse_args()

    payload = fetch_recalls_by_make(args.make)
    make_norm = args.make.strip().upper().replace(" ", "_")
    out_path = Path("data/raw/nhtsa") / f"recalls_make_{make_norm}.json"
    cache_recalls_json(payload, out_path=out_path)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

