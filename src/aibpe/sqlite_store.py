from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

class SQLiteIndex:
    def __init__(self, path: str | Path = ".aibpe/index.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, created_at_ns INTEGER NOT NULL, manifest_json TEXT NOT NULL)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS events (run_id TEXT NOT NULL, sequence INTEGER NOT NULL, event_type TEXT NOT NULL, event_json TEXT NOT NULL, PRIMARY KEY(run_id, sequence))"
            )

    def index(self, manifest: dict, events: Iterable[dict]) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT OR REPLACE INTO runs(run_id, created_at_ns, manifest_json) VALUES(?,?,?)",
                (manifest["run_id"], manifest["created_at_ns"], json.dumps(manifest, sort_keys=True)),
            )
            for event in events:
                db.execute(
                    "INSERT OR REPLACE INTO events(run_id, sequence, event_type, event_json) VALUES(?,?,?,?)",
                    (event["run_id"], event["sequence"], event["event_type"], json.dumps(event, sort_keys=True)),
                )

    def recent_runs(self, limit: int = 20) -> list[dict]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute(
                "SELECT run_id, created_at_ns, manifest_json FROM runs ORDER BY created_at_ns DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{"run_id": r[0], "created_at_ns": r[1], "manifest": json.loads(r[2])} for r in rows]
