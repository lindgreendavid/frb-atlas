"""Source-level clustering diagnostics for the repeater vs. non-repeater comparison.

POST-HOC and NOT preregistered (see "Amendment 2" in docs/research-report.md). The
preregistered burst-level KS test treats every repeater burst as an independent draw, but
bursts from the same repeating source share the source's dispersion measure, so they are
clustered. This module measures how much that matters, with four fixed diagnostics, all of
which are reported regardless of outcome:

1. cluster sizes and the intraclass correlation (ICC) of the measure within sources, with
   the Kish design effect and effective sample size;
2. a source-level test: each repeating source collapses to the median of its bursts
   (18 independent units), compared with the non-repeater bursts;
3. random one-burst-per-source draws: the distribution of KS p-values over 10,000 random
   choices of which burst represents each source (the paper's "first detection" is one such
   choice);
4. leave-one-source-out burst-level KS tests.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
from scipy import stats as scipy_stats

from frb_atlas.catalog import Burst

CLUSTERING_SEED = 20261009
CLUSTERING_DRAWS = 10_000
MEASURES = ("dm_exc_ne2001", "width_fitb", "bandwidth")


def _values(bursts: list[Burst], measure: str) -> list[float]:
    return [float(getattr(b, measure)) for b in bursts]


def _by_source(repeaters: list[Burst]) -> dict[str, list[Burst]]:
    groups: dict[str, list[Burst]] = defaultdict(list)
    for burst in repeaters:
        groups[burst.repeater_name].append(burst)
    return dict(sorted(groups.items()))


def cluster_sizes(repeaters: list[Burst]) -> dict[str, int]:
    return {name: len(group) for name, group in _by_source(repeaters).items()}


def intraclass_correlation(repeaters: list[Burst], measure: str) -> dict[str, float]:
    """One-way random-effects ICC(1) with unbalanced groups (ANOVA estimator), the Kish
    effective cluster size, the design effect, and the effective sample size."""
    groups = [np.array(_values(g, measure)) for g in _by_source(repeaters).values()]
    k = len(groups)
    sizes = np.array([len(g) for g in groups], dtype=float)
    n = sizes.sum()
    grand = np.concatenate(groups).mean()
    ssb = float(sum(len(g) * (g.mean() - grand) ** 2 for g in groups))
    ssw = float(sum(((g - g.mean()) ** 2).sum() for g in groups))
    msb = ssb / (k - 1)
    msw = ssw / (n - k)
    n0 = (n - (sizes**2).sum() / n) / (k - 1)
    denominator = msb + (n0 - 1) * msw
    icc = (msb - msw) / denominator if denominator > 0 else float("nan")
    m_eff = float((sizes**2).sum() / n)
    deff = 1 + (m_eff - 1) * icc if denominator > 0 else float("nan")
    return {
        "icc": float(icc),
        "kish_cluster_size": m_eff,
        "design_effect": float(deff),
        "n_bursts": float(n),
        "effective_n": float(n / deff),
        "n_sources": float(k),
    }


def source_median_test(
    repeaters: list[Burst], non_repeaters: list[Burst], measure: str
) -> dict[str, float]:
    """Collapse each repeating source to its median, then compare with non-repeater bursts."""
    medians = [float(np.median(_values(g, measure))) for g in _by_source(repeaters).values()]
    others = _values(non_repeaters, measure)
    ks = scipy_stats.ks_2samp(medians, others)
    mw = scipy_stats.mannwhitneyu(medians, others, alternative="two-sided")
    return {
        "n_sources": float(len(medians)),
        "median_of_source_medians": float(np.median(medians)),
        "median_non_repeater": float(np.median(others)),
        "ks_statistic": float(ks.statistic),
        "ks_p_value": float(ks.pvalue),
        "mannwhitney_p_value": float(mw.pvalue),
    }


def random_one_per_source(
    repeaters: list[Burst],
    non_repeaters: list[Burst],
    measure: str,
    draws: int = CLUSTERING_DRAWS,
    seed: int = CLUSTERING_SEED,
) -> dict[str, float]:
    """KS p-value distribution over random choices of one burst per repeating source."""
    rng = np.random.default_rng(seed)
    groups = [np.array(_values(g, measure)) for g in _by_source(repeaters).values()]
    others = _values(non_repeaters, measure)
    pvalues = np.empty(draws)
    for i in range(draws):
        sample = [float(g[rng.integers(len(g))]) for g in groups]
        pvalues[i] = scipy_stats.ks_2samp(sample, others).pvalue
    q = np.quantile(pvalues, [0.05, 0.5, 0.95])
    return {
        "draws": float(draws),
        "p_min": float(pvalues.min()),
        "p_q05": float(q[0]),
        "p_median": float(q[1]),
        "p_q95": float(q[2]),
        "p_max": float(pvalues.max()),
        "share_below_0.05": float(np.mean(pvalues < 0.05)),
        "share_below_0.01": float(np.mean(pvalues < 0.01)),
    }


def leave_one_source_out(
    repeaters: list[Burst], non_repeaters: list[Burst], measure: str
) -> dict[str, Any]:
    """Burst-level KS test with each repeating source removed in turn."""
    others = _values(non_repeaters, measure)
    results = {}
    for name in _by_source(repeaters):
        kept = [b for b in repeaters if b.repeater_name != name]
        ks = scipy_stats.ks_2samp(_values(kept, measure), others)
        results[name] = {"ks_statistic": float(ks.statistic), "ks_p_value": float(ks.pvalue)}
    pvals = [r["ks_p_value"] for r in results.values()]
    worst = max(results, key=lambda name: results[name]["ks_p_value"])
    return {
        "p_min": float(min(pvals)),
        "p_max": float(max(pvals)),
        "source_with_largest_p": worst,
        "per_source": results,
    }


def build_clustering(repeaters: list[Burst], non_repeaters: list[Burst]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "label": "POST-HOC (not preregistered): source-clustering diagnostics",
        "seed": CLUSTERING_SEED,
        "draws": CLUSTERING_DRAWS,
        "cluster_sizes": cluster_sizes(repeaters),
        "measures": {
            measure: {
                "icc": intraclass_correlation(repeaters, measure),
                "source_median_test": source_median_test(repeaters, non_repeaters, measure),
                "random_one_per_source": random_one_per_source(repeaters, non_repeaters, measure),
                "leave_one_source_out": leave_one_source_out(repeaters, non_repeaters, measure),
            }
            for measure in MEASURES
        },
    }
