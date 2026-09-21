from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

class ReplayError(RuntimeError):
    pass

def load_run(root: str | Path, run_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    run_dir = Path(root) / run_id
    if not run_dir.exists():
        raise ReplayError(f"run not found: {run_id}")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    events = [
        json.loads(line)
        for line in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return manifest, events

def exact_replay(root: str | Path, run_id: str) -> dict[str, Any]:
    manifest, events = load_run(root, run_id)
    finals = [e for e in events if e["event_type"] == "model.final"]
    return {
        "mode": "exact",
        "run_id": run_id,
        "manifest": manifest,
        "final_output": finals[-1]["payload"] if finals else None,
        "event_count": len(events),
    }

def approximate_replay(
    root: str | Path,
    run_id: str,
    executor: Callable[[dict[str, Any], list[dict[str, Any]]], Any],
) -> Any:
    manifest, events = load_run(root, run_id)
    return executor(manifest, events)
