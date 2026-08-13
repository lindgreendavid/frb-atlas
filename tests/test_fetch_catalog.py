from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "fetch_catalog.py"
_spec = importlib.util.spec_from_file_location("fetch_catalog", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
fetch_catalog = importlib.util.module_from_spec(_spec)
sys.modules["fetch_catalog"] = fetch_catalog
_spec.loader.exec_module(fetch_catalog)


SAMPLE_TSV = """#
#   VizieR Astronomical Server
#
recno\tName\tRpName\tNsb\tDMfitb\tDMeNE2001\tDMeYMW16\tWidthfitb\tl_Widthfitb\tB_Freq\tb_Freq\tFlag
 \t \t \t \t \t \t \t \t \t \t \t
--------\t------------\t------------\t-\t------\t------\t------\t------\t-\t-----\t-----\t-
       1\tFRB20180101A\t-9999       \t0\t500\t510\t0.002\t \t700\t500\t0
       2\tFRB20180102A\tFRB20180102A\t0\t100\t110\t0.005\t \t600\t400\t0
       3\tFRB20180102A\tFRB20180102A\t1\t100\t110\t0.006\t \t610\t410\t0
       4\tFRB20180103A\t-9999       \t0\t480\t490\t0.0015\t<\t690\t490\t1
"""


def test_parse_vizier_tsv_skips_headers_and_separators() -> None:
    rows = fetch_catalog._parse_vizier_tsv(SAMPLE_TSV)
    assert len(rows) == 4
    assert rows[0]["Name"] == "FRB20180101A"


def test_normalize_keeps_only_sub_num_zero() -> None:
    raw_rows = fetch_catalog._parse_vizier_tsv(SAMPLE_TSV)
    normalized = fetch_catalog.normalize(raw_rows)
    assert len(normalized) == 3
    assert all(row["sub_num"] == "0" for row in normalized)
    assert normalized[0]["tns_name"] == "FRB20180101A"
    assert normalized[0]["repeater_name"] == "-9999"


def test_verify_passes_for_matching_sample() -> None:
    raw_rows = fetch_catalog._parse_vizier_tsv(SAMPLE_TSV)
    normalized = fetch_catalog.normalize(raw_rows)
    # patch expected counts down to match this tiny sample
    fetch_catalog.EXPECTED_BURSTS = 3
    fetch_catalog.EXPECTED_REPEATER_BURSTS = 1
    fetch_catalog.EXPECTED_REPEATER_SOURCES = 1
    try:
        fetch_catalog.verify(normalized)
    finally:
        fetch_catalog.EXPECTED_BURSTS = 536
        fetch_catalog.EXPECTED_REPEATER_BURSTS = 62
        fetch_catalog.EXPECTED_REPEATER_SOURCES = 18


def test_verify_raises_on_wrong_burst_count() -> None:
    with pytest.raises(RuntimeError, match="expected 536 bursts"):
        fetch_catalog.verify([])


def test_verify_raises_on_wrong_repeater_count() -> None:
    rows = [{"tns_name": f"FRB{i}", "repeater_name": "-9999"} for i in range(535)] + [
        {"tns_name": "FRBrep", "repeater_name": "SRC1"}
    ]
    with pytest.raises(RuntimeError, match="repeater bursts"):
        fetch_catalog.verify(rows)


def test_write_csv_round_trips(tmp_path: Path) -> None:
    raw_rows = fetch_catalog._parse_vizier_tsv(SAMPLE_TSV)
    normalized = fetch_catalog.normalize(raw_rows)
    output = tmp_path / "catalog.csv"
    fetch_catalog.write_csv(normalized, output)
    text = output.read_text()
    assert "tns_name" in text.splitlines()[0]
    assert "FRB20180101A" in text
