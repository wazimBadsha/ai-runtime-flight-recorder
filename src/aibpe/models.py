from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ArtifactRef:
    artifact_id: str
    kind: str
    sha256: str
    size_bytes: int
    uri: str | None = None

@dataclass
class RunManifest:
    run_id: str
    created_at_ns: int
    schema_version: str = "aibpe.manifest.v1"
    runtime: dict[str, Any] = field(default_factory=dict)
    model: dict[str, Any] = field(default_factory=dict)
    prompt: dict[str, Any] = field(default_factory=dict)
    retrieval: dict[str, Any] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)
    tools: dict[str, Any] = field(default_factory=dict)
    policy: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, Any] = field(default_factory=dict)
    artifacts: list[ArtifactRef] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "created_at_ns": self.created_at_ns,
            "schema_version": self.schema_version,
            "runtime": self.runtime,
            "model": self.model,
            "prompt": self.prompt,
            "retrieval": self.retrieval,
            "memory": self.memory,
            "tools": self.tools,
            "policy": self.policy,
            "environment": self.environment,
            "artifacts": [a.__dict__ for a in self.artifacts],
        }
