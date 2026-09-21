# Threat model

AIBPE records potentially sensitive AI runtime information. A local deployment must assume that prompts, retrieved content, tool inputs and outputs may contain secrets or personal data.

## Default posture

- Capture only fields required for the debugging objective.
- Prefer hashes/references over raw payloads when possible.
- Add redaction hooks before persistent storage.
- Treat event stores as sensitive operational data.
- Keep replay offline by default.

## Integrity

The event journal uses a hash chain so accidental modification or truncation can be detected. Hash chaining is integrity evidence, not cryptographic authenticity.

## Future hardening

- envelope encryption for artifact blobs
- key management integrations
- signed run manifests
- retention/TTL policies
- multi-tenant authorization
- audit logging
