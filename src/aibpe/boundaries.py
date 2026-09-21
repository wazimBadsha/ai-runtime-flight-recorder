from __future__ import annotations

from typing import Any, Callable

from .events import EventType
from .recorder import Recorder

class RuntimeBoundary:
    def __init__(self, recorder: Recorder):
        self.recorder = recorder

    def retrieval(self, query: str, documents: list[dict[str, Any]], *, corpus: str, ranker: str = "unknown"):
        self.recorder.event(EventType.CONTEXT_RETRIEVED, {
            "query": query,
            "corpus": corpus,
            "ranker": ranker,
            "documents": documents,
        })
        return documents

    def memory_read(self, key: str, value: Any, *, snapshot: str):
        self.recorder.event(EventType.MEMORY_READ, {
            "key": key,
            "snapshot": snapshot,
            "value": value,
        })
        return value

    def policy(self, action: str, decision: str, *, policy_id: str, reason: str = ""):
        self.recorder.event(EventType.POLICY_DECISION, {
            "action": action,
            "decision": decision,
            "policy_id": policy_id,
            "reason": reason,
        })
        return decision

    def tool(self, name: str, arguments: dict[str, Any], call: Callable[[], Any]) -> Any:
        self.recorder.event(EventType.TOOL_REQUESTED, {"tool": name, "arguments": arguments})
        try:
            result = call()
        except Exception as exc:
            self.recorder.event(EventType.TOOL_RESPONSE, {"tool": name, "error": type(exc).__name__})
            raise
        self.recorder.event(EventType.TOOL_RESPONSE, {"tool": name, "result": result})
        return result
