import { useState, useEffect } from "react";
import TemperatureChart from "./TemperatureChart";
import HistoryTable from "./HistoryTable";

export default function TemperatureHistory({ city: propCity }) {
  const [activeTab, setActiveTab] = useState("chart");
  const [city, setCity] = useState(propCity || "");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`http://localhost:8000/weather/history?limit=20`);
        if (!res.ok) throw new Error("Error fetching history");
        const data = await res.json();
        setHistory(data.records);

        if (!city && data.records.length > 0) {
          setCity(data.records[data.records.length - 1].city);
        }
      } catch (err) {
        console.error(err);
        setHistory([]);
      }
    };

    fetchHistory();
  }, [city]);

  if (!history.length) return <p className="text-gray-500">Loading history...</p>;
  if (!city) return <p className="text-gray-500">No city selected</p>;

  return (
    <div className="w-full h-full flex flex-col bg-white rounded shadow p-4">
      {}
      <div className="flex border-b border-gray-300 pb-2 mb-4">
        <button
          className={`px-4 py-2 font-semibold ${
            activeTab === "chart" ? "border-b-4 border-blue-500 bg-blue-100" : "text-gray-600 hover:bg-gray-100"
          } rounded-t-lg`}
          onClick={() => setActiveTab("chart")}
        >
          Chart
        </button>
        <button
          className={`px-4 py-2 font-semibold ${
            activeTab === "table" ? "border-b-4 border-blue-500 bg-blue-100" : "text-gray-600 hover:bg-gray-100"
          } rounded-t-lg`}
          onClick={() => setActiveTab("table")}
        >
          Table
        </button>
      </div>

      {}
      <div className="flex-1 w-full overflow-auto">
        {activeTab === "chart" && (
          <TemperatureChart city={city} unit="C" history={history} className="w-full h-full" />
        )}
        {activeTab === "table" && (
          <div className="w-full h-full overflow-auto">
            <HistoryTable city={city} unit="C" history={history} />
          </div>
        )}
      </div>
    </div>
  );
}
