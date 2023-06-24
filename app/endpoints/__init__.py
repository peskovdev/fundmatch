from .health_check import router as health_check_router
from .auth import router as auth_router
from .team import router as team_router


list_of_routes = [
    health_check_router,
    auth_router,
    team_router,
]


__all__ = [
    "list_of_routes",
]
