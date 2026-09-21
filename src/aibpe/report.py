from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .compare import Comparison
from .intervention import Evidence, Intervention


def evidence_report(
    *,
    run_id: str,
    comparison: Comparison,
    intervention: Intervention | None = None,
) -> dict[str, Any]:
    evidence = None
    if intervention is not None:
        evidence = Evidence(
            intervention=intervention,
            baseline_fingerprint=comparison.baseline_fingerprint,
            intervened_fingerprint=comparison.candidate_fingerprint,
            observed_behavior_changed=comparison.behavior_changed,
            changed_fields=comparison.changed_paths,
        )

    return {
        "run_id": run_id,
        "behavior_changed": comparison.behavior_changed,
        "changed_paths": list(comparison.changed_paths),
        "baseline_fingerprint": comparison.baseline_fingerprint,
        "candidate_fingerprint": comparison.candidate_fingerprint,
        "evidence": (
            {
                "path": evidence.intervention.path,
                "strength": evidence.strength,
                "observed_behavior_changed": evidence.observed_behavior_changed,
                "changed_fields": list(evidence.changed_fields),
            }
            if evidence
            else None
        ),
        "causality_note": (
            "An intervention-supported contributor is stronger evidence than correlation, "
            "but this artifact is not automatically a causal claim."
        ),
    }


def write_report(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
