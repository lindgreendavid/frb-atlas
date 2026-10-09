import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEX = (ROOT / "paper" / "paper.tex").read_text(encoding="utf-8")
REGISTRY = json.loads((ROOT / "reports" / "v0.1-frb-registry.json").read_text())
CLUSTER = json.loads((ROOT / "reports" / "v0.2-source-clustering.json").read_text())


def test_preregistered_ks_statistics_in_paper_match_registry():
    for key in (
        "dm_exc_ne2001_primary",
        "dm_fitb_secondary",
        "dm_exc_ymw16_secondary",
        "width_fitb",
        "width_fitb_excluding_limits",
        "bandwidth",
        "bandwidth_excluding_width_limits",
    ):
        assert f"{REGISTRY['comparisons'][key]['ks']['statistic']:.3f}" in TEX, key


def test_clustering_numbers_in_paper_match_the_post_hoc_report():
    dm = CLUSTER["measures"]["dm_exc_ne2001"]
    assert f"{dm['icc']['icc']:.5f}" in TEX
    assert f"{dm['icc']['design_effect']:.2f}" in TEX
    assert f"{dm['icc']['effective_n']:.1f}" in TEX
    assert f"{dm['source_median_test']['ks_p_value']:.3f}" in TEX
    assert f"{dm['source_median_test']['mannwhitney_p_value']:.3f}" in TEX
    for measure in ("width_fitb", "bandwidth"):
        icc = CLUSTER["measures"][measure]["icc"]
        assert f"{icc['icc']:.2f}" in TEX
        assert f"{icc['effective_n']:.1f}" in TEX


def test_cluster_sizes_stated_in_paper_are_the_real_ones():
    sizes = sorted(CLUSTER["cluster_sizes"].values(), reverse=True)
    assert sizes[:4] == [19, 8, 3, 3]
    assert sizes.count(2) == 12 and sizes.count(1) == 2 and sum(sizes) == 59
    assert "twelve sources with 2" in TEX and "19, 8, 3, 3" in TEX
    assert "27 of 59" in TEX
