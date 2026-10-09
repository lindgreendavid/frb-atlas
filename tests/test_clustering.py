import pytest

from frb_atlas.catalog import Burst
from frb_atlas.clustering import (
    build_clustering,
    cluster_sizes,
    intraclass_correlation,
    leave_one_source_out,
    random_one_per_source,
    source_median_test,
)


def burst(
    source: str, dm: float, width: float = 0.001, bw: float = 300.0, mjd: float = 0.0
) -> Burst:
    return Burst(
        tns_name=f"{source}-{dm}-{mjd}",
        repeater_name=source,
        dm_fitb=dm,
        dm_exc_ne2001=dm,
        dm_exc_ymw16=dm,
        width_fitb=width,
        width_fitb_is_limit=False,
        high_freq=500.0 + bw,
        low_freq=500.0,
        excluded_flag=False,
        mjd_400=mjd,
    )


def singles(n: int, start: float = 400.0) -> list[Burst]:
    return [
        burst("-9999", start + 7.0 * i, width=0.002 + 1e-4 * i, bw=250 + 3 * i) for i in range(n)
    ]


def test_cluster_sizes_counts_bursts_per_source():
    reps = [burst("A", 1), burst("A", 2), burst("B", 3)]
    assert cluster_sizes(reps) == {"A": 2, "B": 1}


def test_icc_matches_hand_calculation():
    reps = [burst("A", 1), burst("A", 3), burst("B", 5), burst("B", 7)]
    out = intraclass_correlation(reps, "dm_exc_ne2001")
    assert out["icc"] == pytest.approx(14 / 18)
    assert out["kish_cluster_size"] == pytest.approx(2.0)
    assert out["design_effect"] == pytest.approx(1 + 1 * 14 / 18)
    assert out["effective_n"] == pytest.approx(4 / (1 + 14 / 18))


def test_icc_is_one_and_effective_n_collapses_when_sources_are_duplicated():
    reps = [burst("A", 100)] * 4 + [burst("B", 200)] * 2 + [burst("C", 300)]
    out = intraclass_correlation(reps, "dm_exc_ne2001")
    assert out["icc"] == pytest.approx(1.0)
    assert out["effective_n"] < out["n_bursts"] / 2


def test_source_median_test_uses_one_unit_per_source():
    reps = [burst("A", 100)] * 5 + [burst("B", 110)] * 5 + [burst("C", 120)] * 5
    out = source_median_test(reps, singles(60), "dm_exc_ne2001")
    assert out["n_sources"] == 3
    assert out["median_of_source_medians"] == 110
    assert 0 < out["ks_p_value"] <= 1
    assert 0 < out["mannwhitney_p_value"] <= 1


def test_random_one_per_source_is_reproducible_and_constant_for_duplicated_sources():
    reps = [burst("A", 100)] * 3 + [burst("B", 150)] * 3
    a = random_one_per_source(reps, singles(40), "dm_exc_ne2001", draws=50, seed=1)
    b = random_one_per_source(reps, singles(40), "dm_exc_ne2001", draws=50, seed=1)
    assert a == b
    assert a["p_min"] == pytest.approx(a["p_max"])


def test_random_one_per_source_varies_when_bursts_differ_within_source():
    reps = [burst("A", 100 + 80 * i) for i in range(6)] + [
        burst("B", 150 + 80 * i) for i in range(6)
    ]
    out = random_one_per_source(reps, singles(40), "dm_exc_ne2001", draws=200, seed=2)
    assert out["p_min"] < out["p_max"]
    assert 0 <= out["share_below_0.01"] <= out["share_below_0.05"] <= 1


def test_leave_one_source_out_reports_each_source():
    reps = [burst("A", 100)] * 3 + [burst("B", 120)] * 3 + [burst("C", 140)] * 3
    out = leave_one_source_out(reps, singles(40), "dm_exc_ne2001")
    assert set(out["per_source"]) == {"A", "B", "C"}
    assert out["p_min"] <= out["p_max"]
    assert out["source_with_largest_p"] in {"A", "B", "C"}


def test_build_clustering_covers_all_measures():
    reps = [burst("A", 100 + i, mjd=i) for i in range(3)] + [
        burst("B", 200 + i, mjd=i) for i in range(3)
    ]
    reps += [burst("C", 300 + i, mjd=i) for i in range(2)]
    result = build_clustering(reps, singles(40))
    assert set(result["measures"]) == {"dm_exc_ne2001", "width_fitb", "bandwidth"}
    assert result["cluster_sizes"] == {"A": 3, "B": 3, "C": 2}
    assert result["label"].startswith("POST-HOC")


def test_icc_is_nan_for_a_constant_measure():
    import math

    reps = [burst("A", 5.0)] * 3 + [burst("B", 5.0)] * 3
    out = intraclass_correlation(reps, "dm_exc_ne2001")
    assert math.isnan(out["icc"]) and math.isnan(out["design_effect"])
