from fastapi import APIRouter

from .session_router import session_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(session_router)
