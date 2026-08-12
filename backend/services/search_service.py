"""
Manages the Azure AI Search index: creation, clearing, and population
with chunk text and embeddings for vector retrieval.
"""

import logging
import re

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
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
    Creates the Azure AI Search index if it doesn't already exist.
    Safe to call on every upload — no-ops if the index is already present.
    """
    index_client = _get_index_client()
    existing = [idx.name for idx in index_client.list_indexes()]

    if settings.azure_search_index_name in existing:
        return

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="chunk_index", type=SearchFieldDataType.Int32, filterable=True),
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


def index_chunks(chunks, embeddings: list[list[float]], source_file: str) -> int:
    """
    Uploads chunk text and embeddings to the Azure AI Search index.
    The document key is derived from a sanitized version of the filename
    (Search keys disallow periods, spaces, and parentheses); the original
    filename is preserved in the 'source_file' field for display/filtering.
    Returns the number of chunks indexed.
    """
    search_client = _get_search_client()
    safe_name = _sanitize_key(source_file)

    documents = [
        {
            "id": f"{safe_name}-{chunk.chunk_index}",
            "content": chunk.text,
            "chunk_index": chunk.chunk_index,
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