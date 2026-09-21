# AIBPE Specification v0.2

## Run identity

Every run has a stable `run_id`. A run is a collection of runtime events plus a manifest describing the declared behavioral dependencies.

## Event envelope

Each event contains:

- `event_id`
- `run_id`
- `sequence`
- `timestamp_ns`
- `event_type`
- `payload`
- `producer`
- `schema_version`
- `previous_hash`
- `content_hash`

`content_hash` covers the canonical event body. `previous_hash` provides tamper-evident chaining.

## Dependency domains

The initial public domains are:

`model`, `prompt`, `retrieval`, `memory`, `tools`, `policy`, `environment`.

Implementations may add domains without changing the envelope.

## Intervention

An intervention declares a replacement at a dotted dependency path:

`retrieval.corpus = docs-v3`

The baseline remains untouched. The candidate is independently executed and compared.

## Evidence boundary

AIBPE distinguishes:

1. observed behavioral change
2. candidate contributor
3. intervention-supported contributor
4. stronger causal interpretation supported by a separate experimental design

The runtime never treats an LLM-generated explanation as proof of causality.
