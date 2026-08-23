"""
EduBridge AI - FastAPI application entrypoint.

Run with:
    uvicorn backend.main:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.middleware.force_english_middleware import ForceEnglishMiddleware

from backend.config import settings
from backend.database.database import Base, engine
from backend.utils.logging import logger
import backend.models  # noqa: registers all models on Base.metadata

from backend.api import auth, students, teachers, doubts, practice, analytics, knowledge, recommendations

app = FastAPI(
    title="EduBridge AI",
    description="AI-powered platform for equitable education access.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Force English for incoming requests (helps LLM/backend responses remain English)
app.add_middleware(ForceEnglishMiddleware)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    if settings.demo_mode:
        logger.warning(
            "AI_API_KEY not set — EduBridge AI is running in DEMO MODE. "
            "AI explanations/translations will use clearly-labeled sample content."
        )
    else:
        logger.info(f"AI provider '{settings.ai_provider}' configured with model '{settings.ai_model}'.")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Never expose stack traces to the client.
    logger.error(f"Unhandled error on {request.url.path}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "An internal error occurred. Please try again."})


app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(doubts.router)
app.include_router(practice.router)
app.include_router(analytics.router)
app.include_router(knowledge.router)
app.include_router(recommendations.router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "demo_mode": settings.demo_mode,
        "ai_provider": settings.ai_provider,
    }


# Serve the static frontend (HTML/CSS/JS) directly from FastAPI for convenience.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
