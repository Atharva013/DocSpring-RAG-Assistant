"""
Session-scoped PDF upload endpoint. Each PDF is stored permanently under
its chat session, extracted with Azure Document Intelligence, embedded
with Azure OpenAI, and appended to Azure AI Search.

All heavy IO (Document Intelligence, OpenAI embeddings, Search indexing)
runs inside a ThreadPoolExecutor so the FastAPI event loop stays free
for other requests (e.g. new chats) while a large PDF is being processed.
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
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


# One shared thread pool for the heavy blocking pipeline.
# A single worker keeps Azure rate limits manageable; increase if needed.
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="upload-worker")


def _limit_pages_for_student_subscription(pages: list[dict]) -> list[dict]:
    """
    Keeps indexing responsive on Azure for Students by limiting very large
    PDFs before embedding. File size can be small while extracted text is
    huge (e.g. 5 MB / 84 pages / 240k chars).
    """
    limited_pages: list[dict] = []
    total_chars = 0

    for page in pages[: settings.max_pdf_pages]:
        text = page.get("text", "")
        if not text:
            continue

        remaining = settings.max_extracted_chars - total_chars
        if remaining <= 0:
            break

        if len(text) > remaining:
            text = text[:remaining]

        limited_pages.append({"page": page.get("page", 1), "text": text})
        total_chars += len(text)

    return limited_pages


def _process_pdf_blocking(
    sas_url: str,
    filename: str,
    session_id: str,
    document_id: str,
    blob_url: str,
) -> int:
    """
    Runs the entire extraction → chunking → embedding → indexing pipeline
    synchronously.  Executed inside the thread pool so the async event
    loop is never blocked.
    Returns the number of chunks indexed.
    """
    processing_stage = "text extraction"
    pages = extraction_service.extract_pages_from_blob_url(sas_url)
    if not pages:
        raise ValueError("No text could be extracted from this PDF.")
    pages = _limit_pages_for_student_subscription(pages)
    if not pages:
        raise ValueError("No text remained after applying indexing limits.")

    processing_stage = "chunking"
    chunks = chunking_service.chunk_pages(
        pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        max_chunks=settings.max_chunks_per_document,
    )
    if not chunks:
        raise ValueError("Document text was extracted but no chunks were generated.")

    processing_stage = "embedding generation"
    embeddings = embedding_service.generate_embeddings([c.text for c in chunks])
    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Embedding count mismatch: {len(embeddings)} embeddings for {len(chunks)} chunks."
        )

    processing_stage = "search index setup"
    search_service.ensure_index_exists()
    processing_stage = "search indexing"
    chunks_indexed = search_service.index_chunks(
        chunks,
        embeddings,
        filename,
        session_id=session_id,
        document_id=document_id,
    )

    processing_stage = "document metadata persistence"
    session_service.add_document_metadata(
        session_id,
        document_id=document_id,
        filename=filename,
        blob_url=blob_url,
        chunks_indexed=chunks_indexed,
    )

    return chunks_indexed


@router.post("/sessions/{session_id}/upload", response_model=UploadResponse)
async def upload_pdf(session_id: str, file: UploadFile = File(...)) -> UploadResponse:
    session = session_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read & validate size without blocking the loop (file.read is already async)
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds the {settings.max_upload_size_mb} MB limit "
                   f"(received {size_mb:.1f} MB). Split the PDF and try again.",
        )

    # Reset stream so blob_service can re-read it
    file.file.seek(0)
    document_id = str(uuid4())
    blob_name = blob_service.build_blob_name(session_id, document_id, file.filename)

    # ── 1. Upload to blob storage (fast, stays in event loop thread) ──────
    try:
        blob_url = blob_service.upload_pdf(file, blob_name=blob_name)
        sas_url = blob_service.generate_read_sas_url(blob_name)
    except Exception as exc:
        logger.exception("Upload/storage step failed")
        raise HTTPException(status_code=500, detail="Failed to upload file.") from exc

    # ── 2. Heavy pipeline in thread pool — event loop stays free ─────────
    loop = asyncio.get_event_loop()
    try:
        chunks_indexed = await loop.run_in_executor(
            _executor,
            _process_pdf_blocking,
            sas_url,
            file.filename,
            session_id,
            document_id,
            blob_url,
        )
    except Exception as exc:
        logger.exception("Processing/indexing pipeline failed for %s", file.filename)
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {exc}",
        ) from exc

    logger.info(
        "Upload complete — %s | %d chunks | session %s",
        file.filename,
        chunks_indexed,
        session_id,
    )
    return UploadResponse(
        session_id=session_id,
        document_id=document_id,
        filename=file.filename,
        blob_url=blob_url,
        status="indexed",
        message="File uploaded, extracted, and indexed successfully.",
        chunks_indexed=chunks_indexed,
    )
