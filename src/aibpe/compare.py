from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .fingerprint import behavioral_fingerprint
from .intervention import diff_paths


@dataclass(frozen=True)
class Comparison:
    baseline_fingerprint: str
    candidate_fingerprint: str
    changed_paths: tuple[str, ...]

    @property
    def behavior_changed(self) -> bool:
        return self.baseline_fingerprint != self.candidate_fingerprint


def compare_facts(baseline: Mapping[str, Any], candidate: Mapping[str, Any]) -> Comparison:
    return Comparison(
        baseline_fingerprint=behavioral_fingerprint(baseline),
        candidate_fingerprint=behavioral_fingerprint(candidate),
        changed_paths=tuple(diff_paths(baseline, candidate)),
    )
