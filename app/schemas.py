"""Pydantic models for requests, responses, and structured findings."""

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Citation(BaseModel):
    source: str = Field(..., description="e.g. 'OWASP Top 10 A03:2021' or 'CWE-89'")
    excerpt: str = Field(..., description="Retrieved passage the finding is grounded in")


class Finding(BaseModel):
    type: str = Field(..., description="Human-readable vulnerability name")
    cwe_id: str | None = Field(None, description="e.g. 'CWE-89'")
    location: str = Field(..., description="File path and/or line range")
    severity: Severity
    description: str
    remediation: str
    citations: list[Citation] = Field(default_factory=list)
    confidence: float = Field(1.0, ge=0.0, le=1.0)


class AnalyzeRequest(BaseModel):
    filename: str = "snippet.py"
    code: str


class AnalyzeResponse(BaseModel):
    filename: str
    findings: list[Finding]
