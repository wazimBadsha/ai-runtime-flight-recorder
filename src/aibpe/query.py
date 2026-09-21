from __future__ import annotations

import json
from pathlib import Path

def list_run_ids(root: str | Path = ".aibpe") -> list[str]:
    path = Path(root)
    if not path.exists():
        return []
    return sorted(
        p.name for p in path.iterdir()
        if p.is_dir() and (p / "manifest.json").exists()
    )

def summarize_run(root: str | Path, run_id: str) -> dict:
    run = Path(root) / run_id
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    events = [
        json.loads(x) for x in (run / "events.jsonl").read_text(encoding="utf-8").splitlines() if x
    ]
    return {
        "run_id": run_id,
        "events": len(events),
        "event_types": [e["event_type"] for e in events],
        "manifest": manifest,
        "last_event": events[-1] if events else None,
    }
