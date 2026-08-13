# FRB Atlas

<p><a href="https://github.com/lindgreendavid/lindgreendavid/tree/main/brand"><img src="https://raw.githubusercontent.com/lindgreendavid/lindgreendavid/main/brand/lab-notes-mark.svg" width="52" align="right" alt="Lab Notes research-cycle mark"></a></p>

**Part of the [Lab Notes Research Portfolio](https://blog-interactive.lindgreendavid.workers.dev/)** · Astrophysics · Question → evidence → finding → boundary

A reproducible reanalysis of CHIME/FRB Catalog 1: do repeating and non-repeating fast radio
bursts differ in dispersion measure, pulse width, and spectral bandwidth?

**[Open the live interactive atlas](https://frb-atlas-interactive.lindgreendavid.workers.dev)** · **[Read the plain-language write-up](https://blog-interactive.lindgreendavid.workers.dev/posts/frb-atlas-dispersion-measure)**

**Stable product release:** [v1.0.0](https://github.com/lindgreendavid/frb-atlas/releases/tag/v1.0.0) · **Study:** unchanged frozen v0.1 registry.

**Research question:** using the real, published CHIME/FRB Catalog 1 data (536 fast radio
bursts, Amiri et al. 2021), do repeating and apparently non-repeating bursts differ in
dispersion measure (DM), intrinsic pulse width, and spectral bandwidth? The original catalog
paper's own abstract reports finding no significant DM difference but a significant width/
bandwidth difference — this project reproduces that exact comparison on the same public data
with a preregistered, disclosed statistical pipeline, and reports what it actually finds,
including where it disagrees with the paper.

This is **not** an attempt to resolve any open question in fast radio burst astrophysics, and it
does not claim to determine whether repeating and non-repeating FRBs are physically distinct
source populations. It is a bounded reproducibility and analysis exercise on one public catalog
from one telescope over one year of operation, with a preregistered protocol and a frozen,
reproducible result registry.

**Headline finding (v0.1.0):** the pulse-width and spectral-bandwidth comparison **replicates
the paper cleanly** — repeaters in this sample show significantly narrower bandwidth and wider
intrinsic pulse width than non-repeaters (p < 10⁻⁸ by Kolmogorov–Smirnov, robust to every
variant tested). The DM comparison, on this project's preregistered burst-level test, does
**not** replicate the paper's "no significant difference" finding — it finds a highly
significant difference (p ≈ 2×10⁻¹⁰), most likely driven by two exceptionally prolific, nearby,
low-DM repeaters supplying 90% of the repeater sample. A disclosed, non-preregistered follow-up
that reproduces the paper's own per-source deduplication method shrinks this to a
threshold-dependent, marginal result — closer to, but not a clean replication of, the paper's
conclusion. Full reasoning, every hypothesis's disposition, and every limitation: see
[`docs/research-report.md`](docs/research-report.md).

## What this contributes

- A concrete, independently-run replication attempt of one specific, real finding from a
  significant published catalog paper, using the same public data, rather than a restatement of
  the paper's own claims: does the DM/width/bandwidth comparison actually hold up on this exact
  sample under a straightforward, preregistered statistical pipeline? (Answer: partially — width
  and bandwidth replicate cleanly, DM does not at burst level, and the investigation into *why*
  is reported in full rather than hidden.)
- An honest discrepancy, investigated and disclosed rather than quietly explained away: the DM
  finding's likely cause (pseudo-replication from two prolific nearby repeaters) is reported as a
  disclosed, clearly-labeled post-hoc amendment — not folded silently into the preregistered
  result.
- A real internal validity check: the width/bandwidth replication acts as a positive control,
  showing this pipeline can detect a genuine, published, significant effect on this same data,
  which is what makes the DM discrepancy worth taking seriously rather than dismissing as
  underpowered noise.
- What it does **not** contribute: a resolution to the repeater/non-repeater debate in FRB
  astrophysics, a claim about any telescope or catalog other than CHIME/FRB Catalog 1, or any
  claim beyond this specific sample, exclusion criteria, and set of statistical tests.

## What's here

| Path | What it is |
| --- | --- |
| [`docs/research-protocol.md`](docs/research-protocol.md) | The preregistered hypotheses, data source, exclusion criteria, grouping variable, and exact statistical tests — written and committed before any result existed. |
| [`docs/research-report.md`](docs/research-report.md) | What the frozen registry actually shows, hypothesis by hypothesis, including the disclosed post-hoc investigation into the DM discrepancy and every limitation. |
| [`data/provenance.json`](data/provenance.json) | Full data provenance: source, access date, citation, erratum scope, license status, and the structural verification performed against the real catalog. |
| [`scripts/fetch_catalog.py`](scripts/fetch_catalog.py) | Downloads and structurally verifies CHIME/FRB Catalog 1 from VizieR at reproduction time. The raw catalog is not committed to git. |
| [`src/frb_atlas/`](src/frb_atlas/) | The Python package: catalog loading/exclusion, the KS/Anderson–Darling/bootstrap statistics, and the registry builder. |
| [`tests/`](tests/) | Unit tests (small synthetic fixtures, not real catalog data) and a byte-comparison test against the frozen registry. |
| [`reports/v0.1-frb-registry.json`](reports/v0.1-frb-registry.json) | The frozen, deterministic analysis output, generated from the real catalog. |
| [`site/`](site/) | An accessible Next.js (vinext) interactive atlas: DM/width/bandwidth comparison views, full data tables, and a provenance page, built for Cloudflare Workers. |

## Reproduce the analysis locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

# Fetch and structurally verify the real catalog (not committed to git):
python scripts/fetch_catalog.py --output data/external/chime_frb_catalog1.csv

# Regenerate the registry and confirm it matches the committed one:
python scripts/generate_registry.py --output /tmp/v0.1-frb-registry.json \
    --catalog data/external/chime_frb_catalog1.csv
cmp reports/v0.1-frb-registry.json /tmp/v0.1-frb-registry.json  # should be silent

# Or just summarize the catalog:
frb-atlas summarize data/external/chime_frb_catalog1.csv
```

This is deterministic given a fixed catalog (fixed bootstrap seed throughout); CI runs the same
fetch-and-compare on every push.

## Run the interactive site locally

```bash
cd site
pnpm install
pnpm run dev      # local development server
pnpm run build    # production build (Cloudflare Workers target)
pnpm run test     # build + node --test
pnpm run lint     # eslint
```

`site/wrangler.jsonc` is configured for deployment to Cloudflare Workers as
`frb-atlas-interactive`. This repository does not run `wrangler deploy` — that is a manual step
the maintainer runs after reviewing a build.

## Quality gates

```bash
ruff check .
ruff format --check .
mypy src
pytest                      # includes a 95% coverage gate
python -m build

cd site && pnpm run lint && pnpm run build && pnpm run test
```

## Data source and citation

CHIME/FRB Collaboration (M. Amiri et al.) 2021, "The First CHIME/FRB Fast Radio Burst Catalog,"
*The Astrophysical Journal Supplement Series*, 257, 59.
DOI: [10.3847/1538-4365/ac33ab](https://doi.org/10.3847/1538-4365/ac33ab). See
[`data/provenance.json`](data/provenance.json) for the full provenance record, including the
erratum ([ApJS, 264, 53](https://doi.org/10.3847/1538-4365/acb54c)) and its scope, and
[`CITATION.cff`](CITATION.cff) for citing this software.

## Scope and limitations (short version — full version in the report)

One catalog, one telescope, one year (400–800 MHz, CHIME/FRB, 2018-07-25 to 2019-07-01). No
independent selection-function or completeness model. Small, unbalanced repeater/non-repeater
groups. See
[`docs/research-protocol.md`](docs/research-protocol.md#scope-boundaries-declared-before-results)
and [`docs/research-report.md`](docs/research-report.md#limitations) for the complete, disclosed
list.

## License

MIT. See [`LICENSE`](LICENSE). The CHIME/FRB Catalog 1 data itself is not redistributed under
this license — see [`data/provenance.json`](data/provenance.json) for its own terms.

## Citation

See [`CITATION.cff`](CITATION.cff).
