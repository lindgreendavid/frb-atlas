# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- Hardened the transitive `image-size` parsers against malformed ICNS and ISO-BMFF input,
  added executable security regression probes, and kept the production audit strict for every
  other high-severity advisory.
- Made frozen-registry verification portable across operating systems by comparing floating-point
  values with a narrow numerical tolerance while retaining exact checks for all other data.
- Scoped the Anderson-Darling p-value-floor warning to the documented statistical call and aligned
  the Cloudflare compatibility date with the pinned runtime.

## [0.1.0] - 2026-08-13

### Added

- Preregistered research protocol (`docs/research-protocol.md`): data source, exclusion
  criteria, grouping variable, and exact statistical tests, fixed before any analysis was run.
- `scripts/fetch_catalog.py`: fetches CHIME/FRB Catalog 1 from VizieR (`J/ApJS/257/59/table2`)
  and structurally verifies it (536 unique bursts; 62 repeater bursts from 18 sources) before
  writing a normalized CSV. The raw catalog is not committed to git.
- `data/provenance.json`: full data provenance, license status, and erratum-scope disclosure.
- `src/frb_atlas`: catalog loading and exclusion (`catalog.py`), the KS/Anderson–Darling/
  bootstrap statistical pipeline (`stats.py`), the result-registry builder (`registry.py`), and
  a small CLI (`cli.py`).
- `reports/v0.1-frb-registry.json`: the frozen, reproducible v0.1.0 result registry, generated
  from the real catalog data.
- `docs/research-report.md`: hypothesis-by-hypothesis findings, including a disclosed post-hoc
  investigation into a DM-comparison discrepancy from the original catalog paper's own finding,
  and full limitations.
- `site/`: an accessible Next.js (vinext) interactive atlas covering the DM comparison, the
  width/bandwidth validation check, full data tables, and a provenance page, built for Cloudflare
  Workers deployment as `frb-atlas-interactive`.
- Full repository hygiene: `pyproject.toml` (ruff, mypy strict, pytest with a 95% coverage gate),
  `CITATION.cff`, `ACCESSIBILITY.md`, and CI workflows (`ci.yml`, `codeql.yml`).
