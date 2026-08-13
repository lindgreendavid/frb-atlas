"""Fetch CHIME/FRB Catalog 1 from VizieR and normalize it to a clean CSV.

The official chime-frb-open-data project site was unavailable ("temporarily
unavailable, rebuilding") when this project was built, and the `cfod` Python
package only parses an already-downloaded local catalog file rather than
fetching one. VizieR (`J/ApJS/257/59/table2`, CDS's standard long-term mirror
of published astronomical tables) is used instead. See
`docs/research-protocol.md` for the full data-provenance discussion.

Because VizieR's plain-text response embeds a per-request timestamp comment,
the raw response is not byte-stable across fetches, so this script verifies
the download *structurally* instead of via a fixed content checksum:

- exactly 536 rows with `sub_num == 0` (one row per catalog burst, matching
  the paper's stated 536-burst catalog),
- exactly 536 unique `tns_name` values among those rows,
- exactly 62 of those rows have a non-empty `repeater_name`, drawn from
  exactly 18 unique repeater sources (matching the paper abstract's "62
  bursts from 18 previously known repeating sources").

A failure of any of these checks aborts the fetch rather than silently
writing a possibly-wrong file.
"""

from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from pathlib import Path

VIZIER_URL = (
    "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
    "?-source=J/ApJS/257/59/table2&-out.max=9999&-out.form=tsv&-out.all"
)

# Maps VizieR's table2 column header -> this project's normalized column name.
COLUMN_MAP = {
    "Name": "tns_name",
    "OName": "previous_name",
    "RpName": "repeater_name",
    "RAJ2000": "ra",
    "e_RAJ2000": "ra_err",
    "DEJ2000": "dec",
    "e_DEJ2000": "dec_err",
    "GLON": "gl",
    "GLAT": "gb",
    "SNR": "bonsai_snr",
    "DM": "bonsai_dm",
    "SNRfitb": "snr_fitb",
    "DMfitb": "dm_fitb",
    "e_DMfitb": "dm_fitb_err",
    "DMeNE2001": "dm_exc_ne2001",
    "DMeYMW16": "dm_exc_ymw16",
    "BcWidth": "bc_width",
    "Scat": "scat_time",
    "Flux": "flux",
    "Fluence": "fluence",
    "Nsb": "sub_num",
    "MJD400": "mjd_400",
    "l_Widthfitb": "width_fitb_limit_flag",
    "Widthfitb": "width_fitb",
    "e_Widthfitb": "width_fitb_err",
    "SpInd": "sp_idx",
    "B_Freq": "high_freq",
    "b_Freq": "low_freq",
    "Fpk": "peak_freq",
    "Flag": "excluded_flag",
}

REPEATER_SENTINEL = "-9999"
EXPECTED_BURSTS = 536
EXPECTED_REPEATER_BURSTS = 62
EXPECTED_REPEATER_SOURCES = 18


def _download(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310
        return response.read().decode("utf-8")


def _parse_vizier_tsv(text: str) -> list[dict[str, str]]:
    """Parse VizieR's commented TSV format into a list of raw header->value dicts."""
    lines = text.splitlines()
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        cells = [cell.strip() for cell in line.split("\t")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= {"-"} for cell in cells if cell):
            continue  # the dashed separator row
        if cells == header or (cells and cells[0] == ""):
            continue  # the units row (blank first cell) or a repeated header
        first = cells[0]
        if not first.isdigit():
            continue
        rows.append(dict(zip(header, cells, strict=False)))
    return rows


def normalize(raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Rename columns per COLUMN_MAP and keep only sub_num == 0 (one row per burst)."""
    normalized = []
    for raw in raw_rows:
        row = {new: raw.get(old, "") for old, new in COLUMN_MAP.items()}
        if row["sub_num"] != "0":
            continue
        normalized.append(row)
    return normalized


def verify(rows: list[dict[str, str]]) -> None:
    if len(rows) != EXPECTED_BURSTS:
        raise RuntimeError(f"expected {EXPECTED_BURSTS} bursts with sub_num==0, got {len(rows)}")
    names = {row["tns_name"] for row in rows}
    if len(names) != EXPECTED_BURSTS:
        raise RuntimeError(f"expected {EXPECTED_BURSTS} unique tns_name values, got {len(names)}")
    repeater_rows = [row for row in rows if row["repeater_name"] not in ("", REPEATER_SENTINEL)]
    if len(repeater_rows) != EXPECTED_REPEATER_BURSTS:
        raise RuntimeError(
            f"expected {EXPECTED_REPEATER_BURSTS} repeater bursts, got {len(repeater_rows)}"
        )
    sources = {row["repeater_name"] for row in repeater_rows}
    if len(sources) != EXPECTED_REPEATER_SOURCES:
        raise RuntimeError(
            f"expected {EXPECTED_REPEATER_SOURCES} unique repeater sources, got {len(sources)}"
        )


def write_csv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(COLUMN_MAP.values())
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/external/chime_frb_catalog1.csv"),
    )
    parser.add_argument("--url", default=VIZIER_URL)
    args = parser.parse_args(argv)

    text = _download(args.url)
    raw_rows = _parse_vizier_tsv(text)
    rows = normalize(raw_rows)
    verify(rows)
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} verified bursts to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
