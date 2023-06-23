from fastapi import APIRouter


router = APIRouter(prefix="")


@router.get("/ping")
def check_cart() -> dict:
    """Health Check"""
    return {"message": "pong"}
