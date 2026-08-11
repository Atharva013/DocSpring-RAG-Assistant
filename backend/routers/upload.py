"""
POST /upload — accepts a single PDF, clears the previous session's data,
and stores the new file in Azure Blob Storage.
"""

import logging

from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.config import get_settings
from backend.models import UploadResponse
from backend.services import blob_service

router = APIRouter(prefix="/upload", tags=["upload"])
logger = logging.getLogger(__name__)
settings = get_settings()


@router.post("", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds max size of {settings.max_upload_size_mb} MB.",
        )
    file.file.seek(0)

    try:
        blob_service.clear_previous_session()
        blob_url = blob_service.upload_pdf(file)
    except Exception as exc:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail="Failed to upload file.") from exc

    return UploadResponse(
        filename=file.filename,
        blob_url=blob_url,
        status="stored",
        message="File uploaded successfully. Extraction will run next.",
    )