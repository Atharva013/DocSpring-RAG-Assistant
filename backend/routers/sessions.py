"""
Session endpoints for the persistent multi-PDF chat experience.
"""

import logging

from fastapi import APIRouter, HTTPException

from backend.models import SessionCreateResponse, SessionDetail, SessionSummary
from backend.services import session_service

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
