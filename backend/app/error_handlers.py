# app/error_handlers.py
"""
Global exception handlers for Weather Dashboard API.

Provides structured JSON responses and logging for both expected
(application-defined) and unexpected exceptions.
"""
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import AppError

logger = logging.getLogger(__name__)

async def app_error_handler(request: Request, exc: AppError):
    """Handles all AppError exceptions and returns JSON."""
    logger.error(f"AppError: {exc.message}")
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.message}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handles all uncaught exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )