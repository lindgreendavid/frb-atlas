# Accessibility statement

FRB Atlas is designed toward WCAG 2.2 Level AA. Accessibility is treated as a release
requirement, not an optional visual polish step. This statement covers the public interactive
atlas built from `site/`.

## What is supported

- Semantic landmarks, ordered headings, a skip link, descriptive page title, and visible
  keyboard focus.
- The DM-distribution and width/bandwidth comparison views are ECDF/histogram charts that use
  distinct line styles (solid vs. dashed) and text labels in addition to color, so the
  repeater/non-repeater distinction never depends on color alone; the same comparisons are also
  presented as full accessible data tables, always present in the DOM, not hidden behind a
  script-only chart with no fallback.
- Uncertainty and limitations are shown in a visually distinct panel **before** any
  "significant or not" conclusion is presented, on every comparison view — mirroring the
  reading-order discipline used across this maintainer's other research projects (Fairshift Lab,
  Three Body Lab).
- Every statistic is shown with its test, its p-value, and its bootstrap confidence interval
  together — never a bare "significant" or "not significant" label without the numbers behind
  it.
- High-contrast and forced-color mode support; reduced-motion support (no animation depends on
  motion for its meaning; any transition respects `prefers-reduced-motion: reduce`).
- Reflow down to a 320 CSS-pixel viewport and support for 200% text zoom without hiding
  navigation destinations.
- No autoplay of audio/video, no flashing content, no time limits, no authentication walls, no
  user file uploads.

## Verification

Every change passes semantic HTML assertions and `eslint-plugin-jsx-a11y`, plus a dedicated
contrast test (`site/tests/accessibility-contrast.test.mjs`) that computes WCAG relative
luminance and contrast ratios for every foreground/background color pair used in the stylesheet
and fails the build if any required pair falls below 4.5:1. The release checklist also covers
keyboard order, focus visibility, non-text alternatives, labels, zoom/reflow, reduced motion,
target size, and color-independent meaning. Automated checks cannot prove accessibility or
compatibility with every assistive-technology combination.

## Known limitations

- The DM, width, and bandwidth distribution charts are a summary view; the accompanying full
  data tables are the complete, non-visual equivalent.
- Some data tables are wide; a labeled, keyboard-focusable scroll region is used for the widest
  tables at narrow viewport widths.
- Mathematical notation (e.g. p-values, confidence intervals) is expressed as plain text/Unicode
  rather than MathML.
- The interface and documentation are currently in English.

## Feedback

Open an accessibility issue at https://github.com/lindgreendavid/frb-atlas/issues/new and
include the page section, browser, assistive technology, and expected behavior when possible.
Security-sensitive reports should use the private process in [`SECURITY.md`](SECURITY.md).

## Standard

The target is the W3C Web Content Accessibility Guidelines 2.2 Level AA:
https://www.w3.org/TR/WCAG22/. Conformance language is intentionally bounded: this is an
engineering statement and testing record, not a third-party accessibility certification.
