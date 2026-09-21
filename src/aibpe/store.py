from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .events import Event


class LocalStore:
    """Local JSONL event store with append-only semantics."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def append(self, event: Event) -> Path:
        event = event.materialized()
        path = self.root / f"{event.run_id}.jsonl"
        previous_hash = None
        if path.exists():
            last = list(path.read_text(encoding="utf-8").splitlines())[-1]
            previous_hash = json.loads(last).get("content_hash")
            event = Event(
                run_id=event.run_id,
                sequence=event.sequence,
                event_type=event.event_type,
                payload=event.payload,
                producer=event.producer,
                event_id=event.event_id,
                timestamp_ns=event.timestamp_ns,
                schema_version=event.schema_version,
                previous_hash=previous_hash,
            )
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
        return path

    def read(self, run_id: str) -> Iterable[dict]:
        path = self.root / f"{run_id}.jsonl"
        if not path.exists():
            return ()
        return tuple(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
