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
- [API Endpoints](#-api-endpoints)
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

## API Endpoints

| Method | Endpoint                  | Description                                        |
| ------ | ------------------------- | -------------------------------------------------- |
| `GET`  | `/`                       | Health check                                       |
| `GET`  | `/weather/{city}`         | Fetch real-time weather for a city   |
| `GET`  | `/weather/save/{city}`    | Fetch and save weather data into DB                |
| `GET`  | `/weather/history`        | List all saved weather records (paginated)         |
| `GET`  | `/weather/history/{city}` | List saved records for a specific city (paginated) |

---

## Disclaimer 

This project is for educational purposes only. The author is not responsible for any misuse, errors, or damages resulting from the use of this project or third-party APIs.

---
