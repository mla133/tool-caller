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

    def build_prompt(
        self,
        messages: List[Message],
        tools: List[ToolSchema],
    ) -> str:
        tool_block = json.dumps(tools, indent=2)

        convo = "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in messages
        )

        return f"""You are a tool-calling assistant.

TOOLS:
{tool_block}

RULES:
- If calling a tool, output ONLY:
  <tool_call>
  {{ "tool": "...", "args": {{...}} }}
  </tool_call>

- Otherwise return normal assistant text.

{convo}

ASSISTANT:
"""

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/completion",
            headers={"Content-Type": "application/json"},
            json={
                "prompt": prompt,
                "n_predict": self.n_predict,
                "temperature": self.temperature,
                "stop": ["USER:", "</tool_call>"],
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["content"]

    def extract_tool_call(self, output: str) -> Dict[str, Any] | None:
        match = _TOOL_RE.search(output)
        if not match:
            return None
        try:
            return json.loads(match.group(1))
        except Exception:
            return None
