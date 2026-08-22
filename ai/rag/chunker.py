"""Text chunking for RAG ingestion."""
from typing import List


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 80) -> List[str]:
    """
    Split text into overlapping chunks of approximately `chunk_size` characters.
    Overlap preserves context across chunk boundaries.
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
