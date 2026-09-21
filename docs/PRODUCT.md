# Product design

## Primary users

AI platform engineers, LLM engineers, reliability engineers, and developers debugging behavioral regressions.

## Primary workflow

1. Select two runs.
2. Inspect dependency changes.
3. Locate the first meaningful trajectory divergence.
4. Declare one intervention.
5. Re-run the controlled experiment.
6. Inspect the evidence artifact.

## Explorer information architecture

```text
Runs
 ├─ Overview
 │   ├─ behavioral fingerprint
 │   ├─ dependency manifest
 │   └─ event timeline
 ├─ Provenance
 │   ├─ dependency graph
 │   └─ artifact hashes
 └─ Experiments
     ├─ baseline
     ├─ intervention
     └─ observed delta
```

The UI should emphasize evidence and dependency boundaries rather than anthropomorphic explanations of model reasoning.
