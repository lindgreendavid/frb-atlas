"""Load and filter the normalized CHIME/FRB Catalog 1 CSV.

See `docs/research-protocol.md` for the exact exclusion criteria and
grouping variable implemented here.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

REPEATER_SENTINEL = "-9999"


@dataclass(frozen=True)
class Burst:
    """One CHIME/FRB Catalog 1 burst (the sub_num == 0 representative row)."""

    tns_name: str
    repeater_name: str
    dm_fitb: float
    dm_exc_ne2001: float
    dm_exc_ymw16: float
    width_fitb: float
    width_fitb_is_limit: bool
    high_freq: float
    low_freq: float
    excluded_flag: bool
    mjd_400: float

    @property
    def is_repeater(self) -> bool:
        return self.repeater_name not in ("", REPEATER_SENTINEL)

    @property
    def bandwidth(self) -> float:
        """Spectral bandwidth: high_freq - low_freq (MHz)."""
        return self.high_freq - self.low_freq


def _row_to_burst(row: dict[str, str]) -> Burst:
    return Burst(
        tns_name=row["tns_name"],
        repeater_name=row["repeater_name"],
        dm_fitb=float(row["dm_fitb"]),
        dm_exc_ne2001=float(row["dm_exc_ne2001"]),
        dm_exc_ymw16=float(row["dm_exc_ymw16"]),
        width_fitb=float(row["width_fitb"]),
        width_fitb_is_limit=row["width_fitb_limit_flag"].strip() == "<",
        high_freq=float(row["high_freq"]),
        low_freq=float(row["low_freq"]),
        excluded_flag=row["excluded_flag"].strip() == "1",
        mjd_400=float(row["mjd_400"]),
    )


def load_bursts(path: Path) -> list[Burst]:
    """Load the 536 sub_num==0 bursts from the normalized catalog CSV.

    Filters to ``sub_num == 0`` here (not only in ``scripts/fetch_catalog.py``)
    so this function is self-contained and correct even if given an
    un-deduplicated CSV with multi-component sub-burst rows.
    """
    with Path(path).open(newline="") as handle:
        reader = csv.DictReader(handle)
        return [_row_to_burst(row) for row in reader if row["sub_num"].strip() == "0"]


def analyzable_bursts(bursts: list[Burst]) -> list[Burst]:
    """Apply the preregistered exclusion: drop excluded_flag == 1 bursts."""
    return [b for b in bursts if not b.excluded_flag]


def split_by_repeater(bursts: list[Burst]) -> tuple[list[Burst], list[Burst]]:
    """Return (repeaters, non_repeaters)."""
    repeaters = [b for b in bursts if b.is_repeater]
    non_repeaters = [b for b in bursts if not b.is_repeater]
    return repeaters, non_repeaters


def first_detection_per_source(repeaters: list[Burst]) -> list[Burst]:
    """Reduce repeater bursts to one row per repeating source: the earliest (by mjd_400).

    This is a post-hoc, non-preregistered robustness view (see the "Amendment"
    section of docs/research-report.md): the original catalog paper's own
    repeater/non-repeater comparison uses only each repeating source's
    first-detected event, precisely to avoid a handful of especially
    prolific, nearby, low-DM repeaters (FRB20180916B, FRB20180814A)
    dominating a burst-level sample through pseudo-replication. The
    preregistered primary analysis in this project instead uses every
    analyzed repeater burst; this function exists only to reproduce the
    paper's own deduplication as a disclosed, separately labeled check.
    """
    earliest: dict[str, Burst] = {}
    for burst in repeaters:
        current = earliest.get(burst.repeater_name)
        if current is None or burst.mjd_400 < current.mjd_400:
            earliest[burst.repeater_name] = burst
    return list(earliest.values())
