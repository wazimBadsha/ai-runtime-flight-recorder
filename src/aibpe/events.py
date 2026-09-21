from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    RUN_STARTED = "run.started"
    PROMPT_RESOLVED = "prompt.resolved"
    CONTEXT_RETRIEVED = "context.retrieved"
    MEMORY_READ = "memory.read"
    MODEL_REQUESTED = "model.requested"
    MODEL_RESPONSE = "model.response"
    TOOL_REQUESTED = "tool.requested"
    TOOL_RESPONSE = "tool.response"
    POLICY_DECISION = "policy.decision"
    MODEL_FINAL = "model.final"
    RUN_COMPLETED = "run.completed"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class Event:
    run_id: str
    sequence: int
    event_type: EventType
    payload: dict[str, Any]
    producer: str = "aibpe"
    event_id: str = ""
    timestamp_ns: int = 0
    schema_version: str = "aibpe.event.v1"
    previous_hash: str | None = None

    def materialized(self) -> "Event":
        event_id = self.event_id or str(uuid.uuid4())
        timestamp_ns = self.timestamp_ns or time.time_ns()
        return Event(
            run_id=self.run_id,
            sequence=self.sequence,
            event_type=self.event_type,
            payload=self.payload,
            producer=self.producer,
            event_id=event_id,
            timestamp_ns=timestamp_ns,
            schema_version=self.schema_version,
            previous_hash=self.previous_hash,
        )

    def content_hash(self) -> str:
        body = {
            "run_id": self.run_id,
            "sequence": self.sequence,
            "event_type": self.event_type.value,
            "payload": self.payload,
            "producer": self.producer,
            "schema_version": self.schema_version,
            "previous_hash": self.previous_hash,
        }
        return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["event_type"] = self.event_type.value
        value["content_hash"] = self.content_hash()
        return value
