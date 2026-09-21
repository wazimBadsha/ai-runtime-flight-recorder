# Architecture

## Boundary

AIBPE lives at the observation boundary of an AI system. It does not require the project to adopt a particular agent framework.

### Runtime layers

1. **Capture** — normalized events from model, tool, retrieval, memory, policy and environment boundaries.
2. **Canonicalization** — remove transport-only volatility and normalize representations.
3. **Provenance** — connect artifacts to the downstream decisions they can influence.
4. **Fingerprinting** — compute stable identifiers for the declared behavioral inputs.
5. **Intervention** — express a controlled change to one declared dependency.
6. **Evidence** — compare the baseline and intervention results and report observed deltas.

## Why provenance is the unit

A trace is a timeline. A provenance graph is a dependency model.

For example:

```text
retrieval:corpus-v2 ----prompt:template-17 ------memory:snapshot-102 ------> model:request-55 ---> decision:tool.search
tools:schema-4 -----------/
policy:profile-3 --------/
```

This makes it possible to ask what *could* influence a result before deciding what *did* influence it.

## Causality boundary

AIBPE intentionally separates:

- **Observed change** — the output/trajectory differs.
- **Candidate contributor** — a dependency changed between runs.
- **Intervention-supported contributor** — changing the dependency in isolation reproduced a relevant behavioral delta.
- **Causal claim** — reserved for cases with a documented experimental design strong enough to support the claim.

The engine never upgrades a correlation into causation just because a model-written explanation sounds convincing.

## Storage

V0.1 is local-first:

- JSONL for immutable event streams.
- content-addressed artifacts can be layered on later.
- SQLite is the planned index; the event format remains transport-independent.

A production backend can be implemented behind the same storage contract.

## OpenTelemetry

AIBPE can consume/export OTel-compatible identifiers, but the project does not redefine standard telemetry primitives. It adds a provenance/evidence layer above them.
