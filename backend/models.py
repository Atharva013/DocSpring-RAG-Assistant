"""
Pydantic request/response schemas shared across routers.
"""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    filename: str
    blob_url: str
    status: str = Field(description="e.g. 'stored', 'previous_session_cleared'")
    message: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str = "docspring-pdf-chat-backend"