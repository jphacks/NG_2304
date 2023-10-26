from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.github_tokens_model import GithubTokensModel


class GithubTokensDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get(self, github_tokens_id: int) -> Optional[GithubTokensModel]:
        github_tokens = await self.session.get(GithubTokensModel, github_tokens_id)
        return github_tokens

    async def get_from_user_id(self, user_id: int) -> Optional[GithubTokensModel]:
        query = select(GithubTokensModel)
        query = query.filter(GithubTokensModel.user_id == user_id)
        rows = await self.session.execute(query)

        return rows.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        access_token: str,
        refresh_token: str,
        access_token_expires_in: int,
        refresh_token_expires_in: int,
        token_type: str,
        created_at: datetime,
    ) -> GithubTokensModel:
        access_token_expiry = created_at + timedelta(seconds=access_token_expires_in)
        refresh_token_expiry = created_at + timedelta(seconds=refresh_token_expires_in)
        github_tokens = GithubTokensModel(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=access_token_expiry,
            refresh_token_expires_in=refresh_token_expiry,
            token_type=token_type,
        )

        self.session.add(github_tokens)
        await self.session.commit()

        return github_tokens

    async def update(
        self,
        user_id: int,
        access_token: str,
        refresh_token: str,
        access_token_expires_in: int,
        refresh_token_expires_in: int,
        token_type: str,
        created_at: datetime,
    ) -> GithubTokensModel:
        github_tokens = await self.get_from_user_id(user_id)

        if github_tokens is None:
            raise ValueError("Not found Github tokens from user_id.2")

        access_token_expiry = created_at + timedelta(seconds=access_token_expires_in)
        refresh_token_expiry = created_at + timedelta(seconds=refresh_token_expires_in)

        github_tokens.access_token = access_token
        github_tokens.access_token_expires_in = access_token_expiry

        github_tokens.refresh_token = refresh_token
        github_tokens.refresh_token_expires_in = refresh_token_expiry

        github_tokens.token_type = token_type

        await self.session.commit()

        return github_tokens
