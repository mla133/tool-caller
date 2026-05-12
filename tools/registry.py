from tools.location import resolve_location

# ---- Tool Schemas ----
RESOLVE_LOCATION_SCHEMA = {
    "name": "resolve_location",
    "description": "Resolve a location string into structured location data",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Location name, city, or address"
            }
        },
        "required": ["query"]
    }
}

# ---- Unified registry ----
TOOLS = {
    "resolve_location": {
        "fn": resolve_location,
        "schema": RESOLVE_LOCATION_SCHEMA
    }
}

# ---- Standard exports ----
TOOL_SCHEMAS = [tool["schema"] for tool in TOOLS.values()]
TOOL_FUNCTIONS = {name: tool["fn"] for name, tool in TOOLS.items()}


# --------------------------
# Safety validation (runs at import time)

for name, tool in TOOLS.items():
    schema_name = tool["schema"]["name"]
    if name != schema_name:
        raise ValueError(f"Tool mismatch: key='{name}' but schema name='{schema_name}'")

##  from tools.location import resolve_location
##  from tools.weather import get_weather_by_coordinates
##  from tools.distance import calculate_distance
##  from tools.news import get_current_news
##  from tools.time import get_current_time
##  
##  TOOL_FUNCTIONS = {
##      "resolve_location": resolve_location,
##      "get_weather_by_coordinates": get_weather_by_coordinates,
##      "calculate_distance": calculate_distance,
##      "get_current_news": get_current_news,
##      "get_current_time": get_current_time,
##  }



#TOOL_SCHEMAS= [
#    {
#        "type": "function",
#        "function": {
#            "name": "resolve_location",
#            "terminal": False,
#            "description": "Resolve a US city and state to latitude and longitude.",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "city": {"type": "string"},
#                    "state": {"type": "string"}
#                },
#                "required": ["city", "state"]
#            }
#        }
#    },
#    {
#        "type": "function",
#        "function": {
#            "name": "get_weather_by_coordinates",
#            "terminal": True,
#            "description": "Get weather using latitude and longitude.",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "latitude": {"type": "number"},
#                    "longitude": {"type": "number"}
#                },
#                "required": ["latitude", "longitude"]
#            }
#        }
#    },
#     {
#        "type": "function",
#        "function": {
#            "name": "get_current_news",
#            "terminal": True,
#            "description": "Fetches news articles based on a topic or keyword.",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "topic": {
#                        "type": "string",
#                        "description": "The topic or keyword to search news for."
#                    },
#                },
#                "required": []
#            }
#        }
#    },
#
#    {
#        "type": "function",
#        "function": {
#            "name": "calculate_distance",
#            "terminal": True,
#            "description": "Calculate distance between two coordinates.",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "lat1": {"type": "number"},
#                    "lon1": {"type": "number"},
#                    "lat2": {"type": "number"},
#                    "lon2": {"type": "number"},
#                    "unit": {
#                        "type": "string",
#                        "enum": ["miles", "kilometers"]
#                    }
#                },
#                "required": ["lat1", "lon1", "lat2", "lon2"]
#            }
#        }
#    },
#    {
#        "type": "function",
#        "function": {
#            "name": "get_forecast_by_coordinates",
#            "terminal": True,
#            "description": "Get future weather information such as tomorrow's or upcoming precipitation chances.",
#            "parameters": {
#                "type": "object",
#                "properties": {
#                    "latitude": { "type": "number" },
#                    "longitude": { "type": "number" },
#                    "days": { "type": "integer", "default": 3 }
#                },
#            "required": ["latitude", "longitude"]
#          }
#        }
#    },
#]
