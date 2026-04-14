from tools.location import resolve_us_location
from tools.weather import get_weather_by_coordinates
from tools.distance import calculate_distance
from tools.news import get_current_news
from tools.time import get_current_time

TOOL_FUNCTIONS = {
    "resolve_us_location": resolve_us_location,
    "get_weather_by_coordinates": get_weather_by_coordinates,
    "calculate_distance": calculate_distance,
    "get_current_news": get_current_news,
    "get_current_time": get_current_time,
}
