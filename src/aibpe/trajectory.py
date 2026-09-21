from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable

TOKEN_RE = re.compile(r"\w+")

def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))

def jaccard_similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))

@dataclass(frozen=True)
class StepDelta:
    index: int
    left: Any
    right: Any
    changed: bool

@dataclass(frozen=True)
class TrajectoryDiff:
    changed_steps: tuple[StepDelta, ...]
    similarity: float

def compare_trajectories(left: Iterable[Any], right: Iterable[Any]) -> TrajectoryDiff:
    a, b = list(left), list(right)
    n = max(len(a), len(b))
    deltas: list[StepDelta] = []
    texts_left, texts_right = [], []
    for i in range(n):
        lv = a[i] if i < len(a) else None
        rv = b[i] if i < len(b) else None
        deltas.append(StepDelta(i, lv, rv, lv != rv))
        texts_left.append(str(lv))
        texts_right.append(str(rv))
    return TrajectoryDiff(
        changed_steps=tuple(d for d in deltas if d.changed),
        similarity=jaccard_similarity(" ".join(texts_left), " ".join(texts_right)),
    )
