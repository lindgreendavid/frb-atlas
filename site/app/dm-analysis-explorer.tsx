"use client";

import { useState } from "react";
import type { Comparison } from "./registry-types";

type AnalysisUnit = "bursts" | "sources";
type Alpha = 0.05 | 0.01;

interface DmAnalysisExplorerProps {
  burstLevel: Comparison;
  firstDetectionPerSource: Comparison;
}

function formatP(value: number) {
  return value < 0.0001 ? value.toExponential(2) : value.toFixed(4);
}

export function DmAnalysisExplorer({
  burstLevel,
  firstDetectionPerSource,
}: DmAnalysisExplorerProps) {
  const [unit, setUnit] = useState<AnalysisUnit>("bursts");
  const [alpha, setAlpha] = useState<Alpha>(0.05);
  const selected = unit === "bursts" ? burstLevel : firstDetectionPerSource;
  const rejectsEqualDistributions = selected.ks.p_value < alpha;
  const retainedRepeaterUnits = (selected.n_repeater / burstLevel.n_repeater) * 100;

  return (
    <section className="analysis-explorer" id="analysis-unit" aria-labelledby="analysis-title">
      <div className="analysis-explorer__intro">
        <p className="analysis-explorer__eyebrow">Interactive sensitivity analysis</p>
        <h3 id="analysis-title">Change the unit. Watch the conclusion change.</h3>
        <p>
          The catalog is unchanged. Only the independence assumption and decision threshold move.
          This is why an analysis can disagree with a paper without either dataset being wrong.
        </p>
      </div>

      <div className="analysis-controls">
        <fieldset>
          <legend>Repeater analysis unit</legend>
          <button
            type="button"
            aria-pressed={unit === "bursts"}
            onClick={() => setUnit("bursts")}
          >
            All 59 bursts
            <small>Preregistered here</small>
          </button>
          <button
            type="button"
            aria-pressed={unit === "sources"}
            onClick={() => setUnit("sources")}
          >
            18 first detections
            <small>Post-hoc paper method</small>
          </button>
        </fieldset>

        <fieldset>
          <legend>Decision threshold</legend>
          <button type="button" aria-pressed={alpha === 0.05} onClick={() => setAlpha(0.05)}>
            α = 0.05
            <small>Registry threshold</small>
          </button>
          <button type="button" aria-pressed={alpha === 0.01} onClick={() => setAlpha(0.01)}>
            α = 0.01
            <small>Catalog paper threshold</small>
          </button>
        </fieldset>
      </div>

      <div className="analysis-result" aria-live="polite">
        <div className="analysis-result__decision">
          <span>KS decision at α = {alpha.toFixed(2)}</span>
          <strong>{rejectsEqualDistributions ? "Difference detected" : "Not detected"}</strong>
          <p>
            p = {formatP(selected.ks.p_value)}; this is{" "}
            {rejectsEqualDistributions ? "below" : "not below"} the selected threshold.
          </p>
        </div>
        <dl>
          <div>
            <dt>Repeater rows analyzed</dt>
            <dd>{selected.n_repeater}</dd>
          </div>
          <div>
            <dt>Non-repeater units</dt>
            <dd>{selected.n_non_repeater}</dd>
          </div>
          <div>
            <dt>KS distance</dt>
            <dd>{selected.ks.statistic.toFixed(3)}</dd>
          </div>
          <div>
            <dt>Median DM gap</dt>
            <dd>{selected.bootstrap.median_diff_non_repeater_minus_repeater.toFixed(1)} pc/cm³</dd>
          </div>
          <div>
            <dt>Bootstrap 95% interval</dt>
            <dd>
              {selected.bootstrap.ci_95_low.toFixed(1)} to{" "}
              {selected.bootstrap.ci_95_high.toFixed(1)} pc/cm³
            </dd>
          </div>
        </dl>
        <div
          className="analysis-result__retention"
          aria-label={retainedRepeaterUnits.toFixed(0) + " percent of repeater observations retained"}
        >
          <span style={{ width: retainedRepeaterUnits + "%" }} />
        </div>
        <p className="analysis-result__boundary">
          {unit === "bursts"
            ? "Two prolific repeater sources contribute 90% of these 59 bursts, so the rows are not 59 independent sources."
            : "Keeping one first detection per repeating source reduces source-level pseudo-replication, but this was a disclosed post-hoc check—not the preregistered test."}
        </p>
      </div>
    </section>
  );
}
