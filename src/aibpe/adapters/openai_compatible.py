from __future__ import annotations

import json
import urllib.request
from typing import Any

from ..events import EventType
from ..recorder import Recorder

class OpenAICompatibleClient:
    """Tiny dependency-free client for OpenAI-compatible chat endpoints."""

    def __init__(self, base_url: str, api_key: str, model: str, recorder: Recorder | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.recorder = recorder

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> dict[str, Any]:
        payload = {"model": self.model, "messages": messages, **kwargs}
        if self.recorder:
            self.recorder.event(EventType.MODEL_REQUESTED, {"provider": "openai-compatible", "model": self.model, "request": payload})
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        if self.recorder:
            self.recorder.event(EventType.MODEL_RESPONSE, {"provider": "openai-compatible", "response": result})
        return result
