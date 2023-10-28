from datetime import datetime
from typing import Optional
from urllib.parse import urlencode, urljoin

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from github import Auth, Github
from loguru import logger
from yarl import URL

from api.db.dao.github_tokens_dao import GithubTokensDAO
from api.db.dao.token_code_dao import TokenCodeDAO
from api.db.dao.user_dao import UserDao
from api.libs.oauth import NotVerifiedEmailError, TokenRetrievalError, github
from api.settings import settings
from api.static import static

router = APIRouter()
logger = logger.bind(task="GithubAuth")


@router.get("/login")
@router.get("/login-vscode")
async def github_login(request: Request) -> Response:
    """Generate login url and redirect.

    :param request: Request object of fastAPI.
    :raises HTTPException:
        HTTP_500_INTERNAL_SERVER_ERROR, when the client_id or client_secret not found.
    :returns: RefirectReponse for github authentication url.
    """
    if (settings.github_client_id is None) or (settings.github_client_secret is None):
        if settings.github_client_id is None:
            logger.critical("Not found Github client_id.")
        if settings.github_client_secret is None:
            logger.critical("Not found Github client_secret.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="client_id or client_secret are not found for Github login.",
        )

    logger.info("Success to generate login url and redirect.")
    print(request.url.path)

    url_path_without_code = request.url.path
    url_path_without_code = url_path_without_code.split("?")[0]

    if url_path_without_code == "/api/auth/github/login-vscode":
        return RedirectResponse(github.auth_url(settings.github_client_id, request.url_for("github_callback")))
    else:
        return RedirectResponse(github.auth_url(settings.github_client_id))


@router.get("/callback")
@router.get("/callback-vscode")
async def github_callback(
    request: Request,
    code: Optional[str] = None,
    user_dao: UserDao = Depends(),
    token_code_dao: TokenCodeDAO = Depends(),
    github_tokens_dao: GithubTokensDAO = Depends(),
) -> Response:
    """Github Oauth callback endpoint.

    :param request: Request object of fastAPI.
    :param code: code to retrieve the token.
    :param user_dao: UserDAO object
    :param token_code_dao: TokenCodeDAO object
    :param github_tokens_dao: GithubTokensDAO object
    :raises HTTPException:
        500: when failed to retrieve the access token for Github login.
        400: when user's email address is not verified by github.
    :returns: Response object
    """
    if code is None:
        logger.error("Github login failed, Not fonund code to get credentials.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Github login faild.",
        )

    try:
        credentials: github.CredentialsType = await github.get_credentials(
            code=code,
            client_id=settings.github_client_id,
            client_secret=settings.github_client_secret,
            redirect_uri=str(request.url_for("github_callback")),
        )
        credentials["created_at"] = datetime.now(tz=static.TIME_ZONE)
        logger.info("Get auth credentials from github API.")
        logger.info("Success to retrieve access token from Github API.")
    except TokenRetrievalError:
        logger.error("Failed to retrieve access token for Github login.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve the access token for Github login.",
        )

    github_auth = Auth.Token(credentials["access_token"])
    github_client = Github(auth=github_auth)

    user_email: Optional[str] = None
    user_emails = github_client.get_user().get_emails()  # type: ignore

    for email in user_emails:
        if email.primary and email.verified:
            user_email = email.email
            break

    if user_email is None:
        logger.error("The github account is not verified email address.")
        raise NotVerifiedEmailError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your github account is not verified email address.",
        )

    user_info = github_client.get_user()
    user = await user_dao.get_user_by_email(email=user_email)

    if user is None:
        if user_info.name is None:
            display_name = user_info.login
        else:
            display_name = user_info.name
        user = await user_dao.create_user(
            username=user_info.login,
            display_name=display_name,
            email=user_email,
        )
        logger.info("Created new user: {0}".format(user.id))
        await github_tokens_dao.create(
            user_id=user.id,
            access_token=credentials["access_token"],
            access_token_expires_in=credentials["expires_in"],
            refresh_token=credentials["refresh_token"],
            refresh_token_expires_in=credentials["refresh_token_expires_in"],
            token_type=credentials["token_type"],
            created_at=credentials["created_at"],
        )
    else:
        await github_tokens_dao.update(
            user_id=user.id,
            access_token=credentials["access_token"],
            access_token_expires_in=credentials["expires_in"],
            refresh_token=credentials["refresh_token"],
            refresh_token_expires_in=credentials["refresh_token_expires_in"],
            token_type=credentials["token_type"],
            created_at=credentials["created_at"],
        )

    query = {"code": await token_code_dao.create_code(user.id)}
    url_path_without_code = request.url.path
    url_path_without_code = url_path_without_code.split("?")[0]

    if url_path_without_code == "/api/auth/github/callback-vscode":
        vscode_url = URL(static.VSCODE_URL).with_query(query)
        return RedirectResponse(vscode_url)
    else:
        return RedirectResponse(
            "{0}?{1}".format(
                urljoin(settings.web_uri, "callback"),
                urlencode(query),
            ),
        )
