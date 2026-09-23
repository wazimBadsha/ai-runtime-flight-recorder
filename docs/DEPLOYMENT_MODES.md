# Deployment modes

This repository keeps two deployment modes intentionally separate.

## Public open-source cloud demo

- Synthetic, read-only run data.
- Public explorer shows manifests, event payloads, trajectory and evidence boundary.
- Vercel hosts the static explorer and serverless read endpoints.
- No customer prompts, memory, tool outputs, secrets or production traces belong in this environment.

## Customer product

- No permanent shared customer runtime.
- Provision an isolated environment only after an explicit customer request.
- Follow the production guidance: redaction/tokenization, tenant isolation, encryption, retention/deletion, authenticated APIs, schema versioning, ingestion health monitoring, and signed manifests across trust boundaries.
- Exact replay should use recorded outputs; live model/tool re-execution must be explicitly enabled, sandboxed and observable.

## Portfolio paths

`/flight-recorder` — showcase / architecture entry

`/flight-recorder/open-source` — public cloud demo

`/flight-recorder/customer` — customer deployment request

The uploaded showcase HTML remains the visual source artifact; this deployment scaffold separates its public demonstration path from the customer product path.
