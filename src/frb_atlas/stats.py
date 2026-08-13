"""Statistical tests used for the repeater vs. non-repeater comparisons.

See `docs/research-protocol.md` for the preregistered method: two-sample
Kolmogorov-Smirnov as the primary test, two-sample Anderson-Darling as a
robustness check, and a percentile bootstrap confidence interval on the
median difference between groups.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from scipy import stats as scipy_stats

DEFAULT_SEED = 20260813
DEFAULT_BOOTSTRAP_RESAMPLES = 10_000
ALPHA = 0.05


@dataclass(frozen=True)
class KsResult:
    statistic: float
    p_value: float
    significant: bool


@dataclass(frozen=True)
class AndersonResult:
    statistic: float
    p_value: float
    significant: bool


@dataclass(frozen=True)
class BootstrapResult:
    median_a: float
    median_b: float
    median_diff: float
    ci_low: float
    ci_high: float
    resamples: int
    seed: int


def ks_two_sample(a: list[float], b: list[float]) -> KsResult:
    """Two-sided two-sample Kolmogorov-Smirnov test."""
    result = scipy_stats.ks_2samp(a, b)
    return KsResult(
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        significant=bool(result.pvalue < ALPHA),
    )


def anderson_darling_two_sample(a: list[float], b: list[float]) -> AndersonResult:
    """Two-sample Anderson-Darling test (robustness check on tail differences).

    scipy caps the reported p-value between 0.001 and 0.25; values outside
    that range are clipped by scipy itself, which is disclosed here rather
    than silently relied upon.
    """
    with warnings.catch_warnings():
        # SciPy deliberately floors extremely small p-values at 0.001 when
        # no permutation method is supplied. That behavior is disclosed in
        # this function's contract and recorded in the frozen registry.
        warnings.filterwarnings(
            "ignore",
            message="p-value floored:*",
            category=UserWarning,
        )
        result = scipy_stats.anderson_ksamp([a, b], variant="midrank")
    p_value = float(result.pvalue)
    return AndersonResult(
        statistic=float(result.statistic),
        p_value=p_value,
        significant=bool(p_value < ALPHA),
    )


def bootstrap_median_diff(
    a: list[float],
    b: list[float],
    *,
    resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    seed: int = DEFAULT_SEED,
) -> BootstrapResult:
    """Percentile bootstrap 95% CI for (median(b) - median(a)).

    Each group is resampled independently, with replacement, at its own
    observed size, using a seeded generator for exact reproducibility.
    """
    rng = np.random.default_rng(seed)
    arr_a = np.asarray(a, dtype=float)
    arr_b = np.asarray(b, dtype=float)
    diffs = np.empty(resamples, dtype=float)
    for i in range(resamples):
        sample_a = rng.choice(arr_a, size=arr_a.size, replace=True)
        sample_b = rng.choice(arr_b, size=arr_b.size, replace=True)
        diffs[i] = float(np.median(sample_b) - np.median(sample_a))
    ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
    return BootstrapResult(
        median_a=float(np.median(arr_a)),
        median_b=float(np.median(arr_b)),
        median_diff=float(np.median(arr_b) - np.median(arr_a)),
        ci_low=float(ci_low),
        ci_high=float(ci_high),
        resamples=resamples,
        seed=seed,
    )
