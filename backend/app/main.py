from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fish Habit Game API",
        version="0.1.0",
        description="Backend API for the Fish Habit Game web application.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()
