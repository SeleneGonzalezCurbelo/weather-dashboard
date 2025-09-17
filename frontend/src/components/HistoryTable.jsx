import { useEffect, useState } from "react";

export default function HistoryTable({ city, unit }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!city) return;

    const fetchData = async () => {
      try {
        const res = await fetch(`http://localhost:8000/weather/history/${city}?limit=20`);
        if (!res.ok) throw new Error("Error fetching history");
        const data = await res.json();
        setHistory(data.records);
      } catch (err) {
        console.error(err);
        setHistory([]);
      }
    };

    fetchData();
  }, [city]);

  if (!history.length) return <p className="text-gray-500">Loading history...</p>;

  const tempValues = history.map(r =>
    unit === "C" ? r.temperature : r.temperature != null ? Math.round((r.temperature * 9) / 5 + 32) : null
  );
  const maxTemp = Math.max(...tempValues);
  const minTemp = Math.min(...tempValues);

  return (
    <div className="overflow-x-auto">
      <table className="w-full border border-gray-300 table-fixed">
        <thead className="bg-gray-200">
          <tr>
            <th className="border border-gray-300 px-2 py-1 text-center">Time</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Weather</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Temp (°{unit})</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Humidity (%)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Wind Direction (°)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Wind Speed (m/s)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Precipitation (%)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Rain (mm)</th>
          </tr>
        </thead>
        <tbody>
          {history.map((record, index) => {
            const temp =
              unit === "C"
                ? record.temperature
                : record.temperature != null
                ? Math.round((record.temperature * 9) / 5 + 32)
                : null;
            const isMax = temp === maxTemp;
            const isMin = temp === minTemp;

            return (
              <tr
                key={record.id}
                className={`border-b ${
                  isMax
                    ? "bg-red-100 font-bold"
                    : isMin
                    ? "bg-green-100 font-bold"
                    : index % 2 === 0
                    ? "bg-white hover:bg-gray-50"
                    : "bg-gray-50 hover:bg-gray-100"
                }`}
              >
                <td className="border border-gray-300 px-2 py-1 text-center">{new Date(record.created_at).toLocaleTimeString()}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.description || "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{temp != null ? temp : "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.humidity ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.wind_deg ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.wind_speed ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.precip_prob ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.rain_1h ?? "–"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}