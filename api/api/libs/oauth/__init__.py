"""OAuth login service."""


from fastapi import HTTPException


class TokenRetrievalError(Exception):
    """Raised when failed to retrieve access token."""


class AccessTokenExpiredError(Exception):
    """Raised when the access_token was expired."""


class RefreshTokenExpiredError(Exception):
    """Raised when the refresh_token was expired."""


class NotVerifiedEmailError(HTTPException):
    """Raised when a user is not verified email."""
