from fastapi import APIRouter

session_router = APIRouter(tags=["session"])


@session_router.post("/signup")
async def user_signup() -> None:
    pass


@session_router.post("/signin")
async def user_signin() -> None:
    pass
