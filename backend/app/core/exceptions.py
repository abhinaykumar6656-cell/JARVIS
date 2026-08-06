"""
=========================================================
JARVIS Custom Exceptions
=========================================================

Defines custom exceptions used throughout JARVIS.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""


class JarvisException(Exception):
    """
    Base exception for JARVIS.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthenticationException(JarvisException):
    """
    Authentication failure.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
    ):
        super().__init__(
            message=message,
            status_code=401,
        )


class AuthorizationException(JarvisException):
    """
    Authorization failure.
    """

    def __init__(
        self,
        message: str = "Access denied.",
    ):
        super().__init__(
            message=message,
            status_code=403,
        )


class ValidationException(JarvisException):
    """
    Validation failure.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
    ):
        super().__init__(
            message=message,
            status_code=400,
        )


class ResourceNotFoundException(JarvisException):
    """
    Resource not found.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
    ):
        super().__init__(
            message=message,
            status_code=404,
        )


class DatabaseException(JarvisException):
    """
    Database operation failure.
    """

    def __init__(
        self,
        message: str = "Database error.",
    ):
        super().__init__(
            message=message,
            status_code=500,
        )


class AIServiceException(JarvisException):
    """
    AI service failure.
    """

    def __init__(
        self,
        message: str = "AI service unavailable.",
    ):
        super().__init__(
            message=message,
            status_code=503,
        )