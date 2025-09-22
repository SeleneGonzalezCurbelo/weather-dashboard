const API_URL = import.meta.env.VITE_API_BASE_URL;

export async function getWeather(city) {
  const res = await fetch(`${API_URL}/weather?city=${city}`);
  if (!res.ok) throw new Error('Error al obtener el clima');
  return res.json();
}

export async function geocode(lat, lon) {
  try {
    const res = await fetch(`${API_URL}/geocode?lat=${lat}&lon=${lon}`);
    if (!res.ok) throw new Error('Error en geocode');
    return res.json();
  } catch (err) {
    console.error('Failed to fetch geocode:', err);
    return { city: "Arrecife" }; // fallback
  }
}