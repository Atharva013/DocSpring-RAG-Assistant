"""
Splits extracted text into overlapping chunks suitable for embedding
and retrieval. Pure in-memory string processing — no external service
call, since chunking has no Azure equivalent.

The preferred entry point is ``chunk_pages()``, which accepts the
page-aware list returned by ``extraction_service.extract_pages_from_blob_url``
and tags every chunk with the 1-indexed page number it originated from.
"""

from dataclasses import dataclass, field


@dataclass
class Chunk:
    id: str
    text: str
    chunk_index: int
    page_number: int = 1  # 1-indexed; 0 means unknown


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> list[Chunk]:
    """
    Legacy helper — splits a single plain string without page tracking.
    ``page_number`` is left at the default value of 1 for all chunks.
    Kept for backward compatibility; prefer ``chunk_pages()`` for new code.
    """
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        piece = text[start:end].strip()

        if piece:
            chunks.append(Chunk(id=f"chunk-{index}", text=piece, chunk_index=index))
            index += 1

        if end == text_length:
            break
        start = end - chunk_overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    max_chunks: int | None = None,
) -> list[Chunk]:
    """
    Accepts a list of ``{"page": int, "text": str}`` dicts (as returned
    by ``extraction_service.extract_pages_from_blob_url``) and produces
    overlapping text chunks tagged with the originating page number.

    When a page's text is short enough to fit in one chunk it produces
    exactly one chunk; longer pages are split with the usual overlap.
    """
    if not pages:
        return []

    chunks: list[Chunk] = []
    index = 0

    for page_dict in pages:
        if max_chunks is not None and len(chunks) >= max_chunks:
            break

        page_num: int = page_dict.get("page", 1)
        text: str = page_dict.get("text", "").strip()
        if not text:
            continue

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            piece = text[start:end].strip()

            if piece:
                chunks.append(
                    Chunk(
                        id=f"chunk-{index}",
                        text=piece,
                        chunk_index=index,
                        page_number=page_num,
                    )
                )
                index += 1
                if max_chunks is not None and len(chunks) >= max_chunks:
                    break

            if end == text_length:
                break
            start = end - chunk_overlap

    return chunks
