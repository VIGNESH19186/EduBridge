"""
RAG (Retrieval-Augmented Generation) service.

Pipeline:
    Question -> Vector Search over ingested document_chunks -> Top-K sources
    -> Passed to AI service for grounded generation -> Citations attached.

If no relevant source is found, the caller is told explicitly rather than
letting the LLM fabricate an answer.
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from backend.models.document import Document, DocumentChunk
from backend.services.embedding_service import embedding_index

MIN_RELEVANCE_SCORE = 0.05


def build_index(db: Session):
    """(Re)build the in-memory retrieval index from all ingested chunks."""
    chunks = db.query(DocumentChunk).all()
    texts, metadata = [], []
    for chunk in chunks:
        doc = chunk.document
        texts.append(chunk.content)
        metadata.append(
            {
                "chunk_id": chunk.id,
                "content": chunk.content,
                "title": doc.title if doc else "Unknown",
                "section": chunk.section,
                "source": doc.source_url if doc else "",
                "subject": doc.subject if doc else "",
                "topic": doc.topic if doc else "",
            }
        )
    embedding_index.build(texts, metadata)


def retrieve(db: Session, query: str, top_k: int = 3) -> List[Dict]:
    """Return top-k relevant chunks with citation metadata, or [] if none relevant."""
    if embedding_index.matrix is None:
        build_index(db)
    results = embedding_index.search(query, top_k=top_k)
    return [meta for meta, score in results if score >= MIN_RELEVANCE_SCORE]


NO_GROUNDING_MESSAGE = (
    "I couldn't find enough information in the available educational sources "
    "to provide a reliable grounded answer."
)
