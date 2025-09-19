# Weather Dashboard

**Weather Dashboard** is a backend project for collecting, storing, and serving historical and real-time weather data.

It is built with **FastAPI**, uses **PostgreSQL** as database, and runs in **Docker containers** for easy deployment.  

The frontend (React) will be added in upcoming iterations. 

---

## Table of Contents
- [Features](#-features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Background Jobs (Scheduler)](#background-jobs-scheduler)
- [Frontend (React Dashboard)](#frontend-react-dashboard)
- [Disclaimer](#disclaimer)

---

## Features

✅ Fetch real-time weather data from **OpenWeatherMap API**  
✅ Save validated weather data into PostgreSQL  
✅ Query **historical weather records** (with pagination & filtering by city)  
✅ Preconfigured with **Docker + Docker Compose**  
⬜ Interactive React dashboard (upcoming)  
⬜ Data analysis & predictive models (future work)  

---

## Project Structure

### Backend

```
weather-dashboard/
├── app/
│ ├── main.py 
│ ├── models.py 
│ ├── schemas.py 
│ ├── crud.py
│ ├── db.py 
│ ├── weather_client.py 
│ ├── exceptions.py 
│ |── error_handlers.py 
| ├── routers
│ │ └── weather.py
| ├── services
│ │ └── openweather_adapter.py
│ │ └── openweather.py
│ │ └── weather_service.py
├── db/
│ └── init.sql 
├── tests/
│ ├── test_crud.py
│ ├── test_validation.py
│ ├── test_weather_client.py
│ ├── test_main.py
│ └── conftest.py
├── Dockerfile 
├── docker-compose.yml 
├── requirements.txt
├── .env.example
└── README.md
```

### Frontend

```
frontend/
├── public/
├── src/
│ ├── components/
│ │ ├── Header.jsx
│ │ ├── HistoryTable.jsx
│ │ ├── SearchBar.jsx
│ │ ├── WeatherSummary.jsx
│ │ |── TemperatureChart.jsx
│ │ └── TemperatureHistory.jsx
│ ├── App.jsx
│ ├── index.css
│ └── index.js
├── package.json
└── README.md
```

---

## Requirements

- **Python 3.11+** (only if running locally without Docker)  
- **Docker & Docker Compose**  
- External weather API: **OpenWeatherMap** (requires API key)  

Install backend dependencies locally (optional):  

```bash
pip install -r backend/requirements.txt
```

---

## Getting Started

### Backend 

1. Clone the repository:

```
git clone https://github.com/SeleneGonzalezCurbelo/weather-dashboard.git
cd weather-dashboard
```

2. Set up environment variables and fill in your credentials:

```
cp .env.example .env
```
Fill in required values (e.g. OPENWEATHER_API_KEY, DB credentials).

3. Start the containers:

```
docker-compose up --build
```

4. Access the backend FastAPI:
- [API Docs](http://localhost:8000/docs)
- [Health check](http://localhost:8000/)

### Frontend

1. Go into the frontend folder:

```bash
cd frontend
npm install
npm start
```

The app will run on http://localhost:5173/.

---

## Running Tests

The backend includes unit tests for CRUD operations, data validation, and the weather API client.

**Run all tests:**

```
pytest
```

**Notes:**
- Tests use an in-memory SQLite database and do not affect the real PostgreSQL database.
- Some tests mock external API calls to provide deterministic results.
- Make sure dependencies are installed (pip install -r requirements.txt) before running tests.
- The tests cover:
    - test_crud.py → database operations
    - test_validation.py → weather data validation logic
    - test_weather_client.py → API client for fetching weather
    - test_main.py → FastAPI endpoints (requires local DB or mocks)

---

## API Endpoints

| Method | Endpoint                        | Description                                            |
| ------ | ------------------------------- | ------------------------------------------------------ |
| `GET`  | `/`                             | Health check — backend running                         |
| `GET`  | `/weather/{city}`               | Fetch current weather from external API                |
| `POST` | `/weather/save/{city}`          | Fetch current weather and save to DB                   |
| `GET`  | `/weather/history`              | List all saved weather records (paginated)             |
| `GET`  | `/weather/history/{city}`       | List saved records for a specific city (paginated)     |
| `GET`  | `/weather/daily-summary/{city}` | Compute daily summary (min/max/avg) metrics for a city |
| `GET`  | `/weather/latest/{city}`        | Retrieve most recent weather record for a city         |

---

## Background Jobs (Scheduler)

Weather Dashboard automatically collects weather data periodically using **APScheduler**, integrated inside the FastAPI app.

- The scheduler runs when the backend starts.
- It fetches and stores weather data for multiple cities every hour.

If you want to customize the interval or the list of tracked cities, update the configuration in:
```
app/scheduler.py
```

---

## Frontend (React Dashboard)

The frontend is a React app that displays real-time and historical weather data from the backend.

### Features

- Search for a city and display current weather summary  
- View temperature history as a chart or table (hourly and daily breakdown)  
- Chart shows temperature with min/max markers and detailed tooltip including:
  - Humidity
  - Wind speed and cardinal direction
  - Weather icon
- Switch between chart and table tabs  
- 5-day forecast available even if historical DB data is missing
- Automatic user geolocation 
- Future: predictive models and weather alerts 

---

## Disclaimer 

This project is for educational purposes only. The author is not responsible for any misuse, errors, or damages resulting from the use of this project or third-party APIs.

---