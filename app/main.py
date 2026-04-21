from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import engine, get_db, Base
from app.models import Weather
from app.weather_api import fetch_weather_data

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Data Pipeline API")

# ========================================
# ENDPOINTS
# ========================================

@app.get("/")
def root():
    return {
        "message": "Weather Data Pipeline API",
        "endpoints": {
            "/fetch-weather?city=<name>": "Fetch and store weather",
            "/weather": "Get all stored data",
            "/weather?city=<name>": "Filter by city",
            "/weather/latest?city=<name>": "Latest record for city",
            "/run-pipeline?city=<name>": "Full pipeline execution"
        }
    }


@app.get("/fetch-weather")
def fetch_weather(city: str, db: Session = Depends(get_db)):
    """
    Fetch weather from API and store in DB
    """
    weather_data = fetch_weather_data(city)
    
    if not weather_data:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    # Store in database
    db_weather = Weather(**weather_data)
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    
    return {
        "status": "success",
        "data": weather_data,
        "stored_at": db_weather.timestamp
    }


@app.get("/weather")
def get_weather(city: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all weather records (optionally filter by city)
    """
    query = db.query(Weather)
    
    if city:
        query = query.filter(Weather.city == city.lower())
    
    results = query.all()
    
    return {
        "count": len(results),
        "data": results
    }


@app.get("/weather/latest")
def get_latest_weather(city: str, db: Session = Depends(get_db)):
    """
    Get latest weather record for a city
    """
    result = db.query(Weather)\
        .filter(Weather.city == city.lower())\
        .order_by(Weather.timestamp.desc())\
        .first()
    
    if not result:
        raise HTTPException(status_code=404, detail=f"No data for '{city}'")
    
    return result


@app.get("/run-pipeline")
def run_pipeline(city: str, db: Session = Depends(get_db)):
    """
    Complete pipeline: Fetch → Store → Return
    """
    # Fetch from API
    weather_data = fetch_weather_data(city)
    
    if not weather_data:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    # Store in DB
    db_weather = Weather(**weather_data)
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    
    # Return stored data
    return {
        "pipeline_status": "completed",
        "city": city,
        "data": {
            "temperature": db_weather.temperature,
            "humidity": db_weather.humidity,
            "description": db_weather.description
        },
        "stored_at": db_weather.timestamp
    }