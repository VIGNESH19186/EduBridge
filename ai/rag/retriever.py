"""
Pluggable retriever interface.

Current implementation delegates to backend.services.embedding_service
(TF-IDF + cosine similarity) for a fast, dependency-light local vector
search. To swap in ChromaDB or FAISS for production, implement the same
`search(query, top_k)` interface and update backend/services/rag_service.py
to call it instead of embedding_index.
"""
from typing import List, Dict, Tuple
from backend.services.embedding_service import embedding_index


def search(query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
    return embedding_index.search(query, top_k=top_k)
