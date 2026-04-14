import json
import urllib.request
import urllib.parse

from config.env import NEWS_API_KEY

def get_current_news(topic: str = None) -> str:
    if topic:
        url = "https://newsapi.org/v2/everything?" + urllib.parse.urlencode({
            "q": topic,
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        })
    else:
        url = "https://newsapi.org/v2/top-headlines?" + urllib.parse.urlencode({
            "language": "en",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        })

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    articles = data.get("articles", [])
    lines = ["News:"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. {a['title']} ({a['source']['name']})")

    return "\n".join(lines)
