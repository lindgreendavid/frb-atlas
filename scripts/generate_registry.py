#!/usr/bin/env python3
"""Generate the frozen v0.1.0 result registry deterministically.

Usage: python scripts/generate_registry.py --output reports/v0.1-frb-registry.json
       [--catalog data/external/chime_frb_catalog1.csv]

Requires the normalized catalog CSV to already exist locally (see
``scripts/fetch_catalog.py``). Regenerates byte-identically given a fixed
catalog and the fixed bootstrap seed in ``frb_atlas.stats``, and is checked
against the committed registry by ``tests/test_registry.py`` and the CI
``research-registry`` job.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from frb_atlas.registry import build_registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--catalog",
        default="data/external/chime_frb_catalog1.csv",
        help="Path to the normalized catalog CSV produced by scripts/fetch_catalog.py",
    )
    args = parser.parse_args()

    registry = build_registry(Path(args.catalog))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
