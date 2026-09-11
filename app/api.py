"""FastAPI service exposing the security agent."""

from fastapi import FastAPI

from app.agent import SecurityAgent
from app.schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(
    title="SecEvalAgent",
    description="Evaluation-driven, secure AI agent for code & config security analysis.",
    version="0.1.0",
)

_agent = SecurityAgent()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return _agent.analyze(filename=request.filename, code=request.code)
