from typing import Optional
from pydantic import BaseModel, ConfigDict, validator
from datetime import datetime


class UserModelDTO(BaseModel):
    """DTO for User model."""

    id: int
    username: Optional[str]
    display_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthenticatedUser(UserModelDTO):
    email: str


class SessionUser(AuthenticatedUser):
    session_cert: Optional[str] = None
