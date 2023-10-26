import secrets
from typing import Dict, Optional

from fastapi import Depends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.session_model import SessionModel
from api.db.models.user_model import UserModel
from api.libs.jwt_token import create_token
from api.static import static

logger = logger.bind(task="Session")


class SessionAlreadyExpiredError(Exception):
    """Error when tried to expire session was expired."""


class SessionNotFoundError(Exception):
    """Error when not found session in database."""


class SessionDAO:
    """Class for accessing session table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get(self, session_id: int) -> Optional[SessionModel]:
        session = await self.session.get(SessionModel, session_id)
        return session

    async def create(self, user_id: int) -> Dict[str, str]:
        user: Optional[UserModel] = await self.session.get(UserModel, user_id)

        if user is None:
            logger.error(f"Not found session from user_id. {user_id}")
            raise ValueError("Not found session from user_id.")

        session_cert = await self.generate_session_cert()
        refresh_token = self.generate_refresh_token(user)
        access_token = self.generate_access_token(user)

        session = SessionModel(
            user_id=user_id,
            session_cert=session_cert,
            refresh_token=refresh_token,
        )

        self.session.add(session)
        logger.info("Created new session")
        return {
            "session_id": session_cert,
            "access_token": access_token,
        }

    async def generate_session_cert(self, nbytes: Optional[int] = 64) -> str:
        """Fucntion to generate a key_token.

        :param nbytes:
            The string has *nbytes* random bytes.
            If *nbytes* is None or not supplied, a reasonable default is used.
        :returns: Returns the key_token
        """

        session_cert = secrets.token_urlsafe(nbytes)

        if await self.is_session_cert_exist(session_cert=session_cert):
            session_cert = await self.generate_session_cert()

        return session_cert

    def generate_access_token(self, user_model: UserModel) -> str:
        return create_token(
            data={
                "token_type": "token",
                "user_id": user_model.id,
                "username": user_model.username,
                "display_name": user_model.display_name,
                "email": user_model.email,
            },
            expires_delta=static.ACCESS_TOKEN_EXPIRE_TIME,
        )

    def generate_refresh_token(self, user_model: UserModel) -> str:
        return create_token(
            data={
                "token_type": "refresh_token",
                "user_id": user_model.id,
            },
            expires_delta=static.REFRESH_TOKEN_EXPIRE_TIME,
        )

    async def get_from_session_cert(self, session_cert: str) -> Optional[SessionModel]:
        query = select(SessionModel)
        query = query.filter(SessionModel.session_cert == session_cert)
        row = await self.session.execute(query)

        return row.scalar_one_or_none()

    async def get_from_refresh_token(
        self, refresh_token: str
    ) -> Optional[SessionModel]:
        query = select(SessionModel)
        query = query.filter(SessionModel.refresh_token == refresh_token)
        row = await self.session.execute(query)

        return row.scalar_one_or_none()

    async def expire(self, session_id: int) -> None:
        session = await self.get(session_id=session_id)

        if session is not None:
            if session.is_valid():
                logger.info(f"Expired Session_id: {session_id}")
                session.is_discard = True
            elif session.is_discard:
                logger.error(f"Tried to expire session was expired")
                raise SessionAlreadyExpiredError()
        else:
            logger.error(f"Not found session_id: {session_id}")
            raise SessionNotFoundError()

    async def expire_from_session_cert(self, session_cert: str) -> None:
        session = await self.get_from_session_cert(session_cert=session_cert)

        if session is None:
            logger.error(f"Not found session from session_cert. {session_cert}")
            raise ValueError("Not found session from user_id.")

        await self.expire(session.id)

    async def expire_from_refresh_token(self, refresh_token: str) -> None:
        session = await self.get_from_refresh_token(refresh_token=refresh_token)

        if session is None:
            logger.error(f"Not found session from refresh_token. {refresh_token}")
            raise ValueError("Not found session from user_id.")

        await self.expire(session.id)

    async def is_session_cert_exist(self, session_cert: str) -> bool:
        query = select(SessionModel)
        query = query.filter(SessionModel.session_cert == session_cert)
        row = await self.session.execute(query)

        return row.scalar_one_or_none() is not None
