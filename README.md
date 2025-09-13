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
│ └── error_handlers.py 
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

| Method | Endpoint                  | Description                                        |
| ------ | ------------------------- | -------------------------------------------------- |
| `GET`  | `/`                       | Health check                                       |
| `GET`  | `/weather/{city}`         | Fetch real-time weather for a city   |
| `GET`  | `/weather/save/{city}`    | Fetch and save weather data into DB                |
| `GET`  | `/weather/history`        | List all saved weather records (paginated)         |
| `GET`  | `/weather/history/{city}` | List saved records for a specific city (paginated) |

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

## Disclaimer 

This project is for educational purposes only. The author is not responsible for any misuse, errors, or damages resulting from the use of this project or third-party APIs.

---