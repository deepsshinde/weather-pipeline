# 🌦️ Weather Data Pipeline API

A mini data engineering system that fetches, stores, and serves weather data.

## Features

- Fetch weather from OpenWeather API
- Store historical data in SQLite
- Query weather by city
- Get latest weather records
- Full pipeline execution

## Setup

1. Clone repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install: `pip install -r requirements.txt`
5. Create `.env` file with: `WEATHER_API_KEY=your_key`
6. Run: `uvicorn app.main:app --reload`

## Endpoints

- `GET /fetch-weather?city=<name>` - Fetch and store
- `GET /weather` - All records
- `GET /weather?city=<name>` - Filter by city
- `GET /weather/latest?city=<name>` - Latest record
- `GET /run-pipeline?city=<name>` - Full pipeline

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- OpenWeather API

## 🌐 Live Deployment

**API is live at:** https://weather-pipeline-xxxx.onrender.com

### Try it now:

- **Root:** https://weather-pipeline-c6lk.onrender.com/docs
- **Fetch Weather:** https://weather-pipeline-xxxx.onrender.com/fetch-weather?city=mumbai
- **View Data:** https://weather-pipeline-xxxx.onrender.com/weather

⚠️ **Note:** Free tier may take 30-60 seconds to wake up if inactive.