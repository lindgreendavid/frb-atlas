# Research report

What the frozen registry ([`reports/v0.1-frb-registry.json`](../reports/v0.1-frb-registry.json))
actually shows, compared against the preregistered hypotheses in
[`research-protocol.md`](research-protocol.md), reported without suppressing an adverse or
unexpected result.

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

### Why this discrepancy likely exists (post-hoc investigation, disclosed as such)

This burst-level discrepancy prompted a specific, narrow follow-up: reading the original paper's
own methodology more closely, it states (quoted from the paper) that its repeater/non-repeater
comparisons use **"only the first-detected repeater events for each repeating source"** — i.e.,
comparing 18 repeater values (one per source) against the non-repeaters, not all 59 individual
repeater bursts. This project's 59-burst sample is dominated by two exceptionally prolific,
nearby, low-DM repeaters: FRB 20180916B alone contributes 33 of the 59 repeater bursts (56%) and
FRB 20180814A contributes 20 more (34%) — together 90% of the repeater sample comes from just 2
of 18 sources. A burst-level test therefore heavily pseudo-replicates these two sources' unusually
low DM rather than sampling 59 independent repeater events.

**This was not part of the preregistered protocol.** It is reported here as a disclosed amendment,
run once, after the primary result was already generated and recorded — not as a substitute for
the primary finding above, which stands as reported. Reproducing the paper's own
first-detection-per-source deduplication (n=18 repeater sources) on `dm_exc_ne2001`:

| Measure | KS p-value | Anderson–Darling p-value | Median (repeater) | Median (non-repeater) |
| --- | --- | --- | --- | --- |
| `dm_exc_ne2001`, first detection per source (post-hoc) | 0.041 | 0.026 | 359.1 pc/cm³ | 510.7 pc/cm³ |

At this project's preregistered α = 0.05, this post-hoc check is still nominally significant.
However, the paper's own text states it treats **p < 0.01** as the threshold for ">99%
confidence" the samples differ; at that stricter, paper-consistent threshold, this
deduplicated check is **not significant** (0.041 and 0.026 are both > 0.01) — much closer to,
though not a clean replication of, the paper's "consistent with being drawn from the same
distribution" conclusion. The most defensible honest summary: **the strong DM discrepancy in
this project's preregistered burst-level test is very likely driven substantially by
pseudo-replication from a small number of prolific, nearby, low-DM repeating sources**, and
mostly (not completely) resolves under the paper's own per-source deduplication and significance
convention. This project does not claim full resolution — n=18 is a small sample and the
post-hoc p-values (0.041, 0.026) sit close enough to any reasonable threshold that a different
DM convention, exclusion choice, or added source could plausibly flip the classification.

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
- **Sample composition dominates the burst-level DM result.** Two of 18 repeater sources supply
  90% of the repeater bursts analyzed; this is disclosed above as the most likely driver of the
  H1 discrepancy from the paper.
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
