"""
Manages the Azure AI Search index: creation, schema upgrades, and
population with session-scoped chunk text and embeddings for vector
retrieval.
"""

import logging
import re

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

EMBEDDING_DIMENSIONS = 1536  # matches text-embedding-3-small output size
VECTOR_PROFILE_NAME = "default-vector-profile"
HNSW_CONFIG_NAME = "default-hnsw"

# Azure AI Search document keys only allow letters, digits, underscore (_),
# dash (-), and equals (=) — anything else must be stripped/replaced.
_INVALID_KEY_CHARS = re.compile(r"[^A-Za-z0-9_\-=]")


def _sanitize_key(raw: str) -> str:
    """
    Converts an arbitrary filename into a safe Azure AI Search document key
    by replacing any disallowed character with an underscore.
    """
    return _INVALID_KEY_CHARS.sub("_", raw)


def _get_index_client() -> SearchIndexClient:
    return SearchIndexClient(
        endpoint=settings.azure_search_endpoint,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


def _get_search_client() -> SearchClient:
    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


def ensure_index_exists() -> None:
    """
    Creates the Azure AI Search index if it doesn't already exist. If an
    older v1 index exists, adds the v2 filter fields needed for
    multi-session retrieval without deleting existing documents.
    """
    index_client = _get_index_client()
    existing = [idx.name for idx in index_client.list_indexes()]

    if settings.azure_search_index_name in existing:
        index = index_client.get_index(settings.azure_search_index_name)
        field_names = {field.name for field in index.fields}

        if "session_id" not in field_names:
            index.fields.append(
                SimpleField(
                    name="session_id",
                    type=SearchFieldDataType.String,
                    filterable=True,
                )
            )
        if "document_id" not in field_names:
            index.fields.append(
                SimpleField(
                    name="document_id",
                    type=SearchFieldDataType.String,
                    filterable=True,
                )
            )

        updated_field_names = {field.name for field in index.fields}
        if {"session_id", "document_id"}.issubset(updated_field_names) and (
            "session_id" not in field_names or "document_id" not in field_names
        ):
            index_client.create_or_update_index(index)
            logger.info("Upgraded Azure AI Search index with v2 session fields")
        return

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="chunk_index", type=SearchFieldDataType.Int32, filterable=True),
        SimpleField(name="session_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source_file", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name=VECTOR_PROFILE_NAME,
        ),
    ]

    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name=VECTOR_PROFILE_NAME,
                algorithm_configuration_name=HNSW_CONFIG_NAME,
            )
        ],
        algorithms=[HnswAlgorithmConfiguration(name=HNSW_CONFIG_NAME)],
    )

    index = SearchIndex(
        name=settings.azure_search_index_name,
        fields=fields,
        vector_search=vector_search,
    )

    index_client.create_index(index)
    logger.info("Created Azure AI Search index: %s", settings.azure_search_index_name)


def clear_index() -> None:
    """
    Deletes all documents currently in the index — called before indexing
    a new PDF's chunks, since only one document is supported per session.
    """
    search_client = _get_search_client()
    results = search_client.search(search_text="*", select=["id"])
    ids_to_delete = [{"id": doc["id"]} for doc in results]

    if ids_to_delete:
        search_client.delete_documents(documents=ids_to_delete)
        logger.info("Cleared %d previous documents from index", len(ids_to_delete))


def index_chunks(
    chunks,
    embeddings: list[list[float]],
    source_file: str,
    *,
    session_id: str | None = None,
    document_id: str | None = None,
) -> int:
    """
    Uploads chunk text and embeddings to the Azure AI Search index.
    The document key is derived from a sanitized version of the filename
    (Search keys disallow periods, spaces, and parentheses); the original
    filename is preserved in the 'source_file' field for display/filtering.
    Returns the number of chunks indexed.
    """
    search_client = _get_search_client()
    safe_document_id = _sanitize_key(document_id or source_file)

    documents = [
        {
            "id": f"{safe_document_id}-{chunk.chunk_index}",
            "content": chunk.text,
            "chunk_index": chunk.chunk_index,
            "session_id": session_id or "default",
            "document_id": document_id or safe_document_id,
            "source_file": source_file,
            "embedding": embedding,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    if not documents:
        return 0

    search_client.upload_documents(documents=documents)
    logger.info("Indexed %d chunks for %s", len(documents), source_file)
    return len(documents)


def search_session_chunks(
    query_embedding: list[float],
    *,
    session_id: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Runs vector retrieval against only the chunks that belong to one chat
    session. This is the core guardrail that prevents one session from
    seeing another session's PDFs.
    """
    search_client = _get_search_client()
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding",
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        filter=f"session_id eq '{session_id}'",
        select=["content", "source_file", "chunk_index", "document_id"],
        top=top_k,
    )

    chunks = []
    for result in results:
        chunks.append(
            {
                "content": result["content"],
                "source_file": result["source_file"],
                "chunk_index": result["chunk_index"],
                "document_id": result["document_id"],
                "score": result.get("@search.score"),
            }
        )

    logger.info("Retrieved %d chunks for session %s", len(chunks), session_id)
    return chunks
