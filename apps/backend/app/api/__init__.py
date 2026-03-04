from fastapi import APIRouter
from .risk import router as risk_router

api_router = APIRouter()

api_router.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk"]
)