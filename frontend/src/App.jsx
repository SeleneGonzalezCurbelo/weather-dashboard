import "./App.css";
import { useState, useEffect } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import WeatherSummary from "./components/WeatherSummary";
import TemperatureHistory from "./components/TemperatureHistory";

const API_URL = import.meta.env.VITE_API_BASE_URL;

function App() {
  const [city, setCity] = useState(null);
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const detectCityAndWeather = async () => {
      if (!navigator.geolocation) {
        console.log("[App] Geolocation not available, defaulting to Arrecife");
        setCity("Arrecife");
        await fetchWeather("Arrecife");
        return;
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          try {
            const geoUrl = `${API_URL}/weather/reverse-geocode?lat=${latitude}&lon=${longitude}`;
            const geoRes = await fetch(geoUrl);
            if (!geoRes.ok) throw new Error("Reverse geocode failed");

            const geoData = await geoRes.json();
            const detectedCity = geoData.city || "Arrecife";
            setCity(detectedCity);

            await fetchWeather(detectedCity);
          } catch (err) {
            setCity("Arrecife");
            await fetchWeather("Arrecife");
          }
        },
        async () => {
          setCity("Arrecife");
          await fetchWeather("Arrecife");
        }
      );
    };

    const fetchWeather = async (cityName) => {
      const weatherRes = await fetch(`${API_URL}/weather/${cityName}`);
      const weatherData = await weatherRes.json();
      setWeather(weatherData);
      setLoading(false);
    };

    detectCityAndWeather();
  }, []);


  return (
    <div className="min-h-screen flex flex-col overflow-y-auto">
      <Header />
      <div className="max-w-md mx-auto px-4 py-4 flex flex-col space-y-4">
        <div className="py-2">
          <SearchBar onSearch={setCity} />
        </div>
        <div className="py-2">
          {!loading && city && weather && (
            <WeatherSummary city={city} weather={weather} />
          )}
        </div>
      </div>
      <div className="flex-1 flex flex-col p-4 overflow-hidden">
        {!loading && city && <TemperatureHistory city={city} />}
      </div>
    </div>
  );
}

export default App;