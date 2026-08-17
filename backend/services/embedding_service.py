"""
Generates embeddings for text chunks using Azure OpenAI.
"""

import logging

from openai import AzureOpenAI

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_key,
        api_version=settings.azure_openai_api_version,
        timeout=settings.azure_openai_timeout_seconds,
        max_retries=0,
    )


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates one embedding vector per input text using the configured
    Azure OpenAI embedding deployment.
    """
    if not texts:
        return []

    client = _get_client()
    embeddings: list[list[float]] = []

    batch_size = max(1, settings.embedding_batch_size)
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = client.embeddings.create(
            model=settings.azure_openai_embedding_deployment,
            input=batch,
        )
        embeddings.extend(item.embedding for item in response.data)

    logger.info("Generated %d embeddings", len(embeddings))
    return embeddings
