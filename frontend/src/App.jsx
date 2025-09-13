import './App.css'
import Header from "./components/Header"
import SearchBar from "./components/SearchBar"
import WeatherSummary from "./components/WeatherSummary"
import TemperatureChart from "./components/TemperatureChart"
import HistoryTable from "./components/HistoryTable"

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <SearchBar />
      <WeatherSummary />
      <TemperatureChart />
       <HistoryTable />
    </div>
  )
}

export default App