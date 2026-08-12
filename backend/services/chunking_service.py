"""
Splits extracted text into overlapping chunks suitable for embedding
and retrieval. Pure in-memory string processing — no external service
call, since chunking has no Azure equivalent.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    id: str
    text: str
    chunk_index: int


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> list[Chunk]:
    """
    Splits text into overlapping chunks by character count. Overlap
    preserves context across chunk boundaries so answers spanning two
    chunks are still retrievable.
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