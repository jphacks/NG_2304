from api.db.models.user_model import UserModel
from api.libs.middleware.auth import is_authenticated
from api.web.api.users.shema import AuthenticatedUser
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/me", response_model=AuthenticatedUser)
async def user_me(
    user_info: AuthenticatedUser = Depends(is_authenticated),
):
    return user_info
