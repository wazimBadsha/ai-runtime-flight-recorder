from pathlib import Path

from aibpe.diff import compare_runs
from aibpe.intervention import Intervention
from aibpe.recorder import Recorder
from aibpe.replay import exact_replay
from aibpe.runtime import DeterministicAgent

ROOT = Path(".aibpe")
agent = DeterministicAgent()

baseline_state = {
    "model": {"name": "demo-llm", "temperature": 0.2},
    "prompt": {"template": "answer-v1"},
    "retrieval": {"corpus": "docs-v2"},
    "memory": {"snapshot": "mem-01"},
    "tools": {"schema": "tools-v1"},
    "policy": {"profile": "safe-default"},
}

candidate_state = dict(baseline_state)
candidate_state["retrieval"] = {"corpus": "docs-v3"}

baseline = Recorder("baseline", ROOT, capture_raw=True)
baseline.set_component("model", baseline_state["model"])
baseline.set_component("prompt", baseline_state["prompt"])
baseline.set_component("retrieval", baseline_state["retrieval"])
baseline.set_component("memory", baseline_state["memory"])
baseline.set_component("tools", baseline_state["tools"])
baseline.set_component("policy", baseline_state["policy"])
base_result = agent.run(baseline_state, baseline)
baseline.save()

candidate = Recorder("candidate", ROOT, capture_raw=True)
for key in ("model", "prompt", "retrieval", "memory", "tools", "policy"):
    candidate.set_component(key, candidate_state[key])
cand_result = agent.run(candidate_state, candidate)
candidate.save()

print("baseline:", base_result.output)
print("candidate:", cand_result.output)
print("exact replay:", exact_replay(ROOT, "baseline")["final_output"])
print("diff:", compare_runs(
    baseline.manifest.to_dict(),
    candidate.manifest.to_dict(),
    left_output=base_result.output,
    right_output=cand_result.output,
    left_trajectory=list(base_result.trajectory),
    right_trajectory=list(cand_result.trajectory),
))
