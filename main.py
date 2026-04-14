import sys
import os
import json
import time
import urllib.request
import urllib.parse

from dotenv import load_dotenv

# -------------------------------------------------
# ENVIRONMENT SETUP
# -------------------------------------------------

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# -------------------------------------------------
# LOCATION CACHE (persistent)
# -------------------------------------------------

CACHE_FILE = "location_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        LOCATION_CACHE = json.load(f)
else:
    LOCATION_CACHE = {}


def save_location_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(LOCATION_CACHE, f, indent=2)


# -------------------------------------------------
# TOOL FUNCTIONS
# -------------------------------------------------

def resolve_us_location(city: str, state: str) -> dict:
    """
    Resolves a US city and state into latitude and longitude.
    Uses OpenStreetMap Nominatim with caching.
    """

    cache_key = f"{city.strip().lower()},{state.strip().upper()}"

    # Cache hit
    if cache_key in LOCATION_CACHE:
        return {
            **LOCATION_CACHE[cache_key],
            "cached": True
        }

    try:
        # Be polite to Nominatim
        time.sleep(1)

        query = f"{city}, {state}, USA"
        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urllib.parse.urlencode({
                "q": query,
                "format": "json",
                "limit": 1
            })
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "tool-caller-demo/1.0 "
                    "(https://github.com/yourusername/tool-caller)"
                )
            }
        )

        with urllib.request.urlopen(req) as response:
            results = json.loads(response.read().decode("utf-8"))

        if not results:
            return {"error": f"Could not resolve location: {city}, {state}"}

        place = results[0]

        resolved = {
            "city": city,
            "state": state,
            "country": "US",
            "latitude": float(place["lat"]),
            "longitude": float(place["lon"])
        }

        LOCATION_CACHE[cache_key] = resolved
        save_location_cache()

        return {
            **resolved,
            "cached": False
        }

    except Exception as e:
        return {"error": f"Location resolution failed: {e}"}


def get_weather_by_coordinates(latitude: float, longitude: float) -> str:
    """Gets current weather using latitude and longitude."""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            "&current=temperature_2m,wind_speed_10m"
        )

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "tool-caller-demo/1.0"}
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data["current"]
        units = data["current_units"]

        return (
            f"The current temperature is "
            f"{current['temperature_2m']}{units['temperature_2m']} "
            f"with wind speeds of "
            f"{current['wind_speed_10m']}{units['wind_speed_10m']}."
        )

    except Exception as e:
        return f"Error fetching weather: {e}"


def get_current_weather(city: str, unit: str = "celsius") -> str:
    """
    Weather for large, well-known cities only.
    Small US towns should be resolved to coordinates first.
    """
    if "," in city:
        return (
            "Ambiguous or state-qualified location detected. "
            "Please resolve the location to coordinates first."
        )

    try:
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urllib.parse.urlencode({"name": city, "count": 1})
        )

        with urllib.request.urlopen(geo_url) as response:
            geo = json.loads(response.read().decode("utf-8"))

        if not geo.get("results"):
            return f"Could not locate city: {city}"

        loc = geo["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        country = loc.get("country", "")

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m"
            f"&temperature_unit={unit}"
        )

        with urllib.request.urlopen(weather_url) as response:
            data = json.loads(response.read().decode("utf-8"))

        c = data["current"]
        u = data["current_units"]

        return (
            f"The current weather in {city} ({country}) is "
            f"{c['temperature_2m']}{u['temperature_2m']} "
            f"with wind speeds of {c['wind_speed_10m']}{u['wind_speed_10m']}."
        )

    except Exception as e:
        return f"Error fetching weather for {city}: {e}"


def get_current_news(topic: str = None) -> str:
    if not NEWS_API_KEY:
        return (
            "NEWS_API_KEY is not configured. "
            "Set it in a .env file."
        )

    try:
        if topic:
            url = (
                "https://newsapi.org/v2/everything?"
                + urllib.parse.urlencode({
                    "q": topic,
                    "pageSize": 5,
                    "sortBy": "publishedAt",
                    "apiKey": NEWS_API_KEY
                })
            )
        else:
            url = (
                "https://newsapi.org/v2/top-headlines?"
                + urllib.parse.urlencode({
                    "language": "en",
                    "pageSize": 5,
                    "apiKey": NEWS_API_KEY
                })
            )

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))

        articles = data.get("articles", [])
        if not articles:
            return "No news found."

        lines = ["News:"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. {a['title']} ({a['source']['name']})")

        return "\n".join(lines)

    except Exception as e:
        return f"Error fetching news: {e}"


def get_current_time(timezone: str) -> str:
    try:
        url = (
            "https://timeapi.io/api/Time/current/zone?"
            + urllib.parse.urlencode({"timeZone": timezone})
        )

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))

        return (
            f"The current time in {timezone} is "
            f"{data['time']} on {data['date']}."
        )

    except Exception as e:
        return f"Error fetching time: {e}"


# -------------------------------------------------
# TOOL REGISTRY
# -------------------------------------------------

TOOL_FUNCTIONS = {
    "resolve_us_location": resolve_us_location,
    "get_weather_by_coordinates": get_weather_by_coordinates,
    "get_current_weather": get_current_weather,
    "get_current_news": get_current_news,
    "get_current_time": get_current_time,
}

available_tools = [
    {
        "type": "function",
        "function": {
            "name": "resolve_us_location",
            "description": "Resolve a US city and state to latitude and longitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "state": {"type": "string"}
                },
                "required": ["city", "state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_by_coordinates",
            "description": "Get weather using latitude and longitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Weather for large, well-known cities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# -------------------------------------------------
# OLLAMA CALL
# -------------------------------------------------

def call_ollama(payload):
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


# -------------------------------------------------
# MAIN AGENT LOOP
# -------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Please provide a prompt.")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print("\n[Prompt]")
    print(prompt)

    messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": "gemma4:e2b",
        "messages": messages,
        "tools": available_tools,
        "stream": False
    }

    MAX_STEPS = 6

    for _ in range(MAX_STEPS):
        response = call_ollama(payload)
        message = response.get("message", {})

        if not message.get("tool_calls"):
            print("\n[Response]")
            print(message.get("content", ""))
            return

        messages.append(message)
        print("\n[Tool Execution]")

        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]

            print(f" └── Calling {name}({args})")

            if not args:
                result = f"Error: tool '{name}' called without arguments."
            else:
                result = TOOL_FUNCTIONS[name](**args)

            print(f"     └─ Result: {result}")

            messages.append({
                "role": "tool",
                "name": name,
                "content": json.dumps(result)
            })

        payload["messages"] = messages

    print("\n[Error] Agent exceeded maximum steps.")


if __name__ == "__main__":
    main()
