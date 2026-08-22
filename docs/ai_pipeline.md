# AI Pipeline

## Doubt-Solving Pipeline

```
Student Question
      ↓
Question Classification (subject/topic/difficulty — rule-based, deterministic)
      ↓
RAG Retrieval (TF-IDF cosine similarity over ingested document_chunks)
      ↓
Grounded Generation (LLM constrained to retrieved sources only)
      ↓
Citation Attachment
      ↓
Translation (if non-English language selected)
      ↓
Student
```

### Why rule-based classification?

Subject/topic/difficulty detection (`backend/services/doubt_solver.py`) uses
keyword matching rather than an LLM call. This keeps classification fast,
free, deterministic, and fully testable (see `ai/evaluation/evaluate.py`,
which scores 5/5 on the bundled test set) — while the actual explanation
generation still uses the LLM for natural language quality.

### Grounding guarantee

The pipeline never lets the LLM answer from its own memory. If
`rag_service.retrieve()` returns no chunks above the relevance threshold, the
student receives:

> "I couldn't find enough information in the available educational sources to
> provide a reliable grounded answer."

This is enforced in code (`backend/services/doubt_solver.py`), not just in
the prompt — the LLM is never called at all when there's nothing to ground on.

## Demo Mode

When `AI_API_KEY` is empty (the default), `ai_service.AIService.is_demo()`
returns `True` and every `complete()` call returns a clearly labeled
`[DEMO MODE RESPONSE]` string instead of a live LLM call. This means:

- The full RAG retrieval, citation, and classification pipeline still runs
  for real.
- The UI never appears broken — every screen has real (seeded) data.
- Switching to a live provider is just setting `AI_API_KEY` in `.env`.

## Prompts

All prompt templates live in `ai/prompts/*.txt` and are documented inline:
`doubt_solver.txt`, `question_generator.txt`, `explanation.txt`,
`teacher_insight.txt`, `recommendation.txt`. The actual runtime prompts
constructed in `backend/services/*.py` follow the same structure.

## Adaptive Practice

```
Accuracy > 80%   → increase difficulty
Accuracy 50–80%  → maintain difficulty
Accuracy < 50%   → reduce difficulty / foundational practice
```

Implemented in `backend/services/practice_generator.next_difficulty()` and
covered by `tests/test_practice.py::test_adaptive_difficulty_rules`.

## Teacher Insight Agent

`backend/services/teacher_insights.py` computes risk levels purely from
measurable signals:
- Recent topic accuracy
- Consecutive failed attempts
- Days since last practice activity

No psychological or emotional claims are ever generated — this is enforced
both in the prompt (`ai/prompts/teacher_insight.txt`) and in code, and tested
in `tests/test_analytics.py::test_teacher_insights_never_makes_unsupported_psychological_claims`.

## RAG Implementation Notes

- **Chunking**: `ai/rag/chunker.py` splits text into ~600-character chunks
  with 80-character overlap to preserve context across boundaries.
- **Embeddings**: `backend/services/embedding_service.py` uses scikit-learn's
  `TfidfVectorizer` + cosine similarity — no external embedding API required,
  making the whole RAG pipeline free and offline-capable for development.
- **Swapping in ChromaDB/FAISS**: implement the same `search(query, top_k)`
  interface in `ai/rag/retriever.py` and point
  `backend/services/rag_service.retrieve()` at it instead of
  `embedding_index`.
