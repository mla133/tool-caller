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
    }
]
