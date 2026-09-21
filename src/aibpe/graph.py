from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str
    fingerprint: str | None = None
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str


class ProvenanceGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise KeyError("both edge endpoints must exist")
        self.edges.append(edge)

    def dependencies_of(self, node_id: str) -> list[Node]:
        source_ids = [e.source for e in self.edges if e.target == node_id]
        return [self.nodes[s] for s in source_ids]

    def iter_edges(self) -> Iterable[Edge]:
        return tuple(self.edges)
