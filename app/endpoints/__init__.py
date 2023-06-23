from fastapi import APIRouter

from .ping import router as ping_router
from .login import router as login_router
from .get_user import router as get_user_router


router = APIRouter(prefix="")

router.include_router(ping_router)
router.include_router(login_router)
router.include_router(get_user_router)
