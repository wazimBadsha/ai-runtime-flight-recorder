# AIBPE — AI Behavioral Provenance Engine

> Observe the run. Map the causes. Test the change.

AIBPE is an open-source, vendor-neutral runtime for understanding why an AI/LLM/agent system changed behavior.

It records structured runtime evidence, builds a behavioral provenance model, computes fingerprints over declared dependencies, and supports controlled interventions.

## The problem

Modern AI behavior depends on more than the model:

- model/version and inference settings
- prompt/template versions
- retrieved context
- memory state
- tool definitions and outputs
- policies and guardrails
- runtime/environment dependencies

A normal trace answers "what happened."

AIBPE is designed to make the next question inspectable:

> Which behavioral dependency changed, what downstream behavior changed with it, and what evidence did the controlled experiment produce?

## Architecture

AI / Agent Runtime
        |
        v
   AIBPE Recorder
        |
        +-- canonical events
        +-- artifact hashes
        +-- dependency metadata
        |
        v
Behavioral Provenance
        |
        +-- fingerprint
        +-- run diff
        +-- trajectory diff
        +-- intervention
        |
        v
Evidence Artifact

## Implemented in v0.2

- immutable event envelope with hash chaining
- run manifest for model, prompt, retrieval, memory, tools, policy and environment
- local JSONL event store
- content-addressed artifacts
- behavioral fingerprints
- structural dependency diff
- intervention executor
- evidence semantics separating dependency change from behavior change
- trajectory comparison
- retrieval/memory/policy/tool boundary capture
- OpenAI-compatible HTTP adapter
- MCP-style tool recorder
- SQLite run index
- optional FastAPI explorer API
- browser-based explorer UI
- Docker / Compose packaging
- public JSON schemas
- CI, tests, security and production guidance

## Quick start

    python -m pip install -e .
    PYTHONPATH=src python examples/full_demo.py
    PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'

    aibpe record-demo --run-id demo --corpus docs-v1
    aibpe inspect demo
    aibpe replay demo
    aibpe verify demo

Optional explorer:

    python -m pip install -e '.[server]'
    PYTHONPATH=src uvicorn aibpe.serve:app --reload

Then open http://127.0.0.1:8000.

## Evidence model

AIBPE deliberately distinguishes:

Observed change
      |
Candidate contributor
      |
Intervention-supported contributor
      |
Stronger causal interpretation

The library does not convert a model-generated explanation into a causal fact.

## Research positioning

Record/replay, deterministic debugging, trajectory comparison and counterfactual agent systems are already active open-source areas. AIBPE therefore does not claim record/replay as a novel invention.

Its focus is the open contract around:

behavioral provenance graph + declared intervention + evidence artifact

See docs/RESEARCH.md.

## Repository map

src/aibpe/          core engine
schemas/            public contracts
examples/           reproducible demos
tests/              automated verification
docs/               architecture/spec/product/security
ui/                 explorer interface
medium/             technical article

## Status

v0.2 Alpha — production-oriented reference implementation.

The local runtime is functional. Production deployment still requires environment-specific hardening for authentication, encryption, retention, distributed durability, multi-tenancy and trust-boundary signing.

## License

Apache-2.0
