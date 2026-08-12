"""
Handles all interaction with Azure Blob Storage: uploading the current
session's PDF, clearing the previous one, and generating a short-lived
SAS URL so Azure Document Intelligence can read the blob directly.
"""

import logging
from datetime import datetime, timedelta

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from fastapi import UploadFile

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


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


def upload_pdf(file: UploadFile) -> str:
    """
    Uploads the given PDF to Blob Storage and returns its blob URL.
    Assumes clear_previous_session() has already been called.
    """
    container_client = _get_container_client()
    blob_client = container_client.get_blob_client(file.filename)

    file.file.seek(0)
    blob_client.upload_blob(file.file, overwrite=True)

    logger.info("Uploaded new blob: %s", file.filename)
    return blob_client.url


def generate_read_sas_url(filename: str) -> str:
    """
    Generates a short-lived, read-only SAS URL for the given blob so
    Azure Document Intelligence can read it directly from Blob Storage.
    The PDF itself never passes through the backend process.
    """
    blob_service_client = _get_blob_service_client()
    container_client = blob_service_client.get_container_client(
        settings.azure_storage_container_name
    )
    blob_client = container_client.get_blob_client(filename)

    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=settings.azure_storage_container_name,
        blob_name=filename,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=15),
    )
    return f"{blob_client.url}?{sas_token}"