"""
Generates answers with Azure OpenAI using session-scoped retrieved PDF
chunks as grounded context.

Also provides ``generate_session_title()`` which asks the LLM for a
3-5 word chat title based on the user's first question — the same
behaviour as Claude and ChatGPT.
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
        page_num = chunk.get("page_number") or 0
        page_label = f"Page {page_num}" if page_num > 0 else "Page unknown"
        context_blocks.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"File: {chunk['source_file']}",
                    f"{page_label} | Chunk: {chunk['chunk_index']}",
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
                    "Format every substantial answer with short markdown sections: "
                    "Summary, Key points, and Sources. Use bullets when helpful. "
                    "Keep answers clear, practical, and cite source filenames "
                    "and page numbers where relevant."
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


def generate_session_title(question: str) -> str:
    """
    Asks the LLM to produce a short 3-5 word chat title from the user's
    first question — similar to how Claude and ChatGPT auto-name threads.
    Falls back to a truncated version of the question if the API call fails.
    """
    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=settings.azure_openai_chat_deployment,
            temperature=0.3,
            max_tokens=20,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate a very short chat title of 3-5 words that captures "
                        "the essence of the user's question. Return ONLY the title — "
                        "no quotes, no punctuation at the end, no explanation."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        title = (response.choices[0].message.content or "").strip().strip('"').strip("'")
        # Safety cap
        if len(title) > 60:
            title = title[:57] + "…"
        return title if title else _fallback_title(question)
    except Exception as exc:
        logger.warning("generate_session_title failed: %s", exc)
        return _fallback_title(question)


def _fallback_title(question: str) -> str:
    short = question.strip()
    return short[:47] + "…" if len(short) > 50 else short
