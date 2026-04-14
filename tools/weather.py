import json
import urllib.request
import urllib.parse

def get_weather_by_coordinates(latitude: float, longitude: float) -> str:
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
    )

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    c = data["current"]
    u = data["current_units"]

    return (
        f"The current temperature is {c['temperature_2m']}{u['temperature_2m']} "
        f"with wind speeds of {c['wind_speed_10m']}{u['wind_speed_10m']}."
    )
