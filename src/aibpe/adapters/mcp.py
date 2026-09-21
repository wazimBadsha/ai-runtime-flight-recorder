from __future__ import annotations

from typing import Any, Callable

from ..events import EventType
from ..recorder import Recorder

class MCPToolRecorder:
    """Framework-neutral wrapper for MCP-style tool invocation."""

    def __init__(self, call: Callable[[str, dict[str, Any]], Any], recorder: Recorder) -> None:
        self.call = call
        self.recorder = recorder

    def invoke(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        self.recorder.event(
            EventType.TOOL_REQUESTED,
            {"protocol": "mcp", "tool": tool_name, "arguments": arguments},
        )
        try:
            result = self.call(tool_name, arguments)
        except Exception as exc:
            self.recorder.event(
                EventType.TOOL_RESPONSE,
                {"protocol": "mcp", "tool": tool_name, "error": type(exc).__name__},
            )
            raise
        self.recorder.event(
            EventType.TOOL_RESPONSE,
            {"protocol": "mcp", "tool": tool_name, "result": result},
        )
        return result
