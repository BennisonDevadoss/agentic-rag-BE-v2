from fastapi import FastAPI

from app.routers.v1.router import v1_router

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
# from .routers import items, users

app = FastAPI()

app.include_router(v1_router)


# app.include_router(users.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from BookBrowseAI!"}
