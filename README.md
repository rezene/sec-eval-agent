# SecEvalAgent

An evaluation-driven, secure AI agent for code & config security analysis.

It analyzes code and configuration for vulnerabilities, grounds every
finding in OWASP/CWE/MITRE via retrieval, exposes it as a FastAPI service,
and measures its own precision/recall against a labeled benchmark while
defending against prompt injection in untrusted input.

> **Status:** early scaffold (Week 1 of the build plan). Endpoints and
> pipeline exist but return placeholder findings — see the TODOs in
> [app/agent.py](app/agent.py).

## Architecture

See [docs/architecture.md](docs/architecture.md) for the diagram. In short:

```
untrusted code -> input guard -> agent (detect/classify/severity/remediate)
                                    |
                                    v (retrieval)
                             RAG knowledge base (OWASP/CWE/MITRE, Chroma)
                                    |
                                    v
                         structured findings (Pydantic) -> FastAPI JSON API
```

An eval harness runs alongside (not in the request path) to score
precision/recall/F1 and injection resistance.

## Quickstart

```bash
cp .env.example .env   # fill in OPENAI_API_KEY (or your provider of choice)
pip install -e ".[dev]"

# Build the RAG index (once knowledge docs exist under app/rag/knowledge/)
python -m app.rag.ingest

# Run the API
uvicorn app.api:app --reload

# Or via Docker
docker compose up --build
```

```bash
curl -X POST localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"filename": "login.py", "code": "query = \"SELECT * FROM users WHERE id = \" + user_id"}'
```

## Development

```bash
pytest -q          # unit tests
ruff check .        # lint
python -m eval.run_eval            # benchmark precision/recall/F1 (once samples exist)
python -m eval.run_eval --injection  # injection-resistance measurement
```

## Repo layout

```
SecEvalAgent/
├── app/
│   ├── api.py             # FastAPI entrypoints
│   ├── agent.py            # detect -> classify -> severity -> remediate
│   ├── guards.py            # injection defenses, input sanitization
│   ├── llm.py                # swappable LLM provider interface
│   ├── config.py              # settings
│   ├── schemas.py              # Pydantic models
│   └── rag/                     # ingestion, embedding, retrieval
├── eval/
│   ├── benchmark/         # labeled samples (vulnerable + safe)
│   ├── injection/         # prompt-injection test set
│   ├── run_eval.py        # precision/recall/F1 + G-Eval
│   └── results/           # metrics, saved runs
├── tests/                 # unit tests
├── docs/                  # architecture notes/diagrams
└── .github/workflows/     # lint, test, build, eval-gate
```

## Results

_To be filled in from Week 5 onward: precision/recall/F1 per CWE category,
before/after prompt-injection defenses, and G-Eval groundedness scores._

## Security & prompt-injection

_To be filled in Week 7: the injection test set, defenses added
(delimiting/spotlighting, instruction/data separation, output validation),
and measured resistance before vs. after._

## Limitations & what fails

_To be filled in Week 10: an honest accounting of failure modes._

## Build plan

See [flagship-project-plan.md](flagship-project-plan.md) for the full
10-week phased plan and scope-discipline rules.
