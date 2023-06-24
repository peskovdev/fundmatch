from fastapi import APIRouter


router = APIRouter(prefix="/healthcheck")


@router.get("/ping")
def check_cart() -> dict:
    """Health Check"""
    return {"message": "pong"}
