import { useEffect, useState } from "react";
import { flattenByDayAndHour, windDegToDir } from "../utils/weatherHelpers";
import { weatherEmojis } from "../utils/icons";

export default function HistoryTable({ unit, history }) {
  const [flattenedHistory, setFlattenedHistory] = useState([]);

  useEffect(() => {
    if (!history || history.length === 0) return;
    setFlattenedHistory(flattenByDayAndHour(history));
  }, [history]);

  const tempValues = flattenedHistory.map((r) =>
    unit === "C"
      ? r.temperature
      : r.temperature != null
      ? Math.round((r.temperature * 9) / 5 + 32)
      : null
  );
  const maxTemp = Math.max(...tempValues);
  const minTemp = Math.min(...tempValues);

  return (
    <div className="overflow-x-auto rounded-2xl shadow-md card-bg border border-white p-2">
      <table className="w-full text-sm border-collapse">
        <thead className="bg-blue-700 text-white font-semibold uppercase text-xs rounded-t-2xl">
          <tr>
            <th className="px-4 py-2 text-left">Date</th>
            <th className="px-4 py-2 text-left">Hour</th>
            <th className="px-4 py-2 text-center">Weather</th>
            <th className="px-4 py-2 text-center">Temp (°{unit})</th>
            <th className="px-4 py-2 text-center">Humidity (%)</th>
            <th className="px-4 py-2 text-center">Wind</th>
            <th className="px-4 py-2 text-center">Clouds (%)</th>
          </tr>
        </thead>
        <tbody className="text-white">
          {flattenedHistory.map((record, index) => {
            const showDate =
              index === 0 || record.day !== flattenedHistory[index - 1].day;
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
                key={record.id ?? `${record.created_at}-${index}`}
                className={`transition-colors duration-150 ${
                  isMax
                    ? "bg-red-50 font-semibold text-red-700"
                    : isMin
                    ? "bg-green-50 font-semibold text-green-700"
                    : index % 2 === 0
                    ? "bg-card-bg"
                    : "bg-card-bg/90"
                } hover:bg-blue-50 rounded-xl`}
              >
                <td className="px-4 py-2">{showDate ? record.day : ""}</td>
                <td className="px-4 py-2">{record.hour}</td>
                <td className="px-4 py-2 text-center">
                  {weatherEmojis[record.icon] || "–"}
                </td>
                <td className="px-4 py-2 text-center">{temp ?? "–"}</td>
                <td className="px-4 py-2 text-center">{record.humidity ?? "–"}</td>
                <td className="px-4 py-2 text-center">
                  {windDegToDir(record.wind_deg)}{" "}
                  <span className="text-sub text-xs">
                    ({record.wind_speed ?? "–"} m/s)
                  </span>
                </td>
                <td className="px-4 py-2 text-center">{record.cloudiness ?? "–"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
