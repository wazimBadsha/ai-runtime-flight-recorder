from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .intervention import diff_paths
from .trajectory import compare_trajectories, TrajectoryDiff

@dataclass(frozen=True)
class RunDiff:
    changed_inputs: tuple[str, ...]
    output_changed: bool
    trajectory: TrajectoryDiff | None = None

def compare_runs(
    left_manifest: dict[str, Any],
    right_manifest: dict[str, Any],
    *,
    left_output: str | None = None,
    right_output: str | None = None,
    left_trajectory: list[Any] | None = None,
    right_trajectory: list[Any] | None = None,
) -> RunDiff:
    left = {k: left_manifest.get(k, {}) for k in ("model", "prompt", "retrieval", "memory", "tools", "policy", "environment")}
    right = {k: right_manifest.get(k, {}) for k in ("model", "prompt", "retrieval", "memory", "tools", "policy", "environment")}
    td = None
    if left_trajectory is not None and right_trajectory is not None:
        td = compare_trajectories(left_trajectory, right_trajectory)
    return RunDiff(
        changed_inputs=tuple(diff_paths(left, right)),
        output_changed=left_output != right_output,
        trajectory=td,
    )
