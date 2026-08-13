# v1.0.0 release audit

Audit date: 2026-08-13. Scientific baseline: `7b65433e1732f625b2676724ed156241918aeb7b`.
The exact product-release commit is the commit resolved by annotated tag `v1.0.0`.

## Evidence checked

- Primary catalog paper: CHIME/FRB Collaboration, DOI
  [10.3847/1538-4365/ac33ab](https://doi.org/10.3847/1538-4365/ac33ab); erratum DOI
  [10.3847/1538-4365/acb54c](https://doi.org/10.3847/1538-4365/acb54c).
- The pinned VizieR table was retrieved again. Its source structure remains 536 bursts, including
  62 bursts associated with 18 repeating sources. The frozen exclusions leave 497 analyzed bursts:
  438 apparent non-repeaters and 59 repeater bursts.
- The preregistered comparisons, uncertainty procedure, replication/discrepancy language and
  research-report boundaries were checked against the regenerated registry.

## Integrity

SHA-256 of `reports/v0.1-frb-registry.json`:
`5787023d3c974c32852f4eba1d7dd620d22f3f6c766138108b6de9610337e30f`.

## Boundary

v1.0.0 stabilizes the product and preserves the v0.1 study. Catalog labels, selection effects and
multiple bursts from the same source constrain the inference; disagreement with one published
comparison is reported, not erased.
