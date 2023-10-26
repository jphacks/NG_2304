from fastapi import APIRouter

from api.web.api.auth import github

router = APIRouter()
router.include_router(github.router, prefix="/github", tags=["auth", "github"])
