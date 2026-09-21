from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .compare import compare_facts
from .fingerprint import behavioral_fingerprint
from .intervention import Intervention

@dataclass(frozen=True)
class ExperimentResult:
    baseline_fingerprint: str
    candidate_fingerprint: str
    changed_paths: tuple[str, ...]
    baseline_output: Any
    candidate_output: Any
    intervention_path: str
    replacement: Any

    @property
    def dependency_changed(self) -> bool:
        return self.baseline_fingerprint != self.candidate_fingerprint

    @property
    def behavior_changed(self) -> bool:
        return self.baseline_output != self.candidate_output

    @property
    def intervention_supported(self) -> bool:
        return self.dependency_changed and self.behavior_changed

def run_intervention(
    baseline: Mapping[str, Any],
    intervention: Intervention,
    executor: Callable[[Mapping[str, Any]], Any],
) -> ExperimentResult:
    candidate = intervention.apply(baseline)
    base_output = executor(baseline)
    candidate_output = executor(candidate)
    comparison = compare_facts(baseline, candidate)
    return ExperimentResult(
        baseline_fingerprint=behavioral_fingerprint(baseline),
        candidate_fingerprint=behavioral_fingerprint(candidate),
        changed_paths=comparison.changed_paths,
        baseline_output=base_output,
        candidate_output=candidate_output,
        intervention_path=intervention.path,
        replacement=intervention.replacement,
    )
