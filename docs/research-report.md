# Research report

What the frozen registry ([`reports/v0.1-frb-registry.json`](../reports/v0.1-frb-registry.json))
actually shows, compared against the preregistered hypotheses in
[`research-protocol.md`](research-protocol.md), reported without suppressing an adverse or
unexpected result.

> **Erratum (2026-10-09).** An earlier version of this report said that two prolific repeaters (FRB 20180916B
> and FRB 20180814A) contributed 33 and 20 of the 59 repeater bursts, i.e. 90% of the repeater sample, and named
> that as the likely driver of the H1 discrepancy. **That count was wrong.** Recounting from the verified catalog
> gives 19 and 8 bursts, i.e. 27 of 59 (46%). No registry value, test statistic or hypothesis disposition changes
> (the frozen registry regenerates identically). The explanation is replaced below by a measured one: bursts
> from the same repeating source carry essentially the same DM excess (intraclass correlation 0.99999), so the
> 59-burst DM test has an effective sample size of about 7 (see "Why this discrepancy exists" and Amendment 2).

## Sample

536 catalog bursts → 39 dropped (`excluded_flag == 1`, non-nominal telescope operation) → **497
analyzed bursts**: **59 repeater bursts from 18 sources**, **438 non-repeater bursts**. This
matches the paper abstract's "536 ... including 62 bursts from 18 previously known repeating
sources" for the full catalog exactly (62 → 59 after the disclosed exclusion removes 3 repeater
bursts flagged for non-nominal telescope operation).

## H1 — DM distributions: **falsified on this project's preregistered burst-level test**

The preregistered primary test (two-sample KS, `dm_exc_ne2001`, 59 repeater vs. 438
non-repeater bursts) finds a **highly significant difference**, not the "no significant
difference" the paper's abstract reports:

| Measure | KS statistic | KS p-value | Anderson–Darling p-value | Median (repeater) | Median (non-repeater) | Bootstrap 95% CI of the difference |
| --- | --- | --- | --- | --- | --- | --- |
| `dm_exc_ne2001` (primary) | 0.457 | 2.0×10⁻¹⁰ | <0.001 | 157.0 pc/cm³ | 510.7 pc/cm³ | [167.4, 389.4] pc/cm³ |
| `dm_fitb` (secondary) | 0.479 | 2.0×10⁻¹¹ | <0.001 | 349.7 pc/cm³ | 572.8 pc/cm³ | [184.6, 268.5] pc/cm³ |
| `dm_exc_ymw16` (secondary) | 0.487 | 8.1×10⁻¹² | <0.001 | 164.6 pc/cm³ | 498.7 pc/cm³ | [198.0, 454.9] pc/cm³ |

All three DM conventions agree: at burst level, this sample's repeaters have systematically
**lower** DM than non-repeaters, and the difference is significant by a wide margin under every
disclosed test. **This is a genuine discrepancy from the original paper's own stated finding**,
on this project's exact preregistered method — reported honestly, not softened.

### Why this discrepancy exists (post-hoc investigation, disclosed as such)

The original catalog paper states that its repeater/non-repeater comparisons use **"only the first-detected
repeater events for each repeating source"**, i.e. 18 repeater values (one per source) against the non-repeaters,
not all 59 individual repeater bursts. The 59 bursts come from 18 sources with very unequal burst counts
(FRB 20180916B: 19, FRB 20180814A: 8, FRB 20181119A and FRB 20181128A: 3 each, twelve sources with 2, two sources
with 1). Bursts from one source share that source's dispersion measure: within a source the DM excess differs by
a few pc/cm³ at most, against hundreds of pc/cm³ between sources. A burst-level test therefore counts each source's
DM several times, weighted by its burst count. Measured, post-hoc (`reports/v0.2-source-clustering.json`,
`src/frb_atlas/clustering.py`):

| Quantity (DM excess, NE2001) | Value |
| --- | --- |
| Intraclass correlation of DM within sources | 0.99999 |
| Kish design effect (cluster size 8.36) | 8.36 |
| Effective sample size of the 59 repeater bursts | about 7.1 |
| Source-level KS (18 sources vs 438 non-repeaters) | p = 0.041 (identical for all 10,000 random one-burst-per-source draws, because each source has one DM) |
| Source-level Mann–Whitney | p = 0.026 |
| Burst-level KS with any one source removed | p between 2.0×10⁻¹¹ and 4.4×10⁻⁵ (never above 0.01) |

Reading: the burst-level significance (p = 2×10⁻¹⁰) is produced by counting 18 source values 59 times with
unequal weights, not by one or two sources: removing any single source, including FRB 20180916B, leaves the
burst-level difference significant. At the unit that is actually independent (the source), the difference is
marginal: p = 0.041 (KS) and 0.026 (Mann–Whitney) at the preregistered α = 0.05, and not significant at the
paper's stricter p < 0.01 convention. The first-detection-per-source check below is one instance of this
collapse and gives the same KS p-value.

**This was not part of the preregistered protocol.** It is reported as a disclosed amendment, run after the primary
result was generated; the primary finding above stands as reported. This project does not claim the DM
populations are the same: n = 18 sources is small and the source-level p-values sit near any reasonable threshold.

Reproducing the paper's own first-detection-per-source deduplication (n = 18 repeater sources) on `dm_exc_ne2001`:

| Measure | KS p-value | Anderson–Darling p-value | Median (repeater) | Median (non-repeater) |
| --- | --- | --- | --- | --- |
| `dm_exc_ne2001`, first detection per source (post-hoc) | 0.041 | 0.026 | 359.1 pc/cm³ | 510.7 pc/cm³ |

## H2 — pulse width and spectral bandwidth: **confirmed, robustly**

| Measure | KS statistic | KS p-value | Anderson–Darling p-value | Median (repeater) | Median (non-repeater) |
| --- | --- | --- | --- | --- | --- |
| `width_fitb`, all analyzed bursts | 0.433 | 2.4×10⁻⁹ | <0.001 | 2.00 ms | 0.93 ms |
| `width_fitb`, excluding upper-limit-flagged widths | 0.425 | 5.9×10⁻⁹ | <0.001 | 2.00 ms | 0.97 ms |
| bandwidth (`high_freq − low_freq`), all analyzed bursts | 0.522 | 1.3×10⁻¹³ | <0.001 | 206.0 MHz | 346.1 MHz |
| bandwidth, excluding limit-flagged-width bursts | 0.529 | 6.4×10⁻¹⁴ | <0.001 | 206.0 MHz | 351.5 MHz |
| `width_fitb`, first detection per source (post-hoc, n=18) | — | 0.0006 | 0.001 | — | — |
| bandwidth, first detection per source (post-hoc, n=18) | — | ~0 | 0.001 | — | — |

Both width and bandwidth differences are significant at every threshold tested (α = 0.05 or the
paper's stricter 0.01), under every robustness variant tried (excluding limit-flagged widths,
and reproducing the paper's per-source deduplication). This **replicates the paper's own claim**
that repeaters differ from non-repeaters in intrinsic temporal width and spectral bandwidth, and
this project's repeaters show **narrower bandwidth and wider (longer) intrinsic pulse width**
than non-repeaters, consistent with the qualitative direction reported in the literature for
this catalog.

## What H2's clean replication implies about H1

H2 is the protocol's positive control: recovering the published width and bandwidth directions
shows that the pipeline can detect those catalog-level contrasts under the disclosed sample
definitions. It does not prove that every H1 implementation choice matches the paper or that H1
is free of selection bias. The DM difference is a reproducible feature of this project's burst-
level analysis, but it shrinks sharply after source deduplication. This project does not extend
that observation into a claim about the physical DM properties of repeating vs. non-repeating
FRB source populations.

## Evidence published after Catalog 1

A later CHIME/FRB source-level study of 25 newly discovered repeaters reported significantly
lower mean DM and extragalactic DM for repeaters (CHIME/FRB Collaboration 2023,
[doi:10.3847/1538-4357/acc6c1](https://doi.org/10.3847/1538-4357/acc6c1)). That later result is
directionally consistent with this project's burst-level contrast, but it does not retroactively
validate the burst-level p-value: it uses a later source sample and explicitly requires sensitivity
and exposure effects to be considered before physical interpretation. The literature therefore
supports "sample- and selection-dependent evidence," not a settled two-population conclusion.

## Hypothesis dispositions

- **H1 (DM indistinguishable): falsified** on the preregistered burst-level test (highly
  significant difference found); **not clearly falsified** under a disclosed, non-preregistered
  post-hoc check reproducing the paper's own per-source deduplication and significance
  convention (marginal, threshold-dependent).
- **H2 (width/bandwidth distinguishable): confirmed**, robustly, across every measure and
  sample-definition variant tried.

## Limitations

- **Single survey, single band, one year.** 400–800 MHz, CHIME/FRB, 2018-07-25 to 2019-07-01
  only. No claim is made about any other telescope, band, or time period.
- **Small, unbalanced groups.** 59 repeater bursts (18 sources) vs. 438 non-repeater bursts at
  burst level; only 18 independent repeater sources at source level. Neither a significant nor a
  non-significant result at this size should be read as a strong, generalizable population
  claim.
- **Repeater/non-repeater is a detection-window label**, not a guaranteed physical category —
  some "non-repeaters" may repeat below this survey's sensitivity or after this window closed.
- **DM convention matters and is disclosed, not hidden.** All three DM measures (raw `dm_fitb`,
  NE2001-subtracted, YMW16-subtracted) agree qualitatively at burst level in this reanalysis, but
  the magnitude of the median difference varies by convention (167–455 pc/cm³ depending on
  measure and CI bound).
- **Source clustering dominates the burst-level DM result.** Bursts from one repeating source share its DM
  (ICC 0.99999), so the 59 repeater bursts behave like about 7 independent observations; see the erratum and
  Amendment 2. The diagnostics are post-hoc and descriptive.
- **No independent completeness or selection-function model.** CHIME/FRB's sensitivity to DM,
  pulse width, declination, and Galactic latitude is not independently modeled here; the
  catalog's own derived columns are used as-is.
- **Multi-component bursts are reduced to their first fitted sub-burst**, discarding
  sub-burst-level morphology for those events (see the preregistered exclusion in
  `research-protocol.md`).
- **This project does not resolve, and does not claim to resolve**, whether repeating and
  non-repeating FRBs are physically distinct source populations. It reports what one disclosed
  statistical pipeline finds on one public catalog.

## Amendment log

- 2026-08-13: after generating the primary registry and finding H1 falsified at burst level, a
  narrow post-hoc check (first-detection-per-source deduplication, reproducing the original
  paper's own method) was added to `frb_atlas.registry` and re-run once. This is disclosed here
  as a deviation from the frozen preregistered plan, added to explain rather than to overturn the
  primary result, and is labeled `*_first_detection_per_source` and marked "POST-HOC (not
  preregistered)" directly in the registry JSON.
- 2026-10-09 (Amendment 2): the claim that two sources supply 90% of the repeater bursts was found to be
  incorrect (actual: 27 of 59, 46%) while preparing a paper. The explanation was replaced by measured
  source-clustering diagnostics (`reports/v0.2-source-clustering.json`; post-hoc, all four diagnostics for all three
  measures reported). The frozen v0.1 registry is unchanged and regenerates identically.
