"""
=========================================================
JARVIS Global Exception Handlers
=========================================================

Centralized exception handling.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import JarvisException
from app.core.logger import logger


def register_exception_handlers(
    app: FastAPI,
):
    """
    Register all global exception handlers.
    """

    @app.exception_handler(JarvisException)
    async def jarvis_exception_handler(
        request: Request,
        exc: JarvisException,
    ):
        logger.error(
            "JARVIS Exception: %s",
            exc.message,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.warning(
            "Validation Error: %s",
            exc.errors(),
        )

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation failed.",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled Exception"
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error.",
            },
        )