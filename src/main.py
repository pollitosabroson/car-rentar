from fastapi import FastAPI

from src.config.settings import settings

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Car Rental API with Hexagonal Architecture",
)


@app.get("/")
def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to Car Rentar API",
        "version": settings.version,
        "docs": "/docs",
    }
