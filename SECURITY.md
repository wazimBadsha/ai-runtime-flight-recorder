# Security policy

AIBPE can capture prompts, memory, retrieved documents, tool arguments, tool results, and model responses. Treat recorded runs as sensitive operational data.

## Reporting

Please do not disclose sensitive vulnerabilities in a public issue. Use the repository's private security-reporting channel when one is configured.

## Security boundaries

AIBPE's hash chain detects modification of recorded events but is not a signature system. Production deployments crossing trust boundaries should add authenticated transport, encryption, access control, signed manifests, and retention/deletion controls.

## Replay safety

Never connect replay to unrestricted production tools. The safe default is exact replay from recorded outputs.
