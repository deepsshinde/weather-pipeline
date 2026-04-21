import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

print("=" * 60)
print("TESTING API WITH PROXY BYPASS")
print("=" * 60)

if not API_KEY:
    print("❌ No API key in .env file!")
    exit()

print(f"✅ API Key loaded (length: {len(API_KEY)})")

# Test connection
city = "mumbai"
url = "http://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

print(f"\nTesting connection to OpenWeather API...")
print(f"City: {city}")

try:
    # Create session that ignores proxy
    session = requests.Session()
    session.trust_env = False
    session.proxies = {}
    
    print("\n⏳ Sending request (bypassing proxy)...")
    
    response = session.get(
        url,
        params=params,
        timeout=15,
        proxies={"http": None, "https": None}
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Weather data received:")
        print(f"   Temperature: {data['main']['temp']}°C")
        print(f"   Feels like: {data['main']['feels_like']}°C")
        print(f"   Humidity: {data['main']['humidity']}%")
        print(f"   Description: {data['weather'][0]['description']}")
        print("\n🎉 Your API is working! Now restart the FastAPI server.")
    
    elif response.status_code == 401:
        print("\n❌ Invalid API Key")
        print("Go to: https://home.openweathermap.org/api_keys")
        print("Copy your key and update .env file")
    
    else:
        print(f"\n❌ Error: {response.text}")

except requests.exceptions.ProxyError:
    print("\n❌ STILL GETTING PROXY ERROR")
    print("\nThis means:")
    print("1. Hotspot might not be active")
    print("2. Laptop is still on office WiFi")
    print("3. Need to use mock data instead")
    
except requests.exceptions.SSLError:
    print("\n❌ SSL Certificate Error")
    print("Office firewall is intercepting HTTPS")
    print("Solution: Use mock data (see below)")

except requests.exceptions.ConnectionError as e:
    print(f"\n❌ Connection Error: {e}")
    print("\nChecklist:")
    print("✓ Mobile hotspot is ON?")
    print("✓ Laptop connected to hotspot (not office WiFi)?")
    print("✓ Hotspot has internet?")

except Exception as e:
    print(f"\n❌ Unexpected Error: {type(e).__name__}")
    print(f"   {e}")

print("\n" + "=" * 60)