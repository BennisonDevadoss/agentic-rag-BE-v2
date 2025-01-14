import uvicorn
from config.cors_options import configure_cors
from config.settings import SETTINGS
from fastapi import FastAPI
from routers.v1.router import v1_router

app = FastAPI()
configure_cors(app)

app.include_router(v1_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from BookBrowseAI!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SETTINGS.HOST,
        port=SETTINGS.PORT,
        reload=False if SETTINGS.ENVIRONMENT == "production" else True,
        log_level=SETTINGS.LOG_LEVEL.lower(),
    )
