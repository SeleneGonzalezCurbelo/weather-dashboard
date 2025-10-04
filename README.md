# Weather Dashboard

**Weather Dashboard** is a full-stack application for collecting, storing, and visualizing real-time and historical weather data.

Built with FastAPI, PostgreSQL, and Docker on the backend, and a modern React + Vite frontend. It integrates with the OpenWeatherMap API and supports automated data collection via background jobs.

---

## Table of Contents
- [Features](#-features)
  - [Planned Features](#planned-features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Background Jobs (Scheduler)](#background-jobs-scheduler)
- [Frontend (React Dashboard)](#frontend-react-dashboard)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

---

## Features

- 🔄 Fetch current weather from OpenWeatherMap API
- 🗃️ Store validated weather data in PostgreSQL
- 📈 Query historical records with pagination and filtering
- 📊 Daily summaries (min/max/avg) instead of hourly breakdowns
- 🕒 Automated hourly data collection via scheduler
- 🌍 Geolocation-based city detection
- 🧪 Unit tests with SQLite + API mocks
- 🐳 Dockerized for easy deploymen

### Planned Features

- 📉 Data analysis and predictive weather modeling
- 🔔 Smart weather alerts and anomaly detection
- 📅 Flexible time aggregation (weekly, monthly trends)

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
| ├── services/
│ │ └── api.js
| ├── utils/
│ │ ├── data.js
│ │ |── icons.js
│ │ └── weatherHelpers.js
│ ├── App.jsx
│ ├── main.jsx
│ ├── index.css
│ ├── App.css
│ └── index.js
├── package.json
└── README.md
```

---

## Requirements

- **Python 3.11+** 
- **Node.js 18+**
- **Docker & Docker Compose**  
- External weather API: **OpenWeatherMap** (required in .env)

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

2. Configure environment variables

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
| `GET`  | `/weather/reverse-geocode`      | Detect city from coordinates                           |

---

## Background Jobs (Scheduler)

- Uses APScheduler to fetch weather hourly
- Configurable tracked cities and intervals
- Defined in app/scheduler.py

---

## Frontend (React Dashboard)

- 🌐 Search cities and view current weather
- 📊 Temperature history chart with tooltips
- 📋 Table view with hourly breakdown
- 🧭 Wind direction, humidity, pressure, visibility
- 📍 Auto-detect location via geolocation
- 🔮 Forecast fallback if DB data is missing

### City Search + Current Weather

<p align="center">
  <img src="docs/images/search-weather.png" alt="Search and current weather view" width="700"/>
</p>

### Temperature History Chart

<p align="center">
  <img src="docs/images/temperature-chart.png" alt="Temperature history chart" width="700"/>
</p>

### Weather History Table

<p align="center">
  <img src="docs/images/weather-table.png" alt="Weather history table" width="700"/>
</p>

---

## Contributing

We welcome contributions! Please follow these guidelines:
- Use clear commit messages (feat:, fix:, refactor:)
- Write unit tests for new features
- Follow PEP 8 (Python) and ESLint/Prettier (JS)
- Use async/await for I/O operations
- Submit PRs with a clear description and related issue reference

---

## Disclaimer 

This project is for educational purposes only. The author is not responsible for misuse, errors, or third-party API limitations.

---