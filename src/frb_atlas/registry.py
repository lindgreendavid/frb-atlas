"""Build the frozen v0.1.0 result registry from the normalized catalog CSV.

This module implements exactly the preregistered plan in
`docs/research-protocol.md`: load the catalog, apply the disclosed
exclusion, split into repeater/non-repeater groups, and run the primary and
robustness statistical comparisons on DM, pulse width, and spectral
bandwidth.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from frb_atlas.catalog import (
    Burst,
    analyzable_bursts,
    first_detection_per_source,
    load_bursts,
    split_by_repeater,
)
from frb_atlas.stats import (
    ALPHA,
    DEFAULT_BOOTSTRAP_RESAMPLES,
    DEFAULT_SEED,
    anderson_darling_two_sample,
    bootstrap_median_diff,
    ks_two_sample,
)

SCHEMA_VERSION = 1


def _comparison(
    label: str,
    repeater_values: list[float],
    non_repeater_values: list[float],
) -> dict[str, Any]:
    ks = ks_two_sample(non_repeater_values, repeater_values)
    anderson = anderson_darling_two_sample(non_repeater_values, repeater_values)
    boot = bootstrap_median_diff(repeater_values, non_repeater_values)
    return {
        "label": label,
        "n_repeater": len(repeater_values),
        "n_non_repeater": len(non_repeater_values),
        "ks": {
            "statistic": ks.statistic,
            "p_value": ks.p_value,
            "significant": ks.significant,
            "alpha": ALPHA,
        },
        "anderson_darling": {
            "statistic": anderson.statistic,
            "p_value": anderson.p_value,
            "significant": anderson.significant,
            "alpha": ALPHA,
        },
        "bootstrap": {
            "median_repeater": boot.median_a,
            "median_non_repeater": boot.median_b,
            "median_diff_non_repeater_minus_repeater": boot.median_diff,
            "ci_95_low": boot.ci_low,
            "ci_95_high": boot.ci_high,
            "resamples": boot.resamples,
            "seed": boot.seed,
        },
    }


def _dm(bursts: list[Burst], attr: str) -> list[float]:
    return [getattr(b, attr) for b in bursts]


def build_registry(catalog_path: Path) -> dict[str, Any]:
    all_bursts = load_bursts(catalog_path)
    excluded = [b for b in all_bursts if b.excluded_flag]
    analyzed = analyzable_bursts(all_bursts)
    repeaters, non_repeaters = split_by_repeater(analyzed)

    width_repeaters_full = _dm(repeaters, "width_fitb")
    width_non_repeaters_full = _dm(non_repeaters, "width_fitb")
    bandwidth_repeaters_full = [b.bandwidth for b in repeaters]
    bandwidth_non_repeaters_full = [b.bandwidth for b in non_repeaters]

    repeaters_no_limits = [b for b in repeaters if not b.width_fitb_is_limit]
    non_repeaters_no_limits = [b for b in non_repeaters if not b.width_fitb_is_limit]

    registry: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "catalog": {
            "total_bursts": len(all_bursts),
            "excluded_bursts": len(excluded),
            "analyzed_bursts": len(analyzed),
            "repeater_bursts": len(repeaters),
            "non_repeater_bursts": len(non_repeaters),
            "repeater_sources": len({b.repeater_name for b in repeaters}),
        },
        "settings": {
            "alpha": ALPHA,
            "bootstrap_resamples": DEFAULT_BOOTSTRAP_RESAMPLES,
            "bootstrap_seed": DEFAULT_SEED,
        },
        "comparisons": {
            "dm_exc_ne2001_primary": _comparison(
                "Milky Way-subtracted DM excess (NE2001 model), primary measure",
                _dm(repeaters, "dm_exc_ne2001"),
                _dm(non_repeaters, "dm_exc_ne2001"),
            ),
            "dm_fitb_secondary": _comparison(
                "Raw fitburst DM, secondary/robustness measure",
                _dm(repeaters, "dm_fitb"),
                _dm(non_repeaters, "dm_fitb"),
            ),
            "dm_exc_ymw16_secondary": _comparison(
                "Milky Way-subtracted DM excess (YMW16 model), secondary/robustness measure",
                _dm(repeaters, "dm_exc_ymw16"),
                _dm(non_repeaters, "dm_exc_ymw16"),
            ),
            "width_fitb": _comparison(
                "Intrinsic pulse width (fitburst), all analyzed bursts",
                width_repeaters_full,
                width_non_repeaters_full,
            ),
            "bandwidth": _comparison(
                "Spectral bandwidth (high_freq - low_freq), all analyzed bursts",
                bandwidth_repeaters_full,
                bandwidth_non_repeaters_full,
            ),
            "width_fitb_excluding_limits": _comparison(
                "Intrinsic pulse width (fitburst), excluding upper-limit-flagged widths",
                _dm(repeaters_no_limits, "width_fitb"),
                _dm(non_repeaters_no_limits, "width_fitb"),
            ),
            "bandwidth_excluding_width_limits": _comparison(
                "Spectral bandwidth, excluding bursts with an upper-limit-flagged width",
                [b.bandwidth for b in repeaters_no_limits],
                [b.bandwidth for b in non_repeaters_no_limits],
            ),
            "dm_exc_ne2001_first_detection_per_source": _comparison(
                "POST-HOC (not preregistered): DM excess (NE2001) using only each "
                "repeating source's first-detected burst, reproducing the original "
                "paper's own deduplication method instead of this project's "
                "preregistered burst-level comparison",
                _dm(first_detection_per_source(repeaters), "dm_exc_ne2001"),
                _dm(non_repeaters, "dm_exc_ne2001"),
            ),
            "width_fitb_first_detection_per_source": _comparison(
                "POST-HOC (not preregistered): pulse width using only each repeating "
                "source's first-detected burst",
                _dm(first_detection_per_source(repeaters), "width_fitb"),
                width_non_repeaters_full,
            ),
            "bandwidth_first_detection_per_source": _comparison(
                "POST-HOC (not preregistered): spectral bandwidth using only each "
                "repeating source's first-detected burst",
                [b.bandwidth for b in first_detection_per_source(repeaters)],
                bandwidth_non_repeaters_full,
            ),
        },
        "distributions": {
            "dm_exc_ne2001": {
                "repeater": _dm(repeaters, "dm_exc_ne2001"),
                "non_repeater": _dm(non_repeaters, "dm_exc_ne2001"),
            },
            "width_fitb": {
                "repeater": width_repeaters_full,
                "non_repeater": width_non_repeaters_full,
            },
            "bandwidth": {
                "repeater": bandwidth_repeaters_full,
                "non_repeater": bandwidth_non_repeaters_full,
            },
        },
    }
    return registry
