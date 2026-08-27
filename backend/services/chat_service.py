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


import re

def format_answer_markdown(answer: str) -> str:
    """
    Normalizes AI generated answers so markdown headings and bold section titles
    are cleanly formatted on their own lines with proper spacing.
    """
    if not answer:
        return ""

    text = answer.strip()

    # Convert markdown ATX headings (### Heading -> **Heading**) for clean unified style
    text = re.sub(r'^(?:#+\s*)([^\n]+)', r'**\1**', text, flags=re.MULTILINE)

    # Standardize section labels ending with colon like 'Overview:' -> '**Overview**'
    text = re.sub(r'^\*\*(.*?)\*\*\s*:\s*', r'**\1**\n', text, flags=re.MULTILINE)

    # Ensure empty line before standalone bold headers (if not at top of text)
    text = re.sub(r'([^\n])\n(\*\*[^*]+\*\*)\n', r'\1\n\n\2\n', text)

    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def generate_answer(
    question: str,
    chunks: list[dict],
    history: list[dict] | None = None,
) -> str:
    """
    Produces a grounded, dynamically formatted answer from retrieved chunks and
    conversation history (Gemini/GPT style).
    """
    if not chunks:
        return (
            "I could not find relevant information in the PDFs uploaded to this "
            "session. Try uploading the right document or asking a more specific "
            "question."
        )

    client = _get_client()
    context = _build_context(chunks)

    system_prompt = (
        "You are DocSpring AI, an enterprise-grade Retrieval-Augmented Generation (RAG) assistant specialized in analyzing PDF documents.\n\n"
        "RESPONSE FORMATTING & STYLE:\n"
        "1. DYNAMIC PRESENTATION:\n"
        "   - Adapt your output structure flexibly based on the user's question, intent, and turn in the conversation.\n"
        "   - For initial document questions, comprehensive analyses, or multi-faceted inquiries: structure your response with bold section headers on their own lines (e.g., **Overview**, **Key Details**, **Analysis**, **Sources**) followed by clean regular text paragraphs or bullet points.\n"
        "   - For follow-up questions, quick clarifications, brief requests, or direct conversation (e.g. 'explain point 2', 'summarize in 1 sentence', 'thanks'): reply directly, naturally, and concisely without forcing repetitive boilerplate headers like Summary/Key points.\n"
        "   - Always use bold syntax (**Heading Title**) for section titles, and keep the main content in clear regular body text.\n\n"
        "2. STRICT RAG GROUNDING & CITATIONS:\n"
        "   - Answer strictly using the provided PDF context chunks.\n"
        "   - If the provided context does not contain enough information to answer the question, clearly state that you could not find the answer in the uploaded documents.\n"
        "   - Cite exact source filenames and page numbers in inline format where relevant, e.g. [Source: filename.pdf, Page X].\n"
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Append recent chat history if available (up to 8 previous turns)
    if history:
        for msg in history[-8:]:
            role = msg.get("role")
            content = msg.get("message") or msg.get("content")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    # Append current context + user question
    messages.append(
        {
            "role": "user",
            "content": f"Retrieved PDF Context:\n{context}\n\nUser Question: {question}",
        }
    )

    response = client.chat.completions.create(
        model=settings.azure_openai_chat_deployment,
        temperature=0.25,
        messages=messages,
    )

    raw_answer = response.choices[0].message.content or ""
    formatted_answer = format_answer_markdown(raw_answer)
    logger.info("Generated chat answer with %d retrieved chunks", len(chunks))
    return formatted_answer



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
