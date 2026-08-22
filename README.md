# EduBridge AI

> **Learn Without Limits. Understand Without Barriers.**

An AI-powered platform for the challenge **AI for Equitable Education Access**.
EduBridge AI connects a student's specific confusion to the right explanation,
at the right level, in the right language — while helping teachers identify
learning gaps early, based only on measurable data.

This is a complete, working full-stack application: real FastAPI backend,
real database, real REST API, a grounded RAG pipeline, JWT authentication,
adaptive practice, and a responsive frontend — not a static mockup.

---

## Table of Contents

- [Problem & Solution](#problem--solution)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [Demo Accounts](#demo-accounts)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Hackathon Pitch](#hackathon-pitch)
- [Future Scope](#future-scope)

---

## Problem & Solution

Millions of students lack access to personalized tutoring. When they get
stuck, there's often no one to ask "why" — just a textbook or a search engine
that doesn't know their level, their language, or their specific gap.

**EduBridge AI** solves this by combining:
- A **grounded** AI doubt-solver (never fabricates answers — cites real
  educational sources or honestly says it doesn't have enough information)
- **Adaptive practice** that adjusts difficulty based on real accuracy
- **Multilingual support** so language is never the barrier
- A **Teacher Insight Agent** that flags students needing attention using
  only measurable learning data — no unsupported psychological claims

## Features

**Students** can register/login, select subjects and language, ask doubts,
get step-by-step grounded explanations with citations, choose explanation
level, generate and take adaptive practice, view progress and weak topics,
and receive personalized recommendations.

**Teachers** can create classes, view student performance and class
analytics, and receive AI-generated, evidence-based intervention
recommendations for students who need attention.

**Admins** can manage users, subjects, topics, and the knowledge base.

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full diagram and
explanation. In short:

```
Frontend (HTML/CSS/JS) -> REST API -> FastAPI Backend -> {PostgreSQL/SQLite, AI Service, RAG Pipeline}
```

## Core Workflow

```
Student -> Login -> Select Subject + Language -> Ask Doubt
   -> AI Question Analysis (subject/topic/difficulty)
   -> RAG Knowledge Search -> Grounded Explanation + Citations -> Translation
   -> Quick Check -> Adaptive Practice -> Updated Learning Profile
   -> Teacher Analytics -> Teacher Insight Agent -> Recommended Intervention
   -> Student Improvement -> Continuous Learning Loop
```

## Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, JWT (python-jose), bcrypt (passlib)
- **Database**: PostgreSQL (production) / SQLite (local & demo)
- **AI**: Provider-agnostic abstraction (`backend/services/ai_service.py`);
  configured for Anthropic's Claude by default; automatic DEMO MODE fallback
  when no API key is set
- **RAG**: TF-IDF + cosine similarity (scikit-learn) locally, with a pluggable
  retriever interface for ChromaDB/FAISS in production
- **Frontend**: HTML, CSS, vanilla JavaScript (modular, no build step),
  Chart.js for analytics visualizations

## Installation

```bash
git clone <this-repo>
cd edubridge-ai

python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/setup.py     # creates .env from .env.example
```

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed. **No API key is required
to run the app** — it automatically activates DEMO MODE with clearly-labeled
sample AI content so every feature remains fully explorable.

```env
DATABASE_URL=sqlite:///./edubridge.db
JWT_SECRET_KEY=change-this-super-secret-key-in-production
AI_PROVIDER=anthropic
AI_API_KEY=            # leave empty for demo mode
AI_MODEL=claude-sonnet-4-6
```

## Running Locally

```bash
python scripts/seed_database.py
uvicorn backend.main:app --reload
```

Open **http://localhost:8000** — the frontend is served directly by the
FastAPI backend, so there's nothing else to start.

### Docker

```bash
docker compose up --build
```

Runs the backend against PostgreSQL. See [`docs/deployment.md`](docs/deployment.md).

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Student | `student@example.com` | `password123` |
| Teacher | `teacher@example.com` | `password123` |

The seed script also creates 10 additional demo students with varied,
realistic performance data so teacher analytics look genuine out of the box.

## API Documentation

Full endpoint reference: [`docs/api.md`](docs/api.md). Interactive Swagger UI
is also available at **http://localhost:8000/docs** once the server is running.

## Testing

```bash
pytest
```

21 tests cover authentication, role-based access control, the doubt-solving
pipeline, RAG retrieval and grounding, adaptive practice and difficulty
adjustment, and teacher analytics/insight evidence requirements. All pass.

An additional classification-accuracy evaluation harness is available:

```bash
python ai/evaluation/evaluate.py
```

## Deployment

See [`docs/deployment.md`](docs/deployment.md) for a full production
checklist, Docker instructions, and environment variable reference.

## Hackathon Pitch

> Every student deserves a tutor who explains things their way — grounded in
> real sources, in their language, at their level. Every teacher deserves to
> know who needs help *before* they fall behind, based on evidence, not
> guesswork. EduBridge AI makes both possible, today, even without a paid AI
> subscription — the whole platform runs in a transparent Demo Mode out of
> the box.

## Future Scope

- Swap TF-IDF retrieval for ChromaDB/FAISS + real embedding models at scale
- Quiz builder UI for teachers (schema and API already support MCQ/short
  answer/numerical question types)
- Push notifications for teacher intervention reminders
- Offline-first mobile client for low-connectivity regions
- Expanded multilingual coverage beyond the five languages currently supported
- Admin console for platform-wide user/content management
