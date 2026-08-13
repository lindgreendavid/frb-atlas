from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from frb_atlas.registry import build_registry

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_build_registry_schema(sample_catalog_csv: Path) -> None:
    registry = build_registry(sample_catalog_csv)
    assert registry["schema_version"] == 1
    assert registry["catalog"]["total_bursts"] == 16
    assert registry["catalog"]["excluded_bursts"] == 1
    assert registry["catalog"]["analyzed_bursts"] == 15
    assert registry["catalog"]["repeater_bursts"] == 5
    assert registry["catalog"]["non_repeater_bursts"] == 10
    assert registry["catalog"]["repeater_sources"] == 3

    comparisons = registry["comparisons"]
    expected_keys = {
        "dm_exc_ne2001_primary",
        "dm_fitb_secondary",
        "dm_exc_ymw16_secondary",
        "width_fitb",
        "bandwidth",
        "width_fitb_excluding_limits",
        "bandwidth_excluding_width_limits",
        "dm_exc_ne2001_first_detection_per_source",
        "width_fitb_first_detection_per_source",
        "bandwidth_first_detection_per_source",
    }
    assert expected_keys <= comparisons.keys()
    for comparison in comparisons.values():
        assert 0.0 <= comparison["ks"]["p_value"] <= 1.0
        assert comparison["ks"]["alpha"] == 0.05


def test_registry_generation_script_matches_frozen_registry() -> None:
    """The committed reports/v0.1-frb-registry.json must be byte-reproducible."""
    catalog = REPO_ROOT / "data" / "external" / "chime_frb_catalog1.csv"
    frozen = REPO_ROOT / "reports" / "v0.1-frb-registry.json"
    if not catalog.exists():
        return  # raw catalog is gitignored; only runs where it has been fetched
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "generate_registry.py"),
            "--output",
            "/tmp/frb-atlas-registry-check.json",
            "--catalog",
            str(catalog),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    generated = json.loads(Path("/tmp/frb-atlas-registry-check.json").read_text())
    frozen_data = json.loads(frozen.read_text())
    assert generated == frozen_data
