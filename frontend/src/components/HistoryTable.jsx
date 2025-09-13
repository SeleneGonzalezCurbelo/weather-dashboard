export default function HistoryTable() {
  return (
    <div className="p-4 bg-gray-100 mt-4">
      <h2 className="font-bold mb-2">📋 Historial de consultas</h2>
      <table className="min-w-full border border-gray-300">
        <thead className="bg-gray-200">
          <tr>
            <th className="border px-2">Fecha</th>
            <th className="border px-2">Ciudad</th>
            <th className="border px-2">Temp</th>
            <th className="border px-2">Humedad</th>
            <th className="border px-2">Viento</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-2">2025-09-12</td>
            <td className="border px-2">Madrid</td>
            <td className="border px-2">28°C</td>
            <td className="border px-2">55%</td>
            <td className="border px-2">10 km/h</td>
          </tr>
          <tr>
            <td className="border px-2">2025-09-12</td>
            <td className="border px-2">Valencia</td>
            <td className="border px-2">23°C</td>
            <td className="border px-2">65%</td>
            <td className="border px-2">12 km/h</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}