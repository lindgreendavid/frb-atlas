export interface TestResult {
  statistic: number;
  p_value: number;
  significant: boolean;
  alpha: number;
}

export interface Bootstrap {
  median_repeater: number;
  median_non_repeater: number;
  median_diff_non_repeater_minus_repeater: number;
  ci_95_low: number;
  ci_95_high: number;
  resamples: number;
  seed: number;
}

export interface Comparison {
  label: string;
  n_repeater: number;
  n_non_repeater: number;
  ks: TestResult;
  anderson_darling: TestResult;
  bootstrap: Bootstrap;
}

export interface Registry {
  schema_version: number;
  catalog: {
    total_bursts: number;
    excluded_bursts: number;
    analyzed_bursts: number;
    repeater_bursts: number;
    non_repeater_bursts: number;
    repeater_sources: number;
  };
  settings: {
    alpha: number;
    bootstrap_resamples: number;
    bootstrap_seed: number;
  };
  comparisons: Record<string, Comparison>;
  distributions: {
    dm_exc_ne2001: { repeater: number[]; non_repeater: number[] };
    width_fitb: { repeater: number[]; non_repeater: number[] };
    bandwidth: { repeater: number[]; non_repeater: number[] };
  };
}
