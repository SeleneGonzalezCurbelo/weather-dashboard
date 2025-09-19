import { useMemo } from "react";
import { TEChart } from "tw-elements-react";
import { flattenByDayAndHour } from "../utils/weatherHelpers";
import { windDegToDir } from "../utils/weatherHelpers";

export default function TemperatureChart({ unit, history }) {
  const flattenedHistory = useMemo(() => flattenByDayAndHour(history), [history]);

  if (!flattenedHistory.length) return <p className="text-gray-500">No data available</p>;

  const temps = flattenedHistory.map(r => (unit === "C" ? r.temperature : r.temperature != null ? Math.round((r.temperature * 9)/5 + 32) : null));

  const maxIndex = temps.indexOf(Math.max(...temps));
  const minIndex = temps.indexOf(Math.min(...temps));

  const chartData = flattenedHistory.map((r, i) => ({
    label: `${r.day} ${r.hour}`,
    value: temps[i],
    humidity: r.humidity,
    wind_speed: r.wind_speed,
    wind_deg: r.wind_deg,
  }));
  
  return (
    <TEChart
      className="w-full h-full"
      type="line"
      data={{
        labels: chartData.map(d => d.label),
        datasets: [
          {
            label: `Temperature (°${unit})`,
            data: chartData.map(d => d.value),
            borderColor: "rgb(59, 130, 246)",
            backgroundColor: "rgba(59, 130, 246, 0.2)",
            tension: 0.3,
            fill: true,
            pointRadius: chartData.map((_, i) => (i === maxIndex || i === minIndex ? 6 : 3)),
            pointBackgroundColor: chartData.map((_, i) =>
              i === maxIndex ? "red" : i === minIndex ? "green" : "rgb(59, 130, 246)"
            ),
          },
        ],
      }}
      options={{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                const record = chartData[tooltipItem.dataIndex];
                const tempLabel = tooltipItem.dataIndex === maxIndex
                  ? `Max: ${record.value} °${unit}`
                  : tooltipItem.dataIndex === minIndex
                  ? `Min: ${record.value} °${unit}`
                  : `${record.value} °${unit}`;
                return [
                  tempLabel,
                  `Humidity: ${record.humidity ?? "–"} %`,
                  `Wind: ${record.wind_speed ?? "–"} m/s ${windDegToDir(record.wind_deg)}`,
                ];
              },
            },
          },
        },
        scales: {
          x: { title: { display: true, text: "Date & Hour" } },
          y: { title: { display: true, text: `Temperature (°${unit})` } },
        },
      }}
    />
  );
}