"""
Session-scoped chat endpoint. Questions retrieve chunks only from PDFs
uploaded into the selected session, then generate an answer with Azure
OpenAI and persist the conversation in Azure Table Storage.
"""

import logging

from fastapi import APIRouter, HTTPException

from backend.models import ChatRequest, ChatResponse
from backend.services import (
    chat_service,
    embedding_service,
    search_service,
    session_service,
)

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat_with_session(session_id: str, request: ChatRequest) -> ChatResponse:
    session_detail = session_service.get_session_detail(session_id)
    if session_detail is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if not session_detail["documents"]:
        raise HTTPException(
            status_code=400,
            detail="Upload at least one PDF to this session before chatting.",
        )

    try:
        question_embedding = embedding_service.generate_embeddings([request.question])[0]
        chunks = search_service.search_session_chunks(
            question_embedding,
            session_id=session_id,
        )
        answer = chat_service.generate_answer(request.question, chunks)

        session_service.append_chat_message(
            session_id,
            role="user",
            message=request.question,
        )
        session_service.append_chat_message(
            session_id,
            role="assistant",
            message=answer,
        )
    except Exception as exc:
        logger.exception("Session chat failed")
        raise HTTPException(status_code=500, detail="Failed to chat with session.") from exc

    sources = sorted({chunk["source_file"] for chunk in chunks})
    return ChatResponse(
        answer=answer,
        sources=sources,
        retrieved_chunks=len(chunks),
    )
