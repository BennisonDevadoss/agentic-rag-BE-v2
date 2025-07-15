from fastapi import APIRouter

from .chat_router import chat_router
from .session_router import session_router
from .datasource_router import datasource_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(chat_router)
v1_router.include_router(session_router)
v1_router.include_router(datasource_router)
