"""Command-line entry point for FRB Atlas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from frb_atlas.registry import build_registry


def _cmd_summarize(args: argparse.Namespace) -> int:
    registry = build_registry(Path(args.catalog))
    catalog = registry["catalog"]
    print(
        f"{catalog['analyzed_bursts']} analyzed bursts "
        f"({catalog['repeater_bursts']} repeater, {catalog['non_repeater_bursts']} non-repeater) "
        f"of {catalog['total_bursts']} total, {catalog['excluded_bursts']} excluded"
    )
    dm = registry["comparisons"]["dm_exc_ne2001_primary"]["ks"]
    width = registry["comparisons"]["width_fitb"]["ks"]
    print(f"DM (NE2001 excess) KS p-value: {dm['p_value']:.4g} (significant={dm['significant']})")
    print(
        f"Width (fitburst) KS p-value: {width['p_value']:.4g} (significant={width['significant']})"
    )
    return 0


def _cmd_registry(args: argparse.Namespace) -> int:
    registry = build_registry(Path(args.catalog))
    text = json.dumps(registry, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    else:
        sys.stdout.write(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="frb-atlas", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize = subparsers.add_parser("summarize", help="Print a short summary of the catalog")
    summarize.add_argument("catalog", help="Path to the normalized catalog CSV")
    summarize.set_defaults(func=_cmd_summarize)

    registry = subparsers.add_parser("registry", help="Build and print the full result registry")
    registry.add_argument("catalog", help="Path to the normalized catalog CSV")
    registry.add_argument("--output", help="Write JSON to this path instead of stdout")
    registry.set_defaults(func=_cmd_registry)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
