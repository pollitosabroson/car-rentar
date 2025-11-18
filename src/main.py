from fastapi import FastAPI

from src.config.logging_config import setup_logging
from src.config.settings import settings
from src.infrastructure.api.v1.bookings import router as bookings_router
from src.infrastructure.api.v1.cars import router as cars_router

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Car Rental API with Hexagonal Architecture",
)

# Include routers
app.include_router(cars_router, prefix=settings.api_v1_prefix)
app.include_router(bookings_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to Car Rentar API",
        "version": settings.version,
        "docs": "/docs",
    }
