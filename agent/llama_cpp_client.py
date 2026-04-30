# agent/llama_cpp_client.py

import json
import requests
from config.env import LLAMA_SYSTEM_PROMPT_PATH


def load_system_prompt() -> str:
    return LLAMA_SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


SYSTEM_PROMPT = load_system_prompt()


def messages_to_prompt(messages: list) -> str:
    """
    Convert chat messages into a single text prompt for llama.cpp
    """
    parts = ["SYSTEM:\n" + SYSTEM_PROMPT + "\n"]

    for msg in messages:
        role = msg["role"].upper()

        if role == "TOOL":
            # Tool result must be visible to the planner
            parts.append(
                f"{role} ({msg.get('name')}):\n{msg['content']}\n"
            )
        else:
            parts.append(f"{role}:\n{msg['content']}\n")

    parts.append("ASSISTANT:\n")
    return "\n".join(parts)


def call_llama_cpp(messages: list, tools: list):
    prompt = messages_to_prompt(messages)

    response = requests.post(
        "http://localhost:8123/v1/completions",
        json={
            "prompt": prompt,
            "temperature": 0.2,
            "n_predict": 1024,
            "stop": ["\nUSER:", "\nSYSTEM:"],
        },
        timeout=120,
    )
    response.raise_for_status()

    text = response.json().get("content", "").strip()

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
