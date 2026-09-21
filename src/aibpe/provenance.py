from __future__ import annotations

from .graph import Edge, Node, ProvenanceGraph

COMPONENT_EVENT_MAP = {
    "prompt.resolved": "prompt",
    "context.retrieved": "retrieval",
    "memory.read": "memory",
    "model.requested": "model",
    "tool.requested": "tools",
    "policy.decision": "policy",
}

def graph_from_events(events: list[dict]) -> ProvenanceGraph:
    graph = ProvenanceGraph()
    run_ids = {event.get("run_id") for event in events}
    for run_id in run_ids:
        graph.add_node(Node(node_id=f"run:{run_id}", kind="run"))

    for event in events:
        event_node = f"event:{event['event_id']}"
        graph.add_node(Node(
            node_id=event_node,
            kind=event["event_type"],
            metadata={"sequence": event["sequence"], "content_hash": event["content_hash"]},
        ))
        graph.add_edge(Edge(event_node, f"run:{event['run_id']}", "part_of"))

        component = COMPONENT_EVENT_MAP.get(event["event_type"])
        if component:
            component_id = f"{component}:{event_node}"
            graph.add_node(Node(component_id, component, metadata={"event_id": event["event_id"]}))
            graph.add_edge(Edge(component_id, event_node, "influences"))
    return graph
