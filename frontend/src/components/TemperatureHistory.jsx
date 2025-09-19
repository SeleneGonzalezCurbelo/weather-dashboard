import { useEffect, useState } from "react";
import TemperatureChart from "./TemperatureChart";
import HistoryTable from "./HistoryTable";

export default function TemperatureHistory({ city: propCity }) {
  const [activeTab, setActiveTab] = useState("chart");
  const [city, setCity] = useState(propCity || "");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (propCity && propCity !== city) setCity(propCity);
  }, [propCity]);

  useEffect(() => {
    if (!city) {
      setHistory([]);
      return;
    }

    let cancelled = false;

    const fetchHistory = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/weather/forecast/${encodeURIComponent(city)}`);
        if (!res.ok) throw new Error("API unavailable");
        const data = await res.json();
        if (cancelled) return;
        setHistory(data || []);
      } catch (err) {
        console.error("API failed, trying DB fallback:", err);

        try {
          const fallbackRes = await fetch(`http://localhost:8000/weather/history/${encodeURIComponent(city)}?limit=20`);
          const fallbackData = await fallbackRes.json();
          if (!cancelled) setHistory(fallbackData.records || []);
        } catch (dbErr) {
          console.error("DB fallback failed:", dbErr);
          if (!cancelled) setHistory([]);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchHistory();
    return () => { cancelled = true; };
  }, [city]);

  if (loading) return <p className="text-gray-500">Loading history...</p>;
  if (!city) return null;
  if (!history || history.length === 0) return <p className="text-gray-500">No history available</p>;

  return (
    <div className="w-full h-full flex flex-col bg-white rounded shadow p-4">
      <div className="flex border-b border-gray-300 pb-2 mb-4">
        <button className={`px-4 py-2 font-semibold ${activeTab==="chart"?"border-b-4 border-blue-500 bg-blue-100":"text-gray-600 hover:bg-gray-100"} rounded-t-lg`} onClick={()=>setActiveTab("chart")}>Chart</button>
        <button className={`px-4 py-2 font-semibold ${activeTab==="table"?"border-b-4 border-blue-500 bg-blue-100":"text-gray-600 hover:bg-gray-100"} rounded-t-lg`} onClick={()=>setActiveTab("table")}>Table</button>
      </div>
      <div className="flex-1 w-full overflow-auto">
        {activeTab==="chart" ? <TemperatureChart unit="C" history={history} className="w-full h-full"/> :
          <HistoryTable unit="C" history={history}/>}
      </div>
    </div>
  );
}