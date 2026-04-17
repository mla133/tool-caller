import json

from agent.ollama_client import call_ollama
from agent.llama_cpp_client import call_llama_cpp
from tools import TOOL_FUNCTIONS
from config.env import MAX_STEPS, LLM_MODEL, LLM_BACKEND


def run_agent(prompt: str, tool_schemas: list):
    messages = [{"role": "user", "content": prompt}]

    for _ in range(MAX_STEPS):

        # --- BACKEND SWITCH (only place that branches) ---
        if LLM_BACKEND == "ollama":
            payload = {
                "model": LLM_MODEL,
                "messages": messages,
                "tools": tool_schemas,
                "stream": False,
            }
            response = call_ollama(payload)
            message = response.get("message", {})

            if not message.get("tool_calls"):
                print("\n[Response]")
                print(message.get("content", ""))
                return

            tool_calls = message["tool_calls"]

        elif LLM_BACKEND == "llama.cpp":
            result = call_llama_cpp(prompt, tool_schemas)

            if result["type"] == "message":
                print("\n[Response]")
                print(result["content"])
                return

            tool_calls = [
                {
                    "function": {
                        "name": result["name"],
                        "arguments": result["arguments"],
                    }
                }
            ]

        else:
            raise ValueError(f"Unknown LLM_BACKEND: {LLM_BACKEND}")

        print(f"\n[LLM_BACKEND - {LLM_BACKEND}]")

        # --- TOOL EXECUTION (shared) ---
        print("\n[Tool Execution]")
        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]

            print(f" └── Calling {name}({args})")

            if not args:
                result = f"Error: tool '{name}' called without arguments."
            else:
                result = TOOL_FUNCTIONS[name](**args)

            print(f" └─ Result: {result}")

            messages.append({
                "role": "tool",
                "name": name,
                "content": json.dumps(result),
            })

    print("\n[Error] Agent exceeded maximum steps.")
