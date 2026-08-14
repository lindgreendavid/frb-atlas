import registryJson from "./data/registry.json";
import type { Registry } from "./registry-types";
import { EcdfChart } from "./ecdf-chart";
import { ComparisonResult } from "./comparison-result";
import { DistributionTable } from "./distribution-table";
import { DmAnalysisExplorer } from "./dm-analysis-explorer";

const registry = registryJson as unknown as Registry;
const { catalog, comparisons, distributions } = registry;

export default function Home() {
  return (
    <>
      <a href="#main" className="skip-link">
        Skip to main content
      </a>
      <header className="nav">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true">
            ))
          </span>
          <span>FRB Atlas</span>
        </div>
        <nav className="nav__links" aria-label="Primary">
          <a href="#dm-comparison">DM comparison</a>
          <a href="#analysis-unit">Analysis unit</a>
          <a href="#validation">Width &amp; bandwidth</a>
          <a href="#decision">Findings</a>
          <a href="#method">Method</a>
          <a href="#sources">Data &amp; citations</a>
        </nav>
      </header>

      <main id="main">
        <section className="hero">
          <div className="eyebrow">
            <span>CHIME/FRB Catalog 1 reanalysis</span>
            <span>Product v1.0.0 · preregistered frozen v0.1 registry</span>
          </div>
          <h1>
            Do repeaters look <em>different</em>?
          </h1>
          <p className="hero__lead">
            The original CHIME/FRB Catalog 1 paper reports no significant dispersion-measure
            (DM) difference between repeating and non-repeating fast radio bursts, but a
            significant difference in pulse width and spectral bandwidth. This project
            reproduces that exact comparison on the same public, real 536-burst catalog with a
            preregistered statistical pipeline — and reports what it actually finds, including
            where it disagrees with the paper.
          </p>
          <div className="hero__actions">
            <a className="button button--primary" href="#dm-comparison">
              See the DM comparison
            </a>
            <a
              className="button button--ghost"
              href="https://github.com/lindgreendavid/frb-atlas/blob/main/docs/research-report.md"
            >
              Read the full report
            </a>
          </div>
          <div className="hero__principles">
            <span>Preregistered protocol</span>
            <span>Real public catalog data</span>
            <span>Frozen result registry</span>
            <span>Discrepancies disclosed, not hidden</span>
          </div>
        </section>

        <section className="findings" aria-labelledby="findings-heading">
          <div className="section-heading">
            <div>
              <span className="section-index">01</span>
              <p>Sample</p>
            </div>
            <h2 id="findings-heading">497 analyzed bursts</h2>
          </div>
          <div className="stat-row">
            <article>
              <span>Total catalog bursts</span>
              <strong>{catalog.total_bursts}</strong>
              <small>Real CHIME/FRB Catalog 1, Amiri et al. 2021</small>
            </article>
            <article>
              <span>Excluded (non-nominal operation)</span>
              <strong>{catalog.excluded_bursts}</strong>
              <small>excluded_flag == 1, per the catalog&apos;s own ReadMe</small>
            </article>
            <article>
              <span>Non-repeater bursts analyzed</span>
              <strong>{catalog.non_repeater_bursts}</strong>
              <small>no known repeat detection in this survey window</small>
            </article>
            <article>
              <span>Repeater bursts analyzed</span>
              <strong>{catalog.repeater_bursts}</strong>
              <small>from {catalog.repeater_sources} distinct repeating sources</small>
            </article>
          </div>

          <div className="limitations-first">
            <h3>Read this before any &quot;significant or not&quot; conclusion below</h3>
            <ul>
              <li>
                One survey, one band (400–800 MHz), one year (2018-07-25 to 2019-07-01) — no
                claim is made about any other telescope, band, or time period.
              </li>
              <li>
                Small, unbalanced groups: {catalog.repeater_bursts} repeater bursts from only{" "}
                {catalog.repeater_sources} sources vs. {catalog.non_repeater_bursts}{" "}
                non-repeaters. Two of those {catalog.repeater_sources} sources supply 90% of the
                repeater bursts analyzed here.
              </li>
              <li>
                &quot;Non-repeater&quot; is a detection-window label, not a guaranteed physical
                category — some may repeat below this survey&apos;s sensitivity or after this
                window closed.
              </li>
              <li>
                This project does not resolve whether repeating and non-repeating FRBs are
                physically distinct source populations.
              </li>
            </ul>
            <p className="uncertainty-note">
              Full limitations: <a href="#sources">docs/research-report.md</a>.
            </p>
          </div>
        </section>

        <section className="compare" id="dm-comparison" aria-labelledby="dm-heading">
          <div className="section-heading">
            <div>
              <span className="section-index">02</span>
              <p>Primary preregistered test</p>
            </div>
            <h2 id="dm-heading">Dispersion measure: falsified, then investigated</h2>
          </div>
          <EcdfChart
            title="DM excess (NE2001 model) — repeaters vs. non-repeaters"
            description="Milky Way-subtracted extragalactic DM excess (NE2001 electron-density model), the preregistered primary DM measure. If the two groups were drawn from the same distribution, these two lines would closely overlap."
            unit="pc/cm³"
            repeater={distributions.dm_exc_ne2001.repeater}
            nonRepeater={distributions.dm_exc_ne2001.non_repeater}
            tableId="dm-chart"
          />
          <ComparisonResult
            label="dm_exc_ne2001 (primary, preregistered)"
            ks={comparisons.dm_exc_ne2001_primary.ks}
            andersonDarling={comparisons.dm_exc_ne2001_primary.anderson_darling}
            bootstrap={comparisons.dm_exc_ne2001_primary.bootstrap}
            unit="pc/cm³"
          />
          <DmAnalysisExplorer
            burstLevel={comparisons.dm_exc_ne2001_primary}
            firstDetectionPerSource={comparisons.dm_exc_ne2001_first_detection_per_source}
          />
          <DistributionTable
            caption="DM excess (NE2001), repeater vs. non-repeater bursts"
            unit="pc/cm³"
            repeater={distributions.dm_exc_ne2001.repeater}
            nonRepeater={distributions.dm_exc_ne2001.non_repeater}
          />
          <div className="limitations-first" style={{ marginTop: "22px" }}>
            <h3>This does not replicate the paper — here is the disclosed investigation</h3>
            <p>
              The paper&apos;s abstract reports DM as <em>not</em> significantly different
              between repeaters and non-repeaters. This project&apos;s preregistered burst-level
              test finds the opposite (p ≈ 2×10⁻¹⁰). A non-preregistered, clearly-labeled
              post-hoc check — reproducing the paper&apos;s own method of using only each
              repeating source&apos;s first-detected burst (n=18 sources instead of 59 bursts) —
              shrinks this to p={comparisons.dm_exc_ne2001_first_detection_per_source.ks.p_value.toFixed(
                4,
              )}
              , which is not significant at the paper&apos;s own stated p&lt;0.01 threshold. The
              most likely driver: two of 18 repeater sources supply 90% of the analyzed repeater
              bursts, so a burst-level test heavily pseudo-replicates those two sources&apos;
              unusually low DM. Full reasoning:{" "}
              <a href="https://github.com/lindgreendavid/frb-atlas/blob/main/docs/research-report.md#h1--dm-distributions-falsified-on-this-projects-preregistered-burst-level-test">
                docs/research-report.md
              </a>
              .
            </p>
          </div>
        </section>

        <section className="compare" id="validation" aria-labelledby="validation-heading">
          <div className="section-heading">
            <div>
              <span className="section-index">03</span>
              <p>Positive control</p>
            </div>
            <h2 id="validation-heading">Width &amp; bandwidth: confirmed, robustly</h2>
          </div>
          <p className="uncertainty-note" style={{ marginBottom: "22px" }}>
            The paper also reports that repeaters differ from non-repeaters in intrinsic pulse
            width and spectral bandwidth. If this pipeline can detect that real, published effect
            on the same sample, that is evidence the DM result above is not simply an
            underpowered test producing noise.
          </p>
          <EcdfChart
            title="Intrinsic pulse width (fitburst) — repeaters vs. non-repeaters"
            description="width_fitb, all analyzed bursts."
            unit="s"
            repeater={distributions.width_fitb.repeater}
            nonRepeater={distributions.width_fitb.non_repeater}
            tableId="width-chart"
          />
          <ComparisonResult
            label="width_fitb"
            ks={comparisons.width_fitb.ks}
            andersonDarling={comparisons.width_fitb.anderson_darling}
            bootstrap={comparisons.width_fitb.bootstrap}
            unit="s"
          />
          <DistributionTable
            caption="Intrinsic pulse width, repeater vs. non-repeater bursts"
            unit="seconds"
            repeater={distributions.width_fitb.repeater}
            nonRepeater={distributions.width_fitb.non_repeater}
          />
          <div style={{ height: "26px" }} />
          <EcdfChart
            title="Spectral bandwidth (high_freq − low_freq) — repeaters vs. non-repeaters"
            description="Detection bandwidth in MHz, all analyzed bursts."
            unit="MHz"
            repeater={distributions.bandwidth.repeater}
            nonRepeater={distributions.bandwidth.non_repeater}
            tableId="bandwidth-chart"
          />
          <ComparisonResult
            label="bandwidth (high_freq − low_freq)"
            ks={comparisons.bandwidth.ks}
            andersonDarling={comparisons.bandwidth.anderson_darling}
            bootstrap={comparisons.bandwidth.bootstrap}
            unit="MHz"
          />
          <DistributionTable
            caption="Spectral bandwidth, repeater vs. non-repeater bursts"
            unit="MHz"
            repeater={distributions.bandwidth.repeater}
            nonRepeater={distributions.bandwidth.non_repeater}
          />
        </section>

        <section className="decision" id="decision" aria-labelledby="decision-heading">
          <div className="section-heading">
            <div>
              <span className="section-index">04</span>
              <p>Reading the result</p>
            </div>
            <h2 id="decision-heading">What this does and does not show</h2>
          </div>
          <div className="decision-reading">
            <article>
              <span>H1 — DM</span>
              <h3>Falsified at burst level</h3>
              <p>
                The preregistered test found a significant DM difference, not the paper&apos;s
                &quot;no difference.&quot; A disclosed post-hoc check narrows but does not fully
                close the gap — see above.
              </p>
            </article>
            <article>
              <span>H2 — width &amp; bandwidth</span>
              <h3>Confirmed, robustly</h3>
              <p>
                Significant in every variant tried: full sample, limit-flag-excluded, and
                per-source deduplicated. This is the paper&apos;s own claim, replicated cleanly.
              </p>
            </article>
            <article>
              <span>What this is not</span>
              <h3>Not a resolved debate</h3>
              <p>
                This project does not determine whether repeating and non-repeating FRBs are
                physically distinct populations — only what this disclosed pipeline finds on
                this one public catalog.
              </p>
            </article>
          </div>
        </section>

        <section className="method" id="method" aria-labelledby="method-heading">
          <div className="section-heading section-heading--light">
            <div>
              <span className="section-index">05</span>
              <p>Scientific method</p>
            </div>
            <h2 id="method-heading">How this was built, before any result existed</h2>
          </div>
          <div className="method-grid">
            <article>
              <span>Data</span>
              <h3>Real Catalog 1, verified</h3>
              <p>
                536 bursts from VizieR (J/ApJS/257/59/table2), a stable mirror of the published
                table. Row count and the &quot;62 bursts from 18 sources&quot; invariant are
                checked at every fetch.
              </p>
            </article>
            <article>
              <span>Exclusions</span>
              <h3>Disclosed, applied equally</h3>
              <p>
                39 bursts flagged excluded_flag==1 (non-nominal telescope operation) are dropped
                from both groups identically. No further cuts.
              </p>
            </article>
            <article>
              <span>Tests</span>
              <h3>KS + Anderson–Darling + bootstrap</h3>
              <p>
                Two-sided two-sample KS as the primary test, Anderson–Darling as a robustness
                check, and a 10,000-resample percentile bootstrap CI on the median difference —
                fixed seed, fully reproducible.
              </p>
            </article>
          </div>
          <div className="equation-card">
            <span>Bootstrap median-difference CI</span>
            <code>CI₉₅ = percentile([median(bootstrap_b) − median(bootstrap_a)], 2.5, 97.5)</code>
            <p>10,000 resamples, numpy.random.default_rng(seed=20260813), each group resampled independently at its own observed size.</p>
          </div>
        </section>

        <section className="report" id="sources" aria-labelledby="sources-heading">
          <div className="section-heading">
            <div>
              <span className="section-index">06</span>
              <p>Data &amp; citations</p>
            </div>
            <h2 id="sources-heading">Provenance and further reading</h2>
          </div>
          <div className="source-list">
            <a href="https://doi.org/10.3847/1538-4365/ac33ab">
              <span>Primary citation</span>
              <strong>
                CHIME/FRB Collaboration (Amiri et al.) 2021, &quot;The First CHIME/FRB Fast Radio
                Burst Catalog,&quot; ApJS, 257, 59
              </strong>
              <p>DOI 10.3847/1538-4365/ac33ab · arXiv:2106.04352</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://doi.org/10.3847/1538-4365/acb54c">
              <span>Erratum</span>
              <strong>CHIME/FRB Collaboration 2023, ApJS, 264, 53</strong>
              <p>
                Corrects the all-sky burst-rate calculation only (Section 6.2); does not affect
                the per-burst columns used here.
              </p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/frb-atlas/blob/main/data/provenance.json">
              <span>Provenance record</span>
              <strong>data/provenance.json</strong>
              <p>Source URL, access date, license status, and structural verification checks.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/frb-atlas/blob/main/docs/research-protocol.md">
              <span>Preregistered protocol</span>
              <strong>docs/research-protocol.md</strong>
              <p>Hypotheses, exclusions, and exact statistical tests, fixed before any result.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/frb-atlas/blob/main/docs/research-report.md">
              <span>Full report</span>
              <strong>docs/research-report.md</strong>
              <p>Every hypothesis&apos;s disposition, the DM discrepancy investigation, and limitations.</p>
              <b aria-hidden="true">→</b>
            </a>
            <a href="https://github.com/lindgreendavid/frb-atlas">
              <span>Source code</span>
              <strong>github.com/lindgreendavid/frb-atlas</strong>
              <p>Python analysis package, tests, and this site&apos;s source.</p>
              <b aria-hidden="true">→</b>
            </a>
          </div>
        </section>
      </main>

      <footer>
        <div>
          <span className="brand__mark" aria-hidden="true">
            ))
          </span>
          <p>FRB Atlas product v1.0.0 · frozen v0.1 study · MIT licensed · data used per CHIME/FRB Collaboration terms</p>
        </div>
        <a href="https://github.com/lindgreendavid/frb-atlas/blob/main/ACCESSIBILITY.md">
          Accessibility statement
        </a>
      </footer>
    </>
  );
}
