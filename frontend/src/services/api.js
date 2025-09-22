const API_URL = import.meta.env.VITE_API_BASE_URL;

export async function getWeather(city) {
  const res = await fetch(`${API_URL}/weather/${city}`);
  if (!res.ok) throw new Error("Failed to fetch current weather");
  return res.json();
}

export async function getLatest(city) {
  const res = await fetch(`${API_URL}/weather/latest/${city}`);
  if (!res.ok) throw new Error("Failed to fetch latest weather");
  return res.json();
}

export async function getHistory(city = null, limit = 50, offset = 0) {
  const url = city
    ? `${API_URL}/weather/history/${city}?limit=${limit}&offset=${offset}`
    : `${API_URL}/weather/history?limit=${limit}&offset=${offset}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch weather history");
  return res.json();
}

export async function getDailySummary(city) {
  const res = await fetch(`${API_URL}/weather/daily-summary/${city}`);
  if (!res.ok) throw new Error("Failed to fetch daily summary");
  return res.json();
}

export async function getForecast(city) {
  const res = await fetch(`${API_URL}/weather/forecast/${city}`);
  if (!res.ok) throw new Error("Failed to fetch forecast");
  return res.json();
}

export async function geocode(lat, lon) {
  const res = await fetch(`${API_URL}/weather/geocode?lat=${lat}&lon=${lon}`);
  if (!res.ok) {
    const text = await res.text(); 
    console.error("Geocode failed, response:", text);
    throw new Error("Failed to fetch geocode");
  }
  return res.json();
}