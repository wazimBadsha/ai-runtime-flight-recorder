from __future__ import annotations

from collections.abc import Iterable, Mapping


def verify_chain(events: Iterable[Mapping[str, object]]) -> tuple[bool, str]:
    previous = None
    for index, event in enumerate(events):
        expected_previous = event.get("previous_hash")
        if expected_previous != previous:
            return False, f"event {index}: previous_hash mismatch"
        previous = event.get("content_hash")
        if not isinstance(previous, str) or len(previous) != 64:
            return False, f"event {index}: invalid content_hash"
    return True, "chain verified"
