import "./App.css";
import { useState } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import WeatherSummary from "./components/WeatherSummary";
import TemperatureHistory from "./components/TemperatureHistory";

function App() {
  const [city, setCity] = useState("");

  return (
    <div className="h-screen flex flex-col">
      <Header />

      {}
      <div className="max-w-md mx-auto px-4 py-4 flex flex-col space-y-4">
        <SearchBar onSearch={setCity} />
        <WeatherSummary city={city} />
      </div>

      {}
      <div className="flex-1 flex flex-col p-4 overflow-hidden">
        <TemperatureHistory city={city} />
      </div>
    </div>
  );
}

export default App;