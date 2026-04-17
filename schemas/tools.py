AVAILABLE_TOOLS = [
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
            "name": "get_current_news",
            "description": "Fetches news articles based on a topic or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic or keyword to search news for."
                    },
                },
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_distance",
            "description": "Calculate distance between two coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat1": {"type": "number"},
                    "lon1": {"type": "number"},
                    "lat2": {"type": "number"},
                    "lon2": {"type": "number"},
                    "unit": {
                        "type": "string",
                        "enum": ["miles", "kilometers"]
                    }
                },
                "required": ["lat1", "lon1", "lat2", "lon2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast_by_coordinates",
            "description": "Get future weather information such as tomorrow's or upcoming precipitation chances.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": { "type": "number" },
                    "longitude": { "type": "number" },
                    "days": { "type": "integer", "default": 3 }
                },
            "required": ["latitude", "longitude"]
          }
        }
    },
]
