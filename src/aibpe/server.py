from __future__ import annotations

import json
from pathlib import Path

def create_app(root: str = ".aibpe"):
    try:
        from fastapi import FastAPI, HTTPException
    except ImportError as exc:
        raise RuntimeError("Install the server extra: pip install 'aibpe[server]'") from exc

    app = FastAPI(title="AIBPE Explorer API", version="0.2.0")
    base = Path(root)

    @app.get("/health")
    def health():
        return {"status": "ok", "storage": str(base)}

    @app.get("/runs")
    def runs():
        if not base.exists():
            return []
        return sorted(
            p.name for p in base.iterdir()
            if p.is_dir() and (p / "manifest.json").exists()
        )

    @app.get("/runs/{run_id}")
    def run(run_id: str):
        path = base / run_id
        if not path.exists():
            raise HTTPException(status_code=404, detail="run not found")
        manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        events = [json.loads(x) for x in (path / "events.jsonl").read_text(encoding="utf-8").splitlines() if x]
        return {"manifest": manifest, "events": events}

    return app
