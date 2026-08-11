"""
Handles all interaction with Azure Blob Storage:
uploading the current session's PDF and clearing the previous one.
"""

import logging

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from fastapi import UploadFile

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_container_client():
    blob_service_client = BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    )
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