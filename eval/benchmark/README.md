# Labeled benchmark

60–100 code samples, each labeled with its ground-truth CWE (or `null` for
known-safe/clean samples). Sources: OWASP Benchmark, SARD/Juliet test
cases, plus a handful hand-crafted samples.

## Format

One JSONL file, `samples.jsonl`, one sample per line:

```json
{"id": "sqli-001", "filename": "login.py", "code": "...", "label_cwe": "CWE-89", "notes": "string-concatenated SQL query"}
{"id": "clean-001", "filename": "hash.py", "code": "...", "label_cwe": null, "notes": "known-safe control sample"}
```

Keep `code` as a single-file snippet for Week 1–5; multi-file samples can
be added once the agent supports multi-file input (Week 3+).
