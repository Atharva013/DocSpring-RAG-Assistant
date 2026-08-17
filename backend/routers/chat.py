"""
Session-scoped chat endpoint. Questions retrieve chunks only from PDFs
uploaded into the selected session, then generate an answer with Azure
OpenAI and persist the conversation in Azure Table Storage.

After the very first user message the session is automatically renamed
to a short LLM-generated title (3-5 words) — the same behaviour as
Claude and ChatGPT.
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

    # ── Auto-rename on first question (like Claude/GPT) ──────────────────────
    # Only rename if the session still has the default placeholder title.
    current_title = session_detail["session"].get("title", "")
    is_placeholder = current_title in ("New chat", "Untitled session", "", None)
    is_first_message = len(session_detail.get("messages", [])) == 0

    if is_first_message or is_placeholder:
        try:
            new_title = chat_service.generate_session_title(request.question)
            session_service.touch_session(session_id, title=new_title)
            logger.info("Auto-renamed session %s → '%s'", session_id, new_title)
        except Exception as rename_exc:
            logger.warning("Session auto-rename failed: %s", rename_exc)
    # ─────────────────────────────────────────────────────────────────────────

    sources = sorted({chunk["source_file"] for chunk in chunks})

    # Build per-chunk provenance detail (deduplicated by file+page)
    seen: set[tuple] = set()
    sources_detail: list[dict] = []
    for chunk in chunks:
        key = (chunk["source_file"], chunk.get("page_number") or 0)
        if key not in seen:
            seen.add(key)
            sources_detail.append(
                {
                    "source_file": chunk["source_file"],
                    "page_number": chunk.get("page_number") or 0,
                    "chunk_index": chunk["chunk_index"],
                }
            )
    # Sort by file then page
    sources_detail.sort(key=lambda x: (x["source_file"], x["page_number"]))

    return ChatResponse(
        answer=answer,
        sources=sources,
        retrieved_chunks=len(chunks),
        sources_detail=sources_detail,
    )
