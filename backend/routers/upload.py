"""
Session-scoped PDF upload endpoint. Each PDF is stored permanently under
its chat session, extracted with Azure Document Intelligence, embedded
with Azure OpenAI, and appended to Azure AI Search.
"""

import logging
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.config import get_settings
from backend.models import UploadResponse
from backend.services import (
    blob_service,
    chunking_service,
    embedding_service,
    extraction_service,
    search_service,
    session_service,
)

router = APIRouter(tags=["upload"])
logger = logging.getLogger(__name__)
settings = get_settings()


@router.post("/sessions/{session_id}/upload", response_model=UploadResponse)
async def upload_pdf(session_id: str, file: UploadFile = File(...)) -> UploadResponse:
    session = session_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

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
    document_id = str(uuid4())
    blob_name = blob_service.build_blob_name(session_id, document_id, file.filename)

    try:
        blob_url = blob_service.upload_pdf(file, blob_name=blob_name)
        sas_url = blob_service.generate_read_sas_url(blob_name)
    except Exception as exc:
        logger.exception("Upload/storage step failed")
        raise HTTPException(status_code=500, detail="Failed to upload file.") from exc

    try:
        extracted_text = extraction_service.extract_text_from_blob_url(sas_url)
        if not extracted_text:
            raise ValueError("No text could be extracted from this PDF.")

        chunks = chunking_service.chunk_text(extracted_text)
        embeddings = embedding_service.generate_embeddings([c.text for c in chunks])

        search_service.ensure_index_exists()
        chunks_indexed = search_service.index_chunks(
            chunks,
            embeddings,
            file.filename,
            session_id=session_id,
            document_id=document_id,
        )
        session_service.add_document_metadata(
            session_id,
            document_id=document_id,
            filename=file.filename,
            blob_url=blob_url,
            chunks_indexed=chunks_indexed,
        )
    except Exception as exc:
        logger.exception("Processing/indexing step failed")
        raise HTTPException(status_code=500, detail="Failed to process document.") from exc

    return UploadResponse(
        session_id=session_id,
        document_id=document_id,
        filename=file.filename,
        blob_url=blob_url,
        status="indexed",
        message="File uploaded, extracted, and indexed successfully.",
        chunks_indexed=chunks_indexed,
    )
