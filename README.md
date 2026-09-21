# AI Behavioral Provenance Engine (AIBPE)

> **Observe the run. Map the causes. Test the change.**

A vendor-neutral, open-source runtime for understanding *why* an AI/LLM/agent system changed behavior.

AIBPE is not another tracing dashboard and not another generic record/replay tool. It builds a **behavioral provenance graph** for each run, computes reproducible fingerprints over the inputs that can affect behavior, and supports **controlled interventions** that change one declared variable at a time.

## Why

Modern AI systems are assembled from moving parts:

- model/version and inference parameters
- prompt/template versions
- retrieved documents and ranking
- memory state
- tool definitions and tool outputs
- policies/guardrails
- runtime and dependency versions
- external environment state

When behavior changes, a trace can tell you *what happened*, but teams still need a structured way to ask:

> **Which changed input is actually associated with the behavioral change, and what evidence do we have?**

AIBPE turns that question into an inspectable artifact.

## Core workflow

```text
AI / Agent Runtime
      |
      v
AIBPE Recorder
      |
      +--> Canonical Events
      +--> Artifact Hashes
      +--> Dependency Edges
      |
      v
Behavioral Provenance Graph
      |
      +--> Fingerprint
      +--> Compare
      +--> Intervention Plan
      +--> Re-run
      |
      v
Evidence Report
```

### Example

```bash
aibpe record --config examples/basic.yaml
aibpe inspect runs/01
aibpe compare runs/01 runs/02
aibpe intervene runs/02 --change retrieval.corpus=docs-v3
aibpe report runs/02
```

## Design principles

1. **Vendor neutral** — works at the application boundary; adapters are optional.
2. **Evidence over narrative** — reports cite concrete events, hashes and artifacts.
3. **No false causality** — the engine reports *candidate contributors* unless a controlled intervention supports the conclusion.
4. **Reproducibility is explicit** — replay modes are labelled exactly; model determinism is never assumed.
5. **Privacy by construction** — payload capture can be redacted, hashed or omitted.
6. **Open schema first** — the on-disk format is documented and usable without the server.

## V0.1 scope

- Python SDK and CLI
- append-only event journal
- content-addressed artifacts
- behavioral fingerprinting
- structural and semantic diff hooks
- provenance graph construction
- one-variable intervention plans
- offline deterministic demo runtime
- verification and tamper-evident hash chains
- OpenTelemetry bridge
- SQLite local index
- JSON/JSONL interchange
- test suite and CI

## Repository map

```text
src/aibpe/             # runtime + core engine
schemas/               # public event and artifact schemas
examples/              # offline reproducible scenarios
docs/                  # architecture, specification, security
tests/                 # unit/integration tests
medium/                # technical article
.github/workflows/     # CI
```

## Status

**Alpha / production-oriented reference implementation.**

The project is designed around production constraints, but deployment-specific security, durability, scale and compliance requirements must be validated for each environment.

## Research positioning

Current open-source projects already provide strong record/replay and trace-diff capabilities. AIBPE deliberately focuses on the layer above raw replay: **structured behavioral provenance + controlled intervention evidence**.

This is not a claim that no one else has ever implemented any individual feature. The project's scope is intentionally defined around the combination and its open specification.

## License

Apache-2.0.