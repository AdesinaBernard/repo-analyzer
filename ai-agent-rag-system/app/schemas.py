from pydantic import BaseModel
from typing import Any, Optional


class QueryRequest(BaseModel):
    query: str


class RAGResponse(BaseModel):
    type: str
    query: str
    result: str


class ResearchResponse(BaseModel):
    type: str
    query: str
    report: str
    details: Any


class AgentResponse(BaseModel):
    type: str
    query: str
    result: Any


class HealthResponse(BaseModel):
    status: str
    service: str

class ResearchJobCreatedResponse(BaseModel):
    job_id: str
    status: str
    query: str


class ResearchJobStatusResponse(BaseModel):
    job_id: str
    status: str
    query: str
    result: Optional[Any] = None
    error: Optional[str] = None