export default function WeatherSummary() {
  return (
    <div className="p-4 bg-gray-100">
      <h2 className="font-bold mb-2">📊 Resumen (última ciudad consultada)</h2>
      <div className="space-y-1">
        <div>Ciudad: Valencia</div>
        <div>Temperatura: 23°C</div>
        <div>Humedad: 65%</div>
        <div>Viento: 12 km/h</div>
      </div>
    </div>
  )
}