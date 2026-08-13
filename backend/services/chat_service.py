"""
Generates answers with Azure OpenAI using session-scoped retrieved PDF
chunks as grounded context.
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
    )


def _build_context(chunks: list[dict]) -> str:
    context_blocks = []
    for index, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"File: {chunk['source_file']}",
                    f"Chunk: {chunk['chunk_index']}",
                    chunk["content"],
                ]
            )
        )
    return "\n\n---\n\n".join(context_blocks)


def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Produces a grounded answer from retrieved chunks. If the answer is not
    present in the context, the model is instructed to say so clearly.
    """
    if not chunks:
        return (
            "I could not find relevant information in the PDFs uploaded to this "
            "session. Try uploading the right document or asking a more specific "
            "question."
        )

    client = _get_client()
    context = _build_context(chunks)

    response = client.chat.completions.create(
        model=settings.azure_openai_chat_deployment,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are DocSpring, a helpful RAG assistant for PDFs. "
                    "Answer only from the provided PDF context. If the context "
                    "does not contain the answer, say that you could not find it. "
                    "Keep answers clear, practical, and cite source filenames "
                    "when useful."
                ),
            },
            {
                "role": "user",
                "content": f"PDF context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    answer = response.choices[0].message.content or ""
    logger.info("Generated chat answer with %d retrieved chunks", len(chunks))
    return answer.strip()
