# Architecture

```mermaid
flowchart TD
    A[Untrusted input: code / config / small repo] --> B[Input guard\nsanitization + prompt-injection defenses]
    B --> C[Agent\ndetect -> classify CWE -> assess severity -> suggest fix]
    C <--> D[RAG knowledge base\nOWASP Top 10 + CWE + MITRE ATT&CK\nChroma]
    C --> E[Structured findings\nPydantic: type, location, CWE, severity, remediation, citation]
    E --> F[FastAPI service -> JSON API]

    G[Eval harness\nprecision/recall/F1 + G-Eval] -.-> C
```

Replace this Mermaid diagram with `architecture.png` once the design is
stable (Week 10 polish), or keep the Mermaid source — GitHub renders it
natively.

See [flagship-project-plan.md](../flagship-project-plan.md) for the full
phased build plan and scope-discipline rules.
