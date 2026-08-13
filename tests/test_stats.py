from __future__ import annotations

from frb_atlas.stats import (
    anderson_darling_two_sample,
    bootstrap_median_diff,
    ks_two_sample,
)


def test_ks_two_sample_identical_distributions_not_significant() -> None:
    a = [1.0, 2.0, 3.0, 4.0, 5.0] * 10
    b = [1.0, 2.0, 3.0, 4.0, 5.0] * 10
    result = ks_two_sample(a, b)
    assert result.p_value == 1.0
    assert result.significant is False


def test_ks_two_sample_clearly_different_distributions_significant() -> None:
    a = list(range(100))
    b = [x + 1000 for x in range(100)]
    result = ks_two_sample(a, b)
    assert result.statistic == 1.0
    assert result.significant is True


def test_anderson_darling_clearly_different_significant() -> None:
    a = list(range(50))
    b = [x + 500 for x in range(50)]
    result = anderson_darling_two_sample(a, b)
    assert result.significant is True
    assert result.p_value <= 0.05


def test_bootstrap_median_diff_deterministic_given_seed() -> None:
    a = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = [10.0, 20.0, 30.0, 40.0, 50.0]
    first = bootstrap_median_diff(a, b, resamples=200, seed=42)
    second = bootstrap_median_diff(a, b, resamples=200, seed=42)
    assert first == second
    assert first.median_a == 3.0
    assert first.median_b == 30.0
    assert first.median_diff == 27.0
    assert first.ci_low <= first.median_diff <= first.ci_high


def test_bootstrap_median_diff_different_seed_can_differ() -> None:
    a = [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]
    b = [10.0, 20.0, 30.0, 40.0, 50.0, 5.0]
    first = bootstrap_median_diff(a, b, resamples=200, seed=1)
    second = bootstrap_median_diff(a, b, resamples=200, seed=2)
    assert first.seed != second.seed
