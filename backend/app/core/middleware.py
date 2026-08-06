"""
=========================================================
JARVIS Logging Middleware
=========================================================

Logs every API request and response.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

import time

from fastapi import FastAPI
from fastapi import Request

from app.core.logger import logger


def register_middlewares(app: FastAPI):
    """
    Register application middlewares.
    """

    @app.middleware("http")
    async def log_requests(
        request: Request,
        call_next,
    ):
        """
        Log every HTTP request.
        """

        start_time = time.perf_counter()

        logger.info(
            "Incoming Request | %s | %s | %s",
            request.method,
            request.url.path,
            request.client.host,
        )

        response = await call_next(request)

        duration = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "Completed Request | %s | %s | %d | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response