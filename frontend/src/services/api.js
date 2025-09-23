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
    console.log("Fetching geocode:", url);

    const res = await fetch(url);

    console.log("Geocode raw response:", res.status, res.statusText);

    let data = null;
    try {
      data = await res.json();
    } catch (parseErr) {
      console.error("Failed to parse geocode JSON:", parseErr);
    }

    console.log("Geocode response body:", data);

    if (!res.ok) {
      throw new Error(`Failed to fetch geocode: ${res.status} ${res.statusText}`);
    }

    return data;
  } catch (err) {
    console.error("Geocode failed:", err);
    return { city: "Arrecife" };
  }
}

export async function detectCity(lat, lon) {
  try {
    const geoRes = await fetch(`${API_URL}/weather?lat=${lat}&lon=${lon}`);
    if (!geoRes.ok) {
      throw new Error("Failed to fetch geocode");
    }
    const geoData = await geoRes.json();
    console.log("Geocode response:", geoData);

    const city = geoData.city;
    const weatherRes = await fetch(`${API_URL}/weather/${city}`);
    if (!weatherRes.ok) {
      throw new Error("Failed to fetch weather for city");
    }
    const weatherData = await weatherRes.json();

    return { city, weather: weatherData };
  } catch (err) {
    console.error("Error detecting city:", err);
    throw err;
  }
}