# llm/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List


Message = Dict[str, str]
ToolSchema = Dict[str, Any]


class LLMAdapter(ABC):
    """
    Runtime-enforced contract for all LLM backends.
    """

    @abstractmethod
    def build_prompt(
        self,
        messages: List[Message],
        tools: List[ToolSchema],
    ) -> Any:
        """
        Convert messages + tool schemas into a backend-specific prompt.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: Any) -> str:
        """
        Execute inference and return raw model output text.
        """
        raise NotImplementedError

    @abstractmethod
    def extract_tool_call(self, output: str) -> Dict[str, Any] | None:
        """
        Parse and validate a tool call request from model output.
        Return None if no tool call is requested.
        """
        raise NotImplementedError
