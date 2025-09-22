import { useEffect, useState } from "react";
import { weatherEmojis, metricEmojis } from "../utils/icons";
import { formattedDate } from "../utils/date";
import { windDegToDir } from "../utils/weatherHelpers";

export default function WeatherSummary({ city }) {
  const [latest, setLatest] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!city) {
      setLatest(null);
      return;
    }

    const fetchLatest = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:8000/weather/${encodeURIComponent(city)}`);
        if (!res.ok) throw new Error("API unavailable");
        const data = await res.json();

        const formatted = {
          created_at: new Date(),
          city: data.name,
          country: data.sys?.country || "",
          temperature: data.main?.temp,
          feels_like: data.main?.feels_like,
          humidity: data.main?.humidity,
          pressure: data.main?.pressure,
          visibility: data.visibility,
          wind_speed: data.wind?.speed,
          wind_deg: data.wind?.deg,
          icon: data.weather?.[0]?.icon,
          alerts: [],
        };

        setLatest(formatted);
      } catch (err) {
        console.error("API failed, trying DB fallback:", err);
        try {
          const fallbackRes = await fetch(
            `http://localhost:8000/weather/history/${encodeURIComponent(city)}?limit=1`
          );
          const fallbackData = await fallbackRes.json();
          setLatest(fallbackData.records[0] || null);
        } catch (dbErr) {
          console.error("DB fallback failed:", dbErr);
          setLatest(null);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchLatest();
  }, [city]);

  if (loading) return <p className="text-white">Loading...</p>;
  if (!latest) return <p className="text-white">No data available</p>;

  return (
    <div className="max-w-md mx-auto rounded-[2rem] shadow-xl card-bg border border-white p-6 flex flex-col items-center space-y-6">
      <div className="flex justify-between items-center w-full p-4">
        {/* Ciudad, fecha y temperatura */}
        <div className="flex flex-col justify-center">
          <h2 className="text-3xl font-extrabold text-white">
            {latest.city}, {latest.country}
          </h2>
          <p className="text-sub text-sm mt-1">{formattedDate(latest)}</p>

          {/* Temperatura y sensación térmica */}
          <div className="mt-2">
            <div className="text-5xl font-bold text-white">
              {latest.temperature != null ? Math.round(latest.temperature) : "--"}°C
            </div>
            <p className="text-sm text-sub mt-1">
              Feels like: {latest.feels_like != null ? Math.round(latest.feels_like) : "--"}°C
            </p>
          </div>
        </div>

        {/* Icono */}
        <div className="text-[7rem] flex items-center justify-center">
          {weatherEmojis[latest.icon] || "🌤"}
        </div>
      </div>
 

      {/* Detalles */}
      <div className="grid grid-cols-3 gap-4 w-full mt-6 px-2 pb-2">
        <div className="flex flex-col items-center p-3 rounded-2xl border border-white card-bg shadow-sm rounded-[2rem]">

          <div className="text-3xl">{metricEmojis.humidity}</div>
          <span className="font-bold mt-1 text-white">{latest.humidity ?? "--"}%</span>
          <span className="text-xs text-sub mt-1">Humidity</span>
        </div>

        <div className="flex flex-col items-center p-3 rounded-2xl border border-white card-bg shadow-sm rounded-[2rem]">

          <div className="text-3xl">{metricEmojis.pressure}</div>
          <span className="font-bold mt-1 text-white">{latest.pressure ?? "--"} hPa</span>
          <span className="text-xs text-sub mt-1">Pressure</span>
        </div>

        <div className="flex flex-col items-center p-3 rounded-2xl border border-white card-bg shadow-sm rounded-[2rem]">
          <div className="text-3xl">{metricEmojis.wind}</div>
          <span className="font-bold mt-1 text-white">
            {latest.wind_speed ?? "--"} m/s{" "}
            {latest.wind_deg != null ? `(${windDegToDir(latest.wind_deg)})` : ""}
          </span>
          <span className="text-xs text-sub mt-1">Wind</span>
        </div>
      </div>
    </div>
  );
}
