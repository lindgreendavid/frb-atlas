#!/usr/bin/env python3
"""Generate the POST-HOC source-clustering diagnostics (not part of the frozen v0.1 registry).

Usage: python scripts/generate_clustering.py --output reports/v0.2-source-clustering.json
       [--catalog data/external/chime_frb_catalog1.csv]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from frb_atlas.catalog import analyzable_bursts, load_bursts, split_by_repeater
from frb_atlas.clustering import build_clustering


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--catalog", default="data/external/chime_frb_catalog1.csv")
    args = parser.parse_args()

    bursts = analyzable_bursts(load_bursts(Path(args.catalog)))
    repeaters, non_repeaters = split_by_repeater(bursts)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as handle:
        json.dump(build_clustering(repeaters, non_repeaters), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
