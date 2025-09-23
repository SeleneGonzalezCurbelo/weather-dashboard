const API_URL = import.meta.env.VITE_API_BASE_URL;

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