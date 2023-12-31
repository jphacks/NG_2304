from fastapi.routing import APIRouter

from api.web.api import auth, docs, monitoring, token, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(token.router, tags=["auth", "token"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
