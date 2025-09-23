const API_URL = import.meta.env.VITE_API_BASE_URL;

export async function getWeather(city) {
  const res = await fetch(`${API_URL}/weather/${city}`); 
  if (!res.ok) throw new Error("Failed to fetch weather");
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
  try {
    const url = `${API_URL}/weather/geocode?lat=${lat}&lon=${lon}`;
    console.log("[geocode] Fetching:", url);

    const res = await fetch(url);
    console.log("[geocode] Raw response:", res.status, res.statusText);

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed geocode: ${res.status} ${text}`);
    }

    const data = await res.json();
    console.log("[geocode] Parsed JSON:", data);

    return data;
  } catch (err) {
    console.error("[geocode] Error:", err);
    return { city: "Arrecife" }; 
  }
}

export async function detectCity(lat, lon) {
  try {
    console.log("[detectCity] Detecting city for coords:", lat, lon);
    const geoData = await geocode(lat, lon);

    const city = geoData.city;
    console.log("[detectCity] Got city:", city);

    const res = await fetch(`${API_URL}/weather/${city}`);
    console.log("[detectCity] Weather response status:", res.status);

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed weather fetch for ${city}: ${res.status} ${text}`);
    }

    const weatherData = await res.json();
    console.log("[detectCity] Weather data:", weatherData);

    return { city, weather: weatherData };
  } catch (err) {
    console.error("[detectCity] Error:", err);
    return { city: "Arrecife", weather: null };
  }
}
