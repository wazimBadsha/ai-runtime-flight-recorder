from aibpe.compare import compare_facts
from aibpe.intervention import Intervention
from aibpe.report import evidence_report


baseline = {
    "model": {"name": "demo-llm", "temperature": 0.2},
    "prompt": {"template": "answer-v1"},
    "retrieval": {"corpus": "docs-v2"},
}

intervention = Intervention(
    "retrieval.corpus",
    "docs-v3",
    rationale="test whether retrieval version is a behavioral contributor",
)

candidate = intervention.apply(baseline)
comparison = compare_facts(baseline, candidate)

report = evidence_report(
    run_id="offline-demo",
    comparison=comparison,
    intervention=intervention,
)

print(report)
