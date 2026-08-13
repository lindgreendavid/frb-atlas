"""Shared pytest fixtures: a small synthetic catalog CSV for unit tests.

This fixture data is NOT real CHIME/FRB Catalog 1 data — it exists only to
exercise the parsing, exclusion, and statistics code paths deterministically
and quickly. Real-data verification lives in scripts/fetch_catalog.py and is
run against the live VizieR source, not in this offline test suite.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

FIELDNAMES = [
    "tns_name",
    "previous_name",
    "repeater_name",
    "ra",
    "ra_err",
    "dec",
    "dec_err",
    "gl",
    "gb",
    "bonsai_snr",
    "bonsai_dm",
    "snr_fitb",
    "dm_fitb",
    "dm_fitb_err",
    "dm_exc_ne2001",
    "dm_exc_ymw16",
    "bc_width",
    "scat_time",
    "flux",
    "fluence",
    "sub_num",
    "mjd_400",
    "width_fitb_limit_flag",
    "width_fitb",
    "width_fitb_err",
    "sp_idx",
    "high_freq",
    "low_freq",
    "peak_freq",
    "excluded_flag",
]


def _row(**overrides: str) -> dict[str, str]:
    base = dict.fromkeys(FIELDNAMES, "0")
    base.update(
        {
            "tns_name": "FRBTEST",
            "previous_name": "",
            "repeater_name": "-9999",
            "sub_num": "0",
            "dm_fitb": "500",
            "dm_exc_ne2001": "400",
            "dm_exc_ymw16": "410",
            "width_fitb": "0.002",
            "width_fitb_limit_flag": "",
            "high_freq": "700",
            "low_freq": "500",
            "excluded_flag": "0",
            "mjd_400": "58400.0",
        }
    )
    base.update(overrides)
    return base


@pytest.fixture
def sample_rows() -> list[dict[str, str]]:
    rows = []
    # 10 non-repeater bursts, higher/varied DM, width, and bandwidth
    for i in range(10):
        rows.append(
            _row(
                tns_name=f"FRB2018{i:04d}A",
                dm_fitb=str(600 + i * 22.1),
                dm_exc_ne2001=str(380 + i * 17.3),
                dm_exc_ymw16=str(390 + i * 18.1),
                width_fitb=str(0.0008 + i * 0.00013),
                high_freq=str(680 + i * 3),
                low_freq=str(500 - i * 7),
            )
        )
    # a duplicate sub-burst row for the first non-repeater (should be dropped)
    rows.append(_row(tns_name="FRB20180000A", sub_num="1", dm_exc_ne2001="999"))
    # 5 repeater bursts across 3 sources, lower/varied DM, width, and bandwidth
    repeater_specs = [
        ("FRB20190101A", "SRC_A", "230", "100", "108", "0.0045", "58500.0", "600", "400", ""),
        ("FRB20190102A", "SRC_A", "245", "108", "116", "0.0052", "58510.0", "615", "415", ""),
        ("FRB20190103A", "SRC_A", "220", "95", "101", "0.0049", "58490.0", "590", "405", ""),
        ("FRB20190201A", "SRC_B", "260", "112", "119", "0.0055", "58520.0", "610", "410", "<"),
        ("FRB20190301A", "SRC_C", "275", "121", "129", "0.0061", "58530.0", "625", "420", ""),
    ]
    for name, source, dm_fitb, dm_ne, dm_ymw, width, mjd, high, low, limit in repeater_specs:
        rows.append(
            _row(
                tns_name=name,
                repeater_name=source,
                dm_fitb=dm_fitb,
                dm_exc_ne2001=dm_ne,
                dm_exc_ymw16=dm_ymw,
                width_fitb=width,
                width_fitb_limit_flag=limit,
                mjd_400=mjd,
                high_freq=high,
                low_freq=low,
            )
        )
    # one excluded burst (should be dropped from analysis)
    rows.append(_row(tns_name="FRB20180999A", dm_exc_ne2001="450", excluded_flag="1"))
    return rows


@pytest.fixture
def sample_catalog_csv(tmp_path: Path, sample_rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "catalog.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(sample_rows)
    return path
