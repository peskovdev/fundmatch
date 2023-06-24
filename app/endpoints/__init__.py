from fastapi import APIRouter

from .login import router as login_router
from .ping import router as ping_router
from .team import router as team_router


router = APIRouter(prefix="")

router.include_router(ping_router)
router.include_router(login_router)
router.include_router(team_router)
