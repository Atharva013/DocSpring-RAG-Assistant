"""
GET /health — basic liveness check.
"""

from fastapi import APIRouter

from backend.config import get_settings
from backend.models import HealthResponse, ReadinessResponse
from backend.services import chat_service, embedding_service, search_service

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/info")
async def model_info() -> dict:
    """Lightweight — returns deployment names with no external service calls."""
    return {
        "chat_model": settings.azure_openai_chat_deployment or "—",
        "embedding_model": settings.azure_openai_embedding_deployment or "—",
        "search_index": settings.azure_search_index_name or "—",
    }


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check() -> ReadinessResponse:
    embeddings = embedding_service.generate_embeddings(["DocSpring readiness check"])
    answer = chat_service.generate_answer(
        "Reply with the word ready.",
        [
            {
                "source_file": "readiness.txt",
                "chunk_index": 0,
                "content": "The DocSpring system is ready.",
            }
        ],
    )
    if not answer:
        raise RuntimeError("Chat deployment returned an empty answer.")

    search_service.ensure_index_exists()
    index = search_service._get_index_client().get_index(settings.azure_search_index_name)

    return ReadinessResponse(
        status="ready",
        openai_endpoint=settings.azure_openai_endpoint,
        chat_deployment=settings.azure_openai_chat_deployment,
        embedding_deployment=settings.azure_openai_embedding_deployment,
        embedding_dimensions=len(embeddings[0]) if embeddings else 0,
        search_index=settings.azure_search_index_name,
        search_fields=sorted(field.name for field in index.fields),
    )
