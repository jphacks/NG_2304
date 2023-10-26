from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from api.db.dao.session_dao import SessionDAO
from api.db.dao.token_code_dao import TokenCodeDAO
from api.db.dao.user_dao import UserDao
from api.settings import settings
from api.static import static
from api.web.api.token.shema import JWTTokenPostDTO, TokenCodeDTO

router = APIRouter()
logger = logger.bind(Task="Token")


@router.post("/token")
async def generate_token(
    token_code_dto: TokenCodeDTO,
    token_code_dao: TokenCodeDAO = Depends(),
    session_dao: SessionDAO = Depends(),
) -> Response:
    token_code = await token_code_dao.get_code_from_seal(seal=token_code_dto.seal)

    if token_code is None:
        logger.error("Not found seal to generate token.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not found seal to generate token.",
        )

    if token_code.is_valid():
        token_code.expire()
        session_info = await session_dao.create(token_code.user_id)
        response = JSONResponse(session_info)
        response.set_cookie(
            key="access_token",
            value=session_info["access_token"],
            max_age=int(static.ACCESS_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )
        response.set_cookie(
            key="session_id",
            value=session_info["session_id"],
            max_age=int(static.REFRESH_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )

        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Your seal is expired."
    )


@router.post("/token/refresh")
async def generate_jwt_token(
    token_dto: JWTTokenPostDTO,
    user_dao: UserDao = Depends(),
    session_dao: SessionDAO = Depends(),
    session_id: str = Cookie(default=None),
) -> Response:
    """Function to generate a JWT token from refresh token."""
    if session_id is None and token_dto.session_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not found session_id in the request.",
        )

    session_cert = ""
    if token_dto.session_id is not None:
        session_cert = token_dto.session_id
    elif session_id is not None:
        session_cert = session_id

    session = await session_dao.get_from_session_cert(session_cert)

    if session is not None and session.is_valid():
        user = await user_dao.get_user(session.user_id)

        if user is None:
            # Normaly NO WAY!
            logger.critical("Not found user at created session")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error.",
            )

        new_access_token = session_dao.generate_access_token(user)
        response = JSONResponse({"access_token": new_access_token})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            max_age=int(static.ACCESS_TOKEN_EXPIRE_TIME.total_seconds()),
            secure=settings.is_production,
            domain=settings.domain,
            samesite="strict",
            httponly=True,
        )

        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired session_id."
    )
