from fastapi import FastAPI

from app.endpoints import router
from app.config import settings


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Мегапроект по сбору средств. Описание добавить позже"

    app = FastAPI(
        title="FundMatch",
        description=description,
        version="0.1.0",
    )
    app.state.settings = settings
    app.include_router(router)
    return app


app = get_app()
