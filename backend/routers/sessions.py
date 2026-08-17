"""
Session endpoints for the persistent multi-PDF chat experience.
"""

import logging

from fastapi import APIRouter, HTTPException

from backend.models import (
    DeleteSessionResponse,
    SessionCreateResponse,
    SessionDetail,
    SessionSummary,
    TitleUpdateRequest,
    TitleUpdateResponse,
)
from backend.services import blob_service, search_service, session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])
logger = logging.getLogger(__name__)


@router.post("", response_model=SessionCreateResponse)
async def create_session() -> SessionCreateResponse:
    try:
        session = session_service.create_session()
    except Exception as exc:
        logger.exception("Failed to create session")
        raise HTTPException(status_code=500, detail="Failed to create session.") from exc

    return SessionCreateResponse(**session)


@router.get("", response_model=list[SessionSummary])
async def list_sessions() -> list[SessionSummary]:
    try:
        sessions = session_service.list_sessions()
    except Exception as exc:
        logger.exception("Failed to list sessions")
        raise HTTPException(status_code=500, detail="Failed to list sessions.") from exc

    return [SessionSummary(**session) for session in sessions]


@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(session_id: str) -> SessionDetail:
    try:
        detail = session_service.get_session_detail(session_id)
    except Exception as exc:
        logger.exception("Failed to load session detail")
        raise HTTPException(status_code=500, detail="Failed to load session.") from exc

    if detail is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    return SessionDetail(**detail)


@router.delete("/{session_id}", response_model=DeleteSessionResponse)
async def delete_session(session_id: str) -> DeleteSessionResponse:
    if session_service.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        deleted_blobs = blob_service.delete_session_blobs(session_id)
        deleted_search_chunks = search_service.delete_session_chunks(session_id)
        deleted_records = session_service.delete_session_records(session_id)
    except Exception as exc:
        logger.exception("Failed to delete session")
        raise HTTPException(status_code=500, detail="Failed to delete session.") from exc

    return DeleteSessionResponse(
        session_id=session_id,
        deleted_blobs=deleted_blobs,
        deleted_search_chunks=deleted_search_chunks,
        deleted_documents=deleted_records["deleted_documents"],
        deleted_messages=deleted_records["deleted_messages"],
    )


@router.patch("/{session_id}/title", response_model=TitleUpdateResponse)
async def rename_session(session_id: str, request: TitleUpdateRequest) -> TitleUpdateResponse:
    """Renames a session — called automatically after the first user question."""
    if session_service.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        session_service.touch_session(session_id, title=request.title.strip())
    except Exception as exc:
        logger.exception("Failed to rename session")
        raise HTTPException(status_code=500, detail="Failed to rename session.") from exc

    return TitleUpdateResponse(session_id=session_id, title=request.title.strip())
