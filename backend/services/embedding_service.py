"""
Generates embeddings for text chunks using Azure OpenAI.
"""

import logging

from openai import AzureOpenAI

from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
BATCH_SIZE = 16


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_key,
        api_version=settings.azure_openai_api_version,
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

    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        response = client.embeddings.create(
            model=settings.azure_openai_embedding_deployment,
            input=batch,
        )
        embeddings.extend(item.embedding for item in response.data)

    logger.info("Generated %d embeddings", len(embeddings))
    return embeddings
