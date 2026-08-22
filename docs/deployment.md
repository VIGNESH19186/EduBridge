# Deployment

## Local Development (SQLite, no Docker)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed_database.py
uvicorn backend.main:app --reload
```

Open http://localhost:8000 — the frontend is served directly by FastAPI.

## Docker (Postgres)

```bash
docker compose up --build
```

This starts:
- `db`: PostgreSQL 16, with a persistent volume
- `backend`: seeds the database on first boot, then runs Uvicorn on port 8000

Set `AI_API_KEY` as an environment variable before running to enable live AI
responses; otherwise the app runs in DEMO MODE automatically.

```bash
AI_API_KEY=sk-ant-... docker compose up --build
```

## Environment Variables

See `.env.example` for the full list. Key variables:

| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./edubridge.db` |
| `JWT_SECRET_KEY` | Signing key for auth tokens | dev-only placeholder — **change in production** |
| `AI_API_KEY` | LLM provider API key | empty → DEMO MODE |
| `AI_PROVIDER` | LLM provider identifier | `anthropic` |
| `AI_MODEL` | Model name | `claude-sonnet-4-6` |
| `CORS_ORIGINS` | Comma-separated allowed origins | localhost dev ports |

## Production Checklist

- [ ] Set a strong, unique `JWT_SECRET_KEY`.
- [ ] Use PostgreSQL (`DATABASE_URL=postgresql://...`), not SQLite.
- [ ] Set `AI_API_KEY` for live AI responses (optional — DEMO MODE is safe to
      ship if you don't have one yet).
- [ ] Restrict `CORS_ORIGINS` to your actual frontend domain(s).
- [ ] Put the app behind HTTPS (e.g. a reverse proxy / managed load balancer).
- [ ] Review file upload limits in `backend/utils/validators.py` for your
      storage constraints.
- [ ] Run `pytest` in CI before every deploy.
