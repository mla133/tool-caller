# llm/llamaserver.py

import json
import re
import requests
from typing import Any, Dict, List

from .base import LLMAdapter, Message, ToolSchema


_TOOL_RE = re.compile(
    r"<tool_call>\s*(\{.*?\})\s*</tool_call>",
    re.DOTALL,
)


class LlamaServerAdapter(LLMAdapter):
    def __init__(
        self,
        base_url: str = "http://localhost:8123",
        n_predict: int = 512,
        temperature: float = 0.1,
    ):
        self.base_url = base_url.rstrip("/")
        self.n_predict = n_predict
        self.temperature = temperature

    def build_prompt(self, messages, tools) -> str:
        parts = []

        parts.append(
            "You are a helpful assistant. Answer the user clearly and directly.\n"
        )

        for m in messages:
            if m["role"] == "user":
                parts.append(f"### User\n{m['content']}\n")
            elif m["role"] == "assistant":
                parts.append(f"### Assistant\n{m['content']}\n")
            elif m["role"] == "tool":
                parts.append(f"### Tool\n{m['content']}\n")

        # 🔑 This line is critical
        parts.append("### Assistant\n")

        return "\n".join(parts)

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/completion",
            headers={"Content-Type": "application/json"},
            json={
                "prompt": prompt,
                "n_predict": self.n_predict,
                "temperature": self.temperature,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        raw = data.get("content", "")

        # Strip echoed prompt/history
        if "### Assistant" in raw:
            raw = raw.split("### Assistant")[-1]

        return raw.strip()

    def extract_tool_call(self, output: str) -> Dict[str, Any] | None:
        match = _TOOL_RE.search(output)
        if not match:
            return None
        try:
            return json.loads(match.group(1))
        except Exception:
            return None
