import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

print("=" * 50)
print("TESTING API KEY")
print("=" * 50)
print(f"API Key loaded: {API_KEY}")
print(f"Key length: {len(API_KEY) if API_KEY else 0}")
print()

if not API_KEY or API_KEY == "placeholder":
    print("❌ ERROR: API key not set properly in .env file")
    print("\nFix:")
    print("1. Open .env file")
    print("2. Add: WEATHER_API_KEY=your_actual_key")
    print("3. Save and run this again")
    exit()

# Test API call
city = "london"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

print(f"Testing API call for: {city}")
print(f"URL: {url[:80]}...")
print()

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! API Key is working!")
        print(f"\nWeather in {city}:")
        print(f"  Temperature: {data['main']['temp']}°C")
        print(f"  Humidity: {data['main']['humidity']}%")
        print(f"  Description: {data['weather'][0]['description']}")
    
    elif response.status_code == 401:
        print("\n❌ ERROR: Invalid API Key")
        print("\nPossible fixes:")
        print("1. Check your API key at: https://home.openweathermap.org/api_keys")
        print("2. Copy the FULL key (usually 32 characters)")
        print("3. Paste in .env file: WEATHER_API_KEY=your_key")
        print("4. If key is NEW, wait 10-15 minutes for activation")
    
    elif response.status_code == 404:
        print(f"\n❌ City '{city}' not found")
        print("(But this means API key IS working!)")
    
    else:
        print(f"\n❌ Unexpected error: {response.text}")

except Exception as e:
    print(f"\n❌ Connection error: {e}")

print("\n" + "=" * 50)