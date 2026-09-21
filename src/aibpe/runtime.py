from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .events import EventType
from .recorder import Recorder

@dataclass(frozen=True)
class AgentResult:
    output: str
    trajectory: tuple[str, ...]

class DeterministicAgent:
    """Offline demo agent. The same state yields the same output."""

    def __init__(self, responder: Callable[[dict[str, Any]], str] | None = None) -> None:
        self.responder = responder or self._default

    @staticmethod
    def _default(state: dict[str, Any]) -> str:
        corpus = state.get("retrieval", {}).get("corpus", "unknown")
        prompt = state.get("prompt", {}).get("template", "default")
        return f"answer[{prompt}|{corpus}]"

    def run(self, state: dict[str, Any], recorder: Recorder | None = None) -> AgentResult:
        trajectory = ("start", "context-loaded", "model-called", "final")
        if recorder:
            recorder.event(EventType.RUN_STARTED, {"state": state})
            recorder.event(EventType.PROMPT_RESOLVED, state.get("prompt", {}))
            recorder.event(EventType.CONTEXT_RETRIEVED, state.get("retrieval", {}))
            recorder.event(EventType.MODEL_REQUESTED, {"model": state.get("model", {}), "input": state})
        output = self.responder(state)
        if recorder:
            recorder.event(EventType.MODEL_RESPONSE, {"output": output})
            recorder.event(EventType.MODEL_FINAL, {"output": output, "trajectory": trajectory})
            recorder.event(EventType.RUN_COMPLETED, {"status": "ok"})
        return AgentResult(output=output, trajectory=trajectory)
