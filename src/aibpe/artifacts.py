from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .events import canonical_json
from .models import ArtifactRef

class ContentAddressedStore:
    def __init__(self, root: str | Path = ".aibpe/blobs") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, kind: str, value: Any) -> ArtifactRef:
        raw = canonical_json(value).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        path = self.root / digest
        if not path.exists():
            path.write_bytes(raw)
        return ArtifactRef(f"{kind}-{digest[:16]}", kind, digest, len(raw), str(path))

    def get(self, sha256: str) -> bytes:
        path = self.root / sha256
        if not path.exists():
            raise FileNotFoundError(sha256)
        return path.read_bytes()
