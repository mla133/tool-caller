# llm/ollama.py

import json
import ollama
from typing import Any, Dict, List

from .base import LLMAdapter, Message, ToolSchema


class OllamaAdapter(LLMAdapter):
    def __init__(self, model: str):
        self.model = model

    def build_prompt(
        self,
        messages: List[Message],
        tools: List[ToolSchema],
    ) -> Any:
        system_msg = {
            "role": "system",
            "content": (
                "You may call tools using JSON.\n\n"
                "TOOLS:\n"
                f"{json.dumps(tools, indent=2)}\n\n"
                "Return either normal text or a JSON tool call."
            ),
        }
        return [system_msg, *messages]

    def generate(self, prompt: Any) -> str:
        response = ollama.chat(
            model=self.model,
            messages=prompt,
        )
        return response["message"]["content"]

    def extract_tool_call(self, output: str) -> Dict[str, Any] | None:
        try:
            data = json.loads(output)
            if isinstance(data, dict) and "tool" in data:
                return data
        except Exception:
            pass
        return None
