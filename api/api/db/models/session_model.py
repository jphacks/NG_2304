from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from api.db.base import Base
from api.db.models.user_model import UserModel
from api.static import static


class SessionModel(Base):
    """Model for store session data."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(UserModel.id, onupdate="CASCADE", ondelete="CASCADE")
    )
    session_cert: Mapped[str] = mapped_column(String(100))
    refresh_token: Mapped[str] = mapped_column(String(512))
    is_discard: Mapped[bool] = mapped_column(Boolean, default=False)

    @hybrid_method
    def is_valid(self) -> bool:
        if self.is_discard:
            return False

        expire_time = self.created_at + static.REFRESH_TOKEN_EXPIRE_TIME
        return datetime.now(static.TIME_ZONE) < expire_time

    @hybrid_method
    def discard(self) -> None:
        self.is_discard = True
