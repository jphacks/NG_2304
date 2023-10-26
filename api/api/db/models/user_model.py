from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String
from sqlalchemy_utils import EmailType

from api.db.base import Base

if TYPE_CHECKING:
    from api.db.models.github_tokens_model import GithubTokensModel


class UserModel(Base):
    """Model for user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(length=50), nullable=False)
    display_name: Mapped[str] = mapped_column(String(length=50), nullable=True)
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)

    github_tokens: Mapped["GithubTokensModel"] = relationship(
        back_populates="user", uselist=False
    )
