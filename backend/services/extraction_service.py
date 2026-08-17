"""
Extracts text from a PDF stored in Azure Blob Storage using Azure
Document Intelligence's prebuilt-read model. Reads directly from the
blob's SAS URL — the file is never downloaded into the backend process.

IMPORTANT: page text is extracted via page.spans sliced against
result.content (the authoritative full-text string) rather than
iterating page.lines.  This matches the original result.content
behaviour — all pages, all elements — while also capturing the exact
1-indexed page number for each chunk.
"""

import logging

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_client() -> DocumentIntelligenceClient:
    return DocumentIntelligenceClient(
        endpoint=settings.azure_document_intelligence_endpoint,
        credential=AzureKeyCredential(settings.azure_document_intelligence_key),
    )


def extract_pages_from_blob_url(blob_sas_url: str) -> list[dict]:
    """
    Runs prebuilt-read and returns ``[{"page": int, "text": str}, ...]``.

    Text is sliced from ``result.content`` (the complete document text)
    using each page's character-offset spans.  This preserves 100% of
    the content Azure Document Intelligence returns — paragraphs, tables,
    headers, everything — while tagging every chunk with the correct page
    number.

    Falls back gracefully:
      1. page.spans  → slice result.content  (preferred, full fidelity)
      2. page.lines  → join line text        (fallback, slightly less complete)
      3. result.content whole document       (last resort, page = 1 for all)
    """
    client = _get_client()

    logger.info("Starting page-aware text extraction from blob URL")
    poller = client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(url_source=blob_sas_url),
    )
    result = poller.result()

    full_content: str = result.content or ""
    if not full_content:
        logger.warning("Document Intelligence returned empty content")
        return []

    pages: list[dict] = []

    if result.pages:
        for page in result.pages:
            page_num: int = page.page_number or (len(pages) + 1)
            page_text = ""

            # ── preferred: use character-offset spans ──────────────────
            if page.spans:
                page_text = "".join(
                    full_content[span.offset : span.offset + span.length]
                    for span in page.spans
                    if span.offset is not None and span.length is not None
                ).strip()

            # ── fallback: join the lines on the page ───────────────────
            if not page_text and page.lines:
                page_text = "\n".join(
                    line.content for line in page.lines if line.content
                ).strip()

            if page_text:
                pages.append({"page": page_num, "text": page_text})

        logger.info(
            "Extracted %d page(s) via page.spans, total chars=%d (full doc=%d)",
            len(pages),
            sum(len(p["text"]) for p in pages),
            len(full_content),
        )
    else:
        # No page metadata at all — treat entire content as a single page
        logger.warning("result.pages is empty; treating entire content as page 1")
        pages = [{"page": 1, "text": full_content.strip()}]

    return pages


def extract_text_from_blob_url(blob_sas_url: str) -> str:
    """
    Legacy helper — joins all pages into a single plain string.
    Kept so that any external callers continue to work unchanged.
    """
    pages = extract_pages_from_blob_url(blob_sas_url)
    return "\n\n".join(p["text"] for p in pages)