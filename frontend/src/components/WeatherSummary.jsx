import { useEffect, useState } from "react";
import {
  WiCloud,
  WiDaySunny,
  WiRain,
  WiCloudy,
  WiShowers,
  WiStrongWind,
  WiWindDeg,
} from "react-icons/wi";

export default function WeatherSummary({ city }) {
  const [latest, setLatest] = useState(null);
  const [loading, setLoading] = useState(false);

  const iconMap = {
    "01d": <WiDaySunny size={64} />,
    "01n": <WiDaySunny size={64} />,
    "02d": <WiCloud size={64} />,
    "02n": <WiCloud size={64} />,
    "03d": <WiCloudy size={64} />,
    "03n": <WiCloudy size={64} />,
    "04d": <WiCloudy size={64} />,
    "04n": <WiCloudy size={64} />,
    "09d": <WiShowers size={64} />,
    "09n": <WiShowers size={64} />,
    "10d": <WiRain size={64} />,
    "10n": <WiRain size={64} />,
    "11d": <WiRain size={64} />,
    "11n": <WiRain size={64} />,
    "13d": <WiDaySunny size={64} />,
    "13n": <WiDaySunny size={64} />,
    "50d": <WiCloudy size={64} />,
    "50n": <WiCloudy size={64} />,
  };

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
          const fallbackRes = await fetch(`http://localhost:8000/weather/history/${encodeURIComponent(city)}?limit=1`);
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

  if (loading) return <p className="text-gray-500">Loading...</p>;
  if (!latest) return <p className="text-gray-500">No data available</p>;

  return (
    <div className="p-4 border rounded bg-white shadow-md text-center">
      <div className="text-gray-500 text-sm mb-2">{new Date(latest.created_at).toLocaleString()}</div>
      <div className="font-bold text-xl mb-4">{latest.city}, {latest.country}</div>
      <div className="flex justify-center mb-4">{iconMap[latest.icon] || <WiDaySunny size={64} />}</div>
      <div className="text-4xl font-bold mb-2">{latest.temperature != null ? Math.round(latest.temperature) : "--"}°C</div>
      <div className="flex justify-around items-center mb-4 text-gray-600">
        <div className="flex flex-col items-center"><span>👁</span><span className="text-sm">{latest.visibility ? latest.visibility/1000 : "--"} km</span></div>
        <div className="flex flex-col items-center"><WiStrongWind size={24} /><span className="text-sm">{latest.wind_speed ?? "--"} m/s</span></div>
        <div className="flex flex-col items-center"><WiWindDeg size={24} style={{ transform: `rotate(${latest.wind_deg ?? 0}deg)` }} /><span className="text-sm">{latest.wind_deg ?? "--"}°</span></div>
      </div>
    </div>
  );
}
