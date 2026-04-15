import time
import urllib.request
import urllib.parse
import json

from cache.location_cache import load_cache, save_cache

_LOCATION_CACHE = load_cache()

def resolve_us_location(city: str, state: str) -> dict:
    key = f"{city.lower()},{state.upper()}"

    if key in _LOCATION_CACHE:
        return {**_LOCATION_CACHE[key], "cached": True}

    time.sleep(1)

    query = f"{city}, {state}, USA"
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "limit": 1
    })

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "tool-caller-demo/1.0 "
                "(https://github.com/mla133/tool-caller)"
            )
        }
    )

    with urllib.request.urlopen(req) as response:
        results = json.loads(response.read().decode("utf-8"))

    if not results:
        return {"error": f"Could not resolve {city}, {state}"}

    place = results[0]
    resolved = {
        "city": city,
        "state": state,
        "country": "US",
        "latitude": float(place["lat"]),
        "longitude": float(place["lon"])
    }

    _LOCATION_CACHE[key] = resolved
    save_cache(_LOCATION_CACHE)

    return resolved
