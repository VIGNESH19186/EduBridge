"""
Lightweight local embedding/similarity service.

For a hackathon/demo-friendly deployment we use scikit-learn's TF-IDF +
cosine similarity as a fast, dependency-light stand-in for a vector
database (ChromaDB/FAISS are supported as drop-in upgrades - see
ai/rag/retriever.py for the pluggable interface).
"""
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingIndex:
    """A simple in-memory TF-IDF index rebuilt whenever documents change."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self.corpus: List[str] = []
        self.metadata: List[dict] = []

    def build(self, texts: List[str], metadata: List[dict]):
        self.corpus = texts
        self.metadata = metadata
        if texts:
            self.matrix = self.vectorizer.fit_transform(texts)
        else:
            self.matrix = None

    def search(self, query: str, top_k: int = 3) -> List[Tuple[dict, float]]:
        if not self.corpus or self.matrix is None:
            return []
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranked = sorted(zip(self.metadata, scores), key=lambda x: x[1], reverse=True)
        return [(meta, float(score)) for meta, score in ranked[:top_k] if score > 0]


embedding_index = EmbeddingIndex()
