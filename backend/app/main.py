"""
=========================================================
JARVIS Main Application
=========================================================

Application entry point for JARVIS.

Responsible for:

• Creating the FastAPI application
• Initializing core services
• Managing startup and shutdown events
• Registering API routers

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.event_bus import event_bus
from app.core.logger import logger


# ==========================================================
# Application Lifecycle
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executed once when JARVIS starts
    and once when it shuts down.
    """

    logger.info("======================================")
    logger.info("Starting %s...", settings.APP_NAME)
    logger.info("Version : %s", settings.APP_VERSION)
    logger.info("Wake Word : %s", settings.WAKE_WORD)
    logger.info("======================================")

    # Store shared objects in application state
    app.state.event_bus = event_bus

    yield

    logger.info("======================================")
    logger.info("Shutting down %s...", settings.APP_NAME)
    logger.info("Goodbye!")
    logger.info("======================================")


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Personal AI Assistant",
    lifespan=lifespan,
)


# ==========================================================
# Register API Routers
# ==========================================================

app.include_router(api_router)


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Welcome to JARVIS!",
    }