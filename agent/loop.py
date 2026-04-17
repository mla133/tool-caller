# agent/loop.py

import json
from schemas.tools import AVAILABLE_TOOLS
from tools import TOOL_FUNCTIONS
from agent.validation import validate_tool_call
from agent.ollama_client import call_ollama
from agent.llama_cpp_client import call_llama_cpp
from config.env import MAX_STEPS, LLM_BACKEND, LLM_MODEL


def run_agent(prompt: str, tool_schemas: list):
    # ---------- INITIAL STATE ----------
    messages = [{"role": "user", "content": prompt}]

    for step in range(MAX_STEPS):

        # ---------- PLANNER ----------
        if LLM_BACKEND == "llama.cpp":
            plan = call_llama_cpp(messages, tool_schemas)

            if plan["type"] == "message":
                print("\n[Response]")
                print(plan["content"])
                return

            tool_calls = [{
                "function": {
                    "name": plan["name"],
                    "arguments": plan["arguments"],
                }
            }]

        elif LLM_BACKEND == "ollama":
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

        else:
            raise ValueError(f"Unknown LLM_BACKEND: {LLM_BACKEND}")

        # ---------- EXECUTOR ----------
        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]

            # --- validation (replan-on-rejection) ---
            is_valid, error, tool_schema = validate_tool_call(
                name, args, AVAILABLE_TOOLS
            )

            if not is_valid:
                messages.append({
                    "role": "system",
                    "content": f"REJECTION: {error}",
                })
                continue  # planner retries

            # --- defensive numeric coercion ---
            for k in ("latitude", "longitude", "lat1", "lon1", "lat2", "lon2"):
                if k in args:
                    args[k] = float(args[k])

            print("\n[Tool Execution]")
            print(f" └── Calling {name}({args})")

            result = TOOL_FUNCTIONS[name](**args)

            print(f" └─ Result: {result}")

            # --- record tool output ---
            messages.append({
                "role": "tool",
                "name": name,
                "content": json.dumps(result),
            })

            # ✅ STATE COMPLETION MARKER (prevents repeats)
            if not tool_schema["function"].get("terminal", False):
                messages.append({
                    "role": "system",
                    "content": (
                        f"Tool '{name}' has completed successfully. "
                        "Its results are now available for the next step."
                    ),
                })
                continue  # allow planner to move forward

            # ✅ TERMINAL TOOL → STOP
            print("\n[Response]")
            print(result)
            return

    print("\n[Error] Agent exceeded maximum steps.")
