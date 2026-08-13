interface DistributionTableProps {
  caption: string;
  unit: string;
  repeater: number[];
  nonRepeater: number[];
}

/** A scrollable, fully accessible data table listing every value behind a chart. */
export function DistributionTable({
  caption,
  unit,
  repeater,
  nonRepeater,
}: DistributionTableProps) {
  const rows = Math.max(repeater.length, nonRepeater.length);
  const repeaterSorted = [...repeater].sort((a, b) => a - b);
  const nonRepeaterSorted = [...nonRepeater].sort((a, b) => a - b);
  return (
    <details className="data-alternative">
      <summary>Read the complete data table for {caption} (values sorted ascending, {unit})</summary>
      <div className="table-scroll">
        <table>
          <caption>{caption}</caption>
          <thead>
            <tr>
              <th scope="col">Row</th>
              <th scope="col">Non-repeater ({nonRepeater.length} bursts)</th>
              <th scope="col">Repeater ({repeater.length} bursts)</th>
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: rows }, (_, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{nonRepeaterSorted[index]?.toFixed(4) ?? "—"}</td>
                <td>{repeaterSorted[index]?.toFixed(4) ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}
