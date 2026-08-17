"""
Centralized application configuration.
Loads Azure service credentials and settings from environment variables.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Azure Blob Storage
    azure_storage_connection_string: str
    azure_storage_container_name: str = "pdf-uploads"

    # Azure Document Intelligence
    azure_document_intelligence_endpoint: str = ""
    azure_document_intelligence_key: str = ""

    # Azure OpenAI
    azure_openai_endpoint: str = ""
    azure_openai_key: str = ""
    azure_openai_api_version: str = "2024-08-01-preview"
    azure_openai_chat_deployment: str = ""
    azure_openai_embedding_deployment: str = ""

    # Azure AI Search
    azure_search_endpoint: str = ""
    azure_search_key: str = ""
    azure_search_index_name: str = "pdf-chat-index"

    # App
    max_upload_size_mb: int = 20
    max_pdf_pages: int = 40
    max_extracted_chars: int = 90000
    max_chunks_per_document: int = 80
    chunk_size: int = 1600
    chunk_overlap: int = 200
    embedding_batch_size: int = 8
    azure_openai_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance so .env is parsed only once."""
    return Settings()
