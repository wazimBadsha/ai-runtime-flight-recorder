from pathlib import Path

from aibpe.boundaries import RuntimeBoundary
from aibpe.events import EventType
from aibpe.recorder import Recorder
from aibpe.runtime import DeterministicAgent

root = Path(".aibpe")
recorder = Recorder(
    "agent-pipeline-demo",
    root,
    capture_raw=False,
    runtime={"framework": "custom", "mode": "offline-demo"},
)
boundary = RuntimeBoundary(recorder)

recorder.set_component("model", {"name": "demo-llm", "temperature": 0.1})
recorder.set_component("prompt", {"template": "support-v1"})
recorder.set_component("retrieval", {"corpus": "kb-v4"})
recorder.set_component("memory", {"snapshot": "memory-17"})
recorder.set_component("tools", {"schema": "mcp-v1"})
recorder.set_component("policy", {"profile": "support-safe"})

docs = boundary.retrieval(
    "refund status",
    [{"id": "doc-7", "score": 0.97}],
    corpus="kb-v4",
    ranker="bm25",
)
memory = boundary.memory_read("customer_preferences", {"language": "en"}, snapshot="memory-17")
decision = boundary.policy("refund.lookup", "allow", policy_id="support-safe")
tool_result = boundary.tool(
    "refund.lookup",
    {"customer_ref": "redacted"},
    lambda: {"status": "processing"},
)

state = {
    "model": recorder.manifest.model,
    "prompt": recorder.manifest.prompt,
    "retrieval": {"corpus": recorder.manifest.retrieval["corpus"], "docs": docs},
    "memory": {"snapshot": recorder.manifest.memory["snapshot"], "value": memory},
    "tools": {"decision": decision, "result": tool_result},
    "policy": recorder.manifest.policy,
}
DeterministicAgent().run(state, recorder)
recorder.event(EventType.RUN_COMPLETED, {"status": "ok"})
print(recorder.save())
