from __future__ import annotations

from pathlib import Path

from frb_atlas.catalog import (
    analyzable_bursts,
    first_detection_per_source,
    load_bursts,
    split_by_repeater,
)


def test_load_bursts_drops_duplicate_sub_bursts(sample_catalog_csv: Path) -> None:
    bursts = load_bursts(sample_catalog_csv)
    names = [b.tns_name for b in bursts]
    assert names.count("FRB20180000A") == 1
    assert len(bursts) == 16  # 10 non-repeater + 5 repeater + 1 excluded, sub_num==0 only


def test_analyzable_bursts_drops_excluded(sample_catalog_csv: Path) -> None:
    bursts = load_bursts(sample_catalog_csv)
    analyzed = analyzable_bursts(bursts)
    assert all(not b.excluded_flag for b in analyzed)
    assert len(analyzed) == len(bursts) - 1


def test_split_by_repeater(sample_catalog_csv: Path) -> None:
    bursts = analyzable_bursts(load_bursts(sample_catalog_csv))
    repeaters, non_repeaters = split_by_repeater(bursts)
    assert len(repeaters) == 5
    assert len(non_repeaters) == 10
    assert all(b.is_repeater for b in repeaters)
    assert all(not b.is_repeater for b in non_repeaters)


def test_bandwidth_property(sample_catalog_csv: Path) -> None:
    bursts = load_bursts(sample_catalog_csv)
    burst = next(b for b in bursts if b.tns_name == "FRB20190101A")
    assert burst.bandwidth == burst.high_freq - burst.low_freq


def test_width_limit_flag_parsed(sample_catalog_csv: Path) -> None:
    bursts = load_bursts(sample_catalog_csv)
    limited = next(b for b in bursts if b.tns_name == "FRB20190201A")
    not_limited = next(b for b in bursts if b.tns_name == "FRB20190101A")
    assert limited.width_fitb_is_limit is True
    assert not_limited.width_fitb_is_limit is False


def test_first_detection_per_source(sample_catalog_csv: Path) -> None:
    bursts = analyzable_bursts(load_bursts(sample_catalog_csv))
    repeaters, _ = split_by_repeater(bursts)
    first = first_detection_per_source(repeaters)
    assert len(first) == 3  # three unique repeater sources
    source_a = next(b for b in first if b.repeater_name == "SRC_A")
    assert source_a.tns_name == "FRB20190103A"  # earliest mjd_400 among the three source-A bursts
