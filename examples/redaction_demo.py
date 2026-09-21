from aibpe.redaction import redact

payload = {
    "message": "authorization=secret-token",
    "customer_note": "Call 4111 1111 1111 1111",
    "safe": "retrieval corpus v3",
}
print(redact(payload))
