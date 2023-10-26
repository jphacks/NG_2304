from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.base import Base

if TYPE_CHECKING:
    from api.db.models.user_model import UserModel


class GithubTokensModel(Base):

    __tablename__ = "github_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("users.id"), unique=True)
    token_type: Mapped[str] = mapped_column(String(255))
    access_token: Mapped[str] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(String(255))
    access_token_expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    refresh_token_expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["UserModel"] = relationship(
        back_populates="github_tokens", single_parent=True
    )
