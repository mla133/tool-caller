# tools/weather.py
import json
import urllib.request
import urllib.parse

def get_weather_by_coordinates(latitude: float, longitude: float) -> str:
#    url = (
#        "https://api.open-meteo.com/v1/forecast?"
#        f"latitude={latitude}&longitude={longitude}"
#        "&current=temperature_2m,wind_speed_10m"
#    )

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
        "&temperature_unit=fahrenheit"
    )

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    c = data["current"]
    u = data["current_units"]

    return (
        f"The current temperature is {c['temperature_2m']}{u['temperature_2m']} "
        f"with wind speeds of {c['wind_speed_10m']}{u['wind_speed_10m']}."
    )

def get_forecast_by_coordinates(latitude: float, longitude: float, days: int = 3) -> str:
    days = max(1, min(days, 7))  # clamp 1–7

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&forecast_days={days}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&temperature_unit=fahrenheit"
        "&timezone=auto"
    )

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    daily = data["daily"]

    lines = []
    for i in range(days):
        lines.append(
            f"Day {i + 1}: "
            f"High {daily['temperature_2m_max'][i]}, "
            f"Low {daily['temperature_2m_min'][i]}, "
            f"Precipitation {daily['precipitation_probability_max'][i]}%"
        )

    return " ".join(lines)
