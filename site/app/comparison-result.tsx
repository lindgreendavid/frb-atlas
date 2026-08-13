interface TestResult {
  statistic: number;
  p_value: number;
  significant: boolean;
  alpha: number;
}

interface Bootstrap {
  median_repeater: number;
  median_non_repeater: number;
  median_diff_non_repeater_minus_repeater: number;
  ci_95_low: number;
  ci_95_high: number;
  resamples: number;
}

interface ComparisonResultProps {
  label: string;
  ks: TestResult;
  andersonDarling: TestResult;
  bootstrap: Bootstrap;
  unit: string;
}

function fmt(value: number, digits = 3): string {
  if (Math.abs(value) < 0.001 && value !== 0) {
    return value.toExponential(2);
  }
  return value.toFixed(digits);
}

export function ComparisonResult({
  label,
  ks,
  andersonDarling,
  bootstrap,
  unit,
}: ComparisonResultProps) {
  return (
    <div>
      <p>
        <strong>{label}</strong>
        <span
          className={`result-tag ${ks.significant ? "result-tag--significant" : "result-tag--not-significant"}`}
        >
          {ks.significant ? "Significant (KS)" : "Not significant (KS)"}
        </span>
      </p>
      <div className="stat-footer">
        <div>
          <span>KS statistic / p-value</span>
          <strong>
            D={fmt(ks.statistic)}, p={fmt(ks.p_value, 4)}
          </strong>
        </div>
        <div>
          <span>Anderson-Darling p-value</span>
          <strong>
            p={fmt(andersonDarling.p_value, 4)}{" "}
            {andersonDarling.significant ? "(significant)" : "(not significant)"}
          </strong>
        </div>
        <div>
          <span>Median repeater / non-repeater</span>
          <strong>
            {fmt(bootstrap.median_repeater)} / {fmt(bootstrap.median_non_repeater)} {unit}
          </strong>
        </div>
        <div>
          <span>Bootstrap 95% CI of the difference</span>
          <strong>
            [{fmt(bootstrap.ci_95_low)}, {fmt(bootstrap.ci_95_high)}] {unit} (
            {bootstrap.resamples.toLocaleString()} resamples)
          </strong>
        </div>
      </div>
    </div>
  );
}
