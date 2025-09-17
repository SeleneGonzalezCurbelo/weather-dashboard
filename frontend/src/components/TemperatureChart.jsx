import { useEffect, useState } from "react";
import { TEChart } from "tw-elements-react";

export default function TemperatureChart({ city, unit }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (!city) return;

    const fetchData = async () => {
      try {
        const res = await fetch(`http://localhost:8000/weather/history/${city}?limit=20`);
        if (!res.ok) throw new Error("Error fetching history");
        const data = await res.json();

        const transformed = data.records.map((r) => ({
          date: new Date(r.created_at).toLocaleTimeString(),
          temperature:
            unit === "C"
              ? r.temperature ?? 0
              : r.temperature != null
              ? Math.round((r.temperature * 9) / 5 + 32)
              : 0,
        }));

        setChartData(transformed.reverse());
      } catch (err) {
        console.error(err);
        setChartData([]);
      }
    };

    fetchData();
  }, [city, unit]);

  if (!chartData.length) return <p className="text-gray-500">Cargando gráfica...</p>;

  const temps = chartData.map((d) => d.temperature);
  const maxIndex = temps.indexOf(Math.max(...temps));
  const minIndex = temps.indexOf(Math.min(...temps));

  return (
    <div className="w-full h-full">
      <TEChart
        className="w-full h-full"
        type="line"
        data={{
          labels: chartData.map((d) => d.date),
          datasets: [
            {
              label: `Temperature (°C)`,
              data: temps,
              borderColor: "rgb(59, 130, 246)",
              backgroundColor: "rgba(59, 130, 246, 0.2)",
              tension: 0.3,
              fill: true,
              pointRadius: chartData.map((_, i) =>
                i === maxIndex || i === minIndex ? 6 : 3
              ),
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
                  const value = tooltipItem.parsed.y;
                  if (tooltipItem.dataIndex === maxIndex) return `Max: ${value} °${unit}`;
                  if (tooltipItem.dataIndex === minIndex) return `Min: ${value} °${unit}`;
                  return `${value} °${unit}`;
                },
              },
            },
          },
          scales: {
            x: { title: { display: true, text: "Hour", color: "#374151", font: { size: 14, weight: "bold" } }, ticks: { color: "#374151" }, grid: { color: "#e5e7eb" } },
            y: { title: { display: true, text: `Temperature (°${unit})`, color: "#374151", font: { size: 14, weight: "bold" } }, ticks: { color: "#374151" }, grid: { color: "#e5e7eb" } },
          },
        }}
      />
    </div>
  );
}