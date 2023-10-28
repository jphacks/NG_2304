from datetime import datetime
from typing import Dict, TypedDict

import httpx

from api.libs.oauth import TokenRetrievalError
from api.static import static


class CredentialsType(TypedDict):
    """Class for typing the github credentials response data."""

    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_type: str
    created_at: datetime


async def get_credentials(
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str = "",
) -> CredentialsType:
    """
    Get access token from Github API.

    This function is to get access_token from Github API and return it.

    :param code: String will use to get access token.
    :param client_id: The client_id of the Github APP.
    :param client_secret: The client_secret of the Github APP.
    :param redirect_uri: The redirect uri.
    :returns:
        ```
        {
            "access_token": str,
            "expires_in": int (seconds),
            "refresh_token": str,
            "refresh_token_expires_in": int (seconds),
        }
        ```
    :raises TokenRetrievalError: if can't retrieve access token
    """
    params = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    if len(params["redirect_uri"]) == 0:
        params["redirect_uri"] = redirect_uri

    async with httpx.AsyncClient() as client:
        response = await client.post(
            static.GITHUB_TOKEN_URL,
            data=params,
            headers=static.GITHUB_DEFAULT_HEADER,
        )
        response_data: CredentialsType = response.json()

    if "access_token" not in response_data:
        raise TokenRetrievalError()

    return response_data


def auth_url(client_id: str, redirect_uri: str = "") -> str:
    """Generate authorization link for Github login.

    :param client_id: client_id of Github APP.
    :returns: authorization_link for Github login.
    """
    if not static.GITHUB_AUTH_URL.endswith("?"):
        github_auth_url = f"{static.GITHUB_AUTH_URL}?"

    params: Dict[str, str] = {"client_id": client_id, "redirect_uri": redirect_uri}

    query = [f"{p}={v}" for p, v in params.items()]
    query_params = "&".join(query)

    return github_auth_url + query_params
