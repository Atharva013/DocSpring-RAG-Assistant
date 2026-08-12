"""
Extracts text from a PDF stored in Azure Blob Storage using Azure
Document Intelligence's prebuilt-read model. Reads directly from the
blob's SAS URL — the file is never downloaded into the backend process.
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


def extract_text_from_blob_url(blob_sas_url: str) -> str:
    """
    Runs the prebuilt-read model against a blob's SAS URL and returns
    the extracted text as a plain string. Handles both text-based and
    scanned PDFs.
    """
    client = _get_client()

    logger.info("Starting text extraction directly from blob URL")
    poller = client.begin_analyze_document(
        "prebuilt-read",
        AnalyzeDocumentRequest(url_source=blob_sas_url),
    )
    result = poller.result()

    if not result.content:
        logger.warning("No text extracted from document")
        return ""

    logger.info("Extraction complete: %d characters", len(result.content))
    return result.content