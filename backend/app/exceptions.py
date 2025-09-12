# app/exceptions.py
"""
Custom exception classes for Weather Dashboard backend.

Provides structured error handling for API, database, and cron operations.

Exceptions:
- AppError: base class for application errors.
- DatabaseError: raised when a database operation fails.
- APIError: raised when an external API call fails.
- ValidationError: raised when input data is invalid.
"""

from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base class for application errors."""
    def __init__(self, message: str, code: int = 400, log: bool = False):
        """
        Args:
            message (str): Human-readable error message.
            code (int): HTTP status code or error code.
            log (bool): Whether to log this exception immediately.
        """
        super().__init__(message)
        self.message = message
        self.code = code
        if log:
            logger.error(f"{self.__class__.__name__}: {message}")

class DatabaseError(AppError):
    """Raised when a database operation fails."""

    def __init__(self, message: str = "Database operation failed", log: bool = True):
        super().__init__(message, code=500, log=log)

class APIError(AppError):
    """Raised when an external API call fails."""

    def __init__(self, message: str = "External API request failed", log: bool = True):
        super().__init__(message, code=502, log=log)

class ValidationError(AppError):
    """Raised when input data is invalid."""

    def __init__(self, message: str = "Invalid input data", log: bool = False):
        super().__init__(message, code=422, log=log)