from __future__ import annotations

from typing import Any


def trace_attributes(event: dict[str, Any]) -> dict[str, str]:
    """Return OTel-friendly scalar attributes without requiring the SDK."""
    attrs = {
        "aibpe.run_id": str(event.get("run_id", "")),
        "aibpe.event_type": str(event.get("event_type", "")),
        "aibpe.sequence": str(event.get("sequence", "")),
        "aibpe.schema_version": str(event.get("schema_version", "")),
    }
    if event.get("content_hash"):
        attrs["aibpe.content_hash"] = str(event["content_hash"])
    return attrs
