import "./App.css";
import { useState, useEffect } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import WeatherSummary from "./components/WeatherSummary";
import TemperatureHistory from "./components/TemperatureHistory";
import { detectCity, getWeather } from "./services/api";

function App() {
  const [city, setCity] = useState(null);
  const [initialWeather, setInitialWeather] = useState(null);
  const [loadingCity, setLoadingCity] = useState(true);

  useEffect(() => {
    const detect = async () => {
      if (!navigator.geolocation) {
        try {
          const weather = await getWeather("Arrecife");
          setCity("Arrecife");
          setInitialWeather(weather);
        } catch {
          setCity("Arrecife");
        } finally {
          setLoadingCity(false);
        }
        return;
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          console.log("[App] Got geolocation coords:", position.coords);

          try {
            const { city, weather } = await detectCity(latitude, longitude);
            setCity(city);
            setInitialWeather(weather);
            console.log("[App] Detected city:", city);
            console.log("[App] Initial weather data:", weather);
          } catch {
            console.error("[App] Failed to detect city");
            try {
              const weather = await getWeather("Arrecife");
              setCity("Arrecife");
              setInitialWeather(weather);
            } catch {
              setCity("Arrecife");
            }
          } finally {
            setLoadingCity(false);
          }
        },
        async () => {
          console.warn("[App] Geolocation denied/unavailable");
          try {
            const weather = await getWeather("Arrecife");
            setCity("Arrecife");
            setInitialWeather(weather);
          } catch {
            setCity("Arrecife");
          } finally {
            setLoadingCity(false);
          }
        }
      );
    };

    detect();
  }, []);

  return (
    <div className="min-h-screen flex flex-col overflow-y-auto">
      <Header />
      <div className="max-w-md mx-auto px-4 py-4 flex flex-col space-y-4">
        <div className="py-2">
          <SearchBar onSearch={setCity} />
        </div>
        <div className="py-2">
          {!loadingCity && (
            <WeatherSummary 
              city={city}
              initialWeather={initialWeather} 
            />
          )}
        </div>
      </div>
      <div className="flex-1 flex flex-col p-4 overflow-hidden">
        {!loadingCity && (
          <TemperatureHistory 
            city={city}
            initialWeather={initialWeather} 
          />
        )}
      </div>
    </div>
  );
}

export default App;