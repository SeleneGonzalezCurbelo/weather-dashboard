// src/utils/location.js
export function getUserLocation() {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve(null); 
    } else {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          });
        },
        () => {
          resolve(null); 
        }
      );
    }
  });
}

export async function getCityFromCoords(lat, lon, apiKey) {
  try {
    const res = await fetch(
      `http://api.openweathermap.org/geo/1.0/reverse?lat=${lat}&lon=${lon}&limit=1&appid=${apiKey}`
    );
    const data = await res.json();
    return data[0]?.name || null;
  } catch (err) {
    console.error("Reverse geocoding failed:", err);
    return null;
  }
}