import { useEffect, useState } from "react";
import { flattenByDayAndHour } from "../utils/weatherHelpers";
import { windDegToDir } from "../utils/weatherHelpers";
import { 
  WiCloud, WiDaySunny, WiRain, WiCloudy, WiShowers, WiStrongWind, WiWindDeg 
} from "react-icons/wi";

export default function HistoryTable({ unit, history }) {
  const [flattenedHistory, setFlattenedHistory] = useState([]);
  const iconMap = {
    "01d": <WiDaySunny />,
    "01n": <WiDaySunny />,
    "02d": <WiCloud />,
    "02n": <WiCloud />,
    "03d": <WiCloudy />,
    "03n": <WiCloudy />,
    "04d": <WiCloudy />,
    "04n": <WiCloudy />,
    "09d": <WiShowers />,
    "09n": <WiShowers />,
    "10d": <WiRain />,
    "10n": <WiRain />,
    "11d": <WiRain />,
    "11n": <WiRain />,
    "13d": <WiDaySunny />,
    "13n": <WiDaySunny />,
    "50d": <WiCloudy />,
    "50n": <WiCloudy />,
  };

  useEffect(() => {
    if (!history || history.length === 0) return;
    setFlattenedHistory(flattenByDayAndHour(history));
  }, [history]);

  if (!flattenedHistory.length) return <p className="text-gray-500">No history available</p>;
  console.log(flattenedHistory);
  const tempValues = flattenedHistory.map(r =>
    unit === "C" ? r.temperature : r.temperature != null ? Math.round((r.temperature * 9) / 5 + 32) : null
  );
  const maxTemp = Math.max(...tempValues);
  const minTemp = Math.min(...tempValues);

  return (
    <div className="overflow-x-auto">
      <table className="w-full border border-gray-300 table-fixed">
        <thead className="bg-gray-200">
          <tr>
            <th className="border border-gray-300 px-2 py-1 text-center">Date</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Hour</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Weather</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Temp (°{unit})</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Humidity (%)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Wind Direction (°)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Wind Speed (m/s)</th>
            <th className="border border-gray-300 px-2 py-1 text-center">Cloudiness (%)</th>
          </tr>
        </thead>
        <tbody>
          {flattenedHistory.map((record, index) => {
            const showDate = index === 0 || record.day !== flattenedHistory[index - 1].day;
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
                <td className="border border-gray-300 px-2 py-1 text-center">{showDate ? record.day : ""}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.hour}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{iconMap[record.icon] || "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{temp != null ? temp : "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.humidity ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{windDegToDir(record.wind_deg)}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.wind_speed ?? "–"}</td>
                <td className="border border-gray-300 px-2 py-1 text-center">{record.cloudiness ?? "–"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}