from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.endpoints import router


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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = get_app()
