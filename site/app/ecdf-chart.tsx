import { domainOf, ecdf, ecdfPath } from "./ecdf";

interface EcdfChartProps {
  title: string;
  description: string;
  unit: string;
  repeater: number[];
  nonRepeater: number[];
  tableId: string;
}

const WIDTH = 640;
const HEIGHT = 300;
const PADDING = 40;

export function EcdfChart({
  title,
  description,
  unit,
  repeater,
  nonRepeater,
  tableId,
}: EcdfChartProps) {
  const domain = domainOf(repeater, nonRepeater);
  const repeaterPath = ecdfPath(ecdf(repeater), domain, WIDTH, HEIGHT, PADDING);
  const nonRepeaterPath = ecdfPath(ecdf(nonRepeater), domain, WIDTH, HEIGHT, PADDING);
  const gridY = [0, 0.25, 0.5, 0.75, 1];
  const toY = (fraction: number) => HEIGHT - PADDING - fraction * (HEIGHT - 2 * PADDING);
  const [xMin, xMax] = domain;

  return (
    <div className="chart-card">
      <h3>{title}</h3>
      <p>{description}</p>
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        role="img"
        aria-labelledby={`${tableId}-title`}
        aria-describedby={`${tableId}-desc`}
      >
        <title id={`${tableId}-title`}>{title}</title>
        <desc id={`${tableId}-desc`}>
          Empirical cumulative distribution comparing {repeater.length} repeater bursts (dashed
          line) against {nonRepeater.length} non-repeater bursts (solid line), in {unit}. Full
          values are in the accessible data table below this chart.
        </desc>
        {gridY.map((fraction) => (
          <line
            key={fraction}
            x1={PADDING}
            x2={WIDTH - PADDING}
            y1={toY(fraction)}
            y2={toY(fraction)}
            className="chart-grid"
          />
        ))}
        {gridY.map((fraction) => (
          <text key={fraction} x={4} y={toY(fraction) + 3}>
            {fraction.toFixed(2)}
          </text>
        ))}
        <text x={PADDING} y={HEIGHT - 8}>
          {xMin.toFixed(1)}
        </text>
        <text x={WIDTH - PADDING} y={HEIGHT - 8} textAnchor="end">
          {xMax.toFixed(1)} {unit}
        </text>
        <path d={nonRepeaterPath} className="ecdf-line ecdf-line--non-repeater" />
        <path d={repeaterPath} className="ecdf-line ecdf-line--repeater" />
      </svg>
      <div className="chart-legend">
        <span>
          <i className="legend-swatch--non-repeater" aria-hidden="true" /> Non-repeater bursts
          (solid line), n={nonRepeater.length}
        </span>
        <span>
          <i className="legend-swatch--repeater" aria-hidden="true" /> Repeater bursts (dashed
          line), n={repeater.length}
        </span>
      </div>
    </div>
  );
}
