"""
POST /upload — accepts a single PDF, clears the previous session's data,
stores the new file in Azure Blob Storage, extracts its text via Azure
Document Intelligence (reading directly from the blob URL), chunks it
locally, generates embeddings via Azure OpenAI, and indexes it in
Azure AI Search.
"""

import logging

from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.config import get_settings
from backend.models import UploadResponse
from backend.services import (
    blob_service,
    chunking_service,
    embedding_service,
    extraction_service,
    search_service,
)

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
        sas_url = blob_service.generate_read_sas_url(file.filename)
        print("SAS URL:", sas_url)
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
        search_service.clear_index()
        chunks_indexed = search_service.index_chunks(chunks, embeddings, file.filename)
    except Exception as exc:
        logger.exception("Processing/indexing step failed")
        raise HTTPException(status_code=500, detail="Failed to process document.") from exc

    return UploadResponse(
        filename=file.filename,
        blob_url=blob_url,
        status="indexed",
        message="File uploaded, extracted, and indexed successfully.",
        chunks_indexed=chunks_indexed,
    )