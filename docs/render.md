# Deploying the Backend to Render

This repository already contains a root `Dockerfile` that builds the FastAPI backend. Use Render to host the backend and let Vercel host the frontend.

Quick steps

1. Push your repo to GitHub (or connect your Git provider).
2. Edit `render.yaml` at the repo root and replace `REPLACE_WITH_GIT_REPO_URL`, `REPLACE_WITH_DATABASE_URL`, and `REPLACE_WITH_AI_KEY` with real values.
3. In the Render dashboard, create a new service and choose "Import from `render.yaml`" or connect the repo and select the `edubridge-ai-backend` service.

Notes

- The project `Dockerfile` exposes port `8000` and runs `uvicorn backend.main:app` — Render will route HTTP traffic automatically.
- Ensure `DATABASE_URL` points to a managed Postgres instance and that `psycopg2-binary` is appropriate for the platform.
- Set any additional env vars the app needs (see `backend/config.py`).

If you want, I can update `render.yaml` with your Git repo and env var values and then show the exact Render import steps.