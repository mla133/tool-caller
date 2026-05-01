# agent/agent.py

from typing import List, Dict, Any
from llm.base import LLMAdapter

Message = Dict[str, str]
ToolSchema = Dict[str, Any]


class Agent:
    """
    Core agent loop. Completely backend-agnostic.
    """

    def __init__(
        self,
        llm: LLMAdapter,
        tools: List[ToolSchema],
    ):
        self.llm = llm
        self.tools = tools
        self.messages: List[Message] = []

    def add_user_message(self, content: str) -> None:
        self.messages.append({
            "role": "user",
            "content": content,
        })

    def step(self) -> str:
        """
        Execute a single agent step:
        - build prompt
        - generate output
        - detect tool call
        - execute tool if requested
        """
        prompt = self.llm.build_prompt(
            messages=self.messages,
            tools=self.tools,
        )

        output = self.llm.generate(prompt)

        tool_call = self.llm.extract_tool_call(output)
        if tool_call is not None:
            result = self._run_tool(tool_call)

            # feed tool result back into context
            self.messages.append({
                "role": "tool",
                "content": result,
            })

            return result

        # normal assistant response
        self.messages.append({
            "role": "assistant",
            "content": output,
        })
        return output

    def _run_tool(self, tool_call: Dict[str, Any]) -> str:
        """
        Execute a tool call of the form:
        {
          "tool": "tool_name",
          "args": {...}
        }
        """
        name = tool_call.get("tool")
        args = tool_call.get("args", {})

        for tool in self.tools:
            if tool["name"] == name:
                try:
                    return tool["callable"](**args)
                except Exception as e:
                    return f"Tool '{name}' failed: {e}"

        return f"Unknown tool: {name}"
