# tools/time.py
import json
import urllib.request
import urllib.parse

def get_current_time(timezone: str) -> str:
    url = "https://timeapi.io/api/Time/current/zone?" + urllib.parse.urlencode({
        "timeZone": timezone
    })

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    return f"The current time in {timezone} is {data['time']} on {data['date']}."
