# tools/schemas.py

from tools.location import resolve_location
from tools.weather import get_weather_by_coordinates

TOOL_SCHEMAS = [
    {
        "name": "resolve_location",
        "description": "Resolve a city name into latitude and longitude.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "state": {"type": "string"},
            },
            "required": ["city"],
        },
        "callable": resolve_location,
    },
    {
        "name": "get_weather_by_coordinates",
        "description": "Get the weather for a location using latitude and longitude.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
            "required": ["latitude", "longitude"],
        },
        "callable": get_weather_by_coordinates,
    },
]
