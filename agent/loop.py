import json
from agent.ollama_client import call_ollama
from tools import TOOL_FUNCTIONS
from config.env import MAX_STEPS, LLM_MODEL

def run_agent(prompt: str, tool_schemas: list):
    messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "tools": tool_schemas,
        "stream": False
    }

    for _ in range(MAX_STEPS):
        response = call_ollama(payload)
        message = response.get("message", {})

        if not message.get("tool_calls"):
            print("\n[Response]")
            print(message.get("content", ""))
            return

        messages.append(message)
        print("\n[Tool Execution]")

        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]

            print(f" └── Calling {name}({args})")

            if not args:
                result = f"Error: tool '{name}' called without arguments."
            else:
                result = TOOL_FUNCTIONS[name](**args)

            print(f"     └─ Result: {result}")

            messages.append({
                "role": "tool",
                "name": name,
                "content": json.dumps(result)
            })

        payload["messages"] = messages

    print("\n[Error] Agent exceeded maximum steps.")
