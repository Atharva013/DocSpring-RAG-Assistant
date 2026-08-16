"""
Persists chat session metadata, uploaded document metadata, and chat
history in Azure Table Storage.

The app uses the same Azure Storage Account already configured for Blob
Storage, which keeps the v2 multi-session design friendly for an Azure
for Students subscription.
"""

import logging
from functools import lru_cache
from datetime import datetime, timezone
from uuid import uuid4

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.data.tables import TableClient, TableServiceClient, UpdateMode

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

SESSIONS_TABLE = "Sessions"
DOCUMENTS_TABLE = "SessionDocuments"
CHAT_HISTORY_TABLE = "ChatHistory"
SESSION_PARTITION_KEY = "session"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@lru_cache
def _get_table_service_client() -> TableServiceClient:
    return TableServiceClient.from_connection_string(
        conn_str=settings.azure_storage_connection_string
    )


def _get_table_client(table_name: str) -> TableClient:
    return _get_table_service_client().get_table_client(table_name=table_name)


@lru_cache
def ensure_tables_exist() -> None:
    """Creates the v2 persistence tables if they are missing."""
    service_client = _get_table_service_client()
    for table_name in (SESSIONS_TABLE, DOCUMENTS_TABLE, CHAT_HISTORY_TABLE):
        try:
            service_client.create_table(table_name)
            logger.info("Created Azure Table Storage table: %s", table_name)
        except ResourceExistsError:
            pass


def _to_session_summary(entity: dict) -> dict:
    return {
        "session_id": entity["RowKey"],
        "title": entity.get("title", "Untitled session"),
        "created_at": entity["created_at"],
        "updated_at": entity["updated_at"],
        "document_count": entity.get("document_count", 0),
    }


def _to_document(entity: dict) -> dict:
    return {
        "document_id": entity["RowKey"],
        "filename": entity.get("filename", ""),
        "blob_url": entity.get("blob_url", ""),
        "uploaded_at": entity["uploaded_at"],
        "chunks_indexed": entity.get("chunks_indexed", 0),
    }


def _to_chat_message(entity: dict) -> dict:
    return {
        "message_id": entity["RowKey"],
        "role": entity.get("role", ""),
        "message": entity.get("message", ""),
        "timestamp": entity["timestamp"],
    }


def create_session(title: str | None = None) -> dict:
    """Creates a new empty chat session and returns its summary."""
    ensure_tables_exist()

    session_id = str(uuid4())
    now = _utc_now()
    session_title = title or "New chat"

    entity = {
        "PartitionKey": SESSION_PARTITION_KEY,
        "RowKey": session_id,
        "title": session_title,
        "created_at": now,
        "updated_at": now,
        "document_count": 0,
    }

    _get_table_client(SESSIONS_TABLE).create_entity(entity=entity)
    logger.info("Created session: %s", session_id)
    return _to_session_summary(entity)


def list_sessions() -> list[dict]:
    """Returns all sessions, newest updated first."""
    ensure_tables_exist()
    table_client = _get_table_client(SESSIONS_TABLE)
    entities = table_client.query_entities(
        query_filter="PartitionKey eq @partition_key",
        parameters={"partition_key": SESSION_PARTITION_KEY},
    )
    sessions = [_to_session_summary(entity) for entity in entities]
    return sorted(sessions, key=lambda item: item["updated_at"], reverse=True)


def get_session(session_id: str) -> dict | None:
    """Returns a single session summary, or None when not found."""
    ensure_tables_exist()
    table_client = _get_table_client(SESSIONS_TABLE)
    try:
        entity = table_client.get_entity(
            partition_key=SESSION_PARTITION_KEY,
            row_key=session_id,
        )
    except ResourceNotFoundError:
        return None
    return _to_session_summary(entity)


def get_session_detail(session_id: str) -> dict | None:
    """Returns session metadata, documents, and full chat history."""
    session = get_session(session_id)
    if session is None:
        return None

    documents_client = _get_table_client(DOCUMENTS_TABLE)
    messages_client = _get_table_client(CHAT_HISTORY_TABLE)

    documents = [
        _to_document(entity)
        for entity in documents_client.query_entities(
            query_filter="PartitionKey eq @session_id",
            parameters={"session_id": session_id},
        )
    ]
    messages = [
        _to_chat_message(entity)
        for entity in messages_client.query_entities(
            query_filter="PartitionKey eq @session_id",
            parameters={"session_id": session_id},
        )
    ]

    documents.sort(key=lambda item: item["uploaded_at"])
    messages.sort(key=lambda item: item["timestamp"])

    return {"session": session, "documents": documents, "messages": messages}


def touch_session(session_id: str, *, title: str | None = None) -> None:
    """Updates session timestamp and, optionally, the title."""
    session = get_session(session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    entity = {
        "PartitionKey": SESSION_PARTITION_KEY,
        "RowKey": session_id,
        "title": title or session["title"],
        "created_at": session["created_at"],
        "updated_at": _utc_now(),
        "document_count": session["document_count"],
    }
    _get_table_client(SESSIONS_TABLE).update_entity(
        mode=UpdateMode.REPLACE,
        entity=entity,
    )


def add_document_metadata(
    session_id: str,
    *,
    document_id: str,
    filename: str,
    blob_url: str,
    chunks_indexed: int,
) -> dict:
    """Stores metadata for a PDF uploaded into a session."""
    session = get_session(session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    now = _utc_now()
    document_entity = {
        "PartitionKey": session_id,
        "RowKey": document_id,
        "filename": filename,
        "blob_url": blob_url,
        "uploaded_at": now,
        "chunks_indexed": chunks_indexed,
    }
    _get_table_client(DOCUMENTS_TABLE).create_entity(entity=document_entity)

    # Update session: increment document count and bump updated_at.
    # NOTE: We deliberately do NOT rename the session here. The title will be
    # set automatically by the LLM after the user sends their first question
    # (see chat router). This prevents duplicate-name confusion when the same
    # PDF is uploaded into multiple sessions.
    session_entity = {
        "PartitionKey": SESSION_PARTITION_KEY,
        "RowKey": session_id,
        "title": session["title"],
        "created_at": session["created_at"],
        "updated_at": now,
        "document_count": session["document_count"] + 1,
    }
    _get_table_client(SESSIONS_TABLE).update_entity(
        mode=UpdateMode.REPLACE,
        entity=session_entity,
    )

    return _to_document(document_entity)


def append_chat_message(session_id: str, *, role: str, message: str) -> dict:
    """Appends one chat message to a session."""
    if role not in {"user", "assistant"}:
        raise ValueError("role must be either 'user' or 'assistant'")

    if get_session(session_id) is None:
        raise ValueError(f"Session not found: {session_id}")

    now = _utc_now()
    row_key = f"{now.strftime('%Y%m%d%H%M%S%f')}_{uuid4()}"
    entity = {
        "PartitionKey": session_id,
        "RowKey": row_key,
        "role": role,
        "message": message,
        "timestamp": now,
    }
    _get_table_client(CHAT_HISTORY_TABLE).create_entity(entity=entity)
    touch_session(session_id)

    return _to_chat_message(entity)


def delete_session_records(session_id: str) -> dict:
    """
    Deletes session metadata, document metadata, and chat messages from
    Azure Table Storage. Blob/Search cleanup is handled by their services.
    """
    session = get_session(session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    documents_client = _get_table_client(DOCUMENTS_TABLE)
    messages_client = _get_table_client(CHAT_HISTORY_TABLE)
    sessions_client = _get_table_client(SESSIONS_TABLE)

    document_entities = list(
        documents_client.query_entities(
            query_filter="PartitionKey eq @session_id",
            parameters={"session_id": session_id},
            select=["PartitionKey", "RowKey"],
        )
    )
    message_entities = list(
        messages_client.query_entities(
            query_filter="PartitionKey eq @session_id",
            parameters={"session_id": session_id},
            select=["PartitionKey", "RowKey"],
        )
    )

    for entity in document_entities:
        documents_client.delete_entity(
            partition_key=entity["PartitionKey"],
            row_key=entity["RowKey"],
        )

    for entity in message_entities:
        messages_client.delete_entity(
            partition_key=entity["PartitionKey"],
            row_key=entity["RowKey"],
        )

    sessions_client.delete_entity(
        partition_key=SESSION_PARTITION_KEY,
        row_key=session_id,
    )

    logger.info(
        "Deleted session records for %s: %d documents, %d messages",
        session_id,
        len(document_entities),
        len(message_entities),
    )
    return {
        "deleted_documents": len(document_entities),
        "deleted_messages": len(message_entities),
    }
