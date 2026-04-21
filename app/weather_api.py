import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str):
    """
    Fetch weather from OpenWeather API
    Returns dict or None if failed
    """
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Celsius
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error for bad status
        
        data = response.json()
        
        # Extract only what we need
        return {
            "city": city.lower(),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None