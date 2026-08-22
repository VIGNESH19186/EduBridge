# Architecture

## System Overview

```
                    ┌─────────────────────┐
                    │      STUDENT        │
                    │      TEACHER        │
                    │       ADMIN         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FRONTEND       │
                    │   HTML / CSS / JS   │
                    │  (served by FastAPI │
                    │   StaticFiles)      │
                    └──────────┬──────────┘
                               │
                         REST API (JWT)
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FASTAPI        │
                    │      BACKEND        │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼───────────────────┐
          │                    │                   │
          ▼                    ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │ PostgreSQL  │     │ AI SERVICE  │     │   RAG       │
   │ / SQLite    │     │ (provider-  │     │  Pipeline   │
   │  Database   │     │  agnostic)  │     │             │
   └─────────────┘     └──────┬──────┘     └──────┬──────┘
                              │                   │
                              ▼                   ▼
                         ┌─────────┐       ┌─────────────┐
                         │   LLM   │       │ TF-IDF Index│
                         │(Claude) │       │ (swap-in:   │
                         │ or DEMO │       │ ChromaDB /  │
                         │  MODE   │       │  FAISS)     │
                         └─────────┘       └─────────────┘
```

## Layers

- **Frontend**: Static HTML/CSS/JS, no build step required. All data comes from
  the REST API via `frontend/js/api.js`. Served directly by FastAPI's
  `StaticFiles` mount for a single-process deployment, or can be hosted
  separately (e.g. Nginx, Vercel) with `CORS_ORIGINS` updated accordingly.
- **Backend (FastAPI)**: `backend/api/*.py` routers handle HTTP concerns only;
  business logic lives in `backend/services/*.py`.
- **Database**: SQLAlchemy ORM models in `backend/models/*.py`. SQLite by
  default for zero-config local runs; swap `DATABASE_URL` to Postgres for
  production (see docker-compose.yml).
- **AI Service**: `backend/services/ai_service.py` abstracts the LLM provider
  behind a single `complete()` method. Automatically falls back to a clearly
  labeled DEMO MODE response if `AI_API_KEY` is empty or the live call fails.
- **RAG Pipeline**: `ai/rag/*.py` (ingest, chunk, retrieve, cite) +
  `backend/services/rag_service.py` + `backend/services/embedding_service.py`.
  Uses TF-IDF + cosine similarity locally for zero-dependency operation;
  the retriever interface is pluggable so ChromaDB/FAISS can be swapped in
  without touching calling code.

## Data Flow: Doubt Solving

1. Student submits a question via `POST /api/doubts`.
2. `backend/services/doubt_solver.py` classifies subject/topic/difficulty using
   rule-based keyword matching (fast, deterministic, and explainable).
3. `rag_service.retrieve()` searches the TF-IDF index built from ingested
   `document_chunks`.
4. If no relevant chunk is found, the pipeline returns an honest "couldn't find
   enough information" message rather than fabricating an answer.
5. If sources are found, they are passed to `ai_service.complete()` with a
   grounding-only system prompt.
6. The explanation is translated (if a non-English language was requested) via
   `translation_service.py`.
7. The result, including source citations, is persisted to the `doubts` table
   and returned to the student.

## Role-Based Access Control

JWT tokens carry `user_id` and `role`. `backend/api/auth.py` exposes a
`require_role(*roles)` FastAPI dependency used throughout the API routers to
enforce that students cannot access teacher/admin routes and vice versa.
