from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .events import Event, EventType, canonical_json
from .models import ArtifactRef, RunManifest
from .redaction import redact

class Recorder:
    def __init__(
        self,
        run_id: str,
        root: str | Path = ".aibpe",
        *,
        capture_raw: bool = True,
        runtime: dict[str, Any] | None = None,
    ) -> None:
        self.run_id = run_id
        self.root = Path(root)
        self.capture_raw = capture_raw
        self.manifest = RunManifest(run_id=run_id, created_at_ns=time.time_ns(), runtime=runtime or {})
        self.events: list[Event] = []
        self._seq = 0
        self._previous_hash: str | None = None

    def event(self, event_type: EventType, payload: dict[str, Any]) -> Event:
        self._seq += 1
        safe_payload = redact(payload) if not self.capture_raw else payload
        event = Event(
            run_id=self.run_id,
            sequence=self._seq,
            event_type=event_type,
            payload=safe_payload,
            timestamp_ns=time.time_ns(),
            previous_hash=self._previous_hash,
        ).materialized()
        self._previous_hash = event.content_hash()
        self.events.append(event)
        return event

    def set_component(self, name: str, value: dict[str, Any]) -> None:
        if not hasattr(self.manifest, name):
            raise AttributeError(name)
        setattr(self.manifest, name, value)

    def add_artifact(self, kind: str, value: Any, uri: str | None = None) -> ArtifactRef:
        encoded = canonical_json(value).encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        artifact_id = f"{kind}-{digest[:16]}"
        ref = ArtifactRef(artifact_id, kind, digest, len(encoded), uri)
        self.manifest.artifacts.append(ref)
        artifact_dir = self.root / self.run_id / "artifacts"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / f"{artifact_id}.json").write_bytes(encoded)
        return ref

    def save(self) -> Path:
        run_dir = self.root / self.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "manifest.json").write_text(
            json.dumps(self.manifest.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        with (run_dir / "events.jsonl").open("w", encoding="utf-8") as fh:
            for event in self.events:
                fh.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
        return run_dir
