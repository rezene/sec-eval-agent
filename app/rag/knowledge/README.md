# Knowledge sources

Drop OWASP Top 10, CWE, and MITRE ATT&CK reference documents here as
Markdown files (one topic per file). `app/rag/ingest.py` picks up every
`*.md` file under this directory and indexes it into Chroma.

Suggested starting set (Week 2 of the plan):
- `owasp-top-10-2021.md` — one section per category (A01..A10)
- `cwe-*.md` — a handful of the most common weakness entries (e.g. CWE-89 SQL Injection, CWE-79 XSS, CWE-798 Hardcoded Credentials)
- `mitre-attack-*.md` — reuse content from the existing MITRE ATT&CK pipeline
