// src/utils/weatherHelpers.js
export function flattenByDayAndHour(history) {
  if (!Array.isArray(history)) return [];

  return history
    .map(record => {
      const dateObj = new Date(record.created_at);
      if (isNaN(dateObj)) return null;

      return {
        ...record,
        day: dateObj.toLocaleDateString("es-ES"), 
        hour: dateObj.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }),
      };
    })
    .filter(Boolean)
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
}

export function windDegToDir(deg) {
  if (deg == null) return "–";
  const directions = ["N","NE","E","SE","S","SW","W","NW"];
  const index = Math.round(deg / 45) % 8;
  return directions[index];
}