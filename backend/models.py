"""
Pydantic request/response schemas shared across routers.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    session_id: str | None = None
    document_id: str | None = None
    filename: str
    blob_url: str
    status: str = Field(description="e.g. 'stored', 'indexed'")
    message: str
    chunks_indexed: int = 0


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    retrieved_chunks: int = 0
    # Detailed per-chunk provenance: [{source_file, page_number, chunk_index}]
    sources_detail: list[dict] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str = "docspring-pdf-chat-backend"


class ReadinessResponse(BaseModel):
    status: str
    openai_endpoint: str
    chat_deployment: str
    embedding_deployment: str
    embedding_dimensions: int
    search_index: str
    search_fields: list[str] = Field(default_factory=list)


class SessionCreateResponse(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    document_count: int = 0


class SessionSummary(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    document_count: int = 0


class SessionDocument(BaseModel):
    document_id: str
    filename: str
    blob_url: str
    uploaded_at: datetime
    chunks_indexed: int = 0


class ChatMessage(BaseModel):
    message_id: str
    role: str
    message: str
    timestamp: datetime


class SessionDetail(BaseModel):
    session: SessionSummary
    documents: list[SessionDocument] = Field(default_factory=list)
    messages: list[ChatMessage] = Field(default_factory=list)


class DeleteSessionResponse(BaseModel):
    session_id: str
    deleted_documents: int = 0
    deleted_messages: int = 0
    deleted_blobs: int = 0
    deleted_search_chunks: int = 0
    status: str = "deleted"


class TitleUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class TitleUpdateResponse(BaseModel):
    session_id: str
    title: str
