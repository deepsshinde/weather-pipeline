import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str):
    """
    Fetch weather - BYPASSES ALL PROXIES
    """
    if not API_KEY:
        print("No API key found")
        return None
    
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        
        # 🔥 FORCE BYPASS PROXY
        session = requests.Session()
        session.trust_env = False  # Ignores HTTP_PROXY env vars
        session.proxies = {}        # Clears any proxy settings
        
        print(f"Fetching weather for {city} (bypassing proxy)...")
        
        response = session.get(
            BASE_URL, 
            params=params,
            timeout=15,
            proxies={"http": None, "https": None}  # Extra safety
        )
        
        print(f"Status: {response.status_code}")
        
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "city": city.lower(),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None