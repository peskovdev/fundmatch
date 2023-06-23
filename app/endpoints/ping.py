from fastapi import APIRouter


router = APIRouter(prefix="")


@router.get("/ping")
def check_cart() -> tuple:
    """Health Check"""
    return {"message": "pong"}, 200
