import json
import requests

def call_llama_cpp(prompt: str, tools: list):
    system = (
        "You are a helpful assistant with access to tools.\n\n"
        "When calling a tool, respond ONLY with JSON:\n"
        '{ "name": "<tool_name>", "arguments": { ... } }\n'
        "Do not include any other text.\n"
        "You may ONLY call tools whose names are listed below."
        "You must NOT invent new tool names."
        "If no tool matches exactly, respond with text instead.\n"
        "Allowed tool names: \n"
        "- resolve_us_location\n"
        "- get_weather_by_coordinates\n"
        "- get_forecast_by_coordinates\n"
        "- get_current_news\n"
        "- calculate_distance\n"
    )

    prompt_text = "SYSTEM:\n" + system + "\nUSER:\n" + prompt + "\nASSISTANT:\n"

    r = requests.post(
        "http://localhost:8080/completion",
        json={
            "prompt": prompt_text,
            "temperature": 0.2,
            "n_predict": 1024,
            "stop": ["\nUSER:", "\nSYSTEM:"],
        },
        timeout=120,
    )
    r.raise_for_status()

    text = r.json().get("content", "").strip()

    # Try to parse tool call
    if text.startswith("{"):
        try:
            data = json.loads(text)
            if "name" in data and "arguments" in data:
                return {
                    "type": "tool_call",
                    "name": data["name"],
                    "arguments": data["arguments"],
                }
        except json.JSONDecodeError:
            pass

    return {
        "type": "message",
        "content": text,
    }
