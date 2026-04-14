import sys
import json
import urllib.request
import urllib.parse

NEWS_API_KEY = "YOUR_NEWS_API_KEY"

# -----------------------------
# TOOL FUNCTIONS
# -----------------------------

def get_current_weather(city: str, unit: str = "celsius") -> str:
    """
    Gets the current temperature for a given city using Open-Meteo.
    Large or internationally well-known cities only.
    """
    # Force the model to resolve small US towns first
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
        geo_req = urllib.request.Request(
            geo_url, headers={"User-Agent": "OllamaToolDemo/1.0"}
        )

        with urllib.request.urlopen(geo_req) as response:
            geo_data = json.loads(response.read().decode("utf-8"))

        if not geo_data.get("results"):
            return f"Could not find coordinates for city: {city}."

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        country = location.get("country", "")

        temp_unit = "fahrenheit" if unit == "fahrenheit" else "celsius"

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m"
            f"&temperature_unit={temp_unit}"
        )

        weather_req = urllib.request.Request(
            weather_url, headers={"User-Agent": "OllamaToolDemo/1.0"}
        )

        with urllib.request.urlopen(weather_req) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data.get("current")
        units = data.get("current_units", {})

        return (
            f"The current weather in {city} ({country}) is "
            f"{current['temperature_2m']}{units['temperature_2m']} "
            f"with wind speeds of {current['wind_speed_10m']}{units['wind_speed_10m']}."
        )

    except Exception as e:
        return f"Error fetching weather for {city}: {e}"


def get_weather_by_coordinates(latitude: float, longitude: float) -> str:
    """Gets weather using latitude and longitude."""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            "&current=temperature_2m,wind_speed_10m"
        )

        req = urllib.request.Request(
            url, headers={"User-Agent": "OllamaToolDemo/1.0"}
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
        return f"Error fetching weather by coordinates: {e}"


def resolve_us_location(city: str, state: str) -> dict:
    """Resolves a US city/state to latitude and longitude using Nominatim."""
    try:
        query = f"{city}, {state}, USA"
        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urllib.parse.urlencode(
                {"q": query, "format": "json", "limit": 1}
            )
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "tool-caller-demo/1.0 (contact: matthew.l.allen@gmail.com)"
            },
        )

        with urllib.request.urlopen(req) as response:
            results = json.loads(response.read().decode("utf-8"))

        if not results:
            return {"error": f"Could not resolve location: {city}, {state}"}

        place = results[0]

        return {
            "city": city,
            "state": state,
            "country": "US",
            "latitude": float(place["lat"]),
            "longitude": float(place["lon"]),
        }

    except Exception as e:
        return {"error": f"Location resolution failed: {e}"}


def get_current_news(topic: str = None) -> str:
    if NEWS_API_KEY == "YOUR_NEWS_API_KEY":
        return "Error: Please set your NewsAPI key."

    try:
        if topic:
            url = (
                "https://newsapi.org/v2/everything?"
                + urllib.parse.urlencode(
                    {
                        "q": topic,
                        "sortBy": "publishedAt",
                        "pageSize": 5,
                        "apiKey": NEWS_API_KEY,
                    }
                )
            )
        else:
            url = (
                "https://newsapi.org/v2/top-headlines?"
                + urllib.parse.urlencode(
                    {
                        "language": "en",
                        "pageSize": 5,
                        "apiKey": NEWS_API_KEY,
                    }
                )
            )

        req = urllib.request.Request(
            url, headers={"User-Agent": "OllamaToolDemo/1.0"}
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        articles = data.get("articles", [])
        if not articles:
            return "No news articles found."

        lines = ["News:"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. {a.get('title')} ({a['source']['name']})")

        return "\n".join(lines)

    except Exception as e:
        return f"Error fetching news: {e}"


def get_current_time(timezone: str) -> str:
    try:
        url = (
            "https://timeapi.io/api/Time/current/zone?"
            + urllib.parse.urlencode({"timeZone": timezone})
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "OllamaToolDemo/1.0",
                "Accept": "application/json",
            },
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))

        return f"The current time in {timezone} is {data['time']} on {data['date']}."

    except Exception as e:
        return f"Error fetching time: {e}"


# -----------------------------
# TOOL REGISTRY
# -----------------------------

TOOL_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_weather_by_coordinates": get_weather_by_coordinates,
    "resolve_us_location": resolve_us_location,
    "get_current_news": get_current_news,
    "get_current_time": get_current_time,
}

available_tools = [
    {
        "type": "function",
        "function": {
            "name": "resolve_us_location",
            "description": "Resolves a US city and state to latitude and longitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City or town name, e.g. 'Harborcreek'"
                    },
                    "state": {
                        "type": "string",
                        "description": "US state abbreviation, e.g. 'PA'"
                    }
                },
                "required": ["city", "state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_by_coordinates",
            "description": "Gets current weather using latitude and longitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": { "type": "number" },
                    "longitude": { "type": "number" }
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Gets weather for large, well-known cities only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": { "type": "string" },
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

# -----------------------------
# OLLAMA CALL
# -----------------------------

def call_ollama(payload):
    url = "http://localhost:11434/api/chat"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


# -----------------------------
# MAIN AGENT LOOP
# -----------------------------

def main():
    if len(sys.argv) < 2:
        print("Please provide a prompt.")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    print("\n[Prompt]\n" + user_query + "\n")

    messages = [{"role": "user", "content": user_query}]
    payload = {
        "model": "gemma4:e2b",
        "messages": messages,
        "tools": available_tools,
        "stream": False,
    }

    MAX_STEPS = 6

    for step in range(MAX_STEPS):
        response = call_ollama(payload)
        message = response.get("message", {})

        if not message.get("tool_calls"):
            print("[Response]")
            print(message.get("content", ""))
            return

        messages.append(message)
        print("[Tool Execution]")

        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]

            print(f" └── Calling {name}({args})")

            if name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {name}"
            else:
                result = TOOL_FUNCTIONS[name](**args)

            if not args:
                result = f"Error: Tool '{name}' was called without arguments."
            else:
                result = TOOL_FUNCTIONS[name](**args)

            print(f"     └─ Result: {result}")

            messages.append(
                {
                    "role": "tool",
                    "name": name,
                    "content": json.dumps(result),
                }
            )

        payload["messages"] = messages

    print("[Error] Maximum agent steps exceeded.")


if __name__ == "__main__":
    main()
