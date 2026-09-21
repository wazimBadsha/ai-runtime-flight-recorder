# Production deployment guide

AIBPE is local-first by design. Keep the public event and manifest contracts stable while swapping the storage layer for the scale and security requirements of a deployment.

## Recommended topology

```text
AI services -> SDK / collector -> durable queue -> event store
                                      |
                                      +-> object storage
                                      +-> relational index
                                      +-> analytical store
                                      +-> explorer API
```

## Required controls

- redact or tokenize sensitive payloads before persistence
- isolate tenants and projects
- encrypt stored artifacts
- enforce retention and deletion workflows
- authenticate ingestion and read APIs
- version every schema
- monitor event loss and ingestion latency

## Replay safety

Exact replay should use recorded outputs. Any live model or tool re-execution must be explicitly enabled, sandboxed, and observable.

## Integrity

Hash chains provide tamper evidence. They do not provide cryptographic authenticity; signed manifests should be added when evidence crosses trust boundaries.
