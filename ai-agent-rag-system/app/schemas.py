from pydantic import BaseModel
from typing import Any


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