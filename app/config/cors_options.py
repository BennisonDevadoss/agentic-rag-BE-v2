from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import SETTINGS


def configure_cors(app_: FastAPI) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=[SETTINGS.ALLOWED_ORIGIN],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        expose_headers=["Authorization"],
    )
