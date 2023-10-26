from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import ExpiredSignatureError, JWTError, jwt

from api.settings import settings


def create_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Fucntion to create a new JWT token.

    This function generates a JSON Web Token (JWT)
    with the provided data and an optional expiration time.
    :param data: Data to be stored in the token.
    :param expires_delta: Optional timedelta for token expiration (default: 15 minutes).
    :returns: A new JWT token as a string.
    """
    data_dict = data.copy()

    if expires_delta is not None:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)  # noqa: WPS432

    data_dict.update({"exp": expires})

    return jwt.encode(  # type: ignore
        data_dict,
        settings.token_secret_key,
        algorithm=settings.token_algorithm,
    )


def check_token(token: str) -> Optional[Dict[str, Any]]:
    """Check the validity of a JWT token.

    This function decodes and verifies the provided JWT token
    and returns its payload if the token is valid.
    :param token: The JWT token to be checked.
    :returns: The payload of the JWT token if valid. or None if token is invalid.
    """
    try:
        return jwt.decode(  # type: ignore
            token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
    except (JWTError, ExpiredSignatureError):
        return None


def is_valid(token: str) -> bool:
    """Check if a JWT token is valid.

    This function checks the validity of the provided JWT token
    without returning its payload.
    :param token: The JWT token to be checked.
    :returns: True if the JWT token is valid
    """
    try:
        jwt.decode(
            token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
        return True
    except (JWTError, ExpiredSignatureError):
        return False
