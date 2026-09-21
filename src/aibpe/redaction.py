from __future__ import annotations

import re
from typing import Any, Mapping

DEFAULT_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|authorization|secret|password)\s*[:=]\s*[^\s,}]+"),
    re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
)

def redact_text(text: str, patterns=DEFAULT_PATTERNS, replacement: str = "[REDACTED]") -> str:
    out = text
    for pattern in patterns:
        out = pattern.sub(lambda m: replacement, out)
    return out

def redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return {str(k): redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value
