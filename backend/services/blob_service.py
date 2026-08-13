"""
Handles all interaction with Azure Blob Storage: uploading PDFs into
session/document scoped paths and generating short-lived SAS URLs so
Azure Document Intelligence can read blobs directly.
"""

import logging
from datetime import datetime, timedelta
from pathlib import PurePosixPath

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from fastapi import UploadFile

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def build_blob_name(session_id: str, document_id: str, filename: str) -> str:
    """
    Builds a stable blob path for a PDF inside a chat session.
    PurePosixPath keeps Azure blob names slash-separated on every OS.
    """
    safe_filename = PurePosixPath(filename).name
    return str(PurePosixPath(session_id, document_id, safe_filename))


def _get_blob_service_client() -> BlobServiceClient:
    return BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    )


def _get_container_client():
    blob_service_client = _get_blob_service_client()
    container_client = blob_service_client.get_container_client(
        settings.azure_storage_container_name
    )
    if not container_client.exists():
        container_client.create_container()
    return container_client


def clear_previous_session() -> None:
    """
    Deletes all blobs in the container. Called before every new upload
    since the app supports only one PDF per session.
    """
    container_client = _get_container_client()
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        try:
            container_client.delete_blob(blob.name)
            logger.info("Deleted previous session blob: %s", blob.name)
        except ResourceNotFoundError:
            continue


def upload_pdf(file: UploadFile, *, blob_name: str | None = None) -> str:
    """
    Uploads the given PDF to Blob Storage and returns its blob URL. When
    blob_name is provided, it stores the file under that full path.
    """
    container_client = _get_container_client()
    target_blob_name = blob_name or file.filename
    blob_client = container_client.get_blob_client(target_blob_name)

    file.file.seek(0)
    blob_client.upload_blob(file.file, overwrite=True)

    logger.info("Uploaded blob: %s", target_blob_name)
    return blob_client.url


def generate_read_sas_url(blob_name: str) -> str:
    """
    Generates a short-lived, read-only SAS URL for the given blob so
    Azure Document Intelligence can read it directly from Blob Storage.
    The PDF itself never passes through the backend process.
    """
    blob_service_client = _get_blob_service_client()
    container_client = blob_service_client.get_container_client(
        settings.azure_storage_container_name
    )
    blob_client = container_client.get_blob_client(blob_name)

    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=settings.azure_storage_container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=15),
    )
    return f"{blob_client.url}?{sas_token}"
