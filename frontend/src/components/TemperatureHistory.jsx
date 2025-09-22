import { useEffect, useState } from "react";
import TemperatureChart from "./TemperatureChart";
import HistoryTable from "./HistoryTable";

export default function TemperatureHistory({ city: propCity }) {
  const [activeTab, setActiveTab] = useState("chart");
  const [city, setCity] = useState(propCity || "");
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    setCity(propCity || "");
  }, [propCity]);

  useEffect(() => {
    if (!city) {
      setHistory([]);
      return;
    }

    
  
    let cancelled = false;
    const fetchHistory = async () => {
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
      } 
    };

    fetchHistory();
    return () => { cancelled = true; };
  }, [city]);

  if (!city) return null;
  if (!history || history.length === 0) {
    return null; 
  }
  return (
    <div className="w-full h-full flex flex-col card-bg rounded-2xl shadow-xl p-4">
      {/* Tabs */}
      <div className="flex border-b border-secondary pb-2 mb-4">
        <button
          className={`px-4 py-2 font-semibold rounded-t-xl transition-colors
            ${activeTab === "chart"
              ? "border-b-4 border-white"
              : "text-sub text-black"} `}
          onClick={() => setActiveTab("chart")}
        >
          Chart
        </button>
        <button
          className={`px-4 py-2 font-semibold rounded-t-xl transition-colors
            ${activeTab === "table"
              ? "border-b-4 border-white "
              : "text-sub text-black"} `}
          onClick={() => setActiveTab("table")}
        >
          Table
        </button>
      </div>

      {/* Contenido */}
      <div className="flex-1 w-full overflow-auto">
        {activeTab === "chart" ? (
          <TemperatureChart unit="C" history={history} className="w-full h-full" />
        ) : (
          <HistoryTable unit="C" history={history} />
        )}
      </div>
    </div>
  );
}