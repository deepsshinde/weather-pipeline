from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.database import engine, get_db, Base
from app.models import Weather
from app.weather_api import fetch_weather_data


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Data Pipeline API")

# ========================================
# ENDPOINTS
# ========================================
@app.get("/health")
def health_check():
    """
    Health check endpoint for deployment platforms
    """
    return {"status": "healthy", "service": "Weather Pipeline API"}
@app.get("/")
def root():
    return {
        "message": "Weather Data Pipeline API",
        "endpoints": {
            "/fetch-weather?city=<name>": "Fetch and store weather",
            "/weather": "Get all stored data",
            "/weather?city=<name>": "Filter by city",
            "/weather/latest?city=<name>": "Latest record for city",
            "/weather/unique": "Latest record per city (no duplicates)",
            "/weather/duplicates/count": "Count duplicate records",
            "/cleanup-duplicates": "Delete duplicates (POST)",
            "/run-pipeline?city=<name>": "Full pipeline execution"
        }
    }


@app.get("/fetch-weather")
def fetch_weather(city: str, db: Session = Depends(get_db)):
    """
    Fetch weather from API and store in DB
    Returns cached data if fetched recently (within 10 min)
    """
    city_lower = city.lower()
    
    # Check if we have recent data (within last 10 minutes)
    ten_min_ago = datetime.utcnow() - timedelta(minutes=10)
    
    recent_record = db.query(Weather)\
        .filter(Weather.city == city_lower)\
        .filter(Weather.timestamp > ten_min_ago)\
        .order_by(Weather.timestamp.desc())\
        .first()
    
    # If recent data exists, return it (don't fetch again)
    if recent_record:
        return {
            "status": "cached",
            "message": f"Using recent data (fetched {int((datetime.utcnow() - recent_record.timestamp).seconds / 60)} min ago)",
            "data": {
                "city": recent_record.city,
                "temperature": recent_record.temperature,
                "feels_like": recent_record.feels_like,
                "humidity": recent_record.humidity,
                "description": recent_record.description
            },
            "stored_at": recent_record.timestamp
        }
    
    # Fetch fresh data from API
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
        "message": f"Fresh weather data fetched and stored",
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

@app.post("/cleanup-duplicates")
def cleanup_duplicates(db: Session = Depends(get_db)):
    """
    Keep only the latest record for each city
    Delete all older duplicates
    """
    # Get all unique cities
    cities = db.query(Weather.city).distinct().all()
    cities = [city[0] for city in cities]
    
    deleted_count = 0
    
    for city in cities:
        # Get all records for this city, ordered by timestamp (newest first)
        records = db.query(Weather)\
            .filter(Weather.city == city)\
            .order_by(Weather.timestamp.desc())\
            .all()
        
        # Keep the first (latest), delete the rest
        if len(records) > 1:
            for record in records[1:]:  # Skip first, delete rest
                db.delete(record)
                deleted_count += 1
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Deleted {deleted_count} duplicate records",
        "cities_cleaned": len(cities)
    }
@app.get("/weather/unique")
def get_unique_weather(db: Session = Depends(get_db)):
    """
    Get only the latest record for each city
    """
    # Get all unique cities
    cities = db.query(Weather.city).distinct().all()
    cities = [city[0] for city in cities]
    
    results = []
    
    for city in cities:
        # Get latest record for each city
        latest = db.query(Weather)\
            .filter(Weather.city == city)\
            .order_by(Weather.timestamp.desc())\
            .first()
        
        if latest:
            results.append(latest)
    
    return {
        "count": len(results),
        "data": results
    }
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