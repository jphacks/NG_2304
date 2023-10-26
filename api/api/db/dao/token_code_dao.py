import secrets
from typing import Optional

from fastapi import Depends
from loguru import logger
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from api.db.dependencies import get_db_session
from api.db.models.token_code_model import TokenCodeModel

logger = logger.bind(task="TokenCode")


class SealAlreadyExpiredError(Exception):
    """ "Error when tried to expire token_code was expired."""


class SealNotFoundError(Exception):
    """Error when not found token_code in database."""


class TokenCodeDAO:
    """Class for accessing token_code table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def generate_seal(self, nbytes: Optional[int] = 64) -> str:
        seal = secrets.token_urlsafe(nbytes)

        if await self.is_seal_exist_in_not_expired(seal):
            return await self.generate_seal()

        return seal

    async def create_code(self, user_id: int) -> str:
        seal = await self.generate_seal()
        self.session.add(
            TokenCodeModel(user_id=user_id, seal=seal),
        )

        return seal

    async def get_code(self, token_code_id: int) -> Optional[TokenCodeModel]:
        code = await self.session.get(TokenCodeModel, token_code_id)
        return code

    async def get_code_from_seal(self, seal: str) -> Optional[TokenCodeModel]:
        query = select(TokenCodeModel)
        query = query.filter(
            and_(TokenCodeModel.seal == seal, TokenCodeModel.is_used == False),
        )
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()

    async def expire_code(self, token_code_id: int) -> None:
        token_code: Optional[TokenCodeModel] = await self.get_code(token_code_id)
        if token_code is not None:
            if not token_code.is_valid():
                logger.info(f"Expired token: (id: {token_code.id}) {token_code.seal}")
                token_code.is_used = True
            elif token_code.is_used:
                logger.error("tried to expire token was expired.")
                raise SealAlreadyExpiredError()
        else:
            logger.error(f"Not found token_code: {token_code}")
            raise SealNotFoundError()

    async def is_seal_exist(self, seal: str) -> bool:
        query = select(TokenCodeModel)
        query = query.filter(TokenCodeModel.seal == seal)
        row = await self.session.execute(query)

        return row.scalar_one_or_none() is not None

    async def is_seal_exist_in_not_expired(self, seal: str) -> bool:
        query = select(TokenCodeModel)
        query = query.filter(
            and_(TokenCodeModel.seal == seal, TokenCodeModel.is_valid() == false())
        )
        row = await self.session.execute(query)

        return row.scalar_one_or_none() is not None
