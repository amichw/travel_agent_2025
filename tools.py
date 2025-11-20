# tools.py
import os
import requests

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> dict:
    if not WEATHER_API_KEY:
        return {"status": "mock", "city": city,
                "temp": 22, "description": "partly cloudy"}

    try:
        res = requests.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
        ).json()

        return {
            "status": "ok",
            "city": city,
            "temp": res["main"]["temp"],
            "description": res["weather"][0]["description"]
        }
    except:
        return {"status": "error", "city": city}

def get_attractions(city: str) -> dict:
    mock = {
        "paris": ["Eiffel Tower", "Louvre Museum", "Montmartre"],
        "tokyo": ["Shibuya Crossing", "Senso-ji Temple", "Meiji Shrine"],
        "rome": ["Colosseum", "Trevi Fountain", "Vatican Museums"],
        "london": [" British Museum", "Tower of London","London Eye"],
        "new york": ["Statue of Liberty", "Central Park", "Empire State Building"]
    }
    return {"city": city, "items": mock.get(city.lower(), [])}


def get_knowledge_base_context(topic: str) -> str:
    """
    Simulates a vector database search. The output text is crafted by the LLM
    to ensure the RAG context is natural and concise.
    """
    topic_lower = topic.lower()

    if "visa" in topic_lower or "passport" in topic_lower:
        # LLM-Crafted Response
        return "Static Knowledge for Visas: As of 2025, British citizens require a minimum of six months validity remaining on their passport for entry into the Schengen area, but short-term tourism (under 90 days) does not require a visa."
    elif "currency" in topic_lower or "money" in topic_lower:
        # LLM-Crafted Response
        return "Static Knowledge for Currency: While most large cities accept credit cards, local vendors and public transport in less touristy areas often require local currency. It is advised to use ATMs at major bank branches for better exchange rates."
    else:
        # Node G -> No KB Chunks Retrieved
        return f"[KB_FAILURE] No relevant static knowledge found for topic: {topic}. Try rephrasing with a more specific location or document type."


def web_search_tool(query: str) -> str:
    """
    Conceptual tool: Orchestrator will execute a live Google Search
    (using the google_search capability) and inject the summarized result.
    This function simply defines the required input/output for the Router.
    """
    # The Orchestrator calls the search, summarizes the result, and returns
    # a clean string like: "Live Search Results: The price of oil is $92 per barrel..."
    return f"[WEB_SEARCH_ACTIVE] Please instruct the LLM to summarize the top 3 search results for: '{query}'"

# --- TOOL REGISTRY ---
# The Router will use this dictionary to find the right function

AVAILABLE_TOOLS = {
    "weather": get_weather,
    "attractions": get_attractions,
    "kb_search": get_knowledge_base_context,
    "web_search": web_search_tool,
}

# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    print("1. Testing Weather (Mock or Real)...")
    print(get_weather("Paris"))
    print(get_weather("Narnia"))  # Test error handling

    print("\n2. Testing Attractions...")
    print(get_attractions("Tokyo"))