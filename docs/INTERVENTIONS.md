# Intervention model

AIBPE treats an intervention as a declared change to one dependency of a run.

## Example

Baseline:

```json
{
  "retrieval": {"corpus": "docs-v2"},
  "model": {"name": "demo-llm"},
  "prompt": {"template": "answer-v1"}
}
```

Intervention:

```text
retrieval.corpus := docs-v3
```

The engine can then compare the resulting behavioral fingerprint and record which fields changed.

## Evidence levels

### Observed change
The baseline and candidate differ.

### Candidate contributor
A dependency changed between runs and is therefore eligible for analysis.

### Intervention-supported contributor
Changing that dependency in an isolated intervention produced a relevant behavioral delta.

### Causal claim
Reserved for experimental designs that support a causal interpretation beyond this library's basic comparison.

AIBPE does not infer causality from model-generated explanations.
