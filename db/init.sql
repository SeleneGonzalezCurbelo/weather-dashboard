CREATE DATABASE weather_db;

\c weather_db;

CREATE TABLE weather_data (
    id UUID PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    feels_like FLOAT,
    humidity FLOAT NOT NULL,
    pressure FLOAT,
    wind_speed FLOAT,
    wind_deg FLOAT,
    cloudiness FLOAT,
    description VARCHAR(255),
    icon VARCHAR(10),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);