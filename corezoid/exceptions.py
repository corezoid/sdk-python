"""
Exceptions for the Corezoid SDK.
"""


class CorezoidError(Exception):
    """Base exception for all Corezoid SDK errors."""
    pass


class AuthenticationError(CorezoidError):
    """Raised when authentication fails."""
    pass


class APIError(CorezoidError):
    """Raised when the Corezoid API returns an error."""
    def __init__(self, message, code=None, response=None):
        self.message = message
        self.code = code
        self.response = response
        super().__init__(message)


class ValidationError(CorezoidError):
    """Raised when input validation fails."""
    pass


class ConnectionError(CorezoidError):
    """Raised when connection to Corezoid API fails."""
    pass
