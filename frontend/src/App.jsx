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

      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;
        console.log("[App] Got geolocation coords:", position.coords);

        const geoUrl = `${API_URL}/weather/reverse-geocode?lat=${latitude}&lon=${longitude}`;
        console.log("[App] Fetching reverse-geocode:", geoUrl);

        const geoRes = await fetch(geoUrl);
        console.log("[App] Reverse-geocode response status:", geoRes.status, geoRes.statusText);

        const geoData = await geoRes.json();
        console.log("[App] Reverse-geocode data:", geoData);

        const detectedCity = geoData.city || "Arrecife";
        console.log("[App] Detected city:", detectedCity);
        setCity(detectedCity);

        const weatherUrl = `${API_URL}/weather/${detectedCity}`;
        console.log("[App] Fetching weather:", weatherUrl);

        const weatherRes = await fetch(weatherUrl);
        console.log("[App] Weather response status:", weatherRes.status);

        const weatherData = await weatherRes.json();
        console.log("[App] Weather data:", weatherData);

        setWeather(weatherData);
        setLoading(false);

      }, (err) => {
        console.warn("[App] Geolocation denied or unavailable:", err);
        setCity("Arrecife");
        fetchWeather("Arrecife");
      });
    };

    const fetchWeather = async (cityName) => {
      console.log("[App] fetchWeather called for city:", cityName);
      const weatherRes = await fetch(`${API_URL}/weather/${cityName}`);
      console.log("[App] fetchWeather status:", weatherRes.status);
      const weatherData = await weatherRes.json();
      console.log("[App] fetchWeather data:", weatherData);
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