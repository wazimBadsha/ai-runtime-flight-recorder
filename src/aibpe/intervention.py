from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Mapping


@dataclass(frozen=True)
class Intervention:
    path: str
    replacement: Any
    rationale: str = ""

    def apply(self, facts: Mapping[str, Any]) -> dict[str, Any]:
        out = deepcopy(dict(facts))
        cursor: Any = out
        parts = self.path.split(".")
        if not parts or any(not p for p in parts):
            raise ValueError("path must be a non-empty dotted path")

        for part in parts[:-1]:
            if not isinstance(cursor, dict) or part not in cursor:
                raise KeyError(f"unknown intervention path: {self.path}")
            cursor = cursor[part]

        if not isinstance(cursor, dict):
            raise TypeError(f"cannot assign through non-object path: {self.path}")
        cursor[parts[-1]] = deepcopy(self.replacement)
        return out


@dataclass(frozen=True)
class Evidence:
    intervention: Intervention
    baseline_fingerprint: str
    intervened_fingerprint: str
    observed_behavior_changed: bool
    changed_fields: tuple[str, ...]

    @property
    def strength(self) -> str:
        if not self.observed_behavior_changed:
            return "no-observed-effect"
        return "intervention-supported-contributor"


def diff_paths(before: Mapping[str, Any], after: Mapping[str, Any], prefix: str = "") -> list[str]:
    paths: list[str] = []
    keys = set(before) | set(after)
    for key in sorted(keys):
        path = f"{prefix}.{key}" if prefix else key
        if key not in before or key not in after:
            paths.append(path)
            continue
        left, right = before[key], after[key]
        if isinstance(left, Mapping) and isinstance(right, Mapping):
            paths.extend(diff_paths(left, right, path))
        elif left != right:
            paths.append(path)
    return paths
