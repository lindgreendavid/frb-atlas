# Research protocol

Frozen before generating or interpreting any v0.1.0 result.

## Status

This protocol is fixed before running `scripts/generate_registry.py` or looking at the
resulting registry. It describes the data source, the exact exclusion criteria, the grouping
variable, the statistical tests, and the analysis plan. Any deviation from this document
discovered after results exist will be recorded as an amendment in
[`research-report.md`](research-report.md), not silently applied.

## Research question

Using the real, published CHIME/FRB Catalog 1 data (Amiri et al. 2021, ApJS 257, 59): do
repeating and apparently non-repeating fast radio bursts, as detected by CHIME/FRB between
2018-07-25 and 2019-07-01, differ in dispersion measure (DM)? And, as an internal validity
check on the same pipeline, do they differ in intrinsic pulse width and spectral bandwidth, a
difference the original catalog paper's own abstract reports finding?

## What this project is not

This is a reproducibility and analysis exercise on one public catalog from one telescope over
one year of operation. It does not resolve any open question in fast radio burst
astrophysics, does not claim to determine whether repeating and non-repeating FRBs are
physically distinct source populations, and does not extend, correct, or supersede the CHIME/FRB
Collaboration's own published analysis. It reports what a straightforward, disclosed
statistical pipeline finds on this specific 536-burst sample, compared honestly against what
the original paper's abstract claims.

## Scope boundaries (declared before results)

1. **One catalog, one instrument, one year.** CHIME/FRB Catalog 1 only: 536 bursts detected
   400–800 MHz, 2018-07-25 to 2019-07-01. No later CHIME/FRB catalogs, no other telescopes, no
   later-discovered repeat activity from sources first classified as non-repeaters after this
   window.
2. **Detection-pipeline selection effects are not modeled or corrected for.** CHIME/FRB's
   sensitivity varies with declination, DM (via intra-channel dispersion smearing), pulse
   width, and Galactic latitude (Milky Way DM contribution and scattering). This project uses
   the catalog's own derived columns as-is; it does not build an independent completeness or
   selection function.
3. **Repeater/non-repeater is a detection-window label, not a physical guarantee.** A burst is
   labeled "non-repeater" if no repeat burst from the same sky location was detected *during
   this catalog's window*. Some apparent non-repeaters plausibly repeat at a rate below this
   survey's sensitivity, or repeated later. This project does not correct for that; it is
   reported as a limitation.
4. **Multi-component bursts are reduced to one row per event** (see Exclusions below), which
   discards sub-burst-level morphology. This is a disclosed scope boundary, not an oversight.

## Data source and access

- **Primary citation:** CHIME/FRB Collaboration (M. Amiri et al.) 2021, "The First CHIME/FRB
  Fast Radio Burst Catalog," *The Astrophysical Journal Supplement Series*, 257, 59.
  DOI: [10.3847/1538-4365/ac33ab](https://doi.org/10.3847/1538-4365/ac33ab). arXiv:
  [2106.04352](https://arxiv.org/abs/2106.04352).
- **Erratum:** CHIME/FRB Collaboration 2023, ApJS, 264, 53.
  DOI: [10.3847/1538-4365/acb54c](https://doi.org/10.3847/1538-4365/acb54c). The erratum
  corrects a normalization bug and a selection-criteria bug in the **all-sky burst rate**
  calculation of Section 6.2 (revising the quoted rate from
  820<sup>+220</sup><sub>−200</sub> to 525<sup>+142</sup><sub>−131</sub> bursts sky⁻¹ day⁻¹,
  both with a separate ±30–60 statistical term). This project does not use or reproduce the
  all-sky rate calculation. The erratum does not mention any correction to the per-burst
  catalog columns (DM, width, spectral index, sky position, repeater flag) used here, and the
  data-access channel used below (VizieR) mirrors the same published table the erratum leaves
  unmodified. This is disclosed rather than silently assumed: no independent confirmation that
  every individual catalog cell is error-free was performed beyond the erratum's own stated
  scope.
- **Machine-readable table used:** VizieR catalog `J/ApJS/257/59/table2` (CDS/VizieR,
  `https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/257/59/table2`), chosen over
  the official chime-frb-open-data project site because that site was unavailable
  ("rebuilding") during this project's data-access research, and over the `cfod` Python
  package because `cfod` only *parses* a local catalog file — it does not itself fetch or
  bundle Catalog 1 data — whereas VizieR is CDS's standard long-term archive mirror of
  published astronomical tables and is expected to remain stable independent of the survey's
  own site.
- **Verification performed before building anything on this source (2026-08-13):**
  - VizieR's column list for `table2` matches the catalog columns and value ranges quoted in
    the paper's Table 2 documentation exactly, including bracketed value ranges (e.g. DM
    103–3039 pc/cm³, matching the paper).
  - The table contains 600 rows total, corresponding to per-sub-burst (multi-component) rows;
    selecting `sub_num == 0` yields exactly 536 rows with 536 unique `tns_name` values, matching
    the paper's stated 536-burst catalog exactly.
  - Among those 536, exactly 62 rows have a non-empty `repeater_name` (`RpName` in VizieR),
    drawn from exactly 18 unique repeater source names — matching the paper abstract's "62
    bursts from 18 previously known repeating sources" exactly.
  - `scripts/fetch_catalog.py` re-runs these two checks (536-row count, 62-bursts/18-sources
    invariant) at fetch time and fails loudly if either does not hold, so a future re-fetch
    cannot silently drift onto a different or corrupted table.
- **License:** the official CHIME/FRB site states no formal open-data license, only "you may
  use the data for publications; cite the relevant CHIME/FRB Collaboration papers." VizieR
  distributes CDS-hosted astronomical catalogs under its standard research-use terms. Per this
  maintainer's established pattern (see Fairshift Lab's `data/provenance/`), the raw catalog
  file is **not committed to git**; `data/provenance.json` records the source URL, access date,
  and citation, and `scripts/fetch_catalog.py` re-downloads it at reproduction time.

## Columns used

| Column | Meaning | Role |
| --- | --- | --- |
| `tns_name` | TNS burst identifier | unique key |
| `repeater_name` | non-empty for known-repeater bursts | grouping variable |
| `dm_fitb` | DM from fitburst model fit | secondary DM measure (reported, not primary) |
| `dm_exc_ne2001` | Milky-Way-subtracted "extragalactic" DM excess, NE2001 electron-density model | **primary DM measure** |
| `dm_exc_ymw16` | same, YMW16 electron-density model | secondary DM measure (reported, not primary) |
| `width_fitb` | intrinsic pulse width from fitburst | primary width measure |
| `high_freq`, `low_freq` | FWTM band edges of detection | spectral bandwidth = `high_freq − low_freq` |
| `excluded_flag` | 1 = excluded from parameter inference (non-nominal telescope operation), 0 = included | exclusion criterion |
| `sub_num` | sub-burst component index (0, 1, 2, …) within a multi-component event | de-duplication key |

**Primary DM measure justification:** `dm_exc_ne2001` is chosen over raw `dm_fitb` because raw
DM is dominated by each burst's Galactic-latitude-dependent Milky Way contribution, which is a
foreground effect unrelated to the source population question; subtracting a Galactic
electron-density model isolates the (still model-dependent) extragalactic/host contribution
that is the physically relevant quantity for a source-population comparison. NE2001 is chosen
over YMW16 only because it is listed first in the catalog and is the more widely used legacy
model in the FRB literature at the time of the original paper; this is an arbitrary tie-break,
disclosed as such. `dm_fitb` and `dm_exc_ymw16` are computed and reported alongside as a
robustness check — the report states whether the conclusion changes under either alternative
DM measure.

## Exclusions (declared before results)

1. **Sub-burst de-duplication:** keep only rows with `sub_num == 0` (596 of the 600 raw
   VizieR rows are dropped as duplicate sub-burst components of an already-represented event),
   leaving exactly 536 rows, one per catalog burst. This discards sub-burst-level morphology
   for multi-component bursts; the width and bandwidth reported for those events describe only
   their first fitted sub-burst, not the whole multi-component profile. This is a scope
   boundary, not a data-quality exclusion.
2. **Telescope-operation exclusion:** drop rows with `excluded_flag == 1` (39 of the 536,
   flagged for non-nominal telescope operation during detection per the catalog's own
   documentation) from all statistical comparisons. **497 bursts remain**: 59 repeater bursts
   from 18 sources, 438 non-repeater bursts.
3. **No further exclusions.** No additional cuts on SNR, sky position, or declination are
   applied. Upper-limit flagged widths (`l_widthfitb`, 23 of the 497 remaining bursts) are
   included at their reported (limit) value in the primary analysis; a robustness check
   re-runs the width/bandwidth tests excluding these 23 rows and the report states whether the
   result changes.
4. Every exclusion is applied identically to both groups; no group-specific filtering is used.

## Grouping variable

A burst is a **repeater** if `repeater_name` is non-empty (and not the catalog's `-9999`
sentinel); otherwise it is a **non-repeater**. This is exactly the grouping the original paper
uses in its own repeater/non-repeater comparison.

## Falsifiable hypotheses

1. **H1 — DM distributions are indistinguishable (replicating the paper's own finding).**
   The two-sample Kolmogorov–Smirnov test on `dm_exc_ne2001` between the repeater group (n=59)
   and non-repeater group (n=438) does not reject the null hypothesis of equal distributions
   at α = 0.05. This is what the original paper's abstract reports finding. A significant
   result here (p < 0.05) would be a genuine discrepancy from the paper on this specific
   sample and exact test, and will be reported as such, not explained away.
2. **H2 — pulse width and spectral bandwidth distributions ARE distinguishable (replicating
   the paper's own finding).** The two-sample Kolmogorov–Smirnov test on `width_fitb`, and
   separately on spectral bandwidth (`high_freq − low_freq`), between the same two groups,
   rejects the null hypothesis of equal distributions at α = 0.05, matching the paper's
   abstract claim that repeaters differ from non-repeaters in these two properties. This
   hypothesis is a positive control: if this pipeline correctly detects a real, published,
   significant effect here while finding no significant DM difference in H1, that is evidence
   the pipeline has power to detect real differences and H1's null result is not simply an
   artifact of an underpowered test.
3. **No claim of resolving the repeater/non-repeater debate.** Regardless of H1's and H2's
   outcomes, the report will not claim this project determines whether repeaters and
   non-repeaters are physically distinct populations — only what this specific test, on this
   specific sample and DM convention, shows.

## Statistical methods

- **Primary test:** two-sample Kolmogorov–Smirnov test (`scipy.stats.ks_2samp`, two-sided),
  applied separately to `dm_exc_ne2001`, `width_fitb`, and spectral bandwidth
  (`high_freq − low_freq`). Reports the KS statistic `D` and its p-value.
- **Secondary/robustness test:** two-sample Anderson–Darling test
  (`scipy.stats.anderson_ksamp`), applied to the same three quantities, reported alongside the
  KS result. Anderson–Darling is more sensitive to distribution-tail differences than KS; if
  the two tests disagree on significance, that disagreement is reported explicitly rather than
  resolved by picking the more favorable one.
- **Effect size and uncertainty:** for each of the three quantities, the median difference
  (non-repeater median − repeater median) with a percentile bootstrap 95% confidence interval
  (10,000 resamples, `numpy.random.default_rng(seed=20260813)`, resampling each group
  independently with replacement at its own observed size). Reported alongside every p-value,
  never a p-value alone.
- **Significance threshold:** α = 0.05, two-sided, disclosed as a conventional (not uniquely
  correct) threshold. No multiple-comparison correction is applied across the three quantities
  because each addresses a distinct, individually preregistered hypothesis (H1 for DM, H2 for
  width and bandwidth as a single joint claim from the paper's abstract) rather than an
  exploratory multiple-testing search; this choice is disclosed, not hidden.
- **Robustness checks reported alongside the primary result, not used to pick a more
  favorable outcome:**
  - DM comparison repeated on `dm_fitb` (raw) and `dm_exc_ymw16` (alternative Galactic model).
  - Width/bandwidth comparison repeated excluding the 23 upper-limit-flagged width rows.

## Analysis plan

- Report every planned test's statistic, p-value, and bootstrap CI, including a null (not
  significant) result for H1 if that is what the sample shows — a successful DM replication is
  reported as a genuine, interesting finding, not a "nothing to see here."
- Report H2's disposition the same way, including if it unexpectedly fails to replicate.
- State group sizes (59 vs. 438) and the resulting statistical power limitation explicitly:
  this is a small, unbalanced two-sample comparison, and a non-significant result cannot be
  read as proof of "no difference," only as "no difference detected at this sample size and
  test."
- State the single-survey, single-band (400–800 MHz), one-year selection-effect limitation
  before presenting any comparison result, on both the site and in the report, consistent with
  the "uncertainty and limitations first" reading order used in this maintainer's other
  research projects.
- Never claim this project resolves whether repeating and non-repeating FRBs are physically
  distinct source populations — only what this disclosed pipeline finds on this disclosed
  sample.

## Ethics and responsible framing

This is an analysis of public, non-personal, professionally collected astronomical
observations; there are no human subjects and no personal data. The responsible-communication
obligation here is scientific honesty about a small, single-survey sample: not overstating
statistical power, not treating a null DM result as proof of "no difference," and not
overstating a significant width/bandwidth result as a completed explanation of what
distinguishes repeating FRBs.
