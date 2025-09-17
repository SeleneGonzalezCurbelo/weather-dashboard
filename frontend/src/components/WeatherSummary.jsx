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
    "02d": <WiCloud size={64} />,
    "03d": <WiCloudy size={64} />,
    "04d": <WiCloudy size={64} />,
    "09d": <WiShowers size={64} />,
    "10d": <WiRain size={64} />,
    "11d": <WiRain size={64} />,
    "13d": <WiDaySunny size={64} />,
    "50d": <WiCloudy size={64} />,
  };

  useEffect(() => {
    const fetchLatest = async () => {
      setLoading(true);
      try {
        const endpoint = city
          ? `/weather/history/${city}?limit=1`
          : `/weather/history?limit=1`;

        const res = await fetch(`http://localhost:8000${endpoint}`);
        if (!res.ok) throw new Error("Error fetching weather summary");

        const data = await res.json();
        setLatest(data.records[0] || null);
      } catch (err) {
        console.error(err);
        setLatest(null);
      } finally {
        setLoading(false);
      }
    };

    fetchLatest();
  }, [city]);

  if (loading) {
    return (
      <div className="p-6 border rounded bg-gray-50 flex justify-center items-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  if (!latest) {
    return (
      <div className="p-6 border rounded bg-gray-50 flex justify-center items-center">
        <p className="text-gray-600">No data</p>
      </div>
    );
  }

  return (
    <div className="p-4 border rounded bg-white shadow-md">
      {}
      <div className="text-center text-gray-500 text-sm mb-2">
        {new Date(latest.created_at).toLocaleString()}
      </div>

      {}
      <div className="text-center font-bold text-xl mb-4">
        {latest.city}, {latest.country}
      </div>

      {}
      <div className="flex justify-center mb-4">
        {iconMap[latest.icon] || <WiDaySunny size={64} />}
      </div>

      {}
      <div className="text-center text-4xl font-bold mb-2">
        {Math.round(latest.temperature)}°C
      </div>

      {}
      <div className="flex justify-around items-center mb-4 text-gray-600">
        <div className="flex flex-col items-center">
          <span className="text-xl">👁</span>
          <span className="text-sm">{latest.visibility / 1000} km</span>
        </div>
        <div className="flex flex-col items-center">
          <WiStrongWind size={24} />
          <span className="text-sm">{latest.wind_speed} m/s</span>
        </div>
        <div className="flex flex-col items-center">
          <WiWindDeg size={24} style={{ transform: `rotate(${latest.wind_deg}deg)` }} />
          <span className="text-sm">{latest.wind_deg}°</span>
        </div>
      </div>

      {}
      {latest.alerts && latest.alerts.length > 0 && (
        <div className="flex justify-center space-x-2">
          {latest.alerts.map((alert) => (
            <div
              key={alert.id}
              className="p-2 bg-yellow-100 rounded text-yellow-800 text-sm flex items-center"
            >
              ⚠️ {alert.title}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
