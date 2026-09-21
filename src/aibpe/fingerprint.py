from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


VOLATILE_KEYS = {
    "timestamp",
    "timestamp_ns",
    "request_id",
    "response_id",
    "trace_id",
    "span_id",
}


def _normalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            k: _normalize(v)
            for k, v in sorted(value.items())
            if k not in VOLATILE_KEYS
        }
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    return value


def behavioral_fingerprint(facts: Mapping[str, Any]) -> str:
    normalized = _normalize(facts)
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def fingerprint_facts(
    *,
    model: Mapping[str, Any] | None = None,
    prompt: Mapping[str, Any] | None = None,
    retrieval: Mapping[str, Any] | None = None,
    memory: Mapping[str, Any] | None = None,
    tools: Mapping[str, Any] | None = None,
    policy: Mapping[str, Any] | None = None,
    environment: Mapping[str, Any] | None = None,
) -> str:
    return behavioral_fingerprint(
        {
            "model": model or {},
            "prompt": prompt or {},
            "retrieval": retrieval or {},
            "memory": memory or {},
            "tools": tools or {},
            "policy": policy or {},
            "environment": environment or {},
        }
    )
