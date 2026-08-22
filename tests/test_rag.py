from backend.services import rag_service
from backend.services.embedding_service import EmbeddingIndex


def test_embedding_index_returns_empty_for_no_documents():
    index = EmbeddingIndex()
    index.build([], [])
    results = index.search("anything", top_k=3)
    assert results == []


def test_embedding_index_retrieves_relevant_chunk():
    index = EmbeddingIndex()
    texts = [
        "The power rule states that the derivative of x^n is n*x^(n-1).",
        "Newton's second law states force equals mass times acceleration.",
    ]
    metadata = [{"title": "Calculus"}, {"title": "Physics"}]
    index.build(texts, metadata)

    results = index.search("What is the derivative of x squared using the power rule?", top_k=1)
    assert len(results) >= 1
    assert results[0][0]["title"] == "Calculus"


def test_no_grounding_message_is_honest_not_fabricated():
    assert "couldn't find enough information" in rag_service.NO_GROUNDING_MESSAGE
