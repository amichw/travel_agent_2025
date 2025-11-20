# 5c816197fd47b3d9e7bcf8afca578a81

import os
import requests

# --- CONFIGURATION ---
# Get a free key from: https://home.openweathermap.org/users/sign_up
# Export it: export OPENWEATHER_API_KEY="your_key_here"
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city: str) -> str:
    """
    Fetches current weather for a given city.
    Returns a natural language string optimized for LLM ingestion.
    """

    # 1. MOCK MODE (If no key is found, return fake data so you can test logic)
    if not WEATHER_API_KEY:
        print(f"⚠️ [Mock Tool] Returning fake weather for {city}")
        return f"Current weather in {city}: 22°C (72°F), Partially Cloudy. Wind: 15km/h."

    # 2. REAL API CALL
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)

        # Robust Error Handling (Requirement: Handle edge cases)
        if response.status_code == 404:
            return f"Could not find weather data for location: {city}."

        response.raise_for_status()
        data = response.json()

        # Parse specific fields we care about
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        # Return a clean string for the LLM to read
        return f"Current weather in {city}: {temp}°C, {condition}."

    except Exception as e:
        print(f"❌ Weather Tool Error: {e}")
        return "Weather data is currently unavailable due to a network error."


def get_attractions(city: str) -> str:
    """
    A simplified tool to get top 3 attractions.
    In a full app, this would hit Google Places API.
    For this POC, we mock it or use a simple logic.
    """
    # Hardcoded "knowledge base" for the POC to demonstrate tool selection
    # This is faster/cheaper than setting up a SerpAPI account for just one test.
    mock_db = {
        "paris": "1. Eiffel Tower\n2. Louvre Museum\n3. Montmartre",
        "tokyo": "1. Shibuya Crossing\n2. Senso-ji Temple\n3. Meiji Shrine",
        "london": "1. British Museum\n2. Tower of London\n3. London Eye",
        "new york": "1. Statue of Liberty\n2. Central Park\n3. Empire State Building"
    }

    city_key = city.lower().strip()
    if city_key in mock_db:
        return f"Top rated attractions in {city}:\n{mock_db[city_key]}"
    else:
        return f"I don't have specific real-time attraction data for {city} in my database."


# --- TOOL REGISTRY ---
# The Router will use this dictionary to find the right function
AVAILABLE_TOOLS = {
    "weather": get_weather,
    "attractions": get_attractions
}

# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    print("1. Testing Weather (Mock or Real)...")
    print(get_weather("Paris"))
    print(get_weather("Narnia"))  # Test error handling

    print("\n2. Testing Attractions...")
    print(get_attractions("Tokyo"))